---
name: implement
description: Implement a clear coding request, fix, or redesign from the conversation, a specification, or issues. Use when the user has requested changes; review and verification questions alone do not authorize implementation.
argument-hint: "What requested change should be completed?"
---

# Implement

Complete the user's requested change and verify the resulting behavior. A clear
natural-language request is sufficient; a PRD, issue, or configured workspace
is not required.

Read `grilling`'s `references/communication.md` for user-facing replies. Locate
the owning skill through the host's discovered skill paths, or through this
repository's plugin manifest when working from source. Reading a reference does
not invoke its owner's workflow. Use the same lookup for other shared references.

## Establish the work

Read the current request, applicable project instructions, relevant code, and
any supplied PRD, issues, or ADRs. Establish the behavior to deliver and how it
can be checked. Investigate discoverable facts and choose routine reversible
details; use `grilling` only when an important unresolved choice affects the
outcome. Existing authorization carries across these steps.

Capture the initial tracked, staged, and non-ignored untracked changes as working
evidence. Preserve pre-existing work and distinguish it from your own changes.
Keep this baseline in the task context, not a new repository report.

For an implementation issue with `Blocked by`, read the local workspace rules,
or `setup-agent-skills`'s `issue-tracker-local.md` when no local rules exist.
Resolve each dependency relative to the feature directory. A decision requires
`Wayfinder status: resolved`; an implementation requires `Completion: done`,
with a missing completion field treated as open. Legacy issues carrying both
Wayfinder fields remain decisions. A missing, ambiguous, out-of-feature, or
unfinished blocker prevents its dependent from starting; triage status is not
completion. Continue other already authorized, independent work when possible.

## Implement and verify

For uncertain behavior or a claim spanning configuration and runtime, read
[references/evidence.md](references/evidence.md). Use its evidence discipline
without turning every straightforward edit into a separate investigation.

Trace the affected callers and failure paths. Prefer a suitable existing
mechanism, standard library, platform capability, or installed dependency over
new machinery. Choose by correctness, readability, and fit rather than a fixed
ranking or line count. A requested redesign may require substantial change;
minimality must not silently restore constraints the user explicitly removed.

Preserve required behavior, error handling, security boundaries, accessibility,
and compatibility. Add supporting changes only when necessary for the requested
outcome. Keep scratch work in the system temporary directory; keep execution
notes, tool errors, and debug explanations out of deliverables.

Select checks appropriate to the changed behavior and risk. Reuse existing
checks when sufficient; add regression coverage for a meaningful failure or
invariant when needed. Documentation, copy, and metadata do not require new
tests merely because they changed. Broaden or repeat passing checks only after
a new change, failure, or unresolved concern.

When a formal work item records acceptance evidence, preserve its meaning:

- `static`: run the named relevant checks.
- `real-path`: use `real-path-verification` for the recorded runtime observation.
- `target`: measure the recorded metric or definition against its comparison,
  threshold or baseline, unit, source, and observation window. Use
  `real-path-verification` when that source is an approved real runtime path.

Missing formal labels do not block an ordinary request. Missing facts that make
a required result unverifiable must be resolved or reported; never silently
weaken an agreed acceptance criterion.

## Deliver

Compare your final changes with the initial workspace. Check that they implement
the requested behavior, follow project interfaces and conventions, preserve
user-owned changes, and contain no unnecessary agent-added work. Remove your
temporary artifacts and debug content. If this review changes behavior, rerun
the affected acceptance checks. Claim independent review only when it actually
returned evidence.

For an approved wide mechanical migration, keep a temporary bridge only while
its `Transition` names the issue responsible for removing it and the final
removal check. That final issue must remove the bridge before completion.

Mark an implementation issue `Completion: done` only when every criterion is
satisfied. If a target is unmet, leave it open and report the expected and
observed values, source, and observation window. Report the delivered behavior,
verification, and unresolved deviations in the user's language. Continue the
remaining authorized work; commits, deployment, and unrelated changes still
require their own task authorization.
