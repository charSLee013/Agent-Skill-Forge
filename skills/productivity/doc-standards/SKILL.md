---
name: doc-standards
description: Audit whether repository documentation has the right owner, placement, detail, and current-code agreement without turning a documentation review into an automatic rewrite.
argument-hint: "Which documentation scope should be audited?"
license: MIT
disable-model-invocation: true
---

# Documentation standards

Audit a stated documentation scope against the repository's current code,
configuration, workflows, and durable records. This is a documentation-system
review, not a general prose polish pass and not an implementation phase.

This adaptation preserves the documentation-audit core of
[`dsh-doc-standards`](https://github.com/deepseek-ai/deepseek-harness/blob/b150a551b8d465e31e418e1b2eaf5e79bbb7d28e/.agents/skills/dsh-doc-standards/SKILL.md)
while using this repository's `AGENTS.md`, `CONTEXT.md`, ADRs, README files,
and `.codex/agents/` workspace. It is guidance, not a script.

## Boundary

- Require an explicit scope. If none is provided, report the required input and
  stop; do not silently audit the whole repository.
- Read `AGENTS.md`, relevant `CONTEXT.md`, ADRs, README files, and the owning
  code or configuration before judging a claim. Missing context lowers
  confidence; it does not justify inventing a replacement record.
- Default to a read-only audit. Edit only when the user explicitly requests a
  fix, and update the canonical owner before any generated or derivative copy.
- Never write product behavior, acceptance criteria, issue status, or session
  conclusions into `AGENTS.md`. Do not create a parallel notes tree, tracker,
  archive, registry, or state machine.
- Do not treat word count, duplicated language, or a stale-looking sentence as
  proof of a defect. Trace the claim to a real consumer, owner, or current
  execution path first.

For a requested record-retention audit, adapt the future-value judgment of
DeepSeek Harness's `dsh-archive-agent-notes` at
`deepseek-ai/deepseek-harness@22ddee3792402c3e70ec5f86a63c3e3e895a2f60`.
Use this project's ADRs and local decision files; do not introduce an Agent
Notes tree, bilingual sidecars, archived-note manifests, or hash seals.

## Audit the document system

### 1. Establish the document's job

Classify each document by its intended use, not only its path or title:

- a tutorial leads a reader through ordered work to an observable outcome;
- a reference supports lookup within a defined scope;
- a README explains how a consumer configures and uses a surface;
- an ADR owns rationale, alternatives, consequences, and durable evidence;
- an issue or PRD owns execution scope and acceptance, not current-state
  reference prose;
- a generated catalog or projection is derivative of an identified source.

State the audience, direct children, permitted detail, and canonical owner. Keep
one explanation in one home; repeat a short local contract only when the
consumer needs it at the point of use.

### 2. Compare documentation with shipped reality

For behavior claims, read `implement`'s `references/evidence.md`, resolving the
skill through host-discovered paths or the repository plugin manifest. This
reference supports the audit and does not authorize code changes.

For every material claim, inspect the narrowest evidence that can prove it:

- production callers and entry paths;
- configuration, registries, schemas, dynamic strings, and serialized forms;
- scripts used by install, validation, or release workflows;
- tests and examples, distinguishing test-only consumers from production use;
- ADRs and domain records that intentionally protect an unusual structure;
- generated output and the generator or source metadata that owns it.

Classify the result as current behavior, observed fact, derived explanation,
historical record, planned work, or unresolved claim. Do not call a document
stale merely because it differs from another document; determine which source
has authority and whether the difference is intentional.
For a user-visible breaking interface change, check the consuming project's
existing upgrade guidance or owning README for the necessary migration facts.
Do not create a versioned documentation tree solely to imitate another repo.

### 3. Find drift and duplication

Look for:

- a documented entry point that no longer exists or is not reachable;
- a route, command, configuration field, or failure mode missing from the
  owning document;
- the same fact hand-maintained in multiple READMEs, registries, route maps,
  or language counterparts;
- generated catalogs, snapshots, or website projections edited instead of
  their source;
- links, fragments, examples, or navigation entries that cannot resolve from
  the current tree;
- tutorial detail that belongs in a descendant reference, or reference detail
  that makes the parent impossible to scan.

For each finding, name the evidence, the canonical owner, the conflicting or
duplicate surface, the user-visible consequence, and the smallest correction.
Separate a real contradiction from an intentional translation, audience, or
historical-record difference.

### 4. Govern existing decision records when requested

Only when the user names a record scope or requests its maintenance, inspect
the full ADRs, Wayfinder decisions, and related records in that scope. For each
one, identify its original decision, current code or rule owner, any successor,
incoming links and dependents, and whether its rationale still helps a future
decision. Classify it as active; superseded but useful history; redundant and
fully absorbed elsewhere; or unresolved. Age and length are not retention
criteria. A rejected alternative remains useful when it prevents a plausible
repeat mistake; a proposed decision is not archived merely because it is old.

In audit mode, report candidates without changing files. When record cleanup
is expressly authorized, keep a useful historical reason and link it to its
actual successor. Use the existing ADR `superseded by ADR-NNNN` status only
when that successor exists; do not rewrite history as if the new decision were
the old one. Consolidate or delete only after preserving every unique fact and
repairing inbound links and feature-local `Blocked by` paths. Do not remove a
private local decision file whose history cannot be recovered merely to tidy
the workspace. Move to an archive only when the consuming repository already
has a clear archive convention and the user authorized that move; otherwise
retain the record in place. A missing or ambiguous successor or dependent
prevents the destructive change, not the rest of the authorized audit.

### 5. Choose the smallest next action

Classify each finding as `keep`, `add`, `trim`, `restore`, `restructure`, or
`defer`. If a generated surface is wrong, fix its owner first and regenerate
only through the repository's existing command. If the claim changes product
behavior, stop the documentation pass and return it to the owning workflow.

Keep an audit read-only. When the user also requests corrections, continue
bounded authorized work through the appropriate model-invoked skill. Manual
skills remain recommendations unless the user chooses them:

- missing or misplaced technical contract -> recommend `$prose-standard`;
- authoring-session, PR, review, or draft residue -> recommend
  `$trim-cot-leakage`;
- established domain terms or a new qualifying decision -> use
  `domain-modeling` only when this maintenance is already authorized;
- repeated mechanism with uncertain net deletion -> recommend
  `$find-simplifications`;
- unresolved documentation ownership or product scope -> use `grilling` when
  clarification is needed for the current task;
- approved bounded correction -> continue with `implement` when requested.

## Report shape

Return a compact audit with:

1. **Scope and sources** — files, code paths, records, and checks actually
   inspected.
2. **Reality findings** — each claim, its evidence, current owner, and status.
3. **Drift or duplication candidates** — consequence, smallest correction,
   confidence, and recommended next workflow.
4. **Deliberate keeps** — differences that are intentional or protected by an
   ADR, audience, language, or generated-source boundary.
5. **Deferred questions and validation gaps** — only unresolved items that
   block a safe conclusion.

Do not create an audit document unless the user explicitly asks for one. When a
write is authorized, report the owner changed, derivative surfaces updated,
and the exact validation commands that ran.

## Validation

Use checks already provided by the repository. At minimum run `git diff --check`
for an authorized edit; run the relevant registry, link, build, or generated
artifact check only when that command exists and covers the touched surface.
Never claim that a check ran when it was only inferred from a static search.
