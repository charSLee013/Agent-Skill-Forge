#!/usr/bin/env python3
"""Baseline-aware finalization for local implementation issues."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


GATE_DIRECTORY = (".codex", "agents", "runtime", "issue-gates")
CLAIMS_DIRECTORY = (*GATE_DIRECTORY, "claims")
ISSUE_WORK_DIRECTORY = (".codex", "agents", "work")
STATE_FILE = "state.json"
CLAIM_FILE = "claim.json"
SNAPSHOT_DIRECTORY = "baseline"
STATE_VERSION = 2
CLAIM_VERSION = 1
PRIVATE_IGNORED_PREFIX = ".codex/"
BASELINE_HEADING = "## Issue-start baseline"
PROOF_HEADING = "## Finalization proof"
MAPPING_HEADING = "### Delta mapping"
PROOF_FIELDS = (
    "Baseline",
    "Final delta",
    "Scope audit",
    "Interface audit",
    "Dependency and persistence audit",
    "Error-handling audit",
    "Test justification",
    "Cleanup audit",
    "Acceptance evidence",
    "Independent review",
    "Result",
)
PLACEHOLDER = re.compile(r"(?:\bTODO\b|\bTBD\b|\bPLACEHOLDER\b|<[^>]+>)", re.IGNORECASE)
MAPPING_LINE = re.compile(
    r"^- `([^`]+)` -> `(scope|acceptance|support)`: (\S(?:.*\S)?)$"
)


class IssueGateError(Exception):
    """The issue gate cannot establish or verify its contract."""


@dataclass(frozen=True)
class Delta:
    digest: str
    units: tuple[dict[str, Any], ...]
    diffs: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class StopDecision:
    blocked_reason: str | None
    completed_directories: tuple[Path, ...]
    repository_root: Path | None


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True).encode(
        "utf-8"
    )


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _normalize_session_id(raw_session_id: str) -> str:
    try:
        return str(uuid.UUID(raw_session_id))
    except (ValueError, AttributeError) as error:
        raise IssueGateError("session_id must be a UUID") from error


def _repository_root(raw_cwd: str | Path) -> Path:
    cwd = Path(raw_cwd)
    if not cwd.is_absolute() or not cwd.is_dir():
        raise IssueGateError("cwd must be an existing absolute directory")
    cwd = cwd.resolve()
    result = _run_git(cwd, "rev-parse", "--show-toplevel")
    try:
        root = Path(result.stdout.decode("utf-8").strip()).resolve(strict=True)
    except (UnicodeError, OSError) as error:
        raise IssueGateError("git returned an invalid repository root") from error
    if root != cwd:
        raise IssueGateError(f"formal issue commands must run from the repository root: {root}")
    return root


def _run_git_unchecked(cwd: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=cwd,
            capture_output=True,
            check=False,
        )
    except OSError as error:
        raise IssueGateError(f"cannot run git: {error}") from error


def _run_git(cwd: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    result = _run_git_unchecked(cwd, *arguments)
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise IssueGateError(f"git {' '.join(arguments)} failed: {message or result.returncode}")
    return result


def _git_head(root: Path) -> str:
    result = _run_git_unchecked(root, "rev-parse", "--verify", "HEAD")
    if result.returncode == 0:
        return result.stdout.decode("ascii").strip()
    inside = _run_git(root, "rev-parse", "--is-inside-work-tree").stdout.strip()
    if inside == b"true":
        return "unborn"
    message = result.stderr.decode("utf-8", errors="replace").strip()
    raise IssueGateError(f"cannot determine Git HEAD: {message or result.returncode}")


def _git_paths(root: Path, *arguments: str) -> set[str]:
    output = _run_git(root, *arguments, "-z").stdout
    paths: set[str] = set()
    for raw_path in output.split(b"\0"):
        if not raw_path:
            continue
        path = os.fsdecode(raw_path)
        candidate = Path(path)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise IssueGateError(f"git returned an unsafe path: {path}")
        paths.add(candidate.as_posix())
    return paths


def _git_index_digest(root: Path) -> str:
    """Hash semantic index entries, excluding filesystem-only index metadata."""
    output = _run_git(root, "ls-files", "--stage", "-z").stdout
    return hashlib.sha256(output).hexdigest()


def _ignored_paths(root: Path) -> tuple[str, ...]:
    paths = _git_paths(root, "ls-files", "--others", "--ignored", "--exclude-standard")
    visible = {
        path
        for path in paths
        if path != PRIVATE_IGNORED_PREFIX.rstrip("/")
        and not path.startswith(PRIVATE_IGNORED_PREFIX)
    }
    return tuple(sorted(visible))


def _worktree_paths(root: Path) -> tuple[set[str], set[str]]:
    tracked = _git_paths(root, "ls-files")
    untracked = _git_paths(root, "ls-files", "--others", "--exclude-standard")
    overlap = tracked & untracked
    if overlap:
        raise IssueGateError(f"git classified paths as both tracked and untracked: {sorted(overlap)!r}")
    return tracked, untracked


def _resolve_issue(root: Path, issue_argument: str | Path) -> tuple[Path, str]:
    candidate = Path(issue_argument)
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        candidate_mode = candidate.lstat().st_mode
        if stat.S_ISLNK(candidate_mode) or not stat.S_ISREG(candidate_mode):
            raise IssueGateError(f"issue is not a regular file: {candidate}")
        issue = candidate.resolve(strict=True)
        work_root = root.joinpath(*ISSUE_WORK_DIRECTORY).resolve(strict=True)
        relative_to_work = issue.relative_to(work_root)
    except IssueGateError:
        raise
    except (OSError, ValueError) as error:
        raise IssueGateError("issue must exist under .codex/agents/work") from error
    if len(relative_to_work.parts) < 3 or relative_to_work.parts[-2] != "issues":
        raise IssueGateError("issue must be an implementation issue under a feature issues directory")
    return issue, issue.relative_to(root).as_posix()


def _completion(issue_text: str) -> str:
    matches = re.findall(r"^Completion: (open|done)$", issue_text, flags=re.MULTILINE)
    if len(matches) != 1 or not issue_text.startswith(f"Completion: {matches[0]}\n"):
        raise IssueGateError("issue must have exactly one top-level Completion: open|done field")
    return matches[0]


def _file_entry(root: Path, relative_path: str, ownership: str) -> dict[str, Any]:
    path = root / relative_path
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return {"kind": "missing", "mode": None, "sha256": None, "ownership": ownership}
    if stat.S_ISLNK(mode):
        target = os.readlink(path)
        return {
            "kind": "symlink",
            "mode": stat.S_IMODE(mode),
            "sha256": hashlib.sha256(os.fsencode(target)).hexdigest(),
            "target": target,
            "ownership": ownership,
        }
    if not stat.S_ISREG(mode):
        raise IssueGateError(f"unsupported worktree path type: {relative_path}")
    try:
        contents = path.read_bytes()
    except OSError as error:
        raise IssueGateError(f"cannot read worktree path {relative_path}: {error}") from error
    return {
        "kind": "regular",
        "mode": stat.S_IMODE(mode),
        "sha256": hashlib.sha256(contents).hexdigest(),
        "ownership": ownership,
    }


def _capture_manifest(root: Path, snapshot_root: Path | None) -> dict[str, dict[str, Any]]:
    tracked, untracked = _worktree_paths(root)
    entries: dict[str, dict[str, Any]] = {}
    for relative_path in sorted(tracked | untracked):
        ownership = "tracked" if relative_path in tracked else "untracked"
        entry = _file_entry(root, relative_path, ownership)
        entries[relative_path] = entry
        if snapshot_root is not None and entry["kind"] == "regular":
            destination = snapshot_root / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copyfile(root / relative_path, destination, follow_symlinks=False)
                os.chmod(destination, 0o600)
            except OSError as error:
                raise IssueGateError(f"cannot snapshot {relative_path}: {error}") from error
    return entries


def _baseline_digest(
    head: str,
    index_digest: str,
    ignored_paths: Sequence[str],
    entries: dict[str, dict[str, Any]],
) -> str:
    return _digest(
        {
            "entries": entries,
            "head": head,
            "ignored_paths": list(ignored_paths),
            "index_digest": index_digest,
        }
    )


def _gate_root(root: Path) -> Path:
    return root.joinpath(*GATE_DIRECTORY)


def _claim_directory(root: Path, issue_relative: str) -> Path:
    return root.joinpath(*CLAIMS_DIRECTORY, _gate_key(issue_relative))


def _claim_path(root: Path, issue_relative: str) -> Path:
    return _claim_directory(root, issue_relative) / CLAIM_FILE


def _gate_key(issue_relative: str) -> str:
    return hashlib.sha256(issue_relative.encode("utf-8")).hexdigest()[:20]


def _gate_directory(root: Path, session_id: str, issue_relative: str) -> Path:
    return _gate_root(root) / session_id / _gate_key(issue_relative)


def _atomic_write(path: Path, contents: bytes, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as output:
            output.write(contents)
            output.flush()
            os.fsync(output.fileno())
        os.chmod(temporary_path, mode)
        os.replace(temporary_path, path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def _read_claim(claim_path: Path) -> dict[str, Any]:
    try:
        mode = claim_path.lstat().st_mode
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
            raise IssueGateError(f"issue claim is not a regular file: {claim_path}")
        value = json.loads(claim_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise IssueGateError(f"issue claim is missing: {claim_path}") from error
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise IssueGateError(f"cannot read issue claim {claim_path}: {error}") from error
    if not isinstance(value, dict) or value.get("version") != CLAIM_VERSION:
        raise IssueGateError(f"unsupported issue claim: {claim_path}")
    if not isinstance(value.get("session_id"), str) or not isinstance(value.get("issue"), str):
        raise IssueGateError(f"incomplete issue claim: {claim_path}")
    if _normalize_session_id(value["session_id"]) != value["session_id"]:
        raise IssueGateError(f"issue claim session is not canonical: {claim_path}")
    return {"version": value["version"], "session_id": value["session_id"], "issue": value["issue"]}


def _claim_owner(root: Path, issue_relative: str) -> dict[str, Any] | None:
    claim_directory = _claim_directory(root, issue_relative)
    if not claim_directory.exists():
        return None
    if claim_directory.is_symlink() or not claim_directory.is_dir():
        raise IssueGateError(f"issue claim path is not a directory: {claim_directory}")
    return _read_claim(_claim_path(root, issue_relative))


def _acquire_claim(root: Path, session_id: str, issue_relative: str) -> None:
    claim_directory = _claim_directory(root, issue_relative)
    claim_directory.parent.mkdir(parents=True, exist_ok=True)
    try:
        claim_directory.mkdir(mode=0o700)
    except FileExistsError as error:
        try:
            owner = _claim_owner(root, issue_relative)
        except IssueGateError as claim_error:
            raise IssueGateError(
                f"issue claim is being established by another session: {issue_relative}"
            ) from claim_error
        if owner is None:
            raise IssueGateError(
                f"issue claim is being established by another session: {issue_relative}"
            ) from error
        raise IssueGateError(
            f"issue already has an active gate for session {owner['session_id']}"
        ) from error
    try:
        _atomic_write(
            _claim_path(root, issue_relative),
            _canonical_json({"version": CLAIM_VERSION, "session_id": session_id, "issue": issue_relative})
            + b"\n",
        )
    except BaseException:
        shutil.rmtree(claim_directory, ignore_errors=True)
        raise


def _release_claim(root: Path, session_id: str, issue_relative: str) -> None:
    claim_directory = _claim_directory(root, issue_relative)
    claim_root = _gate_root(root).resolve() / "claims"
    try:
        resolved_parent = claim_directory.parent.resolve(strict=True)
        resolved_parent.relative_to(claim_root)
    except (OSError, ValueError) as error:
        raise IssueGateError(f"refusing to remove unsafe issue claim: {claim_directory}") from error
    owner = _read_claim(_claim_path(root, issue_relative))
    if owner["session_id"] != session_id or owner["issue"] != issue_relative:
        raise IssueGateError(f"issue claim owner changed: {issue_relative}")
    if claim_directory.is_symlink() or not claim_directory.is_dir():
        raise IssueGateError(f"issue claim path is not a directory: {claim_directory}")
    shutil.rmtree(claim_directory)
    for parent in (claim_directory.parent, _gate_root(root)):
        try:
            parent.rmdir()
        except OSError:
            pass


def _read_state(state_path: Path) -> dict[str, Any]:
    try:
        mode = state_path.lstat().st_mode
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
            raise IssueGateError(f"gate state is not a regular file: {state_path}")
        value = json.loads(state_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise IssueGateError(f"gate state is missing: {state_path}") from error
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise IssueGateError(f"cannot read gate state {state_path}: {error}") from error
    if not isinstance(value, dict) or value.get("version") != STATE_VERSION:
        raise IssueGateError(f"unsupported gate state: {state_path}")
    required = {
        "session_id",
        "issue",
        "head",
        "baseline_digest",
        "index_digest",
        "ignored_paths",
        "entries",
    }
    if (
        not required.issubset(value)
        or not isinstance(value["entries"], dict)
        or not isinstance(value["ignored_paths"], list)
    ):
        raise IssueGateError(f"incomplete gate state: {state_path}")
    string_fields = required - {"entries", "ignored_paths"}
    if not all(isinstance(value[field], str) for field in string_fields):
        raise IssueGateError(f"invalid gate state fields: {state_path}")
    if _normalize_session_id(value["session_id"]) != value["session_id"]:
        raise IssueGateError(f"gate state session is not canonical: {state_path}")
    for digest_field in ("baseline_digest", "index_digest"):
        if re.fullmatch(r"[0-9a-f]{64}", value[digest_field]) is None:
            raise IssueGateError(f"gate state {digest_field} is invalid: {state_path}")
    for relative_path in value["ignored_paths"]:
        if not isinstance(relative_path, str):
            raise IssueGateError(f"gate state has a non-string ignored path: {state_path}")
        candidate = Path(relative_path)
        if (
            candidate.is_absolute()
            or ".." in candidate.parts
            or relative_path == PRIVATE_IGNORED_PREFIX.rstrip("/")
            or relative_path.startswith(PRIVATE_IGNORED_PREFIX)
        ):
            raise IssueGateError(f"gate state has an unsafe ignored path: {relative_path}")
    if value["ignored_paths"] != sorted(set(value["ignored_paths"])):
        raise IssueGateError(f"gate state ignored paths are not unique and sorted: {state_path}")
    for relative_path, entry in value["entries"].items():
        if not isinstance(relative_path, str) or not isinstance(entry, dict):
            raise IssueGateError(f"gate state has an invalid manifest entry: {state_path}")
        candidate = Path(relative_path)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise IssueGateError(f"gate state has an unsafe manifest path: {relative_path}")
        if entry.get("kind") not in {"missing", "regular", "symlink"}:
            raise IssueGateError(f"gate state has an invalid path kind: {relative_path}")
        if entry.get("ownership") not in {"tracked", "untracked"}:
            raise IssueGateError(f"gate state has invalid path ownership: {relative_path}")
    return value


def _replace_section(issue_text: str, heading: str, body: str) -> str:
    section = f"{heading}\n\n{body.rstrip()}\n\n"
    matches = list(re.finditer(rf"(?m)^{re.escape(heading)}\n", issue_text))
    if not matches:
        return issue_text.rstrip() + "\n\n" + section.rstrip() + "\n"
    if len(matches) != 1:
        raise IssueGateError(f"issue repeats section: {heading}")
    match = matches[0]
    next_heading = re.search(r"(?m)^## ", issue_text[match.end() :])
    end = len(issue_text) if next_heading is None else match.end() + next_heading.start()
    return issue_text[: match.start()] + section + issue_text[end:].lstrip("\n")


def _baseline_section(state: dict[str, Any]) -> str:
    entries = state["entries"]
    tracked_count = sum(entry["ownership"] == "tracked" for entry in entries.values())
    untracked_count = sum(entry["ownership"] == "untracked" for entry in entries.values())
    receipt = Path(*GATE_DIRECTORY, state["session_id"], _gate_key(state["issue"]), STATE_FILE)
    return "\n".join(
        (
            f"- Session: `{state['session_id']}`",
            f"- Git HEAD: `{state['head']}`",
            f"- Git index: `{state['index_digest']}`",
            f"- Snapshot: `{state['baseline_digest']}`",
            f"- Tracked paths: `{tracked_count}`",
            f"- Non-ignored untracked paths: `{untracked_count}`",
            f"- Ignored paths outside .codex/: `{len(state['ignored_paths'])}`",
            f"- Runtime receipt: `{receipt.as_posix()}`",
        )
    )


def begin_issue(root: Path, session_id: str, issue_argument: str | Path) -> dict[str, Any]:
    issue, issue_relative = _resolve_issue(root, issue_argument)
    issue_text = issue.read_text(encoding="utf-8")
    if _completion(issue_text) != "open":
        raise IssueGateError("Finalize Issue can begin only while Completion is open")
    gate_directory = _gate_directory(root, session_id, issue_relative)
    state_path = gate_directory / STATE_FILE
    if state_path.exists():
        state = _read_state(state_path)
        if state["session_id"] != session_id or state["issue"] != issue_relative:
            raise IssueGateError("existing gate state belongs to a different issue or session")
        owner = _claim_owner(root, issue_relative)
        if owner is None or owner["session_id"] != session_id or owner["issue"] != issue_relative:
            raise IssueGateError("existing gate state does not own the issue claim")
        if _section(issue_text, BASELINE_HEADING) != _baseline_section(state):
            raise IssueGateError("existing issue-start baseline does not match its runtime receipt")
        return state

    _acquire_claim(root, session_id, issue_relative)
    temporary: Path | None = None
    published = False
    try:
        head = _git_head(root)
        index_digest = _git_index_digest(root)
        ignored_paths = _ignored_paths(root)
        gate_directory.parent.mkdir(parents=True, exist_ok=True)
        temporary = Path(
            tempfile.mkdtemp(prefix=f".{gate_directory.name}.", dir=gate_directory.parent)
        )
        snapshot_root = temporary / SNAPSHOT_DIRECTORY
        snapshot_root.mkdir(mode=0o700)
        entries = _capture_manifest(root, snapshot_root)
        if (
            entries != _capture_manifest(root, None)
            or index_digest != _git_index_digest(root)
            or ignored_paths != _ignored_paths(root)
        ):
            raise IssueGateError("repository state changed while the issue baseline was being captured")
        state = {
            "version": STATE_VERSION,
            "session_id": session_id,
            "issue": issue_relative,
            "head": head,
            "index_digest": index_digest,
            "ignored_paths": list(ignored_paths),
            "baseline_digest": _baseline_digest(head, index_digest, ignored_paths, entries),
            "entries": entries,
        }
        _atomic_write(temporary / STATE_FILE, _canonical_json(state) + b"\n")
        os.replace(temporary, gate_directory)
        published = True
        updated_issue = _replace_section(issue_text, BASELINE_HEADING, _baseline_section(state))
        _atomic_write(issue, updated_issue.encode("utf-8"), stat.S_IMODE(issue.stat().st_mode))
        return state
    except BaseException:
        if temporary is not None and temporary.exists():
            shutil.rmtree(temporary)
        if published and gate_directory.exists():
            shutil.rmtree(gate_directory)
        _release_claim(root, session_id, issue_relative)
        raise


def _snapshot_contents(gate_directory: Path, relative_path: str, entry: dict[str, Any]) -> bytes:
    if entry["kind"] != "regular":
        return b""
    path = gate_directory / SNAPSHOT_DIRECTORY / relative_path
    try:
        contents = path.read_bytes()
    except OSError as error:
        raise IssueGateError(f"cannot read baseline snapshot {relative_path}: {error}") from error
    if hashlib.sha256(contents).hexdigest() != entry["sha256"]:
        raise IssueGateError(f"baseline snapshot was modified: {relative_path}")
    return contents


def _current_contents(root: Path, relative_path: str, entry: dict[str, Any]) -> bytes:
    if entry["kind"] != "regular":
        return b""
    try:
        contents = (root / relative_path).read_bytes()
    except OSError as error:
        raise IssueGateError(f"cannot read current worktree path {relative_path}: {error}") from error
    if hashlib.sha256(contents).hexdigest() != entry["sha256"]:
        raise IssueGateError(f"worktree changed while reading: {relative_path}")
    return contents


def _text_diff(path: str, before: bytes, after: bytes) -> tuple[str, list[tuple[str, str]]]:
    try:
        before_text = before.decode("utf-8")
        after_text = after.decode("utf-8")
    except UnicodeDecodeError:
        return "", []
    lines = list(
        difflib.unified_diff(
            before_text.splitlines(keepends=True),
            after_text.splitlines(keepends=True),
            fromfile=f"baseline/{path}",
            tofile=f"current/{path}",
            n=3,
        )
    )
    if not lines:
        return "", []
    hunks: list[tuple[str, str]] = []
    current_hunk: list[str] = []
    header = ""
    for line in lines[2:]:
        if line.startswith("@@ "):
            if current_hunk:
                hunks.append((header, "".join(current_hunk)))
            header = line.rstrip("\n")
            current_hunk = [line]
        elif current_hunk:
            current_hunk.append(line)
    if current_hunk:
        hunks.append((header, "".join(current_hunk)))
    return "".join(lines), hunks


def _change_kind(before: dict[str, Any], after: dict[str, Any]) -> str:
    if before["kind"] == "missing":
        return "added"
    if after["kind"] == "missing":
        return "deleted"
    if before["kind"] != after["kind"]:
        return "type-changed"
    if before["sha256"] != after["sha256"]:
        return "modified"
    if before["mode"] != after["mode"]:
        return "mode-changed"
    if before["ownership"] != after["ownership"]:
        return "ownership-changed"
    return "unchanged"


def _path_preview(paths: Sequence[str]) -> str:
    preview = list(paths[:8])
    suffix = " ..." if len(paths) > len(preview) else ""
    return ", ".join(preview) + suffix


def _assert_unchanged_control_state(root: Path, state: dict[str, Any]) -> None:
    current_index_digest = _git_index_digest(root)
    if current_index_digest != state["index_digest"]:
        raise IssueGateError(
            "Git index changed after the issue baseline; restore the issue-start index before finalization"
        )
    current_ignored = _ignored_paths(root)
    baseline_ignored = set(state["ignored_paths"])
    current_ignored_set = set(current_ignored)
    if current_ignored_set != baseline_ignored:
        added = sorted(current_ignored_set - baseline_ignored)
        removed = sorted(baseline_ignored - current_ignored_set)
        details: list[str] = []
        if added:
            details.append(f"new ignored paths: {_path_preview(added)}")
        if removed:
            details.append(f"removed baseline ignored paths: {_path_preview(removed)}")
        raise IssueGateError(
            "ignored path set changed after the issue baseline; clean or restore it before finalization"
            + (f" ({'; '.join(details)})" if details else "")
        )


def calculate_delta(root: Path, gate_directory: Path, state: dict[str, Any]) -> Delta:
    current_head = _git_head(root)
    if current_head != state["head"]:
        raise IssueGateError("Git HEAD changed after the issue baseline; start a new reviewed baseline")
    _assert_unchanged_control_state(root, state)
    current_entries = _capture_manifest(root, None)
    baseline_entries = state["entries"]
    units: list[dict[str, Any]] = []
    rendered_diffs: list[tuple[str, str]] = []
    missing = {"kind": "missing", "mode": None, "sha256": None, "ownership": "absent"}

    for relative_path in sorted(set(baseline_entries) | set(current_entries)):
        before = baseline_entries.get(relative_path, missing)
        after = current_entries.get(relative_path, missing)
        change = _change_kind(before, after)
        if change == "unchanged":
            continue
        file_unit = {
            "id": f"{relative_path}#file",
            "path": relative_path,
            "kind": "file",
            "change": change,
            "before": before,
            "after": after,
        }
        units.append(file_unit)

        before_contents = _snapshot_contents(gate_directory, relative_path, before)
        after_contents = _current_contents(root, relative_path, after)
        rendered, hunks = _text_diff(relative_path, before_contents, after_contents)
        if rendered:
            rendered_diffs.append((relative_path, rendered))
        for index, (header, hunk) in enumerate(hunks, start=1):
            hunk_digest = hashlib.sha256(hunk.encode("utf-8")).hexdigest()[:12]
            units.append(
                {
                    "id": f"{relative_path}#hunk-{index:02d}-{hunk_digest}",
                    "path": relative_path,
                    "kind": "hunk",
                    "change": change,
                    "header": header,
                    "sha256": hashlib.sha256(hunk.encode("utf-8")).hexdigest(),
                }
            )

    digest = _digest(units)
    return Delta(digest=digest, units=tuple(units), diffs=tuple(rendered_diffs))


def _load_gate(
    root: Path, session_id: str, issue_argument: str | Path
) -> tuple[Path, Path, str, dict[str, Any]]:
    issue, issue_relative = _resolve_issue(root, issue_argument)
    gate_directory = _gate_directory(root, session_id, issue_relative)
    state = _read_state(gate_directory / STATE_FILE)
    if state["session_id"] != session_id or state["issue"] != issue_relative:
        raise IssueGateError("gate state does not match the requested issue and session")
    owner = _claim_owner(root, issue_relative)
    if owner is None or owner["session_id"] != session_id or owner["issue"] != issue_relative:
        raise IssueGateError("gate state does not own the issue claim")
    if state["baseline_digest"] != _baseline_digest(
        state["head"], state["index_digest"], state["ignored_paths"], state["entries"]
    ):
        raise IssueGateError("gate baseline digest does not match its manifest")
    return issue, gate_directory, issue_relative, state


def render_report(state: dict[str, Any], delta: Delta) -> str:
    lines = [
        "# Finalize Issue report",
        "",
        f"- Issue: `{state['issue']}`",
        f"- Baseline: `{state['baseline_digest']}`",
        f"- Final delta: `{delta.digest}`",
        f"- Mapping units: `{len(delta.units)}`",
        "",
        "## Required mappings",
        "",
    ]
    if not delta.units:
        lines.append("- None (no issue-attributable delta).")
    else:
        for unit in delta.units:
            detail = unit.get("header", unit["change"])
            lines.append(f"- `{unit['id']}` ({unit['kind']}; {detail})")
    for path, rendered in delta.diffs:
        lines.extend(("", f"## Diff: `{path}`", "", "```diff", rendered.rstrip(), "```"))
    return "\n".join(lines) + "\n"


def inspect_issue(root: Path, session_id: str, issue_argument: str | Path) -> tuple[dict[str, Any], Delta]:
    _, gate_directory, _, state = _load_gate(root, session_id, issue_argument)
    return state, calculate_delta(root, gate_directory, state)


def _section(issue_text: str, heading: str) -> str | None:
    matches = list(re.finditer(rf"(?m)^{re.escape(heading)}\n", issue_text))
    if not matches:
        return None
    if len(matches) != 1:
        raise IssueGateError(f"issue repeats section: {heading}")
    match = matches[0]
    next_heading = re.search(r"(?m)^## ", issue_text[match.end() :])
    end = len(issue_text) if next_heading is None else match.end() + next_heading.start()
    return issue_text[match.end() : end].strip()


def _proof_fields(proof: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    mapping_position = proof.find(MAPPING_HEADING)
    field_text = proof if mapping_position < 0 else proof[:mapping_position]
    for line in field_text.splitlines():
        match = re.match(r"^- ([^:]+):\s*(.*)$", line)
        if match is None:
            continue
        name, value = match.groups()
        if name in fields:
            raise IssueGateError(f"finalization proof repeats field: {name}")
        fields[name] = value.strip()
    missing = [name for name in PROOF_FIELDS if name not in fields]
    if missing:
        raise IssueGateError(f"finalization proof is missing fields: {', '.join(missing)}")
    unexpected = sorted(set(fields) - set(PROOF_FIELDS))
    if unexpected:
        raise IssueGateError(f"finalization proof has unsupported fields: {', '.join(unexpected)}")
    for name in PROOF_FIELDS:
        value = fields[name]
        if not value or PLACEHOLDER.search(value):
            raise IssueGateError(f"finalization proof field is empty or provisional: {name}")
    return fields


def _proof_mappings(proof: str) -> dict[str, tuple[str, str]]:
    mapping_position = proof.find(MAPPING_HEADING)
    if mapping_position < 0:
        raise IssueGateError(f"finalization proof is missing {MAPPING_HEADING}")
    mappings: dict[str, tuple[str, str]] = {}
    saw_empty_marker = False
    for line in proof[mapping_position + len(MAPPING_HEADING) :].splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped == "- None (no issue-attributable delta).":
            if saw_empty_marker:
                raise IssueGateError("finalization proof repeats the empty delta marker")
            saw_empty_marker = True
            continue
        match = MAPPING_LINE.match(line)
        if match is None:
            raise IssueGateError(f"finalization proof has an invalid delta mapping line: {line}")
        unit_id, category, reason = match.groups()
        if unit_id in mappings:
            raise IssueGateError(f"finalization proof repeats delta unit: {unit_id}")
        if PLACEHOLDER.search(reason):
            raise IssueGateError(f"delta mapping is provisional: {unit_id}")
        mappings[unit_id] = (category, reason)
    if saw_empty_marker and mappings:
        raise IssueGateError("finalization proof cannot mix an empty delta marker with mappings")
    return mappings


def _validate_attestation(issue_text: str, state: dict[str, Any], delta: Delta) -> None:
    proof = _section(issue_text, PROOF_HEADING)
    if proof is None:
        raise IssueGateError("Completion: done requires a ## Finalization proof section")
    validate_proof(issue_text, state, delta)
    attestation = state.get("finalization")
    if not isinstance(attestation, dict):
        raise IssueGateError("Completion: done was not written by Finalize Issue")
    if attestation.get("delta_digest") != delta.digest:
        raise IssueGateError("finalization attestation does not match the current issue delta")
    proof_digest = hashlib.sha256(proof.encode("utf-8")).hexdigest()
    if attestation.get("proof_sha256") != proof_digest:
        raise IssueGateError("finalization proof changed after Finalize Issue")


def validate_proof(issue_text: str, state: dict[str, Any], delta: Delta) -> None:
    proof = _section(issue_text, PROOF_HEADING)
    if proof is None:
        raise IssueGateError("Completion: done requires a ## Finalization proof section")
    fields = _proof_fields(proof)
    baseline = fields["Baseline"].strip("`")
    final_delta = fields["Final delta"].strip("`")
    if baseline != state["baseline_digest"]:
        raise IssueGateError("finalization proof names a different issue-start baseline")
    if final_delta != delta.digest:
        raise IssueGateError("finalization proof is stale for the current issue delta")
    if fields["Result"].lower() != "passed":
        raise IssueGateError("finalization proof Result must be passed")
    review = fields["Independent review"].lower()
    if re.fullmatch(r"(?:performed|not required):\s+\S(?:.*\S)?", review) is None:
        raise IssueGateError(
            "Independent review must be 'performed: ...' or 'not required: <reason>'"
        )

    mappings = _proof_mappings(proof)
    expected = {unit["id"] for unit in delta.units}
    actual = set(mappings)
    if expected != actual:
        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)
        details = []
        if missing:
            details.append(f"unmapped units: {', '.join(missing)}")
        if unexpected:
            details.append(f"stale mappings: {', '.join(unexpected)}")
        raise IssueGateError("; ".join(details))


def finalize_issue(root: Path, session_id: str, issue_argument: str | Path) -> Delta:
    issue, gate_directory, _, state = _load_gate(root, session_id, issue_argument)
    issue_text = issue.read_text(encoding="utf-8")
    if _completion(issue_text) != "open":
        raise IssueGateError("Finalize Issue is the only transition and requires Completion: open")
    delta = calculate_delta(root, gate_directory, state)
    validate_proof(issue_text, state, delta)
    confirmed_delta = calculate_delta(root, gate_directory, state)
    if confirmed_delta.digest != delta.digest:
        raise IssueGateError("worktree changed while finalization was being validated")
    proof = _section(issue_text, PROOF_HEADING)
    if proof is None:
        raise IssueGateError("Completion: done requires a ## Finalization proof section")
    finalized_state = dict(state)
    finalized_state["finalization"] = {
        "delta_digest": delta.digest,
        "proof_sha256": hashlib.sha256(proof.encode("utf-8")).hexdigest(),
    }
    _atomic_write(gate_directory / STATE_FILE, _canonical_json(finalized_state) + b"\n")
    completed_text = issue_text.replace("Completion: open\n", "Completion: done\n", 1)
    _atomic_write(issue, completed_text.encode("utf-8"), stat.S_IMODE(issue.stat().st_mode))
    return delta


def _session_gate_directories(root: Path, session_id: str) -> list[Path]:
    session_directory = _gate_root(root) / session_id
    if not session_directory.exists():
        return []
    if session_directory.is_symlink() or not session_directory.is_dir():
        raise IssueGateError(f"issue gate session path is not a directory: {session_directory}")
    directories: list[Path] = []
    for path in session_directory.iterdir():
        if path.is_symlink() or not path.is_dir():
            raise IssueGateError(f"unexpected issue gate entry: {path}")
        directories.append(path)
    return sorted(directories)


def _find_gate_repository(cwd: Path, session_id: str) -> Path | None:
    for candidate in (cwd, *cwd.parents):
        if (_gate_root(candidate) / session_id).exists():
            return candidate
    return None


def evaluate_stop(raw_cwd: str | Path, raw_session_id: str) -> StopDecision:
    session_id = _normalize_session_id(raw_session_id)
    cwd = Path(raw_cwd)
    if not cwd.is_absolute() or not cwd.is_dir():
        return StopDecision("Issue completion gate received an invalid cwd.", (), None)
    candidate = _find_gate_repository(cwd.resolve(), session_id)
    if candidate is None:
        return StopDecision(None, (), None)
    try:
        root = _repository_root(candidate)
        completed: list[Path] = []
        for gate_directory in _session_gate_directories(root, session_id):
            state = _read_state(gate_directory / STATE_FILE)
            if state["session_id"] != session_id:
                raise IssueGateError(f"gate state has the wrong session: {gate_directory}")
            issue, issue_relative = _resolve_issue(root, state["issue"])
            if issue_relative != state["issue"]:
                raise IssueGateError(f"gate state issue path is not canonical: {state['issue']}")
            owner = _claim_owner(root, issue_relative)
            if (
                owner is None
                or owner["session_id"] != session_id
                or owner["issue"] != issue_relative
            ):
                raise IssueGateError("active gate state does not own the issue claim")
            completion = _completion(issue.read_text(encoding="utf-8"))
            if completion == "open":
                continue
            if state["baseline_digest"] != _baseline_digest(
                state["head"], state["index_digest"], state["ignored_paths"], state["entries"]
            ):
                raise IssueGateError("gate baseline digest does not match its manifest")
            delta = calculate_delta(root, gate_directory, state)
            _validate_attestation(issue.read_text(encoding="utf-8"), state, delta)
            completed.append(gate_directory)
        return StopDecision(None, tuple(completed), root)
    except (IssueGateError, KeyError, TypeError, ValueError, OSError, UnicodeError) as error:
        return StopDecision(f"Finalize Issue gate blocked Stop: {error}", (), candidate)


def cleanup_completed(root: Path, completed_directories: Sequence[Path]) -> None:
    gate_root = _gate_root(root).resolve()
    for directory in completed_directories:
        try:
            resolved_parent = directory.parent.resolve(strict=True)
            resolved_parent.relative_to(gate_root)
        except (OSError, ValueError) as error:
            raise IssueGateError(f"refusing to remove unsafe gate directory: {directory}") from error
        if directory.is_symlink() or not directory.is_dir():
            raise IssueGateError(f"gate cleanup target is not a directory: {directory}")
        state = _read_state(directory / STATE_FILE)
        shutil.rmtree(directory)
        try:
            directory.parent.rmdir()
        except OSError:
            pass
        _release_claim(root, state["session_id"], state["issue"])


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("begin", "inspect", "finalize"))
    parser.add_argument("--issue", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--cwd", default=os.getcwd())
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        session_id = _normalize_session_id(arguments.session_id)
        root = _repository_root(arguments.cwd)
        if arguments.command == "begin":
            state = begin_issue(root, session_id, arguments.issue)
            print(f"Baseline recorded: {state['baseline_digest']}")
        elif arguments.command == "inspect":
            state, delta = inspect_issue(root, session_id, arguments.issue)
            print(render_report(state, delta), end="")
        else:
            delta = finalize_issue(root, session_id, arguments.issue)
            print(f"Finalize Issue passed: {delta.digest}")
    except (IssueGateError, OSError, UnicodeError) as error:
        print(f"issue gate error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
