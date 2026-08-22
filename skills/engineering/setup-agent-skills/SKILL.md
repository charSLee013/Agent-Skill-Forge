---
name: setup-agent-skills
description: Configure this repo for engineering skills that require a local `.codex/agents/` workspace, triage label vocabulary, or domain doc layout.
disable-model-invocation: true
---

# Setup Agent Skills

Scaffold the per-repo configuration required by engineering skills with hard local-workspace dependencies:

- **Issue tracker** — a local markdown workspace under `.codex/agents/`
- **Triage labels** — the strings used for the five canonical triage roles
- **Domain docs** — where `CONTEXT.md` and ADRs live, and the consumer rules for reading them

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Artifact ownership

Root `AGENTS.md` is the repository operating contract and navigation map. It may contain durable repository-wide instructions for how agents work, validation commands, directory and ownership maps, and pointers to canonical documentation. A rule belongs there only when it governs agent operation across unrelated work; applying broadly to the product is not enough.

Never put product behavior, feature scope or non-goals, acceptance criteria or evidence, implementation decisions, issue status, progress, or conclusions from the current session in `AGENTS.md`. Route them to their owning artifact:

- domain terms go to `CONTEXT.md`;
- hard-to-reverse architectural decisions with a real trade-off go to an ADR;
- destinations and unresolved feature decisions go to `MAP.md` and decision issues;
- product capabilities, scope, non-goals, and acceptance criteria go to `PRD.md`;
- implementation slices, failure handling, and completion state go to implementation issues.

`AGENTS.md` may point to those artifacts but must not duplicate their contents. Setup configures the Agent workspace; it does not promote the current task into repository instructions.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- Root `AGENTS.md` and its existing `## Agent skills` section. Outside that managed section, identify only lines that clearly name a feature or work item and prescribe product behavior, scope, acceptance, or progress. Treat uncertain cases as valid user content, not contamination.
- Root `CLAUDE.md`, plus every nested `AGENTS.md`, `AGENTS.override.md`, and `CLAUDE.md` that the write phase will remove
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- Workspace and package boundaries such as `pnpm-workspace.yaml`, package-manager workspace declarations, and independently rooted source trees; distinguish a real multi-context structure from a monorepo marker alone
- `.codex/agents/` — does this skill's prior output already exist, which triage label mapping and `Status:` values are already in use, and are there legacy Wayfinder decision files under `work/*/issues/`?
- `.git/info/exclude` — does it already exclude `.codex/`?

### 2. Present findings and ask

Summarise what's present and what's missing. Derive reversible defaults from the repository before asking. Ask about a section only when the evidence shows a conflict, an existing custom triage vocabulary, or a real multi-context structure. If both sections are unambiguous, proceed to the complete setup draft without a preliminary question.

If root `AGENTS.md` contains clear work-item content outside the managed section, report each candidate with its exact line and correct owning artifact. Do not edit, delete, relocate, or ask to migrate it during setup.

When a question is required, ask one section at a time. Start with a short explainer: what it is, why these skills need it, and what changes if they choose differently. Do not ask the user to confirm a reversible default that the final draft will already expose for calibration.

**Section A — Triage label vocabulary.**

> Explainer: These skills store decision maps, decision issues, PRDs, implementation issues, and triage notes as local markdown files under `.codex/agents/`. Wayfinder decisions live under `decisions/`; implementation issues live under `issues/`. When the `triage` skill processes an implementation issue, it moves it through a small state machine — needs evaluation, waiting on the reporter, ready for an AFK agent to pick up, ready for a human, or won't fix. The labels are just strings written into local files, so there is no remote label setup.

The five canonical roles:

- `needs-triage` — maintainer needs to evaluate
- `needs-info` — waiting on reporter
- `ready-for-agent` — fully specified, AFK-ready (an agent can pick it up with no human context)
- `ready-for-human` — needs human implementation
- `wontfix` — will not be actioned

Default: each role's string equals its name. If there is no existing triage vocabulary, use these defaults without asking. Preserve an unambiguous mapping from prior setup output. If consistent custom `Status:` values exist, show the proposed role mapping and ask the user to calibrate it; if custom values conflict or cannot be mapped to one role each, ask only about the unresolved mappings.

**Section B — Domain docs.**

> Explainer: Some skills (`improve-codebase-architecture`, `diagnosing-bugs`) read a `CONTEXT.md` file to learn the project's domain language, and `docs/adr/` for past architectural decisions. They need to know whether the repo has one global context or multiple (e.g. a monorepo with separate frontend/backend contexts) so they look in the right place.

Choose the layout:

- **Single-context** — one `CONTEXT.md` + `docs/adr/` at the repo root. Most repos are this.
- **Multi-context** — `CONTEXT-MAP.md` at the root pointing to per-context `CONTEXT.md` files (typically a monorepo).

Preserve an unambiguous layout from prior setup output. Without a real multi-context signal, default to single-context without asking; a workspace or monorepo marker by itself is not enough. Ask only when existing docs conflict or when separately bounded contexts genuinely need their own domain language and ADR roots. In that case, show the detected context roots and proposed `CONTEXT-MAP.md` mapping for calibration.

If the existing workspace contains legacy Wayfinder decision files under `work/*/issues/`, show the affected paths and explain that setup will normalize every unambiguous feature into `decisions/` during the confirmed write phase. Legacy migration is automatic after the user approves the setup draft; do not ask a separate migration question. A conflicting feature stays unchanged and is reported.

### 3. Confirm and edit

Always show the user a complete draft for final calibration, including defaults that did not require a preliminary question:

- The complete `## Agent skills` block to add to or update in root `AGENTS.md`
- The complete replacement of root `CLAUDE.md` with the one-line `@AGENTS.md` adapter
- Every parallel or nested Agent instruction file that will be removed; their contents are not migrated or merged
- The contents of `.codex/agents/issue-tracker.md`, `.codex/agents/triage-labels.md`, `.codex/agents/domain.md`
- Any legacy decision files that will be moved from `issues/` to `decisions/`, including exact path-reference updates and any conflicts that will leave a feature unchanged
- The `.git/info/exclude` entry that keeps `.codex/` out of git

The `AGENTS.md` portion of the draft is exactly the managed `## Agent skills` block. Do not propose, append, or ask approval for product requirements, feature constraints, or current-task decisions in root `AGENTS.md`.

Include an automatic legacy migration dry-run summary in the setup draft. The summary is part of the normal draft approval, not a separate decision.

Let them edit before writing.

### 4. Write

**Use one instruction source. The write phase always produces this shape:**

- Edit or create root `AGENTS.md` as the only repository Agent instruction body. When the file exists, change only its managed `## Agent skills` block; when it does not exist, create it with only that block.
- Replace root `CLAUDE.md` completely so its only line is `@AGENTS.md`.
- Remove every nested `AGENTS.md`, `AGENTS.override.md`, and `CLAUDE.md` in the repository. Do not read their content into root `AGENTS.md`, preserve it elsewhere, or offer a compatibility path.
- Do not create fallback instruction filenames or make root `AGENTS.md` import `CLAUDE.md`.
- Write root `AGENTS.md` before root `CLAUDE.md`, then remove the parallel instruction files shown in the approved draft.

Update an existing `## Agent skills` block in root `AGENTS.md` in place rather than appending a duplicate. Preserve user edits outside that managed block, including any reported work-item content. Never append current feature constraints elsewhere in the file. Re-running setup with the same choices must produce no changes.

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

After the draft is approved, migrate each affected feature independently:

1. Treat only files with both top-level `Wayfinder type:` and `Wayfinder status:` fields as legacy decisions. Preflight every source, destination, and inbound reference in the feature before moving anything. If a destination exists or any reference is ambiguous, leave that feature unchanged, report the conflict, and continue with other features.
2. Before changing a feature, copy its entire directory to a unique system temporary directory as a rollback snapshot. If the snapshot cannot be created and verified, do not modify the feature.
3. Move each legacy decision to `decisions/` with the same basename and content. Preserve any triage `Status` field. Do not migrate ordinary implementation issues.
4. Scan every Markdown file under the feature directory and rewrite only exact local path references. Replace `issues/<basename>` with `decisions/<basename>` for moved files; convert a bare numeric blocker only when it resolves uniquely.
5. Verify that every destination exists, every source is gone, all rewritten references resolve from the feature directory, and no stale exact reference remains. If any move, rewrite, or verification fails, restore the feature from its snapshot and report the failure.
6. Remove the temporary snapshot after successful verification. A failed or conflicting feature remains entirely in its legacy layout; never leave a mixed or partially migrated feature.

Create `.codex/agents/work/` if it does not exist. Add `.codex/` to `.git/info/exclude` if it is not already excluded. Do not edit the repo's `.gitignore` for this private workspace.

### 5. Done

Tell the user the setup is complete, which engineering skills will now read from these files, and whether any legacy decision files were migrated. Mention they can edit `.codex/agents/*.md` directly later — re-running this skill is also the supported way to normalize a legacy Wayfinder workspace.
