---
name: real-path-verification
description: Verify an approved behavior through a real runtime path or a production-equivalent replay. Use during implement when an acceptance criterion explicitly requires production, real traffic, canary, shadow, replay, migration, release verification, or end-to-end evidence. Do not use for routine unit, smoke, mock, minimal-repro, documentation, or trivial-edit work.
---

# Real Path Verification

Verify the behavior at the runtime path the acceptance condition describes.
Consume the current goal, criteria, required observations, environment, known
entry points, and established risk choices. Ordinary requests need no formal
PRD, new interview, or repartitioning of the task.

Read `implement`'s `references/evidence.md` through host-discovered skill paths
or the source plugin manifest. It owns evidence meanings and claim limits.
This skill supplies the runtime-specific decisions below.

## Authorization and consequences

Before an action introduces an unapproved change to shared or production state,
consequential external traffic, material cost, sensitive-data exposure, or use
of production credentials, present the concrete environment, action, expected
impact, cleanup or rollback, stop condition, and observation that decides the
result. Obtain the missing authorization before that action.

Consume the user's established choice when the actual action fits it. Revisit
only a material change in environment, side effects, traffic, cost, or exposure.
Ordinary reversible local support and read-only inspection need no separate
safety presentation. A verification-only request does not authorize a product
change or deployment to make the criterion pass.

## Reach and observe the required path

Locate a suitable project command, deployed endpoint, CLI, browser flow,
captured trace, or approved replay. Prefer existing entry points. If a necessary
call, temporary input, or measurement is missing, supply narrowly scoped support
when it fits the task's authorization, cost, and side-effect limits. A helper
must reach or observe the required path; its existence or successful execution
is not evidence that the business result occurred.

Establish the relevant environment equivalence for a replay or alternative
runtime: version, configuration, workload, data, dependencies, and effects that
matter to the criterion. A staging path can qualify when that parity is
established; its name alone proves nothing. Unit, mock, smoke, tracer, or
minimal-repro results support only their observed boundary. They cannot replace
a required production or parity-established observation.

If a necessary environment, command, data set, permission, traffic source, or
parity fact cannot be obtained within the task, mark the affected criterion
unverified and describe the exact gap. Continue other available verification
and independent authorized delivery. Do not substitute a weaker observation or
stop the whole task merely because no ready-made command exists.

Run the authorized path and compare observations with every selected criterion.
Capture the actual business result, environment, version or deploy, and time
window. Use existing telemetry, trace/request IDs, or observation links when
available. Preserve all required observations for a criterion that also needs
measurements or source review; runtime execution does not replace them.

## Supporting artifacts and cleanup

Create or retain files only when they serve execution, analysis, recovery, or
an explicitly requested deliverable. Use existing output directly where
sufficient; a transcript directory or raw capture is not a default deliverable.
Keep ordinary scratch inputs and helpers in the system temporary directory.

Arrange reasonable cleanup before use, including failure handling or recovery
where practical. Remove ordinary scratch material after the observation and
report any cleanup failure requiring follow-up. Lack of a guarantee for every
possible interruption does not prohibit an otherwise reasonable local run.
Sensitive data, production changes, and shared resources require protection,
retention limits, and cleanup/rollback appropriate to their actual consequences;
if those cannot be met, do not take the affected action.

## Return to delivery

Report passed, failed, or unverified for each selected criterion, with expected
and observed results, source and observation window, relevant side-effect and
cleanup results, and any unverified boundary. A real-path pass needs the actual
runtime observation and any required parity evidence. A SHA-256 match, process
exit, or HTTP 2xx cannot establish the requested business result.

Remove unnecessary agent-owned support, preserve user work, and continue any
remaining authorized task. Verification is accounted for when every selected
criterion has a supported conclusion; failed or unverified criteria remain
unmet and prevent a claim of full acceptance.
