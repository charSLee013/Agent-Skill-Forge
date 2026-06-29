#!/usr/bin/env python3
"""Run lightweight Teach v2 checks over HTML artifacts."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys


FORBIDDEN_MAIN_TEXT = [
    ".codex/long-horizon",
    "source-matrix.md",
    "subagent report",
    "phase review",
    "Gate 0",
    "Gate 1",
    "Gate 2",
    "Gate 3",
    "Gate 4",
]

STRICT_PROFILE_TERMS = [
    "evidence-intensive",
    "report-grade",
    "expert-audited",
]

MECHANISM_TERMS = [
    "mechanism",
    "state",
    "variable",
    "step",
    "process",
    "transition",
    "procedure",
    "equation",
    "formula",
    "algorithm",
]

EXPLANATORY_PROOF_TERMS = [
    "what this teaches",
    "learner action",
    "misconception",
    "fallback",
]


class HTMLFacts(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1_count = 0
        self.links: list[str] = []
        self.has_viewport = False
        self.tags: list[str] = []
        self.text: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        if tag == "h1":
            self.h1_count += 1
        attrs_dict = dict(attrs)
        if tag == "a" and attrs_dict.get("href"):
            self.links.append(attrs_dict["href"] or "")
        if tag == "meta" and attrs_dict.get("name") == "viewport":
            self.has_viewport = True

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.text.append(data.strip())


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def check_html(path: Path, template_mode: bool) -> None:
    text = path.read_text(encoding="utf-8")
    parser = HTMLFacts()
    parser.feed(text)
    if parser.h1_count != 1:
        fail(f"{path}: expected exactly one h1, found {parser.h1_count}")
    if not parser.has_viewport:
        fail(f"{path}: missing viewport meta")
    body_text = " ".join(parser.text).lower()
    required_terms = ["next action"]
    if "reference" not in path.name:
        required_terms.extend(["remember", "main line"])
    for term in required_terms:
        if term not in body_text:
            fail(f"{path}: missing required learner cue: {term}")
    for forbidden in FORBIDDEN_MAIN_TEXT:
        if forbidden.lower() in body_text:
            fail(f"{path}: forbidden backstage text found: {forbidden}")
    strict_profile = any(term in body_text for term in STRICT_PROFILE_TERMS)
    mechanism_page = strict_profile and any(term in body_text for term in MECHANISM_TERMS)
    explicit_explanatory_proof = "explanatory proof" in body_text
    if not template_mode and (mechanism_page or explicit_explanatory_proof):
        missing = [term for term in EXPLANATORY_PROOF_TERMS if term not in body_text]
        if missing:
            fail(f"{path}: missing explanatory proof terms: {', '.join(missing)}")
    if not template_mode:
        for href in parser.links:
            if re.match(r"^[a-z]+://", href) or href.startswith("#") or href.startswith("mailto:"):
                continue
            target = (path.parent / href.split("#", 1)[0]).resolve()
            if href and not target.exists():
                fail(f"{path}: broken local link: {href}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--template-mode", action="store_true")
    args = parser.parse_args()

    if not args.root.exists():
        fail(f"root does not exist: {args.root}")
    html_files = sorted(args.root.rglob("*.html")) if args.root.is_dir() else [args.root]
    if not html_files:
        fail(f"no html files found under {args.root}")
    for path in html_files:
        check_html(path, args.template_mode)
    print(f"[OK] html artifacts valid: {len(html_files)} file(s)")


if __name__ == "__main__":
    main()
