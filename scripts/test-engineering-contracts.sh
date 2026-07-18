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

wayfinder="skills/engineering/wayfinder/SKILL.md"
to_prd="skills/engineering/to-prd/SKILL.md"
to_issues="skills/engineering/to-issues/SKILL.md"
implement="skills/engineering/implement/SKILL.md"
tracker="skills/engineering/setup-agent-skills/issue-tracker-local.md"
setup="skills/engineering/setup-agent-skills/SKILL.md"

# These skills are prompt contracts rather than an executable workflow engine.
# Pin the user-visible invariants without pretending to execute a model.

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
assert_contains 'add or change its field to `Completion: done`' "$implement"

assert_contains 'Legacy migration is automatic after the user approves the setup draft; do not ask a separate migration question.' "$setup"
assert_contains 'Include an automatic legacy migration dry-run summary in the setup draft.' "$setup"
assert_contains 'Before changing a feature, copy its entire directory to a unique system temporary directory as a rollback snapshot.' "$setup"
assert_contains 'Scan every Markdown file under the feature directory and rewrite only exact local path references.' "$setup"
assert_contains 'If any move, rewrite, or verification fails, restore the feature from its snapshot and report the failure.' "$setup"
assert_not_contains 'If the user confirmed legacy migration' "$setup"

echo "engineering contract smoke checks passed"
