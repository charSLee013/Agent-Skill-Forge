---
name: grill-with-docs
description: Clarify an uncertain plan or design in one session while recording only established domain language and qualifying durable decisions.
argument-hint: "What plan or design should be clarified?"
disable-model-invocation: true
---

# Grill with docs

Clarify the decision trunk of one plan or design, then hand the bounded result to
the smallest delivery workflow. This is a single-session clarification phase,
not a cross-session decision map and not an implementation phase.

## Establish context

Read the conversation, applicable `AGENTS.md`, relevant code, `CONTEXT.md`, ADRs,
and existing PRD or issue material before asking questions. Investigate facts
that the repository can answer. Missing `CONTEXT.md` or ADR directories do not
block the session and are not a reason to create empty scaffolding.

Treat `AGENTS.md` only as repository operating instructions and navigation. Do
not propose or write product behavior, feature scope, acceptance criteria,
implementation decisions, issue state, progress, session feedback, or lessons
from the current conversation into it.

Use this workflow when uncertainty about the goal, scope, architecture, major
risk, domain boundary, or acceptance would make direct planning or
implementation guess. If the request is already bounded, say so and recommend
the appropriate delivery workflow without manufacturing an interview.

## Run the clarification

Invoke `grilling` as the interview discipline. It owns every user question,
asks one highest-leverage question at a time, investigates discoverable facts,
backfills reversible defaults, and produces the final calibration summary.

Invoke `domain-modeling` alongside it only for active domain work:

- challenge a term when its meaning changes the decision trunk or conflicts
  with the existing glossary;
- update `CONTEXT.md` only after a canonical domain term has actually been
  established;
- offer an ADR only when the decision is hard to reverse, surprising without
  context, and the result of a real trade-off.

Do not create or update durable documents merely because the session discussed
a product rule, selected a feature behavior, corrected an answer, or reached a
temporary working assumption. Product scope and acceptance stay in the current
conversation until a user-invoked delivery workflow gives them an owner.

## Complete and route

Finish when the goal, success criteria, scope, major constraints, meaningful
trade-offs, irreversible risks, and acceptance boundary are clear enough that
remaining unknowns are cheap to change, explicitly deferred, or assigned to a
later phase.

Return the `grilling` decision summary and name any glossary or ADR files that
were actually changed. If no durable domain fact qualified, state that no domain
documents were needed.

Recommend exactly one next workflow, then stop:

- `implement` when the result is bounded and directly executable;
- `to-prd` when the clarified result needs a formal specification;
- `to-issues` when an approved plan is ready for implementation slicing;
- `wayfinder` when material route decisions remain and the work must continue
  across sessions.

These are user-invoked workflows. Do not invoke or chain them automatically.
