---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user explicitly asks to diagnose a hard bug, debug an uncertain failure, or investigate a performance regression.
---

# Diagnosing Bugs

A discipline for hard bugs. Use only the phases that resolve the current uncertainty, and record why any phase was skipped.

Do not enter this workflow for a routine failed command, an obvious one-line fix, or a documentation/configuration edit with an existing verification signal. Use the existing signal first. A new test or harness is justified only when it is the smallest correct oracle for the reported bug.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Phase 1 — Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal for the bug — one that goes red on _this_ bug — you will find the cause; bisection, hypothesis-testing, and instrumentation all just consume it. If you don't have one, no amount of staring at code will save you.

Spend effort proportional to the uncertainty and blast radius. Prefer the smallest feedback loop that can distinguish the likely causes.

### Ways to construct one — reuse the smallest existing signal first

Try these existing paths in roughly this order:

1. **Existing test or check** at the seam that reaches the bug — unit, integration, or e2e.
2. **Existing curl / HTTP command** against a running service.
3. **Existing CLI invocation** with a fixture input and a known-good output or oracle.
4. **Existing browser flow** — use the project's current Playwright/Puppeteer path when one exists.
5. **Existing captured trace or replay** — use the real request, payload, or event log already available.
6. **Existing differential or versioned path** — compare the affected version/configuration with a known-good one when that is how the symptom is defined.

Only when no existing signal can expose the reported symptom may you propose an additional oracle. Add a regression test only when the task needs durable regression evidence and a correct seam exists. A temporary diagnostic probe or harness requires a concrete reason and user/task authorization; keep its artifacts under the system temporary directory, not in the repository. Do not create a standalone Python test merely because the existing command is inconvenient.

Property/fuzz loops, bisection, stress runs, and human-in-the-loop scripts are specialized options for symptoms that require them, not default escalation steps. Choose them only when the symptom and expected evidence justify their cost.

Build the right feedback loop before spending effort on a fix.

### Tighten the loop

Tighten the loop only when the current signal is too slow, noisy, or non-deterministic to support the next decision:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is tight — a debugging superpower.

### Non-deterministic bugs

When the symptom is non-deterministic, increase the reproduction rate only as much as needed to distinguish the hypotheses. Start with a small repeat count; add stress, parallelism, or timing perturbation only when the observed failure rate and expected evidence justify the cost.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to whatever environment reproduces it, (b) a captured artifact (HAR file, log dump, core dump, screen recording with timestamps), or (c) permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

### Completion criterion — a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** — a script path, a test invocation, a curl — that you have **already run at least once** (paste the invocation and its output), and that is:

- [ ] **Red-capable** — it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring" — it must be able to _catch this specific bug_.
- [ ] **Deterministic** — same verdict every run (flaky bugs: a pinned, high reproduction rate, per above).
- [ ] **Fast** — seconds, not minutes.
- [ ] **Agent-runnable** — you can run it unattended; a human in the loop only via `scripts/hitl-loop.template.sh`.

If you catch yourself reading code to build a theory before this command exists, **stop — jumping straight to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2.

## Phase 2 — Reproduce + minimise

Run the loop. Watch it go red — the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described — not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut — keep only what's load-bearing for the failure.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and can become a regression test in Phase 5 when the task needs durable evidence and the seam is correct.

Done when **every remaining element is load-bearing** — removing any one of them makes the loop go green.

Do not proceed until you have reproduced **and** minimised.

## Phase 3 — Hypothesise

Generate enough ranked hypotheses to cover the plausible causes. Usually this means two to five; if evidence strongly favors one, state which competing explanations were considered and why they are lower priority.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

Show the ranked list to the user before testing when their domain knowledge can change priority, scope, risk, or the chosen environment. Otherwise record the ranking in the diagnostic report and continue without turning it into a separate interview.

## Phase 4 — Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Prefer an existing benchmark, profiler, or query plan. Create a temporary measurement only when no existing signal answers the question and the extra artifact is authorized. Measure first, fix second.

## Phase 5 — Fix + appropriate verification

Add a regression test only when there is a **correct seam** and the task needs durable regression evidence. Do not add one solely to satisfy this workflow.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists and a regression test is justified:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

If no new regression test is justified, fix the code and re-run the existing Phase 1 loop plus the checks required by the task. Record which existing oracle was used and why it is sufficient.

## Phase 6 — Cleanup + post-mortem

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] The existing verification loop passes, and any added regression test passes (or the absence of a correct seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The hypothesis that turned out correct is stated in the final report or handoff; commit/PR updates happen only when explicitly requested

**Then ask: what would have prevented this bug?** If the answer involves architectural change (no good test seam, tangled callers, hidden coupling), record it as a follow-up recommendation. Run the architecture-review skill only when the user explicitly chooses that follow-up; do not expand the current bug fix automatically.
