# Agent Skill Forge Maintenance Guide

This is a neutral personal `Agent-Skill-Forge` repository. It is not an upstream mirror.

This file is the repository's only Agent instruction source. Do not create parallel or nested instruction files.

## Structure

Skills are organized into three shipped buckets under `skills/`:

- `engineering/` - code work, planning, local issue workflow, architecture, implementation, debugging, and testing.
- `productivity/` - non-code planning, grilling, handoff, course building, and skill-writing guidance.
- `research/` - research retrieval and document-building workflows.

Every shipped skill must have:

- a `SKILL.md`
- an `agents/openai.yaml`
- an entry in the matching bucket `README.md`
- an entry in the top-level `README.md`
- an entry in `.claude-plugin/plugin.json`

Each skill entry in a README must link the skill name to its `SKILL.md`.

## Invocation

Every `SKILL.md` is either:

- user-invoked: `disable-model-invocation: true` plus `policy.allow_implicit_invocation: false` in `agents/openai.yaml`, reachable only when the human asks for it
- model-invoked: both invocation restrictions omitted, model- or user-reachable through its description

Skill discovery and task authorization are separate. A workflow may continue
already authorized work through model-invoked skills; changing phases does not
by itself require another user command. For definitions and reference lookup,
see [docs/invocation.md](./docs/invocation.md).

## Local Workspaces

Engineering skills create only requested PRDs, issues, decision maps, and triage
notes under a private repo-local `.codex/agents/` workspace. Existing local
configuration takes precedence over shipped defaults. `/setup-agent-skills` is
optional for explicit customization and legacy migration.

This repository itself should not keep long-horizon run artifacts, release-process artifacts, or upstream git history.

## Validation

For skill instructions and documentation, read the complete changed passages
and their relevant references. Check meaning, factual accuracy, contradictions,
authorization boundaries, and whether the instructions serve the requested
outcome. Walk through relevant examples and counterexamples. File presence,
keyword matches, and installer success do not establish writing quality.

When adding, removing, or renaming a skill, inspect its metadata, references,
README entries, and plugin registration directly for consistency.

Run `bash scripts/test-install-shape.sh` when core installation behavior changes.
Run `bash scripts/test-ctf-bundle-install.sh` when bundle installation changes or
a core installer change affects that path. Text-only edits do not require these
tests. Use `git diff --check` for whitespace errors, not semantic validation.
