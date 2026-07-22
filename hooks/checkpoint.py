#!/usr/bin/env python3
"""Deliver session checkpoints and backstop local issue completion."""

from __future__ import annotations

import json
import os
import re
import stat
import sys
import uuid
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
from issue_gate import IssueGateError, cleanup_completed, evaluate_stop  # noqa: E402


CHECKPOINT_DIRECTORY = (".codex", "agents", "runtime", "checkpoints")
CHECKPOINT_SECTIONS = (
    "Task",
    "Progress",
    "Decisions",
    "Mistakes and corrections",
    "Binding rules",
    "Verification",
    "Next action",
)
SESSION_START_SOURCES = {"startup", "resume", "clear", "compact"}


class CheckpointHookError(Exception):
    """A hook input or checkpoint violates the confirmed fact contract."""


def _required_string(payload: dict[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value:
        raise CheckpointHookError(f"{field} must be a non-empty string")
    return value


def _session_paths(payload: dict[str, Any]) -> tuple[Path, Path]:
    raw_session_id = _required_string(payload, "session_id")
    try:
        session_id = str(uuid.UUID(raw_session_id))
    except (ValueError, AttributeError) as error:
        raise CheckpointHookError("session_id must be a UUID") from error

    raw_cwd = _required_string(payload, "cwd")
    if "\x00" in raw_cwd or "\n" in raw_cwd or "\r" in raw_cwd:
        raise CheckpointHookError("cwd contains an unsupported control character")
    cwd = Path(raw_cwd)
    if not cwd.is_absolute() or not cwd.is_dir():
        raise CheckpointHookError("cwd must be an existing absolute directory")

    checkpoint_root = cwd.resolve().joinpath(*CHECKPOINT_DIRECTORY)
    current = checkpoint_root / f"{session_id}.md"
    delivered = checkpoint_root / f"{session_id}.delivered.md"
    return current, delivered


def _is_regular_file(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return False
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        raise CheckpointHookError(f"checkpoint path is not a regular file: {path}")
    return True


def _validate_checkpoint(contents: str, path: Path) -> None:
    lines = contents.splitlines()
    if not lines or lines[0] != "# Checkpoint":
        raise CheckpointHookError(f"checkpoint must begin with '# Checkpoint': {path}")

    sections: list[str] = []
    for index, line in enumerate(lines):
        heading = re.match(r"^(#{1,6})(?:\s|$)", line)
        if heading is None:
            continue
        if index == 0 and line == "# Checkpoint":
            continue
        if heading.group(1) == "##" and line.startswith("## "):
            sections.append(line[3:])
            continue
        raise CheckpointHookError(f"checkpoint contains an unapproved heading: {path}")

    if tuple(sections) != CHECKPOINT_SECTIONS:
        expected = ", ".join(CHECKPOINT_SECTIONS)
        raise CheckpointHookError(
            f"checkpoint sections must appear exactly once in this order: {expected}: {path}"
        )


def _read_checkpoint(path: Path) -> str:
    if not _is_regular_file(path):
        raise CheckpointHookError(f"checkpoint does not exist: {path}")
    try:
        contents = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise CheckpointHookError(f"cannot read checkpoint: {path}: {error}") from error
    _validate_checkpoint(contents, path)
    return contents


def _deliver_checkpoint(current: Path, delivered: Path) -> str | None:
    if _is_regular_file(delivered):
        return _read_checkpoint(delivered)
    if not _is_regular_file(current):
        return None

    # Validate before the state transition so malformed state remains repairable.
    _read_checkpoint(current)
    try:
        os.replace(current, delivered)
    except FileNotFoundError as error:
        # A concurrent delivery may have completed after the existence checks.
        if _is_regular_file(delivered):
            return _read_checkpoint(delivered)
        raise CheckpointHookError(f"checkpoint disappeared during delivery: {current}") from error
    except OSError as error:
        raise CheckpointHookError(
            f"cannot atomically deliver checkpoint: {current} -> {delivered}: {error}"
        ) from error
    return _read_checkpoint(delivered)


def _restored_context(current: Path, contents: str | None) -> str:
    path_line = f"Current session checkpoint: {current}"
    if contents is None:
        return path_line
    return f"{path_line}\n\nRestored confirmed fact ledger:\n\n{contents}"


def _handle_session_start(payload: dict[str, Any]) -> None:
    source = _required_string(payload, "source")
    if source not in SESSION_START_SOURCES:
        raise CheckpointHookError(f"unsupported SessionStart source: {source}")

    current, delivered = _session_paths(payload)
    if source == "compact":
        contents = _deliver_checkpoint(current, delivered)
    elif source == "resume" and _is_regular_file(delivered):
        # Replay survives a process failure until a later Stop proves a response occurred.
        contents = _read_checkpoint(delivered)
    else:
        contents = None

    output = {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": _restored_context(current, contents),
        }
    }
    print(json.dumps(output, ensure_ascii=True, separators=(",", ":")))


def _handle_stop(payload: dict[str, Any]) -> None:
    _, delivered = _session_paths(payload)
    decision = evaluate_stop(_required_string(payload, "cwd"), _required_string(payload, "session_id"))
    if decision.blocked_reason is not None:
        print(
            json.dumps(
                {"decision": "block", "reason": decision.blocked_reason},
                ensure_ascii=True,
                separators=(",", ":"),
            )
        )
        return

    if _is_regular_file(delivered):
        # Invalid state is retained for repair instead of being silently burned.
        _read_checkpoint(delivered)
        try:
            delivered.unlink()
        except OSError as error:
            raise CheckpointHookError(
                f"cannot remove delivered checkpoint: {delivered}: {error}"
            ) from error

    try:
        cleanup_root = decision.repository_root or Path(_required_string(payload, "cwd")).resolve()
        cleanup_completed(cleanup_root, decision.completed_directories)
    except IssueGateError as error:
        raise CheckpointHookError(str(error)) from error


def _read_input() -> dict[str, Any]:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeError) as error:
        raise CheckpointHookError(f"stdin must contain one JSON object: {error}") from error
    if not isinstance(payload, dict):
        raise CheckpointHookError("stdin must contain one JSON object")
    return payload


def main() -> int:
    try:
        payload = _read_input()
        event_name = _required_string(payload, "hook_event_name")
        if event_name == "SessionStart":
            _handle_session_start(payload)
        elif event_name == "Stop":
            _handle_stop(payload)
        else:
            raise CheckpointHookError(f"unsupported hook event: {event_name}")
    except CheckpointHookError as error:
        print(f"checkpoint hook error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
