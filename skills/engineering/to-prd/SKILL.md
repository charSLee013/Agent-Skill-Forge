---
name: to-prd
description: Turn the current conversation into a PRD and publish it to the local `.codex/agents/` workspace — no interview, just synthesis of what you've already discussed.
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a PRD. Do NOT interview the user — just synthesize what you already know.

Resolve a matching local map using an explicit MAP path first, then the feature directory of an explicit PRD or issue path, then an exact feature-slug or Destination match under `.codex/agents/work/`. If there are zero or multiple matches, stop and ask rather than guessing. Read the map before synthesising the PRD and use its resolved `Decisions so far` and linked decision issues as the source of established decisions. Proceed only when its decision issues are resolved or explicitly out of scope, every out-of-scope dependency has a `Dependency resolution` record, and no dependent remains blocked. If the map uses the legacy decision path under `issues/`, read it in place and do not migrate or mix layouts; setup-agent-skills is the migration entry point. If material decision fog remains, stop and report the next frontier issue instead of guessing in the PRD.

The local issue workspace and triage label vocabulary should have been provided to you in `.codex/agents/`. If missing, recommend that the user explicitly run `/setup-agent-skills`, then stop this skill.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the PRD, and respect any ADRs in the area you're touching.

2. Record the highest existing interface at which the requested behavior can be verified, if that decision is already established in the conversation or codebase. Prefer existing seams and do not invent a test seam solely to complete the PRD. If the seam is genuinely unresolved and changes scope or risk, record it as an open decision instead of starting an interview inside this synthesis skill.

3. Write the PRD using the template below, then publish it to the local issue workspace at `.codex/agents/work/<feature-slug>/PRD.md`. Apply the `ready-for-agent` triage label - no need for additional triage.

<prd-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A concise numbered list of user stories needed to express the requested behavior. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Cover the requested behavior and its material acceptance cases. Do not add speculative future stories or duplicate implementation details.

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

A list of verification decisions that were made. Include:

- The acceptance oracle for each material behavior
- Existing checks or tests that provide that oracle
- Any new test only when a behavior change or regression needs a correct seam
- Production or production-equivalent evidence when the requirement depends on it

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.

</prd-template>
