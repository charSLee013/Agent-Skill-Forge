# Engineering

Engineering skills for bounded work in an existing repository.

Execution-reliability support is distributed separately from the skill index: plugin packages expose root `hooks/hooks.json`, while the standalone installer writes the same five approved hook and protocol files to `~/.agents/agent-skill-forge/`. `setup-agent-skills` installs that support into the consumer's private `.codex/agents/runtime/support/` directory; it does not add a manifest hook field or another tracker.

## User-invoked

These skills change the task phase or create a durable artifact. Use them only when the user chooses the phase.

- [grill-with-docs](./grill-with-docs/SKILL.md) — resolve an unclear plan or design while recording domain language and durable decisions.
- [triage](./triage/SKILL.md) — move incoming local issues through the triage state machine.
- [improve-codebase-architecture](./improve-codebase-architecture/SKILL.md) — inspect explicit architecture-maintenance work and present deepening opportunities.
- [setup-agent-skills](./setup-agent-skills/SKILL.md) — configure the local workspace and execution-reliability support, and write all repository Agent instructions to root `AGENTS.md`; root `CLAUDE.md` is always the one-line `@AGENTS.md` adapter.
- [wayfinder](./wayfinder/SKILL.md) — map large cross-session work whose material decisions are not yet clear.
- [to-issues](./to-issues/SKILL.md) — split an approved plan into independently verifiable issues.
- [to-prd](./to-prd/SKILL.md) — synthesize the current conversation into a PRD.
- [prototype](./prototype/SKILL.md) — build a throwaway experiment for a state, logic, or UI decision.
- [zoom-out](./zoom-out/SKILL.md) — map unfamiliar modules and callers before making a scoped change.
- [implement](./implement/SKILL.md) — execute an approved PRD or issue and close its acceptance criteria.

## Model-invoked

These skills support a selected workflow. They must not create a new phase or expand scope.

- [diagnosing-bugs](./diagnosing-bugs/SKILL.md) — investigate a hard or uncertain failure and identify its root cause.
- [real-path-verification](./real-path-verification/SKILL.md) — verify an approved real-path or production-equivalent acceptance criterion.
- [domain-modeling](./domain-modeling/SKILL.md) — sharpen domain terms when a real domain decision is being made.
- [codebase-design](./codebase-design/SKILL.md) — provide architecture vocabulary for an explicit module, interface, or seam decision.
- [resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md) — resolve an authorized merge or rebase conflict.

## Default routing

    clear bounded request        -> implement
    unclear plan or design       -> grill-with-docs
    incoming issue pool          -> triage
    hard uncertain bug           -> diagnosing-bugs
    large cross-session fog      -> wayfinder (MAP + decisions/) -> to-prd/to-issues/implement
    real-path proof selected     -> implement -> real-path-verification
    three or more slices         -> final integration -> recommend real-path-verification once
    explicit architecture work  -> improve-codebase-architecture

No engineering skill is a license to add adjacent work. The selected task, its acceptance criteria, and existing project rules remain authoritative.
