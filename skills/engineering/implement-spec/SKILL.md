---
name: implement-spec
description: Complete an explicitly selected local specification and its implementation issues as one dependency-ordered delivery, without requiring a commit, PR, TDD, or implementation subagents.
license: MIT
argument-hint: "Which feature directory or specification should be completed?"
disable-model-invocation: true
---

# Implement Spec

Deliver the whole feature the user selected, not merely its next issue. This
manual entry point orchestrates the existing `implement` discipline and local
issue contracts; it does not create a second tracker or acceptance system.

Adapted from Matt Pocock's `implement-spec` task-graph approach without its
mandatory TDD, implementer subagents, integration branch, or PR workflow.

## Establish the graph

Resolve one exact feature directory under `.codex/agents/work/` from the
user's path or already established context. Read its PRD or approved plan,
implementation issues, decision map when present, and local workspace rules.
If multiple features match, ask for the exact path. Do not manufacture a PRD
or issue merely because this skill is selected.

If the specification is clear but has no implementation issues, deliver its
behavior directly through `implement` and verify the whole specification.
An empty issue set is never evidence that the feature is complete. Resolve
material missing decisions only within the user's existing authorization;
otherwise report the exact decision that prevents delivery.

Treat `Blocked by` paths as edges relative to that feature. Check for missing,
ambiguous, cyclic, or out-of-feature dependencies before starting an affected
issue. Decisions unblock at `Wayfinder status: resolved`; implementations
unblock at `Completion: done`, never merely from triage status. An issue in
`needs-info` or `ready-for-human` is not automatically ready for unattended
work; resolve the material missing choice or respect the human boundary.
Respect completed issues, but check the feature's final acceptance rather than
assuming a recorded completion proves it. Keep unresolved or out-of-scope
blockers visible instead of assuming they are done.

## Deliver available work

Work through the ready issues in dependency order using `implement`. Preserve
each issue's behavior and original evidence oracle; choose tests based on risk
and relevant existing coverage, without TDD or test-first sequencing. Use
read-only, independent exploration in parallel only when the user and runtime
permit it; implementation ownership stays with the executing agent.

After each issue, check the requested behavior and mark `Completion: done` only
when every acceptance condition holds. A failure blocks its dependents but not
other independent, already authorized issues. Re-evaluate the ready frontier
after actual completion rather than adding planning files to simulate progress.

The delivery is complete only when every in-scope implementation issue is done
and the feature's original acceptance boundary is met. Report open issues and
their exact blockers otherwise. An integration branch, commit, push, PR,
deployment, or retro requires separate task authorization; none follows from
selecting this skill.
