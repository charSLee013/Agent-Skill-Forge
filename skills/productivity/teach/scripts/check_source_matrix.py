#!/usr/bin/env python3
"""Validate Teach v2 source matrix structure."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REQUIRED_FIELDS = [
    "claim_id",
    "claim",
    "layer",
    "source",
    "anchor",
    "evidence_summary",
    "boundary",
    "confidence",
    "used_in",
    "misread_risk",
    "review_status",
]

ALLOWED_LAYERS = {
    "paper_fact",
    "lineage_context",
    "course_reconstruction",
    "engineering_transfer",
    "unknown",
}


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        rows.append(cells)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--template-mode", action="store_true")
    args = parser.parse_args()

    if not args.matrix.is_file():
        fail(f"missing source matrix: {args.matrix}")
    text = args.matrix.read_text(encoding="utf-8")
    rows = parse_rows(text)
    if not rows:
        fail("no markdown table found")
    header = rows[0]
    missing = [field for field in REQUIRED_FIELDS if field not in header]
    if missing:
        fail(f"missing required fields: {', '.join(missing)}")

    layer_index = header.index("layer")
    for row in rows[1:]:
        if len(row) <= layer_index:
            continue
        layer = row[layer_index]
        if args.template_mode and layer in {"Replace", ""}:
            continue
        if layer not in ALLOWED_LAYERS:
            fail(f"invalid layer: {layer}")

    for layer in ALLOWED_LAYERS:
        if layer not in text:
            fail(f"allowed layer not documented: {layer}")
    print(f"[OK] source matrix valid: {args.matrix}")


if __name__ == "__main__":
    main()
