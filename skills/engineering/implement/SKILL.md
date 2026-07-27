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

Before writing, read the exact issue or PRD, applicable ADRs, and existing mechanisms in the affected area. Establish the approved scope, non-goals, acceptance criteria, and inline evidence. Stop if any material criterion, evidence fact, or selected oracle is missing, unresolved, or conflicting.

Capture the issue-start worktree as working evidence: `git status --short`, working-tree and staged diffs, and non-ignored untracked paths. Treat every pre-existing change as user-owned. Preserve it, do not map it to the current task, and do not delete or reformat it. Keep this baseline in the current task evidence only; do not create a receipt, proof file, or new state record.

For non-trivial work, an available explorer subagent may perform a bounded read-only preflight. Set `fork_turns="none"`, give it the exact task and relevant paths, and ask only for scope, non-goals, applicable ADRs, pre-existing changes, acceptance entrypoints, and `file:line` evidence. It must not edit, clean up, or create artifacts. The main agent verifies the result and retains all scope, write, acceptance, and completion ownership. A missing agent, empty wait, or status notification is not an audit result.

When an implementation issue has `Blocked by`, resolve each path from that issue's feature directory. A `decisions/` target requires `Wayfinder status: resolved`. An `issues/` target carrying both top-level Wayfinder fields is a legacy decision and uses the same oracle; every other `issues/` target requires `Completion: done`, with a missing field treated as `Completion: open`. Stop before implementation if any target is missing, ambiguous, outside the feature, or still blocked. Triage `Status` is not a completion oracle.

## Implementation

Keep temporary exploration, diagnostics, generated output, and scratch work in the system temporary directory by default. A repository-local temporary artifact needs a current acceptance purpose and must be removed before delivery. Do not write plans, to-dos, tool errors, protocol failures, execution status, debug explanations, or other process text into source, configuration, tests, comments, scripts, logs, or documentation.

Run the existing checks named by `static` evidence and any other checks relevant to the changed behavior. Do not create a test file for documentation, comments, copy, or non-behavioral metadata. Run the full suite only when repository policy, the task, or the breadth of the change requires it.

Execute acceptance evidence exactly as approved. Invoke /real-path-verification only when an acceptance criterion has `real-path` evidence or a `target` criterion names an approved real runtime path as its measurement source. For `target` evidence, require a falsifiable recorded metric or definition, comparison, threshold or named baseline, unit, measurement source, and observation window; measure it through the recorded source during the recorded window. Do not weaken, replace, or defer evidence during implementation.

## Delivery squash

Before declaring done, compare the final tracked, staged, and non-ignored untracked delta with the issue-start baseline. Map every remaining file and hunk directly to approved scope, a named acceptance criterion, or indispensable support. Indispensable support means only code that directly implements approved behavior, a test for a named risk or criterion, the minimum synchronization required by an existing contract, or an approved real-path requirement.

Review the agent-owned baseline-relative delta on two independent axes:

- **Contract**: every file and hunk maps to approved scope, a named acceptance criterion, or indispensable support. No non-goal, missing requirement, or unsupported completion claim remains.
- **Repository fit**: every change follows applicable repository instructions, ADRs, existing module interfaces, naming, error-handling, and verification patterns. It does not introduce an unapproved public interface, duplicate mechanism, speculative generality, or weaker verification seam.

Remove every agent-added item without a mapping: debug output, scratch files, temporary tests, generated noise, commented-out implementations, process text, unrequested documentation, speculative abstractions, compatibility branches, public options, dependencies, persistence, and fallback behavior. A temporary bridge in an approved wide mechanical migration is indispensable support only when its `## Transition` names the Contract issue that removes it and its final removal oracle; the Contract issue must remove it. "Potentially useful later" is not a mapping. Correct a Repository-fit finding only within approved scope. If a change's ownership is unclear, if scope must expand, if required real-path proof is missing, or if a tool or protocol failure may have contaminated an artifact, stop and report the decision to the user; do not delete possible user work.

After both axes are clean, rerun the final required acceptance. A fresh read-only explorer may review a non-trivial final delta when the environment actually supports it; it reports only concrete `file:line` findings, and the main agent owns the final decision. Do not claim independent review when no agent actually returned evidence.

Finalization proof is the main agent's concise final check that the baseline-relative delta is mapped, delivery noise is gone, and every acceptance criterion has evidence. A `target` criterion is complete only when the observed value satisfies its recorded target in its recorded observation window. When it does not, leave the issue open and report the target, observed value, measurement source, observation window, and an evidence-based explanation. It is not a repository artifact. If the source is an implementation issue, add or change its field to `Completion: done` only after that evidence is complete. Do not invoke another workflow to repair unrelated findings. Do not commit, stage unrelated changes, or delete existing files unless the user or task explicitly authorizes it.

Lead the final user delivery with the outcome. Include only delivered behavior, verification results, and unresolved deviations. Omit introductions, plan recaps, raw tool output, debug detail, and process narrative.
