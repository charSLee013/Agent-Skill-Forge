---
name: grilling
description: Clarify a plan or design when unresolved goals, choices, or constraints could change the outcome. Use for a focused interview or to resolve important uncertainty within an already requested task.
---

# Grilling

Help the user make the decisions needed to move forward. Read
[references/communication.md](references/communication.md) for user-facing replies.

## Understand the request

Start from the conversation and available evidence. For code work, inspect the
relevant code, project instructions, existing specifications, and domain records.
For other work, use the supplied material; a repository is not a prerequisite.

Identify the outcome, important constraints, and unresolved choices. If they
are already clear, continue the requested task without manufacturing an interview.

## Resolve important choices

Investigate facts the available sources can answer. Ask when the answer could
change the goal, scope, architecture, acceptance, or an irreversible decision.
Explain the tradeoff and recommend a choice when evidence supports one.

Keep questions easy to answer. Ask one at a time when answers depend on each
other; related independent questions may be grouped. Choose reasonable defaults
for reversible details and mention only assumptions that matter to the result.

When the user corrects an interpretation, apply the correction to all affected
work. Ask a repair question only if the intended meaning remains uncertain.

Finish clarification when the remaining unknowns can be investigated, changed
cheaply, or explicitly deferred without undermining the requested outcome.
Explain the resulting decision and any consequential assumptions in ordinary
language. Confirmation is needed only for a remaining material choice or when
the user asked to review the proposal before further work.

## Documents and continuation

Ordinary discussion stays in the conversation. Record established domain terms
or qualifying architectural decisions only when the task authorizes that work
or applicable project rules require it; use the existing domain workflow and
document locations. Reading a glossary does not authorize editing it. Do not
turn a task decision or user correction into a repository instruction.

Continue according to the user's original request:

- A request to think through an idea ends with the clarified recommendation.
- A request to clarify and build continues into `implement` once important
  choices are resolved.
- Use `to-prd` for a requested specification, `to-issues` for requested task
  decomposition, and `wayfinder` for authorized cross-session decision work.

Selecting another skill does not add authorization. Continue work already
requested without requiring the user to name the next skill; stop at an actual
decision, permission boundary, or the requested deliverable.
