#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

assert_contains() {
  local pattern="$1"
  local file="$2"
  rg -Fq "$pattern" "$file" || fail "expected '$pattern' in $file"
}

assert_not_contains() {
  local pattern="$1"
  local file="$2"
  if rg -Fq "$pattern" "$file"; then
    fail "did not expect '$pattern' in $file"
  fi
}

assert_exact_file() {
  local expected="$1"
  local file="$2"
  printf '%s\n' "$expected" | cmp -s - "$file" || fail "unexpected contents in $file"
}

wayfinder="skills/engineering/wayfinder/SKILL.md"
to_prd="skills/engineering/to-prd/SKILL.md"
to_issues="skills/engineering/to-issues/SKILL.md"
implement="skills/engineering/implement/SKILL.md"
tracker="skills/engineering/setup-agent-skills/issue-tracker-local.md"
setup="skills/engineering/setup-agent-skills/SKILL.md"
agents="AGENTS.md"
readme="README.md"
engineering_readme="skills/engineering/README.md"
manifest=".claude-plugin/plugin.json"

# These skills are prompt contracts rather than an executable workflow engine.
# Pin the user-visible invariants without pretending to execute a model.

[[ -s AGENTS.md ]] || fail "expected a non-empty root AGENTS.md"
assert_exact_file '@AGENTS.md' CLAUDE.md
if find . \( -path './.git' -o -path './.codex' \) -prune -o \( -name AGENTS.md -o -name AGENTS.override.md -o -name CLAUDE.md \) ! -path './AGENTS.md' ! -path './CLAUDE.md' -print | rg -q .; then
  fail "found a nested Agent instruction file"
fi
if git check-ignore --no-index -q AGENTS.md || git check-ignore --no-index -q CLAUDE.md; then
  fail "root Agent instruction files must not be ignored"
fi
assert_contains 'This file is the repository' AGENTS.md
assert_contains 'Do not create parallel or nested instruction files.' AGENTS.md
assert_contains 'Validation' AGENTS.md
assert_not_contains 'CLAUDE.md' AGENTS.md
[[ "$(rg -c '^## Agent skills$' "$agents")" -eq 1 ]] || fail "expected exactly one managed Agent skills block"
git check-ignore --no-index -q .codex/agents/work/private.md || fail ".codex workspace must stay private"

for policy_file in "$agents" "$setup"; do
  assert_contains 'Checkpoints own session continuity facts. Issues own scope, acceptance, issue-start baselines, and finalization proofs.' "$policy_file"
  assert_contains 'Keep session identifiers, task paths, findings, mistakes, issue facts, and delegation conclusions out of this static policy.' "$policy_file"
  assert_contains 'Create and maintain a checkpoint at the `SessionStart`-provided path only for non-trivial work with durable confirmed facts.' "$policy_file"
  assert_contains 'The file must start with `# Checkpoint`, followed exactly once each by these `##` headings in order: `Task`, `Progress`, `Decisions`, `Mistakes and corrections`, `Binding rules`, `Verification`, and `Next action`.' "$policy_file"
  assert_contains 'Update it only when confirmed facts, scope, decisions, corrections, verification evidence, or the next action changes.' "$policy_file"
  assert_contains 'Ordinary reads, repeated tests, formatting, searches, and unchanged tool calls do not update it.' "$policy_file"
  assert_contains 'A direct small edit with no active issue or non-trivial session state uses an ordinary final-diff review.' "$policy_file"
  assert_contains 'Use subagents only for bounded exploration, independent review, or acceptance verification. Do not delegate final scope, architecture, writes, or proof ownership.' "$policy_file"
  assert_contains 'Always set `fork_turns` explicitly; use `none` for independent exploration and review.' "$policy_file"
  assert_contains 'the fixed `REQUEST.md` and `RESULT.md` section contract in a unique assigned temporary directory' "$policy_file"
  assert_contains 'Write `RESULT.md.part` first and atomically rename it to `RESULT.md`; treat `wait_agent` as status only.' "$policy_file"
  assert_contains 'The parent must verify the result, consume its evidence, and delete the complete delegation directory.' "$policy_file"
  assert_contains 'The main agent owns the final worktree diff, scope decision, acceptance evidence, and user-facing result.' "$policy_file"
  assert_contains 'Do not automatically invoke the user-level `handoff` skill or preserve unapproved legacy or fallback behavior.' "$policy_file"
done

python3 - "$manifest" <<'PY'
import json
import sys
from pathlib import Path

manifest_path = Path(sys.argv[1])
data = json.loads(manifest_path.read_text(encoding="utf-8"))
if set(data) != {"name", "skills"}:
    raise SystemExit(f"unsupported plugin manifest fields: {sorted(set(data) - {'name', 'skills'})}")
if "hooks" in data:
    raise SystemExit("plugin manifest must rely on root hooks/hooks.json discovery")
if not Path("hooks/hooks.json").is_file():
    raise SystemExit("missing root hook discovery file")
declared = sorted(data["skills"])
actual = sorted(
    f"./{path.parent.as_posix()}"
    for path in Path("skills").rglob("SKILL.md")
    if "node_modules" not in path.parts
)
if declared != actual:
    raise SystemExit("plugin skill entries do not match the shipped SKILL.md directories")
PY

# A new feature has no MAP by definition. Zero matches must reach the entry
# gate, while a missing explicit MAP or multiple matches must stop.
assert_contains 'If an explicit `MAP.md` path does not exist, stop and report that path.' "$wayfinder"
assert_contains 'If no explicit `MAP.md` path was supplied and there are zero matches, evaluate the new-map entry gate below.' "$wayfinder"
assert_contains 'If there are multiple matches, stop and ask the user to supply the exact `MAP.md` path.' "$wayfinder"

for skill in "$to_prd" "$to_issues"; do
  assert_contains 'If an explicit `MAP.md` path was supplied but does not exist, stop and report the missing path.' "$skill"
  assert_contains 'If no matching map exists and no explicit `MAP.md` path was supplied, continue when the source material is clear enough for this skill; a map is optional.' "$skill"
  assert_contains 'If multiple maps match, stop and ask for the exact `MAP.md` path.' "$skill"
  assert_not_contains 'If there are zero or multiple matches, stop and ask rather than guessing.' "$skill"
done

assert_contains 'Every `Blocked by` path is relative to `.codex/agents/work/<feature-slug>/`, regardless of which issue contains it.' "$tracker"
assert_contains 'A target under `decisions/` unblocks only when it has `Wayfinder status: resolved`.' "$tracker"
assert_contains 'A modern target under `issues/` unblocks only when it has `Completion: done`.' "$tracker"
assert_contains 'The target type, not the source type, selects the oracle for decision-to-decision, implementation-to-implementation, and cross-type dependencies.' "$tracker"
assert_contains 'A legacy target under `issues/` that carries both top-level Wayfinder fields remains a decision target and uses `Wayfinder status: resolved` until migration succeeds.' "$tracker"
assert_contains 'A legacy implementation issue without `Completion` is treated as `Completion: open`.' "$tracker"
assert_not_contains 'affects a dependent decision' "$tracker"
assert_contains 'Completion: open' "$to_issues"
assert_contains '`Finalize Issue` is the only approved transition from `Completion: open` to `Completion: done`.' "$implement"
assert_contains 'Never make that edit directly.' "$implement"
assert_contains 'Map every remaining file and hunk to approved scope, an acceptance criterion, or indispensable supporting implementation.' "$implement"
assert_contains 'With no active formal issue receipt, a direct small change uses an ordinary final diff check' "$implement"
assert_contains '`Finalize Issue` is the only approved operation that changes `Completion: open` to `Completion: done`.' "$tracker"
assert_contains '.codex/agents/runtime/issue-gates/<session-id>/' "$tracker"
assert_contains 'Every emitted unit must appear exactly once' "$tracker"
assert_contains 'The shared `Stop` hook consults only the current session' "$tracker"
assert_contains 'the semantic Git index entries' "$tracker"
assert_contains 'the ignored path set must return exactly to its baseline' "$tracker"
assert_contains 'claims an atomic issue-key receipt' "$tracker"
assert_contains 'Confirm that the Git index is unchanged from issue start' "$implement"
assert_contains 'its temporary baseline receipt and claim are removed' "$implement"
assert_contains '.codex/agents/runtime/support/scripts/finalize-issue.py begin' "$implement"
assert_contains '.codex/agents/runtime/support/scripts/finalize-issue.py begin' "$tracker"
assert_not_contains 'python3 scripts/finalize-issue.py begin' "$implement"
assert_not_contains 'python3 scripts/finalize-issue.py begin' "$tracker"

assert_contains 'Legacy migration is automatic after the user approves the setup draft; do not ask a separate migration question.' "$setup"
assert_contains 'Include an automatic legacy migration dry-run summary in the setup draft.' "$setup"
assert_contains 'Before changing a feature, copy its entire directory to a unique system temporary directory as a rollback snapshot.' "$setup"
assert_contains 'Scan every Markdown file under the feature directory and rewrite only exact local path references.' "$setup"
assert_contains 'If any move, rewrite, or verification fails, restore the feature from its snapshot and report the failure.' "$setup"
assert_not_contains 'If the user confirmed legacy migration' "$setup"
assert_contains 'Replace root `CLAUDE.md` completely so its only line is `@AGENTS.md`.' "$setup"
assert_contains 'Do not read their content into root `AGENTS.md`, preserve it elsewhere, or offer a compatibility path.' "$setup"
assert_contains 'Remove every nested `AGENTS.md`, `AGENTS.override.md`, and `CLAUDE.md` in the repository.' "$setup"
assert_contains 'Re-running setup with the same choices must produce no changes.' "$setup"
assert_contains '.codex/agents/runtime/support/' "$setup"
assert_contains '$HOME/.agents/agent-skill-forge/' "$setup"
assert_contains 'If the installed support tree already has the same file set and bytes, leave it unchanged.' "$setup"
assert_contains 'These are the only supported sources; if the selected source is incomplete, stop and report it.' "$setup"
assert_contains 'Do not copy tests, register hooks through an invented config file, add a `hooks` field to `.claude-plugin/plugin.json`' "$setup"
assert_not_contains 'Preserve any Claude-specific content' "$setup"
assert_not_contains 'Pick the file to edit' "$setup"
assert_not_contains 'runtime-specific' "$engineering_readme"
assert_contains '~/.agents/agent-skill-forge/' "$engineering_readme"
assert_contains '仓库根 `hooks/hooks.json` 是自动发现入口' "$readme"
assert_contains '`.claude-plugin/plugin.json` 仍只声明 skill' "$readme"
assert_contains '.codex/agents/runtime/support/' "$readme"
assert_contains '在消费仓库中只向 `.git/info/exclude` 添加 `.codex/`' "$readme"
assert_not_contains 'AGENT=codex' "$readme"
assert_not_contains 'bash scripts/install.sh teach' "$readme"

echo "engineering contract smoke checks passed"
