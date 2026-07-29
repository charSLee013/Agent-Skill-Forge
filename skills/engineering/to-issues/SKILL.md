---
name: to-issues
description: Break a plan, spec, or PRD into independently-grabbable issues in the local `.codex/agents/` workspace using tracer-bullet vertical slices.
argument-hint: "What should be split into implementation issues?"
disable-model-invocation: true
---

# To Issues

Break a plan into independently-grabbable issues using vertical slices (tracer bullets).

Resolve an optional local map before slicing. If an explicit `MAP.md` path was supplied but does not exist, stop and report the missing path. Without an explicit map path, use `MAP.md` from an explicit PRD or issue's feature directory when present; otherwise search by exact feature slug or Destination under `.codex/agents/work/`. If multiple maps match, stop and ask for the exact `MAP.md` path. If no matching map exists and no explicit `MAP.md` path was supplied, continue when the source material is clear enough for this skill; a map is optional.

When a map exists, read it before drafting implementation slices. Proceed only when its decision issues are resolved or explicitly out of scope, every out-of-scope dependency has a `Dependency resolution` record, and no dependent remains blocked. If the map uses the legacy decision path under `issues/`, read it in place and do not migrate or mix layouts; `setup-agent-skills` is the migration entry point. If material decision fog remains, stop and report the next frontier issue instead of turning a decision into an implementation slice.

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

For every source acceptance criterion covered by a slice, copy its behavior and inline `Evidence` facts into the issue. If the source lacks material acceptance evidence, including a `target` without a falsifiable predicate, ask for it during the breakdown; do not leave that choice to `implement`. An issue has one effective evidence requirement. When its criteria differ, use the strongest evidence: `target` > `real-path` > `static` only when it satisfies every retained criterion's original oracle. Otherwise split the slice before publishing. Do not choose, weaken, or substitute evidence during issue slicing.

### 3a. Wide mechanical migration

A wide mechanical migration is an exception to vertical slicing. Use it only when a shared mechanical change must touch many callers and no individual vertical slice can remain buildable, verifiable, or deployable. Do not use it for a normal cross-layer feature, a speculative abstraction, an unapproved refactor, or a change that can move through an existing seam in small green slices.

When the exception applies, publish these phases in dependency order:

1. **Expand**: introduce the new form. Any temporary bridge for the old form must be explicitly approved, name the local relative path of the Contract-phase issue that will remove it, and exist only until that issue completes.
2. **Migrate**: move stable caller groups by package, directory, or caller group. Each batch has its own issue, acceptance criteria, and `Blocked by` references; do not publish a batch whose work is merely "update all callers".
3. **Contract**: depend on every migrate issue reaching `Completion: done`, prove the old form has no remaining callers, remove the old form and every temporary bridge, then run final acceptance and any selected real-path evidence.

Keep every migrate batch green when possible. When a batch cannot remain green independently, record that constraint before publishing and make the batches block a named final-integration issue. Do not present them as independently verifiable slices.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Blocked by**: which other slices (if any) must complete first
- **Capabilities or user stories covered**: which source behavior this addresses
- **Acceptance evidence**: the inherited evidence and its required facts

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?

Iterate until the user approves the breakdown.

### 5. Publish the issues to the local issue workspace

For each approved slice, write a new implementation issue to `.codex/agents/work/<feature-slug>/issues/<NN>-<slug>.md`. Decision issues belong under `decisions/` and must not be republished here. Use the issue body template below. These issues are considered ready for AFK agents, so publish them with the correct triage label unless instructed otherwise.

Publish issues in dependency order (blockers first) so every `Blocked by` value names a real path relative to `.codex/agents/work/<feature-slug>/`.

For a wide mechanical migration issue only, add this section after `## Acceptance criteria`; omit it for ordinary vertical slices:

```markdown
## Transition

- Phase: expand / migrate / contract (choose one)
- Old form:
- New form:
- Contract issue: <relative path to the Contract-phase issue>
- Batch boundary:
- Final removal oracle:
```

Set `Phase` to exactly one phase. Every wide-migration issue must set `Contract issue` to the relative path of its Contract-phase issue. The Contract issue must list its own local relative path and remove every temporary bridge.

<issue-template>
Completion: open

## Parent

A reference to the parent local issue path (if the source was an existing issue, otherwise omit this section).

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it here and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Acceptance criteria

- [ ] Copy the source criterion's observable behavior.
  Evidence: copy the source `static`, `real-path`, or `target` facts exactly.

Retain every source criterion covered by this issue. State the one effective evidence requirement when it satisfies every source oracle; otherwise split the issue before publishing.

## Blocked by

- A feature-root-relative path to a blocking decision or implementation issue, for example `decisions/01-data-shape.md` or `issues/01-build-api.md` (if any)

Or "None - can start immediately" if no blockers.

</issue-template>

Do NOT close or modify any parent issue.
