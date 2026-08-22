# Engineering

Engineering skills for bounded work in an existing repository.

## User-invoked

These skills change the task phase or create a durable artifact. Use them only when the user chooses the phase.

- [grill-with-docs](./grill-with-docs/SKILL.md) — clarifies an unclear plan in one session and records only established glossary terms or qualifying ADRs; use it before delivery when scope or acceptance is unresolved, not for cross-session mapping or instruction-file updates; it exits to `implement`, `to-prd`, `to-issues`, or `wayfinder`.
- [triage](./triage/SKILL.md) — moves an incoming issue pool through local triage; use it to select work, not to implement an approved item; it requires the configured workspace and exits through `ready-for-agent` or another terminal role.
- [improve-codebase-architecture](./improve-codebase-architecture/SKILL.md) — finds architecture deepening opportunities and presents an HTML report; use it for explicit maintenance, not direct refactoring; it requires repository context and exits to a selected `grill-with-docs` or `implement` path.
- [find-simplifications](./find-simplifications/SKILL.md) — finds evidence-backed opportunities to remove, fold, demote, or replace unnecessary complexity; use it as a read-only simplification audit, not direct refactoring or architecture decision-making; it requires a repository area or question and exits with up to five candidates and one recommended next workflow.
- [setup-agent-skills](./setup-agent-skills/SKILL.md) — configures `.codex/agents/`, triage labels, domain docs, and the root instruction shape; use it once before other engineering skills, not for feature work; it requires repository write access and exits with a ready local workspace.
- [wayfinder](./wayfinder/SKILL.md) — maps large cross-session work whose material route decisions remain open; use it only for decision fog, not a clear PRD or bounded request; it requires the configured workspace and exits to `to-prd`, `to-issues`, or `implement`.
- [to-issues](./to-issues/SKILL.md) — splits an approved plan into independently verifiable implementation issues; use it after the route is clear, not to resolve decisions; it requires a plan, spec, or PRD and exits to per-issue `implement` sessions.
- [issues-to-execution-brief](./issues-to-execution-brief/SKILL.md) — compiles selected executable issues into one decision-complete cold-start brief; use it after slicing when one fresh expert needs the approved set, not to create, modify, close, or implement issues; it requires exact issue paths or one feature directory and exits with one copy-ready brief or blocking facts.
- [to-prd](./to-prd/SKILL.md) — synthesizes a clear conversation into a PRD; use it for durable specification, not discovery or wayfinding; it requires bounded scope and acceptance evidence and exits to `to-issues` or `implement`.
- [prototype](./prototype/SKILL.md) — builds a throwaway executable experiment for a state, logic, or UI decision; use it when discussion cannot settle a concrete question, not as production delivery; it requires a question and stop condition and exits through `handoff` to the main workflow.
- [zoom-out](./zoom-out/SKILL.md) — maps unfamiliar modules and callers in domain language; use it to locate a change before implementation, not to redesign architecture; it requires readable code and exits with bounded implementation context.
- [implement](./implement/SKILL.md) — executes an approved PRD or issue and closes its acceptance criteria; use it when scope and evidence are already clear, not for discovery; it requires a concrete work item and exits with a verified completion conclusion.

## Model-invoked

These skills support a selected workflow. They must not create a new phase or expand scope.

- [evidence-first](./evidence-first/SKILL.md) — establishes a bounded contract and verifies claims at their owning evidence layer; use it when a request spans configuration, prompts, tools, permissions, or runtime behavior, not for an obvious single-layer check; it requires an observable acceptance claim and returns evidence-backed boundaries to the active workflow.
- [diagnosing-bugs](./diagnosing-bugs/SKILL.md) — isolates the root cause of a hard or uncertain failure; use it when the failure path is unknown, not for a mechanical fix; it requires an observable signal and exits with a falsifiable diagnosis for `implement`.
- [real-path-verification](./real-path-verification/SKILL.md) — checks an approved real or production-equivalent acceptance criterion; use it only when the parent criterion selects that evidence, not for routine tests; it requires an executable path and cleanup plan and returns a conclusion to `implement`.
- [domain-modeling](./domain-modeling/SKILL.md) — sharpens domain terms and records decisions; use it for a real terminology or model conflict, not passive context reading; it requires a concrete decision and exits with updated `CONTEXT.md` or ADRs.
- [codebase-design](./codebase-design/SKILL.md) — supplies vocabulary for an explicit module, interface, or architecture decision; use it for deliberate design work, not routine implementation, tests, or diagnosis; it requires a named design object and exits with executable boundaries.
- [resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md) — resolves an active merge or rebase conflict while preserving both intentions; use it only for an authorized conflict state, not proactive refactoring; it requires the conflicting inputs and exits with verified resolution.

## Default routing

    clear bounded request        -> implement
    unclear plan or design       -> grill-with-docs
    incoming issue pool          -> triage
    multi-layer support claim    -> evidence-first -> selected workflow
    hard uncertain bug           -> diagnosing-bugs
    simplification audit          -> find-simplifications -> selected workflow
    large cross-session fog      -> wayfinder (MAP + decisions/) -> to-prd/to-issues/implement
    selected executable issues   -> issues-to-execution-brief -> fresh expert
    real-path evidence selected  -> implement -> real-path-verification
    explicit architecture work  -> improve-codebase-architecture

No engineering skill is a license to add adjacent work. The selected task, its acceptance criteria, and existing project rules remain authoritative.
