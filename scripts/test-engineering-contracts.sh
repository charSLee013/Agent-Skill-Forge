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
real_path="skills/engineering/real-path-verification/SKILL.md"
architecture="skills/engineering/improve-codebase-architecture/SKILL.md"
tracker="skills/engineering/setup-agent-skills/issue-tracker-local.md"
setup="skills/engineering/setup-agent-skills/SKILL.md"

# These skills are prompt contracts rather than an executable workflow engine.
# Pin the user-visible invariants without pretending to execute a model.

[[ -s AGENTS.md ]] || fail "expected a non-empty root AGENTS.md"
assert_exact_file '@AGENTS.md' CLAUDE.md
if find . -path './.git' -prune -o -mindepth 2 \( -name AGENTS.md -o -name AGENTS.override.md -o -name CLAUDE.md \) -print | rg -q .; then
  fail "found a nested Agent instruction file"
fi
if git check-ignore --no-index -q AGENTS.md || git check-ignore --no-index -q CLAUDE.md; then
  fail "root Agent instruction files must not be ignored"
fi
assert_contains 'This file is the repository' AGENTS.md
assert_contains 'Do not create parallel or nested instruction files.' AGENTS.md
assert_contains 'Validation' AGENTS.md
assert_not_contains 'CLAUDE.md' AGENTS.md

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
assert_contains '## Capabilities and User Stories' "$to_prd"
assert_contains '## Acceptance Criteria' "$to_prd"
assert_contains 'When material acceptance evidence is unresolved, ask one direct verification question at a time' "$to_prd"
assert_contains '`static`' "$to_prd"
assert_contains '`real-path`' "$to_prd"
assert_contains '`target`' "$to_prd"
assert_contains 'falsifiable target: metric or definition, comparison, threshold or named baseline, unit, measurement source, and observation window.' "$to_prd"
assert_contains 'copy its behavior and inline `Evidence` facts into the issue' "$to_issues"
assert_contains '`target` > `real-path` > `static`' "$to_issues"
assert_contains 'Otherwise split the slice before publishing.' "$to_issues"
assert_contains 'Do not choose, weaken, or substitute evidence during issue slicing.' "$to_issues"
assert_contains 'Execute acceptance evidence exactly as approved.' "$implement"
assert_contains 'Do not weaken, replace, or defer evidence during implementation.' "$implement"
assert_contains 'A `target` criterion is complete only when the observed value satisfies its recorded target' "$implement"
assert_contains 'require a falsifiable recorded metric or definition, comparison, threshold or named baseline, unit, measurement source, and observation window' "$implement"
assert_contains 'Run only when a parent acceptance criterion has `real-path` evidence' "$real_path"
assert_contains 'Return a conclusion, not a verification transcript.' "$real_path"
assert_contains 'Do not create a run directory, stored bundle, raw response capture, replay copy, generated summary, verification file, or artifact path merely to document verification.' "$real_path"
assert_contains 'arrange cleanup before invocation' "$real_path"
assert_contains 'Remove it on every reachable success, failure, timeout, interruption, or observation-read path' "$real_path"
assert_contains '`Conclusion`: passed, failed, or unverified.' "$real_path"
assert_contains '`Oracle`: expected value compared with observed value.' "$real_path"
assert_contains 'A production runtime observation, or an equivalent path with relevant parity established, can satisfy a real-path criterion.' "$real_path"
assert_contains 'Finalization conclusion is the main agent' "$implement"
assert_contains 'required real-path evidence is missing' "$implement"
assert_contains 'selected real-path evidence.' "$to_issues"
assert_not_contains 'run_dir' "$real_path"
assert_not_contains 'evidence bundle' "$real_path"
assert_not_contains 'evidence paths' "$real_path"
assert_not_contains 'E0' "$real_path"
assert_not_contains 'E1' "$real_path"
assert_not_contains 'E2' "$real_path"
assert_not_contains 'E3' "$real_path"
assert_not_contains 'proof' "$real_path"
assert_not_contains 'proof' "$implement"
assert_not_contains 'real-path proof' "$to_issues"
assert_not_contains 'If the parent plan produces three or more slices' "$to_issues"
assert_not_contains 'If a parent work item has three or more slices' "$implement"
assert_not_contains 'final integration of a work item with three or more slices' "$real_path"
assert_contains 'Choose the active area before exploring:' "$architecture"
assert_contains 'recent non-merge commits and their changed paths' "$architecture"
assert_contains 'Do not use uncommitted worktree changes to infer hotness.' "$architecture"
assert_contains 'Review the agent-owned baseline-relative delta on two independent axes:' "$implement"
assert_contains '**Contract**:' "$implement"
assert_contains '**Repository fit**:' "$implement"
assert_contains 'A temporary bridge in an approved wide mechanical migration is indispensable support only when its `## Transition` names the Contract issue that removes it and its final removal oracle; the Contract issue must remove it.' "$implement"
assert_contains 'After both axes are clean, rerun the final required acceptance.' "$implement"
assert_contains 'A wide mechanical migration is an exception to vertical slicing.' "$to_issues"
assert_contains '**Expand**:' "$to_issues"
assert_contains '**Migrate**:' "$to_issues"
assert_contains '**Contract**:' "$to_issues"
assert_contains 'name the local relative path of the Contract-phase issue that will remove it' "$to_issues"
assert_contains 'Contract issue: <relative path to the Contract-phase issue>' "$to_issues"
assert_contains 'Set `Phase` to exactly one phase.' "$to_issues"
assert_contains 'The Contract issue must list its own local relative path and remove every temporary bridge.' "$to_issues"

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
assert_not_contains 'Preserve any Claude-specific content' "$setup"
assert_not_contains 'Pick the file to edit' "$setup"
assert_not_contains 'runtime-specific' skills/engineering/README.md
assert_not_contains 'AGENT=codex' README.md
assert_not_contains 'bash scripts/install.sh teach' README.md

echo "engineering contract smoke checks passed"
