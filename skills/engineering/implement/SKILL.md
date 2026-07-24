---
name: implement
description: "Implement a piece of work based on a PRD or set of issues."
disable-model-invocation: true
---

Implement the work described by the user in the PRD or issues.

Treat the user-approved PRD, issue, or task contract as the source of truth. Do not add adjacent behavior, refactors, tests, validation, documentation, or commits that are not required by it.

## Delivery integrity

Treat agent process text in persistent files as a product-integrity failure, not a style issue. Plans, tool output, errors, and execution explanations are model-visible context, not deliverable content. This workflow is a soft quality gate: careful prompts and diff review reduce contamination risk, but they do not prove that process text never reached the worktree. Only actual tool boundaries and a final review before delivery improve that assurance.

The gate is: write, main-agent baseline-aware diff review, then an independent read-only review only when one actually ran. A clean result proceeds to final acceptance and delivery. Contamination returns to the main agent for cleanup and a targeted recheck. Never substitute a missing agent, empty wait, or unverified chat summary for independent review.

## Start gate

Before writing, read the exact issue or PRD, applicable ADRs, and existing mechanisms in the affected area. Establish the approved scope, non-goals, acceptance criteria, and whether real-path proof belongs to this issue, a named final-integration issue, or is not applicable. Stop if any of these material facts is unresolved.

Capture the issue-start worktree as working evidence: `git status --short`, working-tree and staged diffs, and non-ignored untracked paths. Treat every pre-existing change as user-owned. Preserve it, do not map it to the current task, and do not delete or reformat it. Keep this baseline in the current task evidence only; do not create a receipt, proof file, or new state record.

For non-trivial work, an available explorer subagent may perform a bounded read-only preflight. Set `fork_turns="none"`, give it the exact task and relevant paths, and ask only for scope, non-goals, applicable ADRs, pre-existing changes, acceptance entrypoints, and `file:line` evidence. It must not edit, clean up, or create artifacts. The main agent verifies the result and retains all scope, write, acceptance, and completion ownership. A missing agent, empty wait, or status notification is not an audit result.

When an implementation issue has `Blocked by`, resolve each path from that issue's feature directory. A `decisions/` target requires `Wayfinder status: resolved`. An `issues/` target carrying both top-level Wayfinder fields is a legacy decision and uses the same oracle; every other `issues/` target requires `Completion: done`, with a missing field treated as `Completion: open`. Stop before implementation if any target is missing, ambiguous, outside the feature, or still blocked. Triage `Status` is not a completion oracle.

## Implementation

Keep temporary exploration, diagnostics, generated output, and scratch work in the system temporary directory by default. A repository-local temporary artifact needs a current acceptance purpose and must be removed before delivery. Do not write plans, to-dos, tool errors, protocol failures, execution status, debug explanations, or other process text into source, configuration, tests, comments, scripts, logs, or documentation.

Run the existing checks relevant to the changed behavior. Do not create a test file for documentation, comments, copy, or non-behavioral metadata. Run the full suite only when repository policy, the task, or the breadth of the change requires it.

If the acceptance criteria require a real runtime path or production-equivalent proof, invoke /real-path-verification as the verification phase. If a parent work item has three or more slices, recommend one real-path run at final integration; do not run it once per slice unless the issue explicitly requires that.

## Delivery squash

Before declaring done, compare the final tracked, staged, and non-ignored untracked delta with the issue-start baseline. Map every remaining file and hunk directly to approved scope, a named acceptance criterion, or indispensable support. Indispensable support means only code that directly implements approved behavior, a test for a named risk or criterion, the minimum synchronization required by an existing contract, or an approved real-path requirement.

Remove every agent-added item without a mapping: debug output, scratch files, temporary tests, generated noise, commented-out implementations, process text, unrequested documentation, speculative abstractions, compatibility branches, public options, dependencies, persistence, and fallback behavior. "Potentially useful later" is not a mapping. If a change's ownership is unclear, if scope must expand, if required real-path proof is missing, or if a tool or protocol failure may have contaminated an artifact, stop and report the decision to the user; do not delete possible user work.

Rerun the final required acceptance after cleanup. A fresh read-only explorer may review a non-trivial final delta when the environment actually supports it; it reports only concrete `file:line` findings, and the main agent owns the final decision. Do not claim independent review when no agent actually returned evidence.

Finalization proof is the main agent's concise final check that the baseline-relative delta is mapped, delivery noise is gone, and every acceptance criterion has evidence. It is not a repository artifact. If the source is an implementation issue, add or change its field to `Completion: done` only after that evidence is complete. Do not invoke another workflow to repair unrelated findings. Do not commit, stage unrelated changes, or delete existing files unless the user or task explicitly authorizes it.

Lead the final user delivery with the outcome. Include only delivered behavior, verification results, and unresolved deviations. Omit introductions, plan recaps, raw tool output, debug detail, and process narrative.
