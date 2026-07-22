---
name: setup-agent-skills
description: Configure this repo for the engineering skills — set up its local `.codex/agents/` workspace, execution-reliability support, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills.
disable-model-invocation: true
---

# Setup Agent Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker** — a local markdown workspace under `.codex/agents/`
- **Execution reliability** — the private runtime support and static ownership rules for checkpoints, issue finalization, and bounded delegation
- **Triage labels** — the strings used for the five canonical triage roles
- **Domain docs** — where `CONTEXT.md` and ADRs live, and the consumer rules for reading them

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- Root `AGENTS.md` and its existing `## Agent skills` section
- Root `CLAUDE.md`, plus every nested `AGENTS.md`, `AGENTS.override.md`, and `CLAUDE.md` that the write phase will remove
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `.codex/agents/` — does this skill's prior output already exist? Are there legacy Wayfinder decision files under `work/*/issues/`?
- The supported execution-reliability source: either the package root containing `.claude-plugin/plugin.json`, or the standalone installer bundle at `$HOME/.agents/agent-skill-forge/`
- `.git/info/exclude` — does it already exclude `.codex/`?

### 2. Present findings and ask

Summarise what's present and what's missing. Then walk the user through the two decisions **one at a time** — present a section, get the user's answer, then move to the next. Don't dump both at once.

Assume the user does not know what these terms mean. Each section starts with a short explainer (what it is, why these skills need it, what changes if they pick differently). Then show the choices and the default.

**Section A — Triage label vocabulary.**

> Explainer: These skills store decision maps, decision issues, PRDs, implementation issues, and triage notes as local markdown files under `.codex/agents/`. Wayfinder decisions live under `decisions/`; implementation issues live under `issues/`. When the `triage` skill processes an implementation issue, it moves it through a small state machine — needs evaluation, waiting on the reporter, ready for an AFK agent to pick up, ready for a human, or won't fix. The labels are just strings written into local files, so there is no remote label setup.

The five canonical roles:

- `needs-triage` — maintainer needs to evaluate
- `needs-info` — waiting on reporter
- `ready-for-agent` — fully specified, AFK-ready (an agent can pick it up with no human context)
- `ready-for-human` — needs human implementation
- `wontfix` — will not be actioned

Default: each role's string equals its name. Ask the user if they want to override any. If they do not already have local status names, the defaults are fine.

**Section B — Domain docs.**

> Explainer: Some skills (`improve-codebase-architecture`, `diagnosing-bugs`) read a `CONTEXT.md` file to learn the project's domain language, and `docs/adr/` for past architectural decisions. They need to know whether the repo has one global context or multiple (e.g. a monorepo with separate frontend/backend contexts) so they look in the right place.

Confirm the layout:

- **Single-context** — one `CONTEXT.md` + `docs/adr/` at the repo root. Most repos are this.
- **Multi-context** — `CONTEXT-MAP.md` at the root pointing to per-context `CONTEXT.md` files (typically a monorepo).

If the existing workspace contains legacy Wayfinder decision files under `work/*/issues/`, show the affected paths and explain that setup will normalize every unambiguous feature into `decisions/` during the confirmed write phase. Legacy migration is automatic after the user approves the setup draft; do not ask a separate migration question. A conflicting feature stays unchanged and is reported.

### 3. Confirm and edit

Show the user a draft of:

- The complete `## Agent skills` block to add to or update in root `AGENTS.md`
- The complete replacement of root `CLAUDE.md` with the one-line `@AGENTS.md` adapter
- Every parallel or nested Agent instruction file that will be removed; their contents are not migrated or merged
- The contents of `.codex/agents/issue-tracker.md`, `.codex/agents/triage-labels.md`, `.codex/agents/domain.md`
- The exact execution-reliability files that will be installed under `.codex/agents/runtime/support/`, including their resolved supported source
- Any legacy decision files that will be moved from `issues/` to `decisions/`, including exact path-reference updates and any conflicts that will leave a feature unchanged
- The `.git/info/exclude` entry that keeps `.codex/` out of git

Include an automatic legacy migration dry-run summary in the setup draft. The summary is part of the normal draft approval, not a separate decision.

Let them edit before writing.

### 4. Write

**Use one instruction source. The write phase always produces this shape:**

- Edit or create root `AGENTS.md` as the only repository Agent instruction body.
- Replace root `CLAUDE.md` completely so its only line is `@AGENTS.md`.
- Remove every nested `AGENTS.md`, `AGENTS.override.md`, and `CLAUDE.md` in the repository. Do not read their content into root `AGENTS.md`, preserve it elsewhere, or offer a compatibility path.
- Do not create fallback instruction filenames or make root `AGENTS.md` import `CLAUDE.md`.
- Write root `AGENTS.md` before root `CLAUDE.md`, then remove the parallel instruction files shown in the approved draft.

Update an existing `## Agent skills` block in root `AGENTS.md` in place rather than appending a duplicate. Preserve user edits outside that managed block. Re-running setup with the same choices must produce no changes.

The block:

```markdown
## Agent skills

### Issue tracker

Local decision maps, decision issues, PRDs, implementation issues, and triage notes live under `.codex/agents/work/`. Decision issues use `decisions/`; implementation issues use `issues/`. See `.codex/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `.codex/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout — "single-context" or "multi-context"]. See `.codex/agents/domain.md`.

### Execution reliability

Checkpoints own session continuity facts. Issues own scope, acceptance, issue-start baselines, and finalization proofs. Delegation directories own temporary request and result exchange. Keep session identifiers, task paths, findings, mistakes, issue facts, and delegation conclusions out of this static policy.

Create and maintain a checkpoint at the `SessionStart`-provided path only for non-trivial work with durable confirmed facts. The file must start with `# Checkpoint`, followed exactly once each by these `##` headings in order: `Task`, `Progress`, `Decisions`, `Mistakes and corrections`, `Binding rules`, `Verification`, and `Next action`. Update it only when confirmed facts, scope, decisions, corrections, verification evidence, or the next action changes. Ordinary reads, repeated tests, formatting, searches, and unchanged tool calls do not update it.

A direct small edit with no active issue or non-trivial session state uses an ordinary final-diff review. It does not require a checkpoint, formal issue finalization, delegation artifacts, or new process documents.

### Subagents

Use subagents only for bounded exploration, independent review, or acceptance verification. Do not delegate final scope, architecture, writes, or proof ownership.

Always set `fork_turns` explicitly; use `none` for independent exploration and review.

For non-trivial delegation, exchange detail through the fixed `REQUEST.md` and `RESULT.md` section contract in a unique assigned temporary directory. Write `RESULT.md.part` first and atomically rename it to `RESULT.md`; treat `wait_agent` as status only. The final agent message is only a completion notification. The parent must verify the result, consume its evidence, and delete the complete delegation directory.

The main agent owns the final worktree diff, scope decision, acceptance evidence, and user-facing result. Do not automatically invoke the user-level `handoff` skill or preserve unapproved legacy or fallback behavior.
```

Then write the three docs files under `.codex/agents/` using the seed templates in this skill folder as a starting point:

- [issue-tracker-local.md](./issue-tracker-local.md) — local Codex workspace
- [triage-labels.md](./triage-labels.md) — label mapping
- [domain.md](./domain.md) — domain doc consumer rules + layout

Install the execution-reliability support into `.codex/agents/runtime/support/` after `.codex/` is excluded from Git:

1. Resolve the source from the invocation mode. A plugin invocation uses its package root, which must contain `.claude-plugin/plugin.json` and every file listed below. A standalone skill invocation uses `$HOME/.agents/agent-skill-forge/`. These are the only supported sources; if the selected source is incomplete, stop and report it. Do not search for, generate, or preserve an alternate compatibility path.
2. Copy exactly these files through a unique staging directory under `.codex/agents/runtime/`:
   - `hooks/hooks.json`
   - `hooks/checkpoint.py`
   - `hooks/issue_gate.py`
   - `scripts/finalize-issue.py`
   - `scripts/delegation.py`
3. Verify that the staged tree contains exactly those regular files and that the Python entrypoints remain executable. If the installed support tree already has the same file set and bytes, leave it unchanged. Otherwise replace only `.codex/agents/runtime/support/` after validation, then remove the staging directory.
4. Do not copy tests, register hooks through an invented config file, add a `hooks` field to `.claude-plugin/plugin.json`, invoke the user-level `handoff` skill, or retain an older support path as a fallback. Plugin loading discovers the package-root `hooks/hooks.json`; standalone installation exposes the same contract through the documented bundle and private setup copy.

After the draft is approved, migrate each affected feature independently:

1. Treat only files with both top-level `Wayfinder type:` and `Wayfinder status:` fields as legacy decisions. Preflight every source, destination, and inbound reference in the feature before moving anything. If a destination exists or any reference is ambiguous, leave that feature unchanged, report the conflict, and continue with other features.
2. Before changing a feature, copy its entire directory to a unique system temporary directory as a rollback snapshot. If the snapshot cannot be created and verified, do not modify the feature.
3. Move each legacy decision to `decisions/` with the same basename and content. Preserve any triage `Status` field. Do not migrate ordinary implementation issues.
4. Scan every Markdown file under the feature directory and rewrite only exact local path references. Replace `issues/<basename>` with `decisions/<basename>` for moved files; convert a bare numeric blocker only when it resolves uniquely.
5. Verify that every destination exists, every source is gone, all rewritten references resolve from the feature directory, and no stale exact reference remains. If any move, rewrite, or verification fails, restore the feature from its snapshot and report the failure.
6. Remove the temporary snapshot after successful verification. A failed or conflicting feature remains entirely in its legacy layout; never leave a mixed or partially migrated feature.

Create `.codex/agents/work/` if it does not exist. Add `.codex/` to `.git/info/exclude` if it is not already excluded. Do not edit the repo's `.gitignore` for this private workspace.

### 5. Done

Tell the user the setup is complete, which engineering skills will now read from these files, where the private execution-reliability support was installed, and whether any legacy decision files were migrated. Mention they can edit `.codex/agents/*.md` directly later — re-running this skill is also the supported way to normalize a legacy Wayfinder workspace.
