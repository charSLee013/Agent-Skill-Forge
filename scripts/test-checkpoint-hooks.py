#!/usr/bin/env python3
"""Deterministic contract tests for the confirmed fact checkpoint hooks."""

from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK = REPO_ROOT / "hooks" / "checkpoint.py"
HOOK_CONFIG = REPO_ROOT / "hooks" / "hooks.json"
CHECKPOINT_SECTIONS = (
    "Task",
    "Progress",
    "Decisions",
    "Mistakes and corrections",
    "Binding rules",
    "Verification",
    "Next action",
)


def checkpoint_text(marker: str) -> str:
    bodies = {
        "Task": f"Task {marker}",
        "Progress": f"Progress {marker}",
        "Decisions": f"Decisions {marker}",
        "Mistakes and corrections": f"Corrections {marker}",
        "Binding rules": f"Rules {marker}",
        "Verification": f"Verification {marker}",
        "Next action": f"Next {marker}",
    }
    parts = ["# Checkpoint"]
    for section in CHECKPOINT_SECTIONS:
        parts.extend(("", f"## {section}", bodies[section]))
    return "\n".join(parts) + "\n"


class CheckpointHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.cwd = Path(self.temporary_directory.name).resolve()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def payload(
        self,
        event_name: str,
        session_id: str,
        *,
        source: str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "session_id": session_id,
            "cwd": str(self.cwd),
            "hook_event_name": event_name,
            "model": "test-model",
            "permission_mode": "default",
            "transcript_path": None,
        }
        if source is not None:
            payload["source"] = source
        if event_name == "Stop":
            payload.update(
                {
                    "turn_id": "turn-test",
                    "stop_hook_active": False,
                    "last_assistant_message": "test response",
                }
            )
        return payload

    def run_hook(self, payload: dict[str, Any]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(payload),
            text=True,
            cwd=self.cwd,
            capture_output=True,
            check=False,
        )

    def paths(self, session_id: str) -> tuple[Path, Path]:
        root = self.cwd / ".codex" / "agents" / "runtime" / "checkpoints"
        normalized = str(uuid.UUID(session_id))
        return root / f"{normalized}.md", root / f"{normalized}.delivered.md"

    def write_current(self, session_id: str, marker: str) -> Path:
        current, _ = self.paths(session_id)
        current.parent.mkdir(parents=True, exist_ok=True)
        current.write_text(checkpoint_text(marker), encoding="utf-8")
        return current

    def context(self, result: subprocess.CompletedProcess[str]) -> str:
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertTrue(output["continue"])
        return output["hookSpecificOutput"]["additionalContext"]

    def test_hook_bundle_uses_only_session_start_and_stop(self) -> None:
        config = json.loads(HOOK_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(set(config), {"description", "hooks"})
        self.assertEqual(set(config["hooks"]), {"SessionStart", "Stop"})
        for event_name in ("SessionStart", "Stop"):
            groups = config["hooks"][event_name]
            self.assertEqual(len(groups), 1)
            self.assertNotIn("matcher", groups[0])
            handlers = groups[0]["hooks"]
            self.assertEqual(len(handlers), 1)
            self.assertEqual(handlers[0]["type"], "command")
            self.assertIn("${PLUGIN_ROOT}/hooks/checkpoint.py", handlers[0]["command"])

        hook_source = HOOK.read_text(encoding="utf-8")
        for forbidden_contract in (
            "PreCompact",
            "PostCompact",
            "PostToolUse",
            "transcript_path",
            "tool_input",
            "changed_files",
            "subprocess",
        ):
            self.assertNotIn(forbidden_contract, hook_source)

        source_tree = ast.parse(hook_source)
        uses_atomic_replace = any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "os"
            and node.func.attr == "replace"
            for node in ast.walk(source_tree)
        )
        self.assertTrue(uses_atomic_replace, "delivery must use os.replace")

    def test_startup_and_empty_stop_do_not_create_state(self) -> None:
        session_id = str(uuid.uuid4())
        current, delivered = self.paths(session_id)

        context = self.context(
            self.run_hook(self.payload("SessionStart", session_id, source="startup"))
        )
        self.assertEqual(context, f"Current session checkpoint: {current}")
        self.assertFalse(current.parent.exists())

        stop = self.run_hook(self.payload("Stop", session_id))
        self.assertEqual(stop.returncode, 0, stop.stderr)
        self.assertEqual(stop.stdout, "")
        self.assertFalse(current.exists())
        self.assertFalse(delivered.exists())
        self.assertFalse(current.parent.exists())

    def test_compact_replay_and_stop_follow_two_phase_lifecycle(self) -> None:
        session_id = str(uuid.uuid4())
        current = self.write_current(session_id, "alpha")
        _, delivered = self.paths(session_id)

        compact_context = self.context(
            self.run_hook(self.payload("SessionStart", session_id, source="compact"))
        )
        self.assertFalse(current.exists())
        self.assertEqual(delivered.read_text(encoding="utf-8"), checkpoint_text("alpha"))
        self.assertIn("Restored confirmed fact ledger:", compact_context)
        self.assertIn("Task alpha", compact_context)

        resume_context = self.context(
            self.run_hook(self.payload("SessionStart", session_id, source="resume"))
        )
        self.assertIn("Task alpha", resume_context)
        self.assertTrue(delivered.exists(), "resume must not burn delivered state")

        stop = self.run_hook(self.payload("Stop", session_id))
        self.assertEqual(stop.returncode, 0, stop.stderr)
        self.assertFalse(delivered.exists())

    def test_repeated_resume_replays_after_pre_stop_failure(self) -> None:
        session_id = str(uuid.uuid4())
        self.write_current(session_id, "crash-safe")
        _, delivered = self.paths(session_id)

        self.context(self.run_hook(self.payload("SessionStart", session_id, source="compact")))
        first_replay = self.context(
            self.run_hook(self.payload("SessionStart", session_id, source="resume"))
        )
        second_replay = self.context(
            self.run_hook(self.payload("SessionStart", session_id, source="resume"))
        )
        self.assertEqual(first_replay, second_replay)
        self.assertIn("crash-safe", second_replay)
        self.assertTrue(delivered.exists())

    def test_startup_and_clear_do_not_replay_delivered_state(self) -> None:
        session_id = str(uuid.uuid4())
        self.write_current(session_id, "not-for-startup")
        _, delivered = self.paths(session_id)
        self.context(self.run_hook(self.payload("SessionStart", session_id, source="compact")))

        startup_context = self.context(
            self.run_hook(self.payload("SessionStart", session_id, source="startup"))
        )
        clear_context = self.context(
            self.run_hook(self.payload("SessionStart", session_id, source="clear"))
        )
        self.assertNotIn("not-for-startup", startup_context)
        self.assertNotIn("not-for-startup", clear_context)
        self.assertEqual(startup_context, clear_context.split("\n\n")[0])
        self.assertTrue(delivered.exists())

    def test_interleaved_sessions_cannot_cross_read_or_delete(self) -> None:
        session_a = str(uuid.uuid4())
        session_b = str(uuid.uuid4())
        current_a = self.write_current(session_a, "session-a-only")
        current_b = self.write_current(session_b, "session-b-only")
        _, delivered_a = self.paths(session_a)
        _, delivered_b = self.paths(session_b)

        context_a = self.context(
            self.run_hook(self.payload("SessionStart", session_a, source="compact"))
        )
        self.assertIn("session-a-only", context_a)
        self.assertNotIn("session-b-only", context_a)
        self.assertTrue(delivered_a.exists())
        self.assertTrue(current_b.exists())

        stop_b = self.run_hook(self.payload("Stop", session_b))
        self.assertEqual(stop_b.returncode, 0, stop_b.stderr)
        self.assertTrue(delivered_a.exists())
        self.assertTrue(current_b.exists())

        context_b = self.context(
            self.run_hook(self.payload("SessionStart", session_b, source="compact"))
        )
        self.assertIn("session-b-only", context_b)
        self.assertNotIn("session-a-only", context_b)
        self.assertTrue(delivered_b.exists())

        stop_a = self.run_hook(self.payload("Stop", session_a))
        self.assertEqual(stop_a.returncode, 0, stop_a.stderr)
        self.assertFalse(delivered_a.exists())
        self.assertTrue(delivered_b.exists())
        self.assertFalse(current_a.exists())

    def test_existing_delivery_is_replayed_without_overwrite(self) -> None:
        session_id = str(uuid.uuid4())
        current = self.write_current(session_id, "new-current")
        _, delivered = self.paths(session_id)
        delivered.write_text(checkpoint_text("old-delivery"), encoding="utf-8")

        context = self.context(
            self.run_hook(self.payload("SessionStart", session_id, source="compact"))
        )
        self.assertIn("old-delivery", context)
        self.assertNotIn("new-current", context)
        self.assertEqual(delivered.read_text(encoding="utf-8"), checkpoint_text("old-delivery"))
        self.assertEqual(current.read_text(encoding="utf-8"), checkpoint_text("new-current"))

        self.assertEqual(self.run_hook(self.payload("Stop", session_id)).returncode, 0)
        next_context = self.context(
            self.run_hook(self.payload("SessionStart", session_id, source="compact"))
        )
        self.assertIn("new-current", next_context)
        self.assertFalse(current.exists())

    def test_malformed_checkpoint_is_never_delivered_or_burned(self) -> None:
        session_id = str(uuid.uuid4())
        current, delivered = self.paths(session_id)
        current.parent.mkdir(parents=True, exist_ok=True)
        malformed = checkpoint_text("bad") + "\n### Extra\nnot approved\n"
        current.write_text(malformed, encoding="utf-8")

        compact = self.run_hook(self.payload("SessionStart", session_id, source="compact"))
        self.assertNotEqual(compact.returncode, 0)
        self.assertIn("contains an unapproved heading", compact.stderr)
        self.assertEqual(current.read_text(encoding="utf-8"), malformed)
        self.assertFalse(delivered.exists())

        current.replace(delivered)
        stop = self.run_hook(self.payload("Stop", session_id))
        self.assertNotEqual(stop.returncode, 0)
        self.assertTrue(delivered.exists(), "malformed delivered state must remain repairable")

    def test_invalid_session_id_cannot_escape_checkpoint_directory(self) -> None:
        result = self.run_hook(
            self.payload("SessionStart", "../../outside", source="startup")
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("session_id must be a UUID", result.stderr)
        self.assertFalse((self.cwd / ".codex").exists())

    @unittest.skipIf(os.name == "nt", "symlink setup differs on Windows")
    def test_checkpoint_symlink_is_not_followed(self) -> None:
        session_id = str(uuid.uuid4())
        current, delivered = self.paths(session_id)
        current.parent.mkdir(parents=True, exist_ok=True)
        outside = self.cwd / "outside.md"
        outside.write_text(checkpoint_text("outside"), encoding="utf-8")
        current.symlink_to(outside)

        result = self.run_hook(self.payload("SessionStart", session_id, source="compact"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not a regular file", result.stderr)
        self.assertTrue(current.is_symlink())
        self.assertFalse(delivered.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
