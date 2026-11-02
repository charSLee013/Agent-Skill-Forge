---
name: to-prd
description: Write a specification from established requirements when the user requests a PRD or the authorized work includes a durable specification. Use the conversation or an existing plan; ordinary implementation does not require a PRD.
argument-hint: "What should become a PRD?"
---

Produce the requested specification from the conversation and relevant source material.
Read `grilling`'s `references/communication.md` for replies and
`setup-agent-skills`'s `issue-tracker-local.md` for workspace defaults. Locate
these skills through host-discovered paths, or the repository plugin manifest
when working from source. Reading references does not invoke their workflows.

Resolve an optional local map before synthesis. If an explicit `MAP.md` path was supplied but does not exist, stop and report the missing path. Without an explicit map path, use `MAP.md` from an explicit PRD or issue's feature directory when present; otherwise search by exact feature slug or Destination under `.codex/agents/work/`. If multiple maps match, stop and ask for the exact `MAP.md` path. If no matching map exists and no explicit `MAP.md` path was supplied, continue when the source material is clear enough for this skill; a map is optional.

When a map exists, read it before synthesising the PRD and use its resolved `Decisions so far` and linked decision issues as the source of established decisions. Proceed only when its decision issues are resolved or explicitly out of scope, every out-of-scope dependency has a `Dependency resolution` record, and no dependent remains blocked. If material decisions remain, resolve them through `wayfinder` when that work is already authorized; otherwise report the next frontier issue. Do not guess their answers in the PRD.

Read existing local workspace configuration when present. Otherwise use the
shipped workspace conventions and default labels, creating only the requested
artifact and its directories. Missing setup is not a prerequisite failure.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the PRD, and respect any ADRs in the area you're touching.

2. For each material behavior, record an observable acceptance criterion and its exact evidence. Prefer existing verification paths; identify necessary support within the task rather than inventing a seam merely to fill the document.

Resolve verification facts from existing code and checks. Ask only about a
material choice that the sources cannot settle; use `grilling` within this task
when clarification is needed. Resume the specification when that choice is
resolved, without requiring another command. Do not publish `ready-for-agent`
content with material behavior or acceptance evidence unresolved.

3. Write the PRD using the template below, then publish it to the local issue workspace at `.codex/agents/work/<feature-slug>/PRD.md`. Apply the `ready-for-agent` triage label - no need for additional triage.

<prd-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## Capabilities and User Stories

A concise list of the requested behavior. Use a user story when an actor and benefit clarify the requirement:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Use a capability statement when behavior has no meaningful user actor, such as a migration, internal contract, or architectural change. Cover every material requested behavior without adding speculative future behavior or duplicate implementation details.

## Acceptance Criteria

Map each criterion to a capability or user story and record every observation
needed to establish it, with its expected result. Use `implement`'s
`references/evidence.md` for the meanings and limits of `static`, `real-path`,
and `target`; locate it through host discovery or the source plugin manifest.
These are descriptions, not a hierarchy. A criterion can require multiple kinds
of evidence. Existing single `Evidence` entries remain valid without conversion.

For example, use this shape when more than one observation is necessary; omit
unused entries and fill in the executable facts for each retained entry:

```markdown
- [ ] <Capability/story and observable acceptance condition>
  Evidence:
    - static: <named check or review predicate; expected result and limits>
    - target: <metric, comparison, threshold/baseline, unit, source, window; expected result>
    - real-path: <runtime path/replay, environment, oracle; expected result>
```

A measurable target must be falsifiable. Do not invent a metric to restate a
structural constraint, or replace required runtime evidence with source review.
Carry combined feature acceptance and shared resource limits explicitly so
later issue-level checks cannot silently replace them.

When the request includes optimization, also state what should improve and in
which direction, the user's tradeoff priorities, hard limits, and any authorized
effort budget. Keep minimum acceptance separate from the improvement objective.
Preserve a supplied stopping condition; otherwise bound effort by the task and
stop when further feasible changes have little expected benefit. Do not invent
a numeric score or turn a resource ceiling into a minimization objective.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Verification Decisions

Record the decisions needed to obtain every required observation. Reuse suitable
existing checks and paths. If narrowly scoped support is necessary, describe
what it must enable and any unresolved authorization or equivalence facts.
Do not create a harness or alternate path merely to fill the PRD.

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.

</prd-template>

## Continue the requested work

If the user requested only a specification or asked to review it first, deliver
the PRD and stop there. If implementation or task decomposition is already
authorized, continue with `implement` or `to-issues` as appropriate. A completed
PRD does not independently authorize either action.
