---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user explicitly asks to diagnose a hard bug, debug an uncertain failure, or investigate a performance regression.
---

# Diagnosing Bugs

Reduce uncertainty about the reported failure, then deliver the supported
conclusion or authorized fix. Start with the symptom, impact, conditions, and
available evidence. Choose the next observation by which plausible explanations
it can distinguish, its cost, and its side effects. Repeat as the evidence changes.

For behavior claims, read `implement`'s `references/evidence.md` through
host-discovered skill paths or the source plugin manifest. It owns the shared
evidence boundaries. A diagnosis-only request stays read-only; implement a fix
only when requested. Routine failed commands and obvious fixes can use their
existing signal without entering a larger investigation.

Read relevant domain context and ADRs when they help identify the affected
modules and contracts.

## Establish what is known

Separate the user's symptom from nearby failures. Inspect available reports,
versions, inputs, workload, recent changes, traces, and source. Distinguish
observed facts from assumptions. Consider competing causes, including a faulty
measurement or environmental difference, rather than accepting the first
plausible explanation.

For each live explanation, identify a prediction and an observation that could
support or weaken it. Prioritize by fit to the evidence, impact, and the cost of
learning more. Ask about missing domain facts or consequential choices only when
they affect the investigation; continue discoverable work in the meantime.

## Choose the next observation

Reuse suitable existing checks, CLI or browser flows, captured traces, profilers,
replays, or comparisons with a known-good version. There is no fixed tool order:

- Reproduce when execution can reveal the failure or test a causal prediction.
  A short deterministic loop is useful when feasible, not an entry condition.
- Reduce inputs, callers, configuration, or steps when that distinguishes causes.
  Preserve the original scenario; further minimization need not delay a supported fix.
- Inspect logs or use a debugger to observe the boundary where explanations differ.
  Account for instrumentation that changes timing or resource use.
- For performance problems, choose measurements that expose the limiting stage:
  profiles, query plans, allocation growth, queue waits, or workload timings.
- For intermittent failures, use controlled scheduling, stress, repeated runs,
  or existing incidents as the symptom warrants. Choose duration and repetitions
  from occurrence rates and the decision needed, within the authorized budget.

A slow leak may need a long observation window. A rare race may remain
probabilistic. Production-only records can support a causal inference without a
local reproduction. None must first become a single-command, seconds-long,
unattended test. When human interaction is useful, coordinate it directly; the
optional [interactive template](scripts/hitl-loop.template.sh) is only a
convenience for an interactive terminal, not a required route.

If a necessary observation needs small instrumentation, a temporary input, or a
measurement helper, judge it by necessity, cost, side effects, and existing task
authorization. Keep scratch work in the system temporary directory and arrange
reasonable cleanup. Read-only diagnosis does not authorize source changes or
new external effects. If a helper fails, investigate that failure only as far as
needed to obtain evidence for the original problem.

## Update the explanation

Compare the observation with the predictions. Reject or revise explanations
that conflict with it; seek a discriminating check when alternatives remain.
Isolate variables where practical, and account for interactions when a combined
change prevents causal attribution. Do not equate correlation with proof or a
failure-free short run with absence of a rare fault.

Improving feedback speed or repeatability is useful when it changes the next
decision. Stop refining the diagnostic method when it adds little information.
If necessary access, records, or runtime conditions are unavailable, identify
the gap and continue independent authorized investigation. A diagnosis can
finish with an evidence-backed limited conclusion and a specific next
observation; do not label it a reproduced cause or verified fix.

## Fix and verify when authorized

Apply a change that addresses the supported cause through `implement`, preserving
required behavior. Choose verification from the actual failure and acceptance
conditions. Revisit the original scenario when available, and cover relevant
failure paths. For a race or slow leak, state the workload, observation window,
and residual uncertainty rather than promising certainty from a short run.

Add regression coverage when a durable check of a meaningful failure or invariant
is needed and the seam exercises the real bug pattern. Choose timing before or
after the fix from the diagnosis; do not require or default to TDD, test-first
sequencing, or a red-green ritual. A shallow test that cannot reach the failure
is not regression evidence. Missing coverage may be a limitation without proving
an architectural defect or requiring an architecture review.

## Deliver an honest conclusion

Remove temporary instrumentation and scratch artifacts actually created for
this investigation, preserving user work and useful authorized changes. Verify
cleanup against the task baseline rather than a universal debug-prefix ritual.

Report the relevant observations, best-supported explanation, competing causes
still plausible, and any delivered change. Keep cause inference, reproduced
failure, and verified repair distinct. Name unavailable checks and their effect
on confidence. A follow-up investigation or architecture review is warranted
only when a concrete remaining problem justifies it; it is not a completion gate.
