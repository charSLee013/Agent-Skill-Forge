# Local Issue Workspace: Codex Agents

Decision maps, decision issues, PRDs, implementation issues, and triage notes for this repo live as local markdown files under `.codex/agents/`.

## Conventions

- One feature per directory: `.codex/agents/work/<feature-slug>/`
- The map is `.codex/agents/work/<feature-slug>/MAP.md`
- The PRD is `.codex/agents/work/<feature-slug>/PRD.md`
- New Wayfinder decision issues are `.codex/agents/work/<feature-slug>/decisions/<NN>-<slug>.md`, numbered from `01`
- Implementation issues are `.codex/agents/work/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- Triage state is recorded as a `Status:` line near the top of implementation issues (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading
- `.codex/` is private local agent state. Keep it out of git with `.git/info/exclude`.

## Publishing and fetching

When a skill says "publish to the local issue workspace", create a file under `.codex/agents/work/<feature-slug>/` and create the feature directory if needed.

When a skill says "fetch the relevant issue", read the exact local path supplied by the user or linked by the MAP. Do not infer a different feature or silently choose between multiple matches.

## Wayfinding operations

Wayfinding is a user-invoked decision-map phase for work that spans sessions and still has material decisions open. It uses the same local workspace; it does not add another tracker.

### Modern layout

- Map: `.codex/agents/work/<feature-slug>/MAP.md`
- Decision issues: `.codex/agents/work/<feature-slug>/decisions/<NN>-<slug>.md`
- Implementation issues: `.codex/agents/work/<feature-slug>/issues/<NN>-<slug>.md`
- Map sections: `Destination`, `Notes`, `Decisions so far`, `Not yet specified`, and `Out of scope`

### Decision fields and status

Each decision issue has:

- `Wayfinder type`: `research`, `prototype`, `grilling`, or `task`
- `Wayfinder status`: `open`, `claimed`, `resolved`, or `out-of-scope`
- `Claimed by` and `Claimed at` when the issue is claimed
- `Blocked by` with relative paths when applicable
- `Question`, followed by `Answer` after resolution

Wayfinder status belongs to decision issues. Triage `Status` belongs to triage-managed implementation issues. If a decision issue is deliberately handed to triage, its Wayfinder fields remain authoritative for decision progress and its additional `Status` must not reinterpret them.

### References and blocking

Use relative paths, never bare numeric identifiers, in `Blocked by`:

```text
Blocked by: decisions/01-data-shape.md
Blocked by: issues/01-build-api.md
```

A decision is unblocked only when every referenced decision has `Wayfinder status: resolved`. `out-of-scope` is terminal for that decision but does not automatically unblock a dependent decision. The dependent must be explicitly re-scoped, have its dependency rewritten, or be marked out-of-scope.

When an out-of-scope blocker affects a dependent decision, record the consequence in the dependent issue:

````markdown
## Dependency resolution

- Blocker: decisions/01-storage-shape.md
- Blocker outcome: out-of-scope
- Effect: re-scoped | no longer required | out-of-scope
- Reason: ...
````

`Effect: out-of-scope` closes the dependent decision. `Effect: re-scoped` and `Effect: no longer required` require a new Question before the issue returns to `open`.

The frontier is the first open, unblocked, unclaimed decision issue by numeric filename order within the map's layout. Claim it before doing work.

The map is clear only when every created decision is `resolved` or `out-of-scope`, no unresolved dependent remains, the destination and acceptance boundary are stable, and the next delivery workflow is explicit.

### Claim and recovery

Claim by writing:

```text
Wayfinder status: claimed
Claimed by: <runtime or session label>
Claimed at: <ISO-8601 timestamp>
```

Claims are advisory coordination, not a hard file lock. If another owner is present, report the owner and timestamp and do not overwrite it. A takeover requires explicit user approval; record the new owner and timestamp and preserve the old owner in comments. Release a claim by returning the issue to `open` before a planned handoff. Re-read the file immediately before writing and stop if its owner or status changed.

If a legacy claimed issue has no `Claimed at`, treat its age as unknown, not as stale. Do not infer that it is safe to take over without explicit user approval.

### Legacy layout

Before setup migration, an existing MAP that links decision issues under `issues/` remains readable as a legacy map. Keep all new decision files for that map in its existing layout until migration; do not mix `issues/` and `decisions/` within one map. New maps always use `decisions/`.

Legacy decision issues are identified only when they contain both top-level `Wayfinder type:` and `Wayfinder status:` fields. An implementation issue with the same numeric prefix is not a legacy decision issue.

## Setup migration

`setup-agent-skills` is the only automatic migration entry point. It discovers legacy decision files during exploration, presents the affected paths, and moves them only after the user confirms the setup write phase.

Migration must:

1. Preflight every legacy decision in a feature directory.
2. Move it to `decisions/` with the same basename, preserving its content and existing `Status` if present.
3. Update exact paths in `MAP.md`, decision issues, and implementation issues in that feature directory.
4. Convert a bare numeric blocker only when it resolves uniquely; otherwise stop that feature's migration without partial changes.
5. Refuse to overwrite an existing destination or proceed through an ambiguous reference.
6. Verify that new paths exist, old paths are gone, and all updated local references resolve.

No other skill silently moves files. `wayfinder`, `to-prd`, `to-issues`, and `handoff` remain read-compatible with a legacy MAP and report that setup migration is available when normalization is needed.

## Triage boundary

By default, triage scans implementation issue files under `issues/`. It excludes `MAP.md`, `PRD.md`, modern `decisions/`, and legacy files carrying Wayfinder fields. A decision issue is triageable only when the user explicitly supplies its path.

Do not add another tracker, label family, vendor-specific setup command, or independent triage state system. Preserve the existing `.codex/agents/` workspace and the meaning of `ready-for-agent`.
