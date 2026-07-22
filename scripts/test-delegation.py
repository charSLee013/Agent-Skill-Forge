#!/usr/bin/env python3
"""Focused contract tests for artifact-based delegation."""

from __future__ import annotations

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
DELEGATION = REPO_ROOT / "scripts" / "delegation.py"


def markdown(title: str, sections: tuple[str, ...], marker: str) -> str:
    lines = [f"# {title}", ""]
    for section in sections:
        lines.extend((f"## {section}", "", f"{marker}: {section}", ""))
    return "\n".join(lines)


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


class DelegationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name).resolve()
        self.temp_root = self.root / "tmp"
        self.workspace = self.root / "workspace"
        self.temp_root.mkdir()
        self.workspace.mkdir()
        self.session_id = str(uuid.uuid4())
        self.environment = os.environ.copy()
        self.environment["TMPDIR"] = str(self.temp_root)
        self.environment["PYTHONDONTWRITEBYTECODE"] = "1"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def command(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(DELEGATION), *arguments],
            cwd=self.workspace,
            env=self.environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def payload(self, result: subprocess.CompletedProcess[str]) -> dict[str, Any]:
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def begin(self, task_name: str = "inspect-auth") -> dict[str, Any]:
        return self.payload(
            self.command(
                "begin",
                "--session-id",
                self.session_id,
                "--task-name",
                task_name,
            )
        )

    def write_request(self, payload: dict[str, Any], marker: str = "request-marker") -> Path:
        request = Path(payload["request_path"])
        request.write_text(markdown("Delegation", REQUEST_SECTIONS, marker), encoding="utf-8")
        return request

    def write_result_part(self, payload: dict[str, Any], marker: str = "result-marker") -> Path:
        result_part = Path(payload["result_part_path"])
        result_part.write_text(markdown("Result", RESULT_SECTIONS, marker), encoding="utf-8")
        return result_part

    def publish_and_inspect(self, payload: dict[str, Any]) -> str:
        request = str(payload["request_path"])
        self.write_result_part(payload)
        self.payload(self.command("publish", "--request", request))
        inspected = self.payload(self.command("inspect", "--request", request))
        return str(inspected["result_digest"])

    def cleanup_arguments(self, payload: dict[str, Any], digest: str) -> list[str]:
        return [
            "cleanup",
            "--request",
            str(payload["request_path"]),
            "--result-digest",
            digest,
            "--file-line-claims-verified",
            "--command-claims-verified",
            "--conclusions-verified",
        ]

    def test_small_task_is_a_true_noop(self) -> None:
        result = self.payload(self.command("begin", "--small-task"))

        self.assertFalse(result["delegation_required"])
        self.assertEqual(result["status"], "small-task-no-op")
        self.assertFalse((self.temp_root / "codex-delegations").exists())

    def test_begin_allocates_unique_session_and_task_scoped_directories(self) -> None:
        first = self.begin()
        second = self.begin()
        other_session = str(uuid.uuid4())
        third = self.payload(
            self.command(
                "begin",
                "--session-id",
                other_session,
                "--task-name",
                "inspect-auth",
            )
        )

        self.assertNotEqual(first["directory"], second["directory"])
        self.assertIn(f"/{self.session_id}/inspect-auth-", first["directory"])
        self.assertIn(f"/{other_session}/inspect-auth-", third["directory"])
        self.assertEqual(Path(first["request_path"]).name, "REQUEST.md")
        self.assertEqual(Path(first["result_path"]).name, "RESULT.md")

    def test_prepare_requires_complete_request_and_emits_minimal_spawn_contract(self) -> None:
        payload = self.begin()
        request = Path(payload["request_path"])
        incomplete = self.command("prepare", "--request", str(request), "--read-only")
        self.assertNotEqual(incomplete.returncode, 0)
        self.assertIn("section is empty", incomplete.stderr)

        self.write_request(payload, marker="secret objective detail")
        prepared = self.payload(
            self.command("prepare", "--request", str(request), "--read-only")
        )

        self.assertEqual(prepared["fork_turns"], "none")
        self.assertTrue(prepared["parent_contract"]["wait_agent_is_status_only"])
        self.assertFalse(prepared["parent_contract"]["chat_is_evidence"])
        self.assertIn(str(request), prepared["message"])
        self.assertIn(str(payload["result_part_path"]), prepared["message"])
        self.assertIn(str(payload["result_path"]), prepared["message"])
        self.assertIn("read-only", prepared["message"])
        self.assertNotIn("secret objective detail", prepared["message"])

        request.write_text(
            "Preamble that is not part of the fixed contract.\n\n"
            + markdown("Delegation", REQUEST_SECTIONS, "request-marker"),
            encoding="utf-8",
        )
        prefixed = self.command("prepare", "--request", str(request), "--read-only")
        self.assertNotEqual(prefixed.returncode, 0)
        self.assertIn("must begin", prefixed.stderr)

    def test_prepare_rejects_write_ownership_outside_workspace(self) -> None:
        payload = self.begin()
        request = self.write_request(payload)

        outside = self.command(
            "prepare",
            "--request",
            str(request),
            "--workspace",
            str(self.workspace),
            "--write-path",
            "../outside.py",
        )
        self.assertNotEqual(outside.returncode, 0)
        self.assertIn("outside the workspace", outside.stderr)

        prepared = self.payload(
            self.command(
                "prepare",
                "--request",
                str(request),
                "--workspace",
                str(self.workspace),
                "--write-path",
                "owned.py",
            )
        )
        self.assertIn(str(self.workspace / "owned.py"), prepared["message"])

    def test_prepare_rejects_a_dangling_owned_path_symlink(self) -> None:
        payload = self.begin()
        request = self.write_request(payload)
        dangling = self.workspace / "owned.py"
        dangling.symlink_to(self.workspace / "missing.py")

        rejected = self.command(
            "prepare",
            "--request",
            str(request),
            "--workspace",
            str(self.workspace),
            "--write-path",
            str(dangling),
        )

        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("real file", rejected.stderr)

    def test_publish_renames_valid_partial_result_to_predetermined_result(self) -> None:
        payload = self.begin()
        request = self.write_request(payload)
        part = self.write_result_part(payload)
        source_inode = part.stat().st_ino

        published = self.payload(self.command("publish", "--request", str(request)))
        result = Path(payload["result_path"])

        self.assertFalse(part.exists())
        self.assertTrue(result.is_file())
        self.assertEqual(result.stat().st_ino, source_inode)
        self.assertEqual(len(published["result_digest"]), 64)

    def test_missing_or_arbitrary_result_is_incomplete_and_requires_reissue(self) -> None:
        payload = self.begin()
        request = self.write_request(payload)
        arbitrary = Path(payload["directory"]) / "CHAT-SUMMARY.md"
        arbitrary.write_text(markdown("Result", RESULT_SECTIONS, "chat"), encoding="utf-8")

        inspected = self.command("inspect", "--request", str(request))
        self.assertEqual(inspected.returncode, 3)
        inspected_payload = json.loads(inspected.stdout)
        self.assertEqual(inspected_payload["status"], "incomplete")
        self.assertTrue(inspected_payload["reissue_required"])
        self.assertIn("RESULT.md is missing", inspected_payload["reason"])

        resumed = self.command("resume", "--request", str(request))
        self.assertEqual(resumed.returncode, 3, resumed.stderr)
        resume_payload = json.loads(resumed.stdout)
        self.assertEqual(resume_payload["status"], "incomplete")
        self.assertTrue(resume_payload["reissue_required"])
        self.assertIn("explicitly start a new unique delegation", resume_payload["next_action"])

    def test_malformed_partial_result_is_not_published(self) -> None:
        payload = self.begin()
        request = self.write_request(payload)
        part = Path(payload["result_part_path"])
        part.write_text("# Result\n\n## Outcome\n\nOnly one section.\n", encoding="utf-8")

        published = self.command("publish", "--request", str(request))

        self.assertNotEqual(published.returncode, 0)
        self.assertTrue(part.exists())
        self.assertFalse(Path(payload["result_path"]).exists())

    def test_cleanup_requires_matching_validation_and_all_parent_attestations(self) -> None:
        payload = self.begin()
        request = self.write_request(payload)
        digest = self.publish_and_inspect(payload)
        directory = Path(payload["directory"])

        unverified = self.command(
            "cleanup",
            "--request",
            str(request),
            "--result-digest",
            digest,
            "--no-durable-facts",
        )
        self.assertNotEqual(unverified.returncode, 0)
        self.assertTrue(directory.exists())

        wrong_digest = self.command(
            *self.cleanup_arguments(payload, "0" * 64),
            "--no-durable-facts",
        )
        self.assertNotEqual(wrong_digest.returncode, 0)
        self.assertTrue(directory.exists())

        cleaned = self.payload(
            self.command(
                *self.cleanup_arguments(payload, digest),
                "--no-durable-facts",
            )
        )
        self.assertEqual(cleaned["status"], "consumed-and-cleaned")
        self.assertFalse(directory.exists())
        self.assertFalse((self.temp_root / "codex-delegations").exists())

    def test_cleanup_rejects_residual_partial_or_extra_material(self) -> None:
        payload = self.begin()
        self.write_request(payload)
        digest = self.publish_and_inspect(payload)
        part = Path(payload["result_part_path"])
        part.write_text("unfinished\n", encoding="utf-8")

        rejected = self.command(
            *self.cleanup_arguments(payload, digest),
            "--no-durable-facts",
        )
        self.assertNotEqual(rejected.returncode, 0)
        self.assertTrue(Path(payload["directory"]).exists())

        part.unlink()
        self.payload(
            self.command(
                *self.cleanup_arguments(payload, digest),
                "--no-durable-facts",
            )
        )

    def test_cleanup_accepts_only_existing_checkpoint_or_issue_fact_owner(self) -> None:
        payload = self.begin()
        self.write_request(payload)
        digest = self.publish_and_inspect(payload)
        unrelated = self.workspace / "NOTES.md"
        unrelated.write_text("not a fact owner\n", encoding="utf-8")

        rejected = self.command(
            *self.cleanup_arguments(payload, digest),
            "--workspace",
            str(self.workspace),
            "--consumed-to",
            str(unrelated),
        )
        self.assertNotEqual(rejected.returncode, 0)
        self.assertTrue(Path(payload["directory"]).exists())

        issue = self.workspace / ".codex/agents/work/example/issues/01-build.md"
        issue.parent.mkdir(parents=True)
        issue.write_text("Completion: open\n", encoding="utf-8")
        cleaned = self.payload(
            self.command(
                *self.cleanup_arguments(payload, digest),
                "--workspace",
                str(self.workspace),
                "--consumed-to",
                str(issue),
            )
        )
        self.assertEqual(cleaned["facts_consumed_to"], [str(issue.resolve())])

    def test_cleanup_rejects_a_checkpoint_from_another_session(self) -> None:
        payload = self.begin()
        self.write_request(payload)
        digest = self.publish_and_inspect(payload)
        checkpoint = self.workspace / ".codex/agents/runtime/checkpoints"
        checkpoint.mkdir(parents=True)
        foreign_checkpoint = checkpoint / f"{uuid.uuid4()}.md"
        foreign_checkpoint.write_text("# Checkpoint\n", encoding="utf-8")

        rejected = self.command(
            *self.cleanup_arguments(payload, digest),
            "--workspace",
            str(self.workspace),
            "--consumed-to",
            str(foreign_checkpoint),
        )

        self.assertNotEqual(rejected.returncode, 0)
        self.assertTrue(Path(payload["directory"]).exists())

    def test_checkpoint_note_and_resume_preserve_only_active_delegation_facts(self) -> None:
        payload = self.begin()
        request = self.write_request(payload)
        note = self.payload(
            self.command(
                "checkpoint",
                "--request",
                str(request),
                "--agent-id",
                "reviewer-1",
                "--next-action",
                "Wait, then inspect the predetermined result.",
            )
        )["checkpoint_markdown"]

        self.assertIn("reviewer-1", note)
        self.assertIn(payload["directory"], note)
        self.assertIn("Wait, then inspect", note)

        digest = self.publish_and_inspect(payload)
        resumed = self.payload(self.command("resume", "--request", str(request)))
        self.assertFalse(resumed["reissue_required"])
        self.assertEqual(resumed["result_digest"], digest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
