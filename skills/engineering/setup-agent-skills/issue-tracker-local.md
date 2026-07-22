# Local Issue Workspace: Codex Agents

Decision maps, decision issues, PRDs, implementation issues, and triage notes for this repo live as local markdown files under `.codex/agents/`.

## Conventions

- One feature per directory: `.codex/agents/work/<feature-slug>/`
- The map is `.codex/agents/work/<feature-slug>/MAP.md`
- The PRD is `.codex/agents/work/<feature-slug>/PRD.md`
- New Wayfinder decision issues are `.codex/agents/work/<feature-slug>/decisions/<NN>-<slug>.md`, numbered from `01`
- Implementation issues are `.codex/agents/work/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- Triage state is recorded as a `Status:` line near the top of implementation issues (see `triage-labels.md` for the role strings)
- Implementation completion is recorded separately as `Completion: open` or `Completion: done`
- Comments and conversation history append to the bottom of the file under a `## Comments` heading
- `.codex/` is private local agent state. Keep it out of git with `.git/info/exclude`.

## Implementation baseline

A formal implementation issue starts with `Completion: open`. Before its first implementation change, run the setup-installed `Finalize Issue` entrypoint with the exact issue path and current session UUID:

```bash
python3 .codex/agents/runtime/support/scripts/finalize-issue.py begin --issue <path> --session-id <uuid>
```

The command records `## Issue-start baseline` in the issue and stores its private snapshot receipt under `.codex/agents/runtime/issue-gates/<session-id>/`. The snapshot includes the current Git HEAD, the semantic Git index entries, every tracked and non-ignored untracked worktree path, and the baseline set of ignored paths outside `.codex/`. The index must remain unchanged, and the ignored path set must return exactly to its baseline before finalization; this catches staged-only edits and newly created debug or generated files without hashing pre-existing virtual environments or caches. Do not clean or rewrite pre-existing user work before capture. A formal issue claims an atomic issue-key receipt and may not share it with another session.

The runtime receipt is temporary comparison state, not a new issue tracker or memory channel. An issue without a receipt remains `Completion: open`; a direct small change with no formal issue creates no receipt.

## Finalize Issue

`Finalize Issue` is the only approved operation that changes `Completion: open` to `Completion: done`. Its `inspect` command compares the current worktree to the issue-start snapshot and emits a stable unit for every changed file and every textual hunk. Binary, type, ownership, and mode changes still receive a file unit. A changed Git index or ignored path set fails closed before a delta can be mapped.

Before finalization, remove every unit that cannot be mapped to approved scope, acceptance, or indispensable support. Audit scratch and debug material, temporary tests, unsolicited documentation, generated noise, public interfaces, dependencies, persistence, error handling, test justification, and required acceptance. Obtain independent review when warranted. Then write this proof before invoking `finalize`:

```markdown
## Finalization proof

- Baseline: `<inspect baseline digest>`
- Final delta: `<inspect final-delta digest>`
- Scope audit: <how every remaining unit belongs>
- Interface audit: <approved interface impact or why there is none>
- Dependency and persistence audit: <approved impact or why there is none>
- Error-handling audit: <reuse and fallback result>
- Test justification: <named risk or acceptance basis for retained tests>
- Cleanup audit: <removed/rejected development-only material>
- Acceptance evidence: <post-cleanup command/path and result>
- Independent review: performed: <review evidence>
- Result: passed

### Delta mapping

- `<unit-id>` -> `scope`: <reason>
- `<unit-id>` -> `acceptance`: <criterion and reason>
- `<unit-id>` -> `support`: <why it is indispensable>
```

Use `Independent review: not required: <reason>` only when risk, breadth, and the acceptance contract do not warrant review. Every emitted unit must appear exactly once; stale or extra mappings fail. If the delta is empty, the mapping list is empty. Placeholder proof, a changed Git HEAD, worktree drift after proof, or direct editing of `Completion` cannot pass the gate.

The shared `Stop` hook consults only the current session's active receipt and verifies that the receipt still owns the issue-key claim. It allows an open issue to end a turn, blocks a done issue without a valid current proof or with index/ignored-path drift, and removes a successfully finalized receipt plus its claim. With no receipt it is a no-op, so unrelated completed issues and direct small edits are not scanned or blocked.

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
- `Blocked by` with feature-root-relative paths when applicable
- `Question`, followed by `Answer` after resolution

Wayfinder status belongs to decision issues. Triage `Status` belongs to triage-managed implementation issues. `Completion` is only the implementation dependency oracle; it does not add triage roles. If a decision issue is deliberately handed to triage, its Wayfinder fields remain authoritative for decision progress and its additional `Status` must not reinterpret them.

### References and blocking

Every `Blocked by` path is relative to `.codex/agents/work/<feature-slug>/`, regardless of which issue contains it. Allowed targets stay inside the same feature under `decisions/` or `issues/`; reject bare numeric identifiers, absolute paths, `..` traversal, missing targets, and ambiguous targets.

```text
Blocked by: decisions/01-data-shape.md
Blocked by: issues/01-build-api.md
```

A target under `decisions/` unblocks only when it has `Wayfinder status: resolved`.

A modern target under `issues/` unblocks only when it has `Completion: done`.

A legacy target under `issues/` that carries both top-level Wayfinder fields remains a decision target and uses `Wayfinder status: resolved` until migration succeeds. A legacy implementation issue without `Completion` is treated as `Completion: open`.

The target type, not the source type, selects the oracle for decision-to-decision, implementation-to-implementation, and cross-type dependencies. Triage `Status` never satisfies a blocker.

An `out-of-scope` decision or implementation carrying the configured `wontfix` role is terminal for that blocker but does not automatically unblock a dependent issue. Re-scope the dependent, remove or replace the blocker, or close the dependent explicitly.

When an out-of-scope or `wontfix` blocker affects a dependent issue, record the consequence in the dependent issue:

````markdown
## Dependency resolution

- Blocker: decisions/01-storage-shape.md
- Blocker outcome: out-of-scope | wontfix
- Effect: re-scoped | no longer required | out-of-scope
- Reason: ...
````

For a dependent decision, `Effect: out-of-scope` sets its Wayfinder status accordingly; the other effects require a revised `Question` before it returns to `open`. For a dependent implementation issue, `Effect: out-of-scope` uses the configured `wontfix` triage role; the other effects require updated `What to build` and acceptance criteria while `Completion` remains `open`.

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

`setup-agent-skills` is the only migration entry point. It discovers legacy decision files during exploration, includes a dry-run summary in the normal setup draft, and automatically migrates unambiguous features after that draft is approved. There is no separate migration question.

Migration must:

1. Preflight every legacy decision, destination, and inbound reference in a feature before changing it. A conflict leaves the whole feature untouched while other features may continue.
2. Copy the entire feature directory to a unique system temporary directory and verify the rollback snapshot before writing.
3. Move each legacy decision to `decisions/` with the same basename, preserving its content and existing `Status` if present.
4. Scan every Markdown file under the feature and update only exact local references to moved paths. Convert a bare numeric blocker only when it resolves uniquely.
5. Refuse to overwrite a destination or proceed through an ambiguous reference.
6. Verify that new paths exist, old paths are gone, and all rewritten paths resolve from the feature directory.
7. Restore the entire feature snapshot after any move, rewrite, or verification failure. Delete the snapshot only after success.

No other skill silently moves files. `wayfinder`, `to-prd`, `to-issues`, and `handoff` remain read-compatible with a legacy MAP and report that setup migration is available when normalization is needed.

## Triage boundary

By default, triage scans implementation issue files under `issues/`. It excludes `MAP.md`, `PRD.md`, modern `decisions/`, and legacy files carrying Wayfinder fields. A decision issue is triageable only when the user explicitly supplies its path.

Do not add another tracker, label family, vendor-specific setup command, or independent triage state system. Preserve the existing `.codex/agents/` workspace and the meaning of `ready-for-agent`.
