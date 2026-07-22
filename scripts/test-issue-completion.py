#!/usr/bin/env python3
"""Focused contract tests for baseline-aware issue completion."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
FINALIZE = REPO_ROOT / "scripts" / "finalize-issue.py"
HOOK = REPO_ROOT / "hooks" / "checkpoint.py"


class IssueCompletionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name).resolve()
        self.session_id = str(uuid.uuid4())
        self.issue = self.root / ".codex/agents/work/example/issues/01-build.md"

        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Issue Gate Test")
        (self.root / ".gitignore").write_text(".codex/\n", encoding="utf-8")
        (self.root / "tracked.txt").write_text("one\ntwo\nthree\n", encoding="utf-8")
        (self.root / "preexisting.txt").write_text("baseline\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

        self.issue.parent.mkdir(parents=True)
        self.issue.write_text(
            "Completion: open\n"
            "Status: ready-for-agent\n\n"
            "## What to build\n\n"
            "Exercise the issue gate.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["git", *arguments],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def command_args(self, action: str, session_id: str | None = None) -> list[str]:
        return [
            sys.executable,
            str(FINALIZE),
            action,
            "--issue",
            str(self.issue.relative_to(self.root)),
            "--session-id",
            session_id or self.session_id,
            "--cwd",
            str(self.root),
        ]

    def command(self, action: str, session_id: str | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            self.command_args(action, session_id),
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )

    def begin(self) -> None:
        result = self.command("begin")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Baseline recorded:", result.stdout)

    def inspect(self) -> tuple[str, str, list[str], str]:
        result = self.command("inspect")
        self.assertEqual(result.returncode, 0, result.stderr)
        baseline = re.search(r"^- Baseline: `([0-9a-f]{64})`$", result.stdout, re.MULTILINE)
        delta = re.search(r"^- Final delta: `([0-9a-f]{64})`$", result.stdout, re.MULTILINE)
        self.assertIsNotNone(baseline)
        self.assertIsNotNone(delta)
        units = re.findall(r"^- `([^`]+)` \((?:file|hunk);", result.stdout, re.MULTILINE)
        return baseline.group(1), delta.group(1), units, result.stdout

    def write_proof(
        self,
        baseline: str,
        delta: str,
        units: list[str],
        *,
        omitted_units: set[str] | None = None,
        omit_field: str | None = None,
    ) -> None:
        fields = {
            "Baseline": f"`{baseline}`",
            "Final delta": f"`{delta}`",
            "Scope audit": "Every listed unit belongs to the fixture acceptance scope.",
            "Interface audit": "No public interface was added or widened.",
            "Dependency and persistence audit": "No dependency, migration, format, or state was added.",
            "Error-handling audit": "Existing behavior is reused without a duplicate fallback.",
            "Test justification": "The retained test covers baseline attribution and Stop decisions.",
            "Cleanup audit": "No debug, scratch, generated, or temporary material remains.",
            "Acceptance evidence": "The focused issue-gate command completed successfully.",
            "Independent review": "not required: the fixture is narrow and deterministic.",
            "Result": "passed",
        }
        if omit_field is not None:
            fields.pop(omit_field)
        lines = ["", "## Finalization proof", ""]
        lines.extend(f"- {name}: {value}" for name, value in fields.items())
        lines.extend(("", "### Delta mapping", ""))
        omitted_units = omitted_units or set()
        for unit in units:
            if unit not in omitted_units:
                lines.append(f"- `{unit}` -> `scope`: Required by the fixture acceptance path.")
        self.issue.write_text(
            self.issue.read_text(encoding="utf-8").rstrip() + "\n" + "\n".join(lines) + "\n",
            encoding="utf-8",
        )

    def stop_payload(self, cwd: Path | None = None) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "turn_id": "turn-test",
            "cwd": str(cwd or self.root),
            "hook_event_name": "Stop",
            "model": "test-model",
            "permission_mode": "default",
            "transcript_path": None,
            "stop_hook_active": False,
            "last_assistant_message": "test response",
        }

    def session_start_payload(self, source: str) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "cwd": str(self.root),
            "hook_event_name": "SessionStart",
            "source": source,
            "model": "test-model",
            "permission_mode": "default",
            "transcript_path": None,
        }

    def run_stop(self, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(self.stop_payload(cwd)),
            cwd=cwd or self.root,
            text=True,
            capture_output=True,
            check=False,
        )

    def run_session_start(self, source: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(self.session_start_payload(source)),
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_baseline_excludes_unchanged_preexisting_dirty_state(self) -> None:
        (self.root / "preexisting.txt").write_text("baseline\nuser change\n", encoding="utf-8")
        (self.root / "preexisting-untracked.txt").write_text("user file\n", encoding="utf-8")
        self.begin()

        baseline, initial_delta, initial_units, _ = self.inspect()
        self.assertRegex(baseline, r"^[0-9a-f]{64}$")
        self.assertRegex(initial_delta, r"^[0-9a-f]{64}$")
        self.assertEqual(initial_units, [])

        (self.root / "tracked.txt").write_text("one\nchanged\nthree\n", encoding="utf-8")
        with (self.root / "preexisting.txt").open("a", encoding="utf-8") as output:
            output.write("issue change\n")
        (self.root / "new-file.txt").write_text("new\n", encoding="utf-8")

        _, _, units, report = self.inspect()
        paths = {unit.split("#", 1)[0] for unit in units}
        self.assertEqual(paths, {"tracked.txt", "preexisting.txt", "new-file.txt"})
        self.assertNotIn("preexisting-untracked.txt#", report)
        self.assertTrue(any("#file" in unit for unit in units))
        self.assertTrue(any("#hunk-" in unit for unit in units))

    def test_preexisting_staged_index_is_preserved_by_the_baseline(self) -> None:
        (self.root / "preexisting.txt").write_text("baseline\nuser staged change\n", encoding="utf-8")
        self.git("add", "preexisting.txt")
        self.begin()

        (self.root / "tracked.txt").write_text("one\naccepted\nthree\n", encoding="utf-8")
        baseline, delta, units, _ = self.inspect()
        self.assertTrue(any(unit.startswith("tracked.txt#") for unit in units))
        self.write_proof(baseline, delta, units)
        self.assertEqual(self.command("finalize").returncode, 0)

    def test_index_only_drift_is_rejected_before_and_after_finalize(self) -> None:
        self.begin()
        baseline, delta, units, _ = self.inspect()
        self.write_proof(baseline, delta, units)

        def assert_index_drift() -> None:
            inspected = self.command("inspect")
            self.assertNotEqual(inspected.returncode, 0)
            self.assertIn("Git index changed", inspected.stderr)

        (self.root / "tracked.txt").write_text("staged only\n", encoding="utf-8")
        self.git("add", "tracked.txt")
        (self.root / "tracked.txt").write_text("one\ntwo\nthree\n", encoding="utf-8")
        assert_index_drift()
        finalize = self.command("finalize")
        self.assertNotEqual(finalize.returncode, 0)
        self.assertIn("Git index changed", finalize.stderr)
        self.git("reset", "--", "tracked.txt")

        self.git("update-index", "--chmod=+x", "tracked.txt")
        assert_index_drift()
        self.git("update-index", "--chmod=-x", "tracked.txt")

        staged_new = self.root / "staged-new.txt"
        staged_new.write_text("new staged file\n", encoding="utf-8")
        self.git("add", "staged-new.txt")
        assert_index_drift()
        self.git("rm", "--cached", "-f", "staged-new.txt")
        staged_new.unlink()

        self.git("rm", "--cached", "tracked.txt")
        assert_index_drift()
        self.git("add", "tracked.txt")

        self.assertEqual(self.command("finalize").returncode, 0)

        (self.root / "tracked.txt").write_text("staged after done\n", encoding="utf-8")
        self.git("add", "tracked.txt")
        (self.root / "tracked.txt").write_text("one\ntwo\nthree\n", encoding="utf-8")
        stop = self.run_stop()
        self.assertEqual(stop.returncode, 0, stop.stderr)
        output = json.loads(stop.stdout)
        self.assertEqual(output["decision"], "block")
        self.assertIn("Git index changed", output["reason"])

    def test_issue_claim_is_atomic_across_concurrent_sessions(self) -> None:
        sessions = [str(uuid.uuid4()), str(uuid.uuid4())]
        processes = [
            subprocess.Popen(
                self.command_args("begin", session),
                cwd=self.root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            for session in sessions
        ]
        results = [process.communicate() for process in processes]
        returncodes = [process.returncode for process in processes]
        self.assertEqual(returncodes.count(0), 1)
        self.assertEqual(returncodes.count(1), 1)
        loser_output = results[returncodes.index(1)][1]
        self.assertIn("issue claim", loser_output)

        claim_files = list(
            (self.root / ".codex/agents/runtime/issue-gates/claims").glob("*/claim.json")
        )
        receipts = list(
            (self.root / ".codex/agents/runtime/issue-gates").glob("*/**/state.json")
        )
        self.assertEqual(len(claim_files), 1)
        self.assertEqual(len(receipts), 1)

    def test_new_ignored_paths_must_be_cleaned_before_inspect_can_pass(self) -> None:
        (self.root / ".gitignore").write_text(".codex/\nignored-output/\n", encoding="utf-8")
        ignored_directory = self.root / "ignored-output"
        ignored_directory.mkdir()
        preexisting = ignored_directory / "preexisting.log"
        preexisting.write_text("baseline\n", encoding="utf-8")
        self.begin()

        debug = ignored_directory / "debug.log"
        debug.write_text("temporary output\n", encoding="utf-8")
        preexisting.unlink()
        blocked = self.command("inspect")
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("new ignored paths", blocked.stderr)
        self.assertIn("removed baseline ignored paths", blocked.stderr)

        preexisting.write_text("baseline\n", encoding="utf-8")
        debug.unlink()
        baseline, delta, units, _ = self.inspect()
        self.assertEqual(units, [])
        self.write_proof(baseline, delta, units)
        self.assertEqual(self.command("finalize").returncode, 0)

    def test_finalize_rejects_every_unmapped_file_and_hunk(self) -> None:
        self.begin()
        (self.root / "tracked.txt").write_text("changed\n", encoding="utf-8")
        (self.root / "scratch.py").write_text("print('debug')\n", encoding="utf-8")
        baseline, delta, units, _ = self.inspect()
        scratch_units = {unit for unit in units if unit.startswith("scratch.py#")}
        self.assertTrue(scratch_units)
        self.write_proof(baseline, delta, units, omitted_units=scratch_units)

        result = self.command("finalize")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unmapped units: scratch.py#", result.stderr)
        self.assertTrue(self.issue.read_text(encoding="utf-8").startswith("Completion: open\n"))

    def test_finalize_requires_all_audit_evidence(self) -> None:
        self.begin()
        (self.root / "tracked.txt").write_text("changed\n", encoding="utf-8")
        baseline, delta, units, _ = self.inspect()
        self.write_proof(baseline, delta, units, omit_field="Interface audit")

        result = self.command("finalize")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing fields: Interface audit", result.stderr)
        self.assertTrue(self.issue.read_text(encoding="utf-8").startswith("Completion: open\n"))

    def test_finalize_is_open_to_done_and_stop_cleans_the_receipt(self) -> None:
        self.begin()
        (self.root / "tracked.txt").write_text("one\naccepted\nthree\n", encoding="utf-8")
        baseline, delta, units, _ = self.inspect()
        self.write_proof(baseline, delta, units)

        finalized = self.command("finalize")
        self.assertEqual(finalized.returncode, 0, finalized.stderr)
        self.assertTrue(self.issue.read_text(encoding="utf-8").startswith("Completion: done\n"))
        repeated = self.command("finalize")
        self.assertNotEqual(repeated.returncode, 0)
        self.assertIn("requires Completion: open", repeated.stderr)

        subdirectory = self.root / "nested"
        subdirectory.mkdir()
        stop = self.run_stop(subdirectory)
        self.assertEqual(stop.returncode, 0, stop.stderr)
        self.assertEqual(stop.stdout, "")
        session_directory = self.root / ".codex/agents/runtime/issue-gates" / self.session_id
        self.assertFalse(session_directory.exists())
        self.assertFalse((self.root / ".codex/agents/runtime/issue-gates").exists())

    def test_stop_allows_open_and_blocks_done_without_proof(self) -> None:
        self.begin()
        open_stop = self.run_stop()
        self.assertEqual(open_stop.returncode, 0, open_stop.stderr)
        self.assertEqual(open_stop.stdout, "")

        issue_text = self.issue.read_text(encoding="utf-8")
        self.issue.write_text(
            issue_text.replace("Completion: open\n", "Completion: done\n", 1),
            encoding="utf-8",
        )
        blocked = self.run_stop()
        self.assertEqual(blocked.returncode, 0, blocked.stderr)
        output = json.loads(blocked.stdout)
        self.assertEqual(output["decision"], "block")
        self.assertIn("requires a ## Finalization proof", output["reason"])

    def test_stop_rejects_a_valid_proof_when_done_was_edited_directly(self) -> None:
        self.begin()
        (self.root / "tracked.txt").write_text("accepted\n", encoding="utf-8")
        baseline, delta, units, _ = self.inspect()
        self.write_proof(baseline, delta, units)
        issue_text = self.issue.read_text(encoding="utf-8")
        self.issue.write_text(
            issue_text.replace("Completion: open\n", "Completion: done\n", 1),
            encoding="utf-8",
        )

        blocked = self.run_stop()
        self.assertEqual(blocked.returncode, 0, blocked.stderr)
        output = json.loads(blocked.stdout)
        self.assertEqual(output["decision"], "block")
        self.assertIn("was not written by Finalize Issue", output["reason"])

    def test_blocked_stop_does_not_burn_a_delivered_checkpoint(self) -> None:
        self.begin()
        checkpoint_root = self.root / ".codex/agents/runtime/checkpoints"
        checkpoint_root.mkdir(parents=True)
        checkpoint = checkpoint_root / f"{self.session_id}.md"
        sections = (
            "Task",
            "Progress",
            "Decisions",
            "Mistakes and corrections",
            "Binding rules",
            "Verification",
            "Next action",
        )
        checkpoint.write_text(
            "# Checkpoint\n\n"
            + "\n\n".join(f"## {section}\nstate" for section in sections)
            + "\n",
            encoding="utf-8",
        )
        compact = self.run_session_start("compact")
        self.assertEqual(compact.returncode, 0, compact.stderr)
        delivered = checkpoint_root / f"{self.session_id}.delivered.md"
        self.assertTrue(delivered.exists())

        issue_text = self.issue.read_text(encoding="utf-8")
        self.issue.write_text(
            issue_text.replace("Completion: open\n", "Completion: done\n", 1),
            encoding="utf-8",
        )
        blocked = self.run_stop()
        self.assertEqual(blocked.returncode, 0, blocked.stderr)
        self.assertEqual(json.loads(blocked.stdout)["decision"], "block")
        self.assertTrue(delivered.exists())

    def test_stop_blocks_when_worktree_changes_after_finalization(self) -> None:
        self.begin()
        (self.root / "tracked.txt").write_text("accepted\n", encoding="utf-8")
        baseline, delta, units, _ = self.inspect()
        self.write_proof(baseline, delta, units)
        self.assertEqual(self.command("finalize").returncode, 0)

        (self.root / "tracked.txt").write_text("drifted after proof\n", encoding="utf-8")
        blocked = self.run_stop()
        self.assertEqual(blocked.returncode, 0, blocked.stderr)
        output = json.loads(blocked.stdout)
        self.assertEqual(output["decision"], "block")
        self.assertIn("proof is stale", output["reason"])

    def test_stop_blocks_when_proof_changes_after_finalization(self) -> None:
        self.begin()
        (self.root / "tracked.txt").write_text("accepted\n", encoding="utf-8")
        baseline, delta, units, _ = self.inspect()
        self.write_proof(baseline, delta, units)
        self.assertEqual(self.command("finalize").returncode, 0)

        proof = self.issue.read_text(encoding="utf-8")
        self.issue.write_text(
            proof.replace(
                "No public interface was added or widened.",
                "No public interface changed; evidence was edited later.",
            ),
            encoding="utf-8",
        )
        blocked = self.run_stop()
        self.assertEqual(blocked.returncode, 0, blocked.stderr)
        output = json.loads(blocked.stdout)
        self.assertEqual(output["decision"], "block")
        self.assertIn("proof changed after Finalize Issue", output["reason"])

    def test_malformed_active_receipt_blocks_instead_of_failing_open(self) -> None:
        state_directory = (
            self.root / ".codex/agents/runtime/issue-gates" / self.session_id / "invalid"
        )
        state_directory.mkdir(parents=True)
        (state_directory / "state.json").write_text("{}\n", encoding="utf-8")

        blocked = self.run_stop()
        self.assertEqual(blocked.returncode, 0, blocked.stderr)
        output = json.loads(blocked.stdout)
        self.assertEqual(output["decision"], "block")
        self.assertIn("unsupported gate state", output["reason"])

    def test_active_receipt_without_its_issue_claim_blocks_stop(self) -> None:
        self.begin()
        claim = next(
            (self.root / ".codex/agents/runtime/issue-gates/claims").glob("*/claim.json")
        )
        claim.unlink()
        claim.parent.rmdir()

        blocked = self.run_stop()
        self.assertEqual(blocked.returncode, 0, blocked.stderr)
        output = json.loads(blocked.stdout)
        self.assertEqual(output["decision"], "block")
        self.assertIn("does not own the issue claim", output["reason"])

    @unittest.skipIf(os.name == "nt", "symlink setup differs on Windows")
    def test_issue_symlink_cannot_redirect_gate_ownership(self) -> None:
        target = self.issue.with_name("target.md")
        self.issue.replace(target)
        self.issue.symlink_to(target)

        result = self.command("begin")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("issue is not a regular file", result.stderr)
        self.assertFalse((self.root / ".codex/agents/runtime/issue-gates").exists())

    def test_direct_small_change_without_receipt_is_a_stop_noop(self) -> None:
        (self.root / "tracked.txt").write_text("small change\n", encoding="utf-8")
        stop = self.run_stop()
        self.assertEqual(stop.returncode, 0, stop.stderr)
        self.assertEqual(stop.stdout, "")
        self.assertFalse((self.root / ".codex/agents/runtime/issue-gates").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
