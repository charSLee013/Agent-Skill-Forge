#!/usr/bin/env python3
"""Create, publish, validate, and clean file-based delegation artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import stat
import sys
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


ROOT_NAME = "codex-delegations"
REQUEST_NAME = "REQUEST.md"
RESULT_PART_NAME = "RESULT.md.part"
RESULT_NAME = "RESULT.md"
TASK_NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
TASK_DIRECTORY_PATTERN = re.compile(r"(?P<task>[a-z0-9]+(?:-[a-z0-9]+)*)-(?P<nonce>[0-9a-f]{16})")
AGENT_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}")

REQUEST_SECTIONS = (
    "Objective",
    "Scope",
    "Non-goals",
    "Established decisions",
    "Relevant paths and evidence",
    "Constraints",
    "Required result",
    "Definition of done",
)
RESULT_SECTIONS = (
    "Outcome",
    "Scope examined",
    "Evidence",
    "Facts and inferences",
    "Verification",
    "Risks and uncovered areas",
    "Recommended next action",
)


class DelegationError(RuntimeError):
    """A delegation artifact or operation violates the protocol."""


@dataclass(frozen=True)
class DelegationPaths:
    root: Path
    session_id: str
    session_directory: Path
    directory: Path
    request: Path
    result_part: Path
    result: Path


def _emit(value: dict[str, object]) -> None:
    print(json.dumps(value, ensure_ascii=True, sort_keys=True))


def _delegation_root() -> Path:
    return Path(tempfile.gettempdir()).resolve() / ROOT_NAME


def _canonical_session_id(value: str) -> str:
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError) as error:
        raise DelegationError("session id must be a canonical UUID") from error
    canonical = str(parsed)
    if value != canonical:
        raise DelegationError("session id must be a canonical UUID")
    return canonical


def _task_name(value: str) -> str:
    if len(value) > 64 or TASK_NAME_PATTERN.fullmatch(value) is None:
        raise DelegationError(
            "task name must be a lowercase hyphenated slug of at most 64 characters"
        )
    return value


def _regular_file(path: Path, label: str) -> None:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError as error:
        raise DelegationError(f"{label} is missing: {path}") from error
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        raise DelegationError(f"{label} is not a regular file: {path}")


def _material_exists(path: Path) -> bool:
    """Return true for regular, dangling, or otherwise present directory entries."""
    return path.exists() or path.is_symlink()


def _real_directory(path: Path, label: str) -> None:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError as error:
        raise DelegationError(f"{label} is missing: {path}") from error
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        raise DelegationError(f"{label} is not a real directory: {path}")


def _make_private_directory(path: Path) -> None:
    try:
        path.mkdir(mode=0o700)
    except FileExistsError:
        _real_directory(path, "delegation directory")


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _atomic_write(path: Path, contents: str) -> None:
    temporary = path.with_name(f".{path.name}.{secrets.token_hex(8)}.part")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(contents)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def _template(title: str, sections: Sequence[str]) -> str:
    lines = [f"# {title}", ""]
    for section in sections:
        lines.extend((f"## {section}", "", ""))
    return "\n".join(lines).rstrip() + "\n"


def _markdown_headings(contents: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    fence: str | None = None
    for line_number, line in enumerate(contents.splitlines()):
        fence_match = re.match(r"^[ ]{0,3}(`{3,}|~{3,})", line)
        if fence_match is not None:
            marker = fence_match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is not None:
            continue
        heading_match = re.match(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", line)
        if heading_match is not None:
            headings.append(
                (line_number, f"{heading_match.group(1)} {heading_match.group(2).strip()}")
            )
    return headings


def _validate_markdown(contents: str, title: str, sections: Sequence[str], path: Path) -> None:
    expected = [f"# {title}", *(f"## {section}" for section in sections)]
    lines = contents.splitlines()
    if not lines or lines[0] != f"# {title}":
        raise DelegationError(f"{path.name} must begin with '# {title}'")
    headings = _markdown_headings(contents)
    observed = [heading for _, heading in headings]
    if observed != expected:
        raise DelegationError(
            f"{path.name} headings must appear exactly once in the approved order: {expected}"
        )
    for index, section in enumerate(sections, start=1):
        start = headings[index][0] + 1
        end = headings[index + 1][0] if index + 1 < len(headings) else len(lines)
        if not any(line.strip() for line in lines[start:end]):
            raise DelegationError(f"{path.name} section is empty: {section}")


def _read_markdown(path: Path, title: str, sections: Sequence[str]) -> str:
    _regular_file(path, path.name)
    try:
        contents = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise DelegationError(f"cannot read {path}: {error}") from error
    _validate_markdown(contents, title, sections, path)
    return contents


def _resolve_request(value: str) -> DelegationPaths:
    supplied = Path(value).expanduser()
    if not supplied.is_absolute():
        supplied = Path.cwd() / supplied
    request = Path(os.path.abspath(supplied))
    root = _delegation_root()
    try:
        relative = request.relative_to(root)
    except ValueError as error:
        raise DelegationError(f"request path is outside the delegation root: {request}") from error
    if len(relative.parts) != 3 or relative.parts[-1] != REQUEST_NAME:
        raise DelegationError(f"request path does not match the delegation layout: {request}")

    session_id, task_directory_name, _ = relative.parts
    session_id = _canonical_session_id(session_id)
    match = TASK_DIRECTORY_PATTERN.fullmatch(task_directory_name)
    if match is None:
        raise DelegationError(f"task directory does not match the delegation layout: {request.parent}")
    _task_name(match.group("task"))

    session_directory = root / session_id
    directory = session_directory / task_directory_name
    _real_directory(root, "delegation root")
    _real_directory(session_directory, "delegation session directory")
    _real_directory(directory, "delegation task directory")
    _regular_file(request, REQUEST_NAME)
    return DelegationPaths(
        root=root,
        session_id=session_id,
        session_directory=session_directory,
        directory=directory,
        request=request,
        result_part=directory / RESULT_PART_NAME,
        result=directory / RESULT_NAME,
    )


def _begin(session_id: str, task_name: str) -> DelegationPaths:
    session_id = _canonical_session_id(session_id)
    task_name = _task_name(task_name)
    root = _delegation_root()
    _make_private_directory(root)
    session_directory = root / session_id
    _make_private_directory(session_directory)

    for _ in range(32):
        directory = session_directory / f"{task_name}-{secrets.token_hex(8)}"
        try:
            directory.mkdir(mode=0o700)
            break
        except FileExistsError:
            continue
    else:
        raise DelegationError("could not allocate a unique delegation directory")

    paths = DelegationPaths(
        root=root,
        session_id=session_id,
        session_directory=session_directory,
        directory=directory,
        request=directory / REQUEST_NAME,
        result_part=directory / RESULT_PART_NAME,
        result=directory / RESULT_NAME,
    )
    try:
        _atomic_write(paths.request, _template("Delegation", REQUEST_SECTIONS))
    except BaseException:
        shutil.rmtree(directory, ignore_errors=True)
        raise
    return paths


def _path_payload(paths: DelegationPaths) -> dict[str, str]:
    return {
        "directory": str(paths.directory),
        "request_path": str(paths.request),
        "result_part_path": str(paths.result_part),
        "result_path": str(paths.result),
    }


def _workspace_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise DelegationError(f"workspace does not exist: {path}") from error
    _real_directory(resolved, "workspace")
    return resolved


def _owned_write_paths(workspace: Path, values: Sequence[str]) -> list[str]:
    owned: list[str] = []
    for value in values:
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = workspace / path
        resolved = path.resolve(strict=False)
        try:
            relative = resolved.relative_to(workspace)
        except ValueError as error:
            raise DelegationError(f"owned write path is outside the workspace: {path}") from error
        if not relative.parts:
            raise DelegationError("workspace root cannot be assigned as an owned write path")
        if path.is_symlink() or path.exists():
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode) or stat.S_ISDIR(mode):
                raise DelegationError(f"owned write path must identify a real file: {path}")
        owned.append(str(resolved))
    if len(set(owned)) != len(owned):
        raise DelegationError("owned write paths must be unique")
    return sorted(owned)


def _spawn_contract(paths: DelegationPaths, ownership: str) -> dict[str, object]:
    message = "\n".join(
        (
            f"REQUEST.md: {paths.request}",
            f"RESULT.md: {paths.result}",
            f"Ownership: {ownership}",
            (
                f"Publication: write {paths.result_part} first, then atomically rename it to "
                f"{paths.result}; no other result path is accepted."
            ),
            (
                "Final message: return only completion state, the predetermined RESULT.md path, "
                "and a minimal summary."
            ),
        )
    )
    return {
        "fork_turns": "none",
        "message": message,
        "parent_contract": {
            "chat_is_evidence": False,
            "result_path": str(paths.result),
            "wait_agent_is_status_only": True,
        },
    }


def _result_digest(paths: DelegationPaths) -> str:
    if _material_exists(paths.result_part):
        raise DelegationError(
            f"partial result remains; delegation is incomplete: {paths.result_part}"
        )
    contents = _read_markdown(paths.result, "Result", RESULT_SECTIONS)
    return hashlib.sha256(contents.encode("utf-8")).hexdigest()


def _publish(paths: DelegationPaths) -> str:
    _read_markdown(paths.request, "Delegation", REQUEST_SECTIONS)
    if _material_exists(paths.result):
        raise DelegationError(f"refusing to overwrite predetermined result: {paths.result}")
    _read_markdown(paths.result_part, "Result", RESULT_SECTIONS)
    try:
        os.replace(paths.result_part, paths.result)
    except OSError as error:
        raise DelegationError(
            f"cannot atomically publish {paths.result_part} as {paths.result}: {error}"
        ) from error
    _fsync_directory(paths.directory)
    return _result_digest(paths)


def _checkpoint_note(paths: DelegationPaths, agent_id: str, next_action: str) -> str:
    if AGENT_ID_PATTERN.fullmatch(agent_id) is None:
        raise DelegationError("agent id contains unsupported characters")
    if not next_action.strip() or "\n" in next_action or "\r" in next_action:
        raise DelegationError("next action must be one non-empty line")
    return "\n".join(
        (
            f"- Active delegation agent: `{agent_id}`",
            f"- Active delegation directory: `{paths.directory}`",
            f"- Next action: {next_action.strip()}",
        )
    )


def _fact_owner(workspace: Path, value: str, session_id: str) -> str:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = workspace / path
    resolved = path.resolve(strict=False)
    try:
        relative = resolved.relative_to(workspace)
    except ValueError as error:
        raise DelegationError(f"fact owner is outside the workspace: {path}") from error
    _regular_file(path, "fact owner")
    parts = relative.parts
    is_work_owner = (
        len(parts) >= 5
        and parts[:3] == (".codex", "agents", "work")
        and path.suffix == ".md"
    )
    is_checkpoint_owner = (
        len(parts) == 5
        and parts[:4] == (".codex", "agents", "runtime", "checkpoints")
        and path.name in {f"{session_id}.md", f"{session_id}.delivered.md"}
    )
    if not is_work_owner and not is_checkpoint_owner:
        raise DelegationError(
            "durable facts may be consumed only into a checkpoint or local work Markdown owner"
        )
    return str(resolved)


def _assert_clean_directory(paths: DelegationPaths) -> None:
    observed = {path.name for path in paths.directory.iterdir()}
    expected = {REQUEST_NAME, RESULT_NAME}
    if observed != expected:
        unexpected = sorted(observed - expected)
        missing = sorted(expected - observed)
        raise DelegationError(
            f"delegation directory is not ready for cleanup; unexpected={unexpected}, missing={missing}"
        )


def _cleanup(paths: DelegationPaths) -> None:
    _assert_clean_directory(paths)
    shutil.rmtree(paths.directory)
    for directory in (paths.session_directory, paths.root):
        try:
            directory.rmdir()
        except OSError:
            pass


def _command_begin(arguments: argparse.Namespace) -> int:
    if arguments.small_task:
        if arguments.session_id is not None or arguments.task_name is not None:
            raise DelegationError("small-task no-op does not accept session or task identifiers")
        _emit({"delegation_required": False, "status": "small-task-no-op"})
        return 0
    if arguments.session_id is None or arguments.task_name is None:
        raise DelegationError("non-trivial delegation requires --session-id and --task-name")
    paths = _begin(arguments.session_id, arguments.task_name)
    _emit({"delegation_required": True, "status": "request-created", **_path_payload(paths)})
    return 0


def _command_prepare(arguments: argparse.Namespace) -> int:
    paths = _resolve_request(arguments.request)
    _read_markdown(paths.request, "Delegation", REQUEST_SECTIONS)
    if _material_exists(paths.result) or _material_exists(paths.result_part):
        raise DelegationError("delegation already contains result material")
    if arguments.read_only:
        ownership = "read-only; repository writes are not permitted."
    else:
        workspace = _workspace_path(arguments.workspace)
        owned = _owned_write_paths(workspace, arguments.write_path)
        ownership = "write only these exact files: " + ", ".join(owned) + "."
    _emit({"status": "ready-to-spawn", **_spawn_contract(paths, ownership)})
    return 0


def _command_publish(arguments: argparse.Namespace) -> int:
    paths = _resolve_request(arguments.request)
    digest = _publish(paths)
    _emit({"status": "published", "result_digest": digest, "result_path": str(paths.result)})
    return 0


def _command_inspect(arguments: argparse.Namespace) -> int:
    paths = _resolve_request(arguments.request)
    _read_markdown(paths.request, "Delegation", REQUEST_SECTIONS)
    try:
        digest = _result_digest(paths)
    except DelegationError as error:
        _emit(
            {
                "status": "incomplete",
                "reason": str(error),
                "reissue_required": True,
                "result_path": str(paths.result),
            }
        )
        return 3
    _emit(
        {
            "status": "ready-for-parent-validation",
            "result_digest": digest,
            "result_path": str(paths.result),
            "required_parent_checks": [
                "important file:line claims",
                "reported commands",
                "facts versus inferences",
                "conclusions",
                "durable fact ownership",
            ],
        }
    )
    return 0


def _command_resume(arguments: argparse.Namespace) -> int:
    paths = _resolve_request(arguments.request)
    _read_markdown(paths.request, "Delegation", REQUEST_SECTIONS)
    try:
        digest = _result_digest(paths)
    except DelegationError as error:
        _emit(
            {
                "status": "incomplete",
                "reason": str(error),
                "reissue_required": True,
                "result_path": str(paths.result),
                "next_action": (
                    "record the failed delegation and explicitly start a new unique delegation "
                    "with fork_turns=none"
                ),
            }
        )
        return 3
    _emit(
        {
            "status": "ready-for-parent-validation",
            "reissue_required": False,
            "result_digest": digest,
            "result_path": str(paths.result),
        }
    )
    return 0


def _command_checkpoint(arguments: argparse.Namespace) -> int:
    paths = _resolve_request(arguments.request)
    note = _checkpoint_note(paths, arguments.agent_id, arguments.next_action)
    _emit({"status": "checkpoint-note-ready", "checkpoint_markdown": note})
    return 0


def _command_cleanup(arguments: argparse.Namespace) -> int:
    paths = _resolve_request(arguments.request)
    _read_markdown(paths.request, "Delegation", REQUEST_SECTIONS)
    digest = _result_digest(paths)
    if arguments.result_digest != digest:
        raise DelegationError("result changed or was not validated before cleanup")
    required_attestations = (
        arguments.file_line_claims_verified,
        arguments.command_claims_verified,
        arguments.conclusions_verified,
    )
    if not all(required_attestations):
        raise DelegationError(
            "cleanup requires file:line, command, and conclusion verification attestations"
        )
    consumed_to: list[str] = []
    if arguments.consumed_to:
        workspace = _workspace_path(arguments.workspace)
        consumed_to = [
            _fact_owner(workspace, value, paths.session_id)
            for value in arguments.consumed_to
        ]
    elif not arguments.no_durable_facts:
        raise DelegationError(
            "cleanup requires --consumed-to or the explicit --no-durable-facts disposition"
        )
    _cleanup(paths)
    _emit(
        {
            "status": "consumed-and-cleaned",
            "facts_consumed_to": consumed_to,
            "no_durable_facts": arguments.no_durable_facts,
            "removed_directory": str(paths.directory),
        }
    )
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage the temporary REQUEST.md and RESULT.md delegation protocol."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    begin = subparsers.add_parser("begin", help="Create a unique non-trivial delegation request.")
    begin.add_argument("--small-task", action="store_true")
    begin.add_argument("--session-id")
    begin.add_argument("--task-name")
    begin.set_defaults(handler=_command_begin)

    prepare = subparsers.add_parser(
        "prepare", help="Validate REQUEST.md and emit the exact independent spawn contract."
    )
    prepare.add_argument("--request", required=True)
    prepare.add_argument("--workspace", default=".")
    ownership = prepare.add_mutually_exclusive_group(required=True)
    ownership.add_argument("--read-only", action="store_true")
    ownership.add_argument("--write-path", action="append")
    prepare.set_defaults(handler=_command_prepare)

    publish = subparsers.add_parser(
        "publish", help="Validate and atomically rename RESULT.md.part to RESULT.md."
    )
    publish.add_argument("--request", required=True)
    publish.set_defaults(handler=_command_publish)

    inspect = subparsers.add_parser(
        "inspect", help="Validate the predetermined result before parent evidence review."
    )
    inspect.add_argument("--request", required=True)
    inspect.set_defaults(handler=_command_inspect)

    resume = subparsers.add_parser(
        "resume", help="Check the predetermined result after a compaction interruption."
    )
    resume.add_argument("--request", required=True)
    resume.set_defaults(handler=_command_resume)

    checkpoint = subparsers.add_parser(
        "checkpoint", help="Render the active delegation facts for the session checkpoint."
    )
    checkpoint.add_argument("--request", required=True)
    checkpoint.add_argument("--agent-id", required=True)
    checkpoint.add_argument("--next-action", required=True)
    checkpoint.set_defaults(handler=_command_checkpoint)

    cleanup = subparsers.add_parser(
        "cleanup", help="Remove a validated result only after parent verification and consumption."
    )
    cleanup.add_argument("--request", required=True)
    cleanup.add_argument("--result-digest", required=True)
    cleanup.add_argument("--file-line-claims-verified", action="store_true")
    cleanup.add_argument("--command-claims-verified", action="store_true")
    cleanup.add_argument("--conclusions-verified", action="store_true")
    cleanup.add_argument("--workspace", default=".")
    fact_disposition = cleanup.add_mutually_exclusive_group(required=True)
    fact_disposition.add_argument("--consumed-to", action="append")
    fact_disposition.add_argument("--no-durable-facts", action="store_true")
    cleanup.set_defaults(handler=_command_cleanup)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    arguments = parser.parse_args(argv)
    try:
        return arguments.handler(arguments)
    except DelegationError as error:
        print(f"delegation error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
