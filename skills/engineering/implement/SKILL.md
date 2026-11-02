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

Identify what makes one feasible result better for this user, separately from
acceptance conditions and hard constraints. Preserve their priority among
quality, throughput, latency, cost, or other relevant outcomes; do not invent a
score or silently make resource economy the objective. For an optimization
request, a minimum acceptance threshold does not replace the requested best
achievable result within the authorized budget. An ordinary bounded change
does not acquire an optimization phase merely by entering this workflow.

Keep the user's unfinished outcome ahead of supporting work. A broken optional
diagnostic, test helper, or documentation path is not a blocker when an existing
path can still deliver and verify the requested behavior. Repair a support path
only when it is necessary for that outcome; report an unavailable required
oracle instead of replacing delivery with tool-building.

Capture the initial tracked, staged, and non-ignored untracked changes as working
evidence. Preserve pre-existing work and distinguish it from your own changes.
Keep this baseline in the task context, not a new repository report.

For an implementation issue with `Blocked by`, read the local workspace rules,
or `setup-agent-skills`'s `issue-tracker-local.md` when no local rules exist.
Resolve each dependency relative to the feature directory. A decision requires
`Wayfinder status: resolved`; an implementation requires `Completion: done`,
with a missing completion field treated as open. A missing, ambiguous,
out-of-feature, or unfinished blocker prevents its dependent from starting;
triage status is not completion. Continue other already authorized, independent work when possible.

## Implement and verify

For uncertain behavior or a claim spanning configuration and runtime, read
[references/evidence.md](references/evidence.md). Use its evidence discipline
without turning every straightforward edit into a separate investigation.

Trace the affected callers and failure paths. Prefer a suitable existing
mechanism, standard library, platform capability, or installed dependency over
new machinery. Choose by correctness, readability, and fit rather than a fixed
ranking or line count. A requested redesign may require substantial change;
minimality must not silently restore constraints the user explicitly removed.

For an optimization request, use a small evidence-driven loop: identify the
limiting stage, choose a promising change, observe its effect against the best
supported feasible result, keep useful improvements, then reassess the next
bottleneck and likely gain. A failed trial can still eliminate an explanation.
Revert only your own unsuccessful changes, preserving the best result and user
work. Added complexity needs a practical benefit.

Choose parameter, capacity, or algorithm changes from the workload. If workers
are already fully supplied, adding queue slots may provide no gain; investigate
the downstream stage. If a decoder frequently waits for input, a bounded trial
of prefetch or capacity may help. Account for total resource use, transient peaks,
and other consumers within the user's limit, with justified headroom. Capacity
limits constrain feasible settings; they do not replace the improvement goal.

Continue while the next feasible trial has worthwhile expected benefit within
the authorized effort and budget. Stop at the requested outcome for a bounded
change, or at the supplied stopping condition, exhausted effort budget, or low
expected further benefit for optimization. Keep the best supported result and
state the remaining bottleneck and limits of the comparison. Ordinary tuning
needs no persistent research ledger; `research-loop` remains a manual option
for a user-selected systematic exploration.

Preserve required behavior, error handling, security boundaries, accessibility,
and compatibility. Add supporting changes only when necessary for the requested
outcome. Keep scratch work in the system temporary directory; keep execution
notes, tool errors, and debug explanations out of deliverables.

Select checks appropriate to the changed behavior and risk. Reuse existing
checks when sufficient; add regression coverage for a meaningful failure or
invariant when needed. Documentation, copy, and metadata do not require new
tests merely because they changed. Broaden or repeat passing checks only after
a new change, failure, or unresolved concern.

Do not require or default to test-driven development, test-first sequencing,
or a red-green ritual. A regression test may be useful before or after a fix;
choose its timing from the actual diagnosis and acceptance need. When a test
owns asynchronous work or shared resources, read `test-reliability` for the
affected boundary. For failures whose recovery or partial effects matter, read
`error-handling`. Locate supporting skills through host discovery or the source
plugin manifest; reading them does not expand the task or authorize new work.

For every acceptance condition, preserve all recorded observations and expected
results. `static`, `real-path`, and `target` describe complementary evidence;
[references/evidence.md](references/evidence.md) owns their meanings. One issue
or condition may require several of them. Existing single `Evidence` records
remain valid. Use `real-path-verification` for required runtime observations,
including target measurements whose source is an approved real runtime path.
Neither a measurement nor a runtime pass replaces an independent correctness,
compatibility, or content-review requirement.

A checksum or byte-identical artifact can establish integrity, not that the
requested runtime behavior worked. Do not replace the recorded behavioral
oracle with a hash, passing process exit, or completion report.

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

If a push was explicitly requested, inspect the outgoing diff and select the
smallest checks that cover its changed behavior before pushing. Do not re-run
passing checks merely because commit or push follows; a new change or observed
failure can justify another run. Report pending remote CI as pending, not as a
passed local or real-path check.

For an approved wide mechanical migration, keep a temporary bridge only while
its `Transition` names the issue responsible for removing it and the final
removal check. That final issue must remove the bridge before completion.

Mark an implementation issue `Completion: done` only when every criterion and
all its required observations are satisfied. Verify the combined feature outcome
at its owning issue or whole-task acceptance; completed local slices alone do
not prove it. Retain shared resource limits across slices. If a target is unmet,
leave its issue open and report the expected and observed values,
source, and observation window. Report the delivered behavior,
verification, and unresolved deviations in the user's language. Continue the
remaining authorized work; commits, deployment, and unrelated changes still
require their own task authorization. Pushes and PR mutations do too.
