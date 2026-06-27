#!/usr/bin/env python3
"""Validate a Teach v2 workspace or the Teach skill package."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REQUIRED_REFERENCES = [
    "task-modes.md",
    "evidence-layer.md",
    "deep-paper-course.md",
    "repo-course.md",
    "research-route.md",
    "misconception-audit.md",
    "student-page-boundary.md",
    "html-quality-proof.md",
    "long-course-proof.md",
]

REQUIRED_TEMPLATES = [
    "source-matrix.md",
    "manifest.json",
    "misconception-audit.md",
    "course-map.html",
    "lesson.html",
    "reference.html",
]

REQUIRED_SCRIPTS = [
    "validate_teaching_workspace.py",
    "check_source_matrix.py",
    "check_manifest.py",
    "verify_html_artifacts.py",
]

REQUIRED_SKILL_PHRASES = [
    "Teach v2",
    "deep-paper",
    "repo-course",
    "research-route",
    "long-course",
    "artifacts/source-matrix.md",
    "misconception audit",
    "HTML Proof",
    "Long-Course Proof",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing file: {path}")


def check_skill_package(root: Path) -> None:
    skill = root / "SKILL.md"
    require_file(skill)
    text = skill.read_text(encoding="utf-8")
    for phrase in REQUIRED_SKILL_PHRASES:
        if phrase not in text:
            fail(f"SKILL.md missing required phrase: {phrase}")
    for name in REQUIRED_REFERENCES:
        require_file(root / "references" / name)
    for name in REQUIRED_TEMPLATES:
        require_file(root / "templates" / name)
    for name in REQUIRED_SCRIPTS:
        require_file(root / "scripts" / name)
    ok(f"Teach v2 skill package is complete: {root}")


def check_workspace(root: Path) -> None:
    mission = root / "MISSION.md"
    resources = root / "RESOURCES.md"
    if not mission.exists():
        print(f"[WARN] missing MISSION.md: {mission}")
    if not resources.exists():
        print(f"[WARN] missing RESOURCES.md: {resources}")
    manifest = root / "manifest.json"
    source_matrix = root / "artifacts" / "source-matrix.md"
    if manifest.exists():
        ok(f"manifest exists: {manifest}")
    if source_matrix.exists():
        ok(f"source matrix exists: {source_matrix}")
    ok(f"workspace checked: {root}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-root", type=Path, default=None)
    parser.add_argument("--workspace-root", type=Path, default=None)
    parser.add_argument("--check-skill-package", action="store_true")
    args = parser.parse_args()

    if args.check_skill_package:
        if args.skill_root is None:
            fail("--check-skill-package requires --skill-root")
        check_skill_package(args.skill_root)
        return

    root = args.workspace_root or Path.cwd()
    check_workspace(root)


if __name__ == "__main__":
    main()
