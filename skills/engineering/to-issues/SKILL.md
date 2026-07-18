---
name: to-issues
description: Break a plan, spec, or PRD into independently-grabbable issues in the local `.codex/agents/` workspace using tracer-bullet vertical slices.
disable-model-invocation: true
---

# To Issues

Break a plan into independently-grabbable issues using vertical slices (tracer bullets).

Resolve a matching local map using an explicit MAP path first, then the feature directory of an explicit PRD or issue path, then an exact feature-slug or Destination match under `.codex/agents/work/`. If there are zero or multiple matches, stop and ask rather than guessing. Read the map before drafting implementation slices. Proceed only when its decision issues are resolved or explicitly out of scope, every out-of-scope dependency has a `Dependency resolution` record, and no dependent remains blocked. If the map uses the legacy decision path under `issues/`, read it in place and do not migrate or mix layouts; setup-agent-skills is the migration entry point. If material decision fog remains, stop and report the next frontier issue instead of turning a decision into an implementation slice.

The local issue workspace and triage label vocabulary should have been provided to you in `.codex/agents/`. If missing, recommend that the user explicitly run `/setup-agent-skills`, then stop this skill.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes an issue reference as an argument, read its full body and comments from the local issue workspace. Issue references are local paths under `.codex/agents/work/`.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Issue titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Do not prefactor by default. Record a prefactor only when the parent plan explicitly includes it or the current design makes the requested slice impossible. Otherwise keep the issue scoped to the requested behavior.

### 3. Draft vertical slices

Break the plan into independently verifiable issues. Use a thin vertical slice when the feature crosses multiple layers, but do not force unrelated layers into every issue.

<vertical-slice-rules>

- Each slice delivers a narrow but complete path through every relevant layer.
- A completed slice is demoable or verifiable on its own
- Prefactoring is included only when the parent plan explicitly authorizes it or the requested slice cannot be implemented without it.

</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?

If the parent plan produces three or more slices, make one explicit decision at this point:

- real-path-proof: recommended-at-final-integration
- real-path-proof: required
- real-path-proof: not-applicable

Explain the risk and expected runtime evidence. Do not run verification during issue slicing and do not repeat this question for every issue.
When real-path proof is required or recommended, show the user the environment, side effects, traffic/cost, data exposure, rollback, cleanup, and stop condition. Record the user's risk choice once before publishing the issues.

Iterate until the user approves the breakdown.

### 5. Publish the issues to the local issue workspace

For each approved slice, write a new implementation issue to `.codex/agents/work/<feature-slug>/issues/<NN>-<slug>.md`. Decision issues belong under `decisions/` and must not be republished here. Use the issue body template below. These issues are considered ready for AFK agents, so publish them with the correct triage label unless instructed otherwise.

Publish issues in dependency order (blockers first) so you can reference real relative paths in the "Blocked by" field.

<issue-template>
## Parent

A reference to the parent local issue path (if the source was an existing issue, otherwise omit this section).

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it here and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Verification profile

- Real-path proof: recommended-at-final-integration / required / not-applicable
- Runtime entrypoint or replay source:
- Risk choice shown to user: yes / no / pending
- Risk approval and rollback owner:

## Blocked by

- A relative path to the blocking implementation issue, for example `issues/01-build-api.md` (if any)

Or "None - can start immediately" if no blockers.

</issue-template>

Do NOT close or modify any parent issue.
