---
name: wayfinder
description: Maintain a decision map when authorized planning spans sessions and important choices remain unresolved, or resume an existing map. Use for cross-session decision work, not a clear task that merely takes a long time.
argument-hint: "What destination should be mapped?"
---

# Wayfinder

Use a local decision map to preserve unresolved questions and established
decisions across sessions. Work on one decision issue at a time, continuing
through authorized questions while their dependencies permit it.

Read `grilling`'s `references/communication.md` for replies and
`setup-agent-skills`'s `issue-tracker-local.md` for workspace defaults. Locate
these skills through host-discovered paths, or the repository plugin manifest
when working from source. Reading references does not invoke their workflows.

Wayfinder plans by default. Once the relevant decisions are resolved, continue
into delivery only when that work is included in the user's request.

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

Bypass Wayfinder for a clear request, an already approved PRD or issue, a known
bug path, or work that merely takes a long time. Use `grilling`, `to-prd`,
`to-issues`, or `implement` only as the requested outcome needs them.

Before writing anything, read the relevant `CONTEXT.md`, ADRs, existing local artifacts, and any existing map.

Read existing local workspace configuration when present. Otherwise use the
shipped defaults and create only the authorized map, decision files, and their
directories. Missing setup does not block planning.

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
- Decisions so far: one-line gists that show each resolved decision's title and feature-root-relative path;
- Not yet specified: in-scope uncertainty that is not sharp enough to make an issue;
- Out of scope: work explicitly ruled out.

Each decision issue contains:

- a first-level heading used as the decision title;
- `Wayfinder type`: `research`, `prototype`, `grilling`, or `task`;
- `Wayfinder status`: `open`, `claimed`, `resolved`, or `out-of-scope`;
- `Claimed by` and `Claimed at` when work is claimed;
- `Blocked by` with paths relative to the feature directory, never bare numeric identifiers;
- a `Question` heading;
- an `Answer` heading after resolution.

Whenever Wayfinder shows a decision issue to the user, format it as `<decision title> (<feature-root-relative path>)`. The path remains the stable identity in `Blocked by`, map links, handoffs, and file operations; the title is display text and may change. Duplicate titles are disambiguated by their paths. For a legacy issue without a first-level heading, derive display text from its filename without rewriting the file. Never replace the relative path with a tracker ID.

Keep the existing triage `Status` field separate. Add it only when the user deliberately hands a decision issue to triage. Do not add another tracker or triage state family, and do not change the meaning of `ready-for-agent`.

If an existing map still uses the legacy decision path `issues/`, keep that map internally consistent and readable until the user reruns `setup-agent-skills`. Do not migrate files during Wayfinder, and do not create a mixed legacy/modern map.

## Chart the map

1. Establish the destination from the user's goal, acceptance boundary, non-goals, and known constraints.
2. Explore breadth-first. Find decisions that can change the destination, scope, architecture, major risk, or acceptance. Do not solve every branch before creating the map.
3. If the route is already clear, create no map and continue the smallest workflow already authorized by the request, or deliver the requested planning conclusion.
4. Keep only questions sharp enough to state now as decision issues. Put foreseeable but unclear questions in `Not yet specified`; do not pre-slice the fog.
5. Establish the destination, initial questions, dependencies, risks, and useful evidence from the request. Ask when a material scope choice remains or the user requested review first. Otherwise create the authorized map without a separate approval round.
6. Create only the issues currently sharp. Record feature-root-relative blockers. A decision requires `Wayfinder status: resolved`; an implementation requires `Completion: done`. Legacy decisions still use Wayfinder status. If the request includes resolving questions, proceed into the work loop; a request only to produce a map ends with that map.

## Work through the map

1. Load `MAP.md`, then read only the selected decision issue and the linked context needed for it.
2. Choose the user-named issue, or the first open, unblocked, unclaimed decision issue in numeric filename order. Show the selected issue as its title plus feature-root-relative path.
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

   Use `to-prd`, `to-issues`, or `implement` only when the relevant decisions
   are resolved and their deliverable is already authorized. `prototype` and
   `zoom-out` remain manual skills; recommend them when the user has not chosen
   them. Release a claim to `open` before a planned handoff or user wait.
6. Keep the work limited to the question. Use existing commands and artifacts first. Put temporary experiments and research artifacts under the system temporary directory, or an isolated copy/worktree inside it, not in the repository. A prototype's co-location rule applies inside that isolated copy. Experiments that modify project code or runtime state require explicit user approval with risk, cleanup, and stop conditions. This does not require another approval for the map and decision updates already requested.
7. Record the answer, relevant non-sensitive evidence, unresolved uncertainty, and any newly sharp question. Set the issue to `resolved` or `out-of-scope`, then update `Decisions so far` or `Out of scope` in the map.
8. A decision marked `out-of-scope` does not automatically unblock a dependent issue. Re-scope the dependent, rewrite its blocker, or close it through its own terminal state and record the required `Dependency resolution` section.
9. Before every write, re-read the issue and stop if its owner or status changed. On a planned handoff, return a claimed issue to `open` and record the progress in the handoff.
10. Continue to the next unblocked, unclaimed question when the request authorizes it. Stop when the requested questions are answered, a material user decision or permission is needed, or the user asked to handle only one issue. Preserve the next frontier for a later session. Do not migrate files or dispatch parallel work merely because a map exists.

Research stays within the questions and scope authorized by the request. Use an
existing specialized research capability only when it matches the subject. Keep
one research issue in progress at a time and record its evidence before proceeding.

## Exit to delivery

The map is clear only when:

- every created decision issue is `resolved` or `out-of-scope`;
- no dependent remains blocked by an out-of-scope decision;
- the destination, scope, non-goals, major risks, and acceptance boundary are stable;
- the map contains decisions and pointers, not implementation detail;
- the next delivery workflow is explicit.

Select the needed delivery step from the existing authorization:

- `to-prd` when a formal specification still needs to be synthesized;
- `to-issues` when the approved plan needs independently verifiable implementation slices;
- `implement` when the destination is already bounded and approved;
- `real-path-verification` only later, when implementation acceptance requires real or production-equivalent execution.

Continue an already authorized delivery step without requiring another command.
Otherwise deliver the planning result with the useful next recommendation.

## Boundaries

- Keep all artifacts in the local `.codex/agents/` workspace.
- Use the existing local fields and file relationships; do not add another tracker, label family, dependency system, or vendor-specific setup command.
- Do not create tests, harnesses, CLIs, production changes, commits, or unrelated issues as part of charting.
- A task issue may perform an explicitly authorized prerequisite, but it is not permission to deliver the destination.
- Preserve project rules, user-approved scope, and the safety gates of any workflow used to resolve a decision.
