---
name: to-prd
description: Turn the current conversation into a PRD and publish it to the local `.codex/agents/` workspace — no discovery interview, with direct confirmation only for unresolved material acceptance evidence.
argument-hint: "What should become a PRD?"
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a PRD. Do NOT interview the user to discover the goal, scope, solution, or architecture — synthesize what you already know.

Resolve an optional local map before synthesis. If an explicit `MAP.md` path was supplied but does not exist, stop and report the missing path. Without an explicit map path, use `MAP.md` from an explicit PRD or issue's feature directory when present; otherwise search by exact feature slug or Destination under `.codex/agents/work/`. If multiple maps match, stop and ask for the exact `MAP.md` path. If no matching map exists and no explicit `MAP.md` path was supplied, continue when the source material is clear enough for this skill; a map is optional.

When a map exists, read it before synthesising the PRD and use its resolved `Decisions so far` and linked decision issues as the source of established decisions. Proceed only when its decision issues are resolved or explicitly out of scope, every out-of-scope dependency has a `Dependency resolution` record, and no dependent remains blocked. If the map uses the legacy decision path under `issues/`, read it in place and do not migrate or mix layouts; `setup-agent-skills` is the migration entry point. If material decision fog remains, stop and report the next frontier issue instead of guessing in the PRD.

The local issue workspace and triage label vocabulary should have been provided to you in `.codex/agents/`. If missing, recommend that the user explicitly run `/setup-agent-skills`, then stop this skill.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the PRD, and respect any ADRs in the area you're touching.

2. For each material behavior, record an observable acceptance criterion and its exact evidence. Prefer an existing verification seam and do not invent a test seam solely to complete the PRD.

When material acceptance evidence is unresolved, ask one direct verification question at a time and wait for the answer before asking the next. This confirmation is limited to the criterion's evidence; do not turn it into discovery. If the question changes the goal, scope, solution, architecture, or other material decision, stop and recommend `grill-with-docs` or Wayfinder instead of publishing a PRD. Do not publish `ready-for-agent` content with material acceptance evidence unresolved.

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

Each criterion must map to a capability or user story and state exactly one `Evidence` value:

- `static`: name the existing relevant static check or checks. Delivery hygiene and the final baseline-relative review remain required.
- `real-path`: name the existing runtime path or replay and the observable oracle. The later real-path safety gate obtains approval for the actual action.
- `target`: state a falsifiable target: metric or definition, comparison, threshold or named baseline, unit, measurement source, and observation window.

Do not use an evidence value as a label without the facts needed to execute it.

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

Record only the decisions needed to execute the stated acceptance evidence. Reuse existing checks and seams. Do not invent a test, harness, seam, or alternate runtime path solely to complete the PRD.

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.

</prd-template>
