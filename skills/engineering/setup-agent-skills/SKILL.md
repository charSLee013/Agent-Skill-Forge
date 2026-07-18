---
name: setup-agent-skills
description: Configure this repo for the engineering skills — set up its local `.codex/agents/` workspace, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills.
disable-model-invocation: true
---

# Setup Agent Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker** — a local markdown workspace under `.codex/agents/`
- **Triage labels** — the strings used for the five canonical triage roles
- **Domain docs** — where `CONTEXT.md` and ADRs live, and the consumer rules for reading them

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `AGENTS.md` and `CLAUDE.md` at the repo root — does either exist? Is there already an `## Agent skills` section in either?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `.codex/agents/` — does this skill's prior output already exist? Are there legacy Wayfinder decision files under `work/*/issues/`?
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

If the existing workspace contains legacy Wayfinder decision files under `work/*/issues/`, show the affected paths and explain that setup can normalize them into `decisions/`. This migration is performed only during the confirmed write phase; it is not a hidden runtime action.

### 3. Confirm and edit

Show the user a draft of:

- The `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules)
- The contents of `.codex/agents/issue-tracker.md`, `.codex/agents/triage-labels.md`, `.codex/agents/domain.md`
- Any legacy decision files that will be moved from `issues/` to `decisions/`, including the path-reference updates that will be made
- The `.git/info/exclude` entry that keeps `.codex/` out of git

Let them edit before writing.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create — don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa) — always edit the one that's already there.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

Local decision maps, decision issues, PRDs, implementation issues, and triage notes live under `.codex/agents/work/`. Decision issues use `decisions/`; implementation issues use `issues/`. See `.codex/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `.codex/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout — "single-context" or "multi-context"]. See `.codex/agents/domain.md`.
```

Then write the three docs files under `.codex/agents/` using the seed templates in this skill folder as a starting point:

- [issue-tracker-local.md](./issue-tracker-local.md) — local Codex workspace
- [triage-labels.md](./triage-labels.md) — label mapping
- [domain.md](./domain.md) — domain doc consumer rules + layout

If the user confirmed legacy migration, preflight every affected feature before moving anything. Move only files with both top-level `Wayfinder type:` and `Wayfinder status:` fields to `decisions/`, preserve their content, update exact local references, and stop that feature without partial changes if a destination or reference is ambiguous. Verify the new paths and references after the move. Do not migrate ordinary implementation issues.

Create `.codex/agents/work/` if it does not exist. Add `.codex/` to `.git/info/exclude` if it is not already excluded. Do not edit the repo's `.gitignore` for this private workspace.

### 5. Done

Tell the user the setup is complete, which engineering skills will now read from these files, and whether any legacy decision files were migrated. Mention they can edit `.codex/agents/*.md` directly later — re-running this skill is also the supported way to normalize a legacy Wayfinder workspace.
