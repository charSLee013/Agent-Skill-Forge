#!/usr/bin/env python3
"""Validate Teach v2 manifest structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REQUIRED_TOP_LEVEL = ["schema", "version", "course", "artifacts", "phase_gates", "final_proof"]
REQUIRED_ARTIFACT_FIELDS = ["path", "type", "audience", "required", "status", "last_validated", "proof"]


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--base", type=Path, default=Path("."))
    parser.add_argument("--template-mode", action="store_true")
    args = parser.parse_args()

    if not args.manifest.is_file():
        fail(f"missing manifest: {args.manifest}")
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid json: {exc}")

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            fail(f"missing top-level key: {key}")
    if data.get("schema") != "teach-v2-manifest":
        fail("schema must be teach-v2-manifest")
    if not isinstance(data.get("artifacts"), list):
        fail("artifacts must be a list")
    for artifact in data["artifacts"]:
        for field in REQUIRED_ARTIFACT_FIELDS:
            if field not in artifact:
                fail(f"artifact missing field {field}: {artifact}")
        path = artifact["path"]
        if artifact.get("required") and not args.template_mode:
            if not (args.base / path).exists():
                fail(f"required artifact missing on disk: {path}")
    print(f"[OK] manifest valid: {args.manifest}")


if __name__ == "__main__":
    main()
