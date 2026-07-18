---
name: wayfinder
description: Plan work that spans multiple agent sessions while material decisions remain unresolved. Use only when a destination can be named but the route is still unclear and direct planning or implementation would require guessing.
disable-model-invocation: true
---

# Wayfinder

Use this skill as a user-invoked decision-map phase for genuinely large work. It creates a low-resolution map and sharp decision issues in the local `.codex/agents/` workspace, then resolves one decision issue at a time until the route is clear.

Wayfinder plans by default. It does not implement the destination, create an implementation PRD, or split implementation slices until its map is clear.

## Locate or create a map

Resolve the feature map in this order:

1. If the user, handoff, PRD, or issue supplies an explicit `MAP.md` path, use it when it exists. If an explicit `MAP.md` path does not exist, stop and report that path. Do not infer a replacement.
2. Otherwise, if the user supplies an explicit PRD or issue path, use `MAP.md` from that feature directory when it exists. If it does not exist, treat this as zero matches for that feature; do not search a different feature.
3. Otherwise, search `.codex/agents/work/*/MAP.md` by exact feature slug or Destination. If there is exactly one match, use it.
4. If there are multiple matches, stop and ask the user to supply the exact `MAP.md` path.
5. If no explicit `MAP.md` path was supplied and there are zero matches, evaluate the new-map entry gate below.

If a matching map exists, enter resume/work mode. Do not apply the new-map entry gate or create a second map.

Create a new map only when all of these are true:

- the work is likely to span more than one agent session;
- a destination can be stated, but the route is not yet clear;
- an unresolved decision or investigation could change scope, architecture, major risk, or acceptance;
- entering `to-prd` or `implement` now would force a material guess.

Bypass Wayfinder for a clear bounded request, a small documentation or metadata change, an already approved PRD or issue, a known bug path, or work that merely looks long but has no decision fog. Use `grill-with-docs`, `to-prd`, `to-issues`, or `implement` directly.

Before writing anything, read the relevant `CONTEXT.md`, ADRs, existing local artifacts, and any existing map.

The local issue workspace should have been provided to you in `.codex/agents/`. If missing, recommend that the user explicitly run `/setup-agent-skills`, then stop this skill.

## Local artifacts

New maps use one feature directory:

    .codex/agents/work/<feature-slug>/
    +-- MAP.md
    +-- decisions/
        +-- 01-<decision>.md
        +-- 02-<decision>.md

Implementation issues, when later published by `to-issues`, remain under the sibling `issues/` directory. Do not mix decision files and implementation files in one new map.

`MAP.md` contains only:

- Destination: what reaching the end of the map means;
- Notes: domain language, skills, and standing constraints;
- Decisions so far: one-line gists with relative links to resolved decision issues;
- Not yet specified: in-scope uncertainty that is not sharp enough to make an issue;
- Out of scope: work explicitly ruled out.

Each decision issue contains:

- `Wayfinder type`: `research`, `prototype`, `grilling`, or `task`;
- `Wayfinder status`: `open`, `claimed`, `resolved`, or `out-of-scope`;
- `Claimed by` and `Claimed at` when work is claimed;
- `Blocked by` with paths relative to the feature directory, never bare numeric identifiers;
- a `Question` heading;
- an `Answer` heading after resolution.

Keep the existing triage `Status` field separate. Add it only when the user deliberately hands a decision issue to triage. Do not add another tracker or triage state family, and do not change the meaning of `ready-for-agent`.

If an existing map still uses the legacy decision path `issues/`, keep that map internally consistent and readable until the user reruns `setup-agent-skills`. Do not migrate files during Wayfinder, and do not create a mixed legacy/modern map.

## Chart the map

1. Establish the destination from the user's goal, acceptance boundary, non-goals, and known constraints.
2. Explore breadth-first. Find decisions that can change the destination, scope, architecture, major risk, or acceptance. Do not solve every branch before creating the map.
3. If the route is already clear, stop without creating a map and recommend the smallest next workflow.
4. Keep only questions sharp enough to state now as decision issues. Put foreseeable but unclear questions in `Not yet specified`; do not pre-slice the fog.
5. Show the proposed destination, first decision issues, dependencies, risk, and expected evidence. Write `MAP.md` and decision issues only after the user approves that scope.
6. Create only the issues currently sharp. Record blockers with feature-root-relative `decisions/` or `issues/` paths and stop charting. A decision target requires `Wayfinder status: resolved`; an implementation target requires `Completion: done`. A legacy decision still under `issues/` uses its Wayfinder status until setup migration succeeds. Do not resolve issues, implement the destination, or dispatch a batch of research work during charting.

## Work through the map

1. Load `MAP.md`, then read only the selected decision issue and the linked context needed for it.
2. Choose the user-named issue, or the first open, unblocked, unclaimed decision issue in numeric filename order.
3. Before working, re-read the issue. If it is claimed by another owner, report `Claimed by` and `Claimed at` and wait for explicit user approval before taking it over. A legacy claim without `Claimed at` has unknown age and is not automatically stale.
4. Claim it by writing:

   ```text
   Wayfinder status: claimed
   Claimed by: <runtime or session label>
   Claimed at: <ISO-8601 timestamp>
   ```

5. Select one smallest applicable workflow. Invoke internally only model-invoked skills:
   - `grilling`, `domain-modeling`, `codebase-design`, or `diagnosing-bugs` for a decision that fits;
   - an approved research capability only when its frontmatter permits model invocation.

   Recommend these user-invoked workflows to the user and stop this decision session: `grill-with-docs`, `prototype`, `zoom-out`, `to-prd`, `to-issues`, or `implement`. Do not trigger them from Wayfinder.
6. Keep the work limited to the question. Use existing commands and artifacts first. Put temporary experiments and research artifacts under the system temporary directory, or an isolated copy/worktree inside it, not in the repository. A prototype's co-location rule applies inside that isolated copy. Modifying the current worktree requires explicit user approval with risk, cleanup, and stop conditions.
7. Record the answer, relevant non-sensitive evidence, unresolved uncertainty, and any newly sharp question. Set the issue to `resolved` or `out-of-scope`, then update `Decisions so far` or `Out of scope` in the map.
8. A decision marked `out-of-scope` does not automatically unblock a dependent issue. Re-scope the dependent, rewrite its blocker, or close it through its own terminal state and record the required `Dependency resolution` section.
9. Before every write, re-read the issue and stop if its owner or status changed. On a planned handoff, return a claimed issue to `open` and record the progress in the handoff.
10. Stop after one decision issue in the session. Recommend the next frontier issue or the next workflow; do not automatically chain user-invoked skills, migrate files, or dispatch parallel subagents.

Research work requires an explicit user-approved question and scope. Use an existing specialized research capability only when it matches the subject. Keep one research issue in progress at a time and return its evidence before creating another.

## Exit to delivery

The map is clear only when:

- every created decision issue is `resolved` or `out-of-scope`;
- no dependent remains blocked by an out-of-scope decision;
- the destination, scope, non-goals, major risks, and acceptance boundary are stable;
- the map contains decisions and pointers, not implementation detail;
- the next delivery workflow is explicit.

Recommend exactly one handoff:

- `to-prd` when a formal specification still needs to be synthesized;
- `to-issues` when the approved plan needs independently verifiable implementation slices;
- `implement` when the destination is already bounded and approved;
- `real-path-verification` only later, when implementation acceptance requires real or production-equivalent execution.

Wayfinder may identify the next skill, but it does not invoke the next phase automatically.

## Boundaries

- Keep all artifacts in the local `.codex/agents/` workspace.
- Use the existing local fields and file relationships; do not add another tracker, label family, dependency system, or vendor-specific setup command.
- Do not create tests, harnesses, CLIs, production changes, commits, or unrelated issues as part of charting.
- A task issue may perform an explicitly authorized prerequisite, but it is not permission to deliver the destination.
- Preserve project rules, user-approved scope, and the safety gates of any workflow used to resolve a decision.
