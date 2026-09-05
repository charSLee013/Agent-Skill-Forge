---
name: find-simplifications
description: Find evidence-backed opportunities to remove, fold, demote, or replace unnecessary codebase complexity without implementing the change.
argument-hint: "Which repository area or simplification question should be audited?"
license: MIT
disable-model-invocation: true
---

# Find codebase simplifications

Turn a broad request to "find things to simplify" into a small set of evidence-backed
candidates. Follow the code and keep judgment active. Prefer a few well-proven
candidates over a pile of thin guesses. This skill is a read-only exploration phase,
not an implementation phase.

This adaptation preserves the review discipline from
[`dsh-find-simplifications`](https://github.com/deepseek-ai/deepseek-harness/blob/b150a551b8d465e31e418e1b2eaf5e79bbb7d28e/.agents/skills/dsh-find-simplifications/SKILL.md)
while replacing its repository-specific record system and paths with the current
repository's existing workflow.

## Start with repository context

- Read `AGENTS.md` and the applicable repository instructions.
- Read `CONTEXT.md` when present for domain vocabulary.
- Read the relevant ADRs, README files, and local issue conventions before judging
  code in that area. Treat accepted ADRs and explicit compatibility constraints as
  intentional architecture unless new evidence is strong enough to reopen them.
- Read the local `.codex/agents/` conventions when present. Use existing issue and
  ADR workflows as the only durable decision path; do not create another notes tree,
  tracker, state machine, or archive mechanism.
- If one of these files is absent, continue. Absence reduces context sharpness; it is
  not a reason to invent a replacement document or stop the read-only audit.

## What counts as a strong candidate

A strong simplification removes, folds, or demotes something real and has clear
evidence that the current design costs more than it buys:

- A public method, event, config knob, registry notification, helper, package,
  durable event, or test artifact has no production consumer.
- Tests or docs are the only consumers, and the behavior they pin is not load-bearing.
- Two representations mirror the same fact, especially across durable and transient
  events, configuration and runtime state, or multiple registries.
- A seam has methods every implementation must support but no consumer uses.
- A separate package exists only for test, demo, or support code and adds publish or
  dependency overhead.
- A feature implements speculative product generality with no current product owner.
- An invariant, rollback path, expected-output set, or special-case test exists only
  to protect an unused API.
- Hand-rolled code reimplements what a well-maintained dependency or a platform
  builtin at the project's supported version already provides, and the swap would
  delete the implementation plus its dedicated tests.
- The simplified behavior may differ slightly, but the result remains reasonable,
  compatible with the approved scope, and easier to explain.

Thin candidates are not enough on their own: deleting one typo, running a dead-code
tool once, removing an intentionally documented adapter or backend, or saying "this
looks complex" without call-site proof. Do not treat code complexity as evidence by
itself.

## Survey broadly

Start with the largest relevant production-code deltas, repeated change areas, and
surfaces with duplicated lifecycle or defensive machinery. If the user names an area,
stay within that area and its direct callers. If the user asks for a broad audit,
cover the relevant domains rather than stopping after the first plausible candidate.

Use bounded read-only exploration. Do not dispatch a new subagent workflow by default;
when delegation is unavailable, perform the breadth pass yourself. Useful domains
include:

- agent loops, session logs, turn/step boundaries, abort/cancel, replay, load/resume;
- protocol, UI, prompt settlement, transcript rendering, and interaction state;
- model/tool streams, assemblers, registries, schema defaults, and presentation hooks;
- process, shell, foreground/background execution, ownership, output spill, and cleanup;
- packages, examples, scripts, tests, snapshots, generated outputs, and support code.

Do not let a static inventory, `knip` result, or the first good candidate stand in for
understanding the production path. Inspect the call sites and the loading paths.

## Audit trust and lifecycle boundaries

For every defensive copy, freeze, validator, and callback capture, name where the
value came from and who owns it next. Same-process typed calls ordinarily borrow
readonly values. Parsers, config loaders, queues, model/tool JSON, durable files,
workers, processes, and wire decoders own or validate their data. Tests built around
hostile getters, fake typed objects, callback replacement, or mutation after a
same-process handoff are evidence of a potentially speculative contract, not
automatic justification for keeping it.

For complex asynchronous code, draw the ownership graph and map every sentinel,
readiness promise, cancellation path, disposer, and state flag to a distinct owner or
transition. When several mechanisms mirror the same liveness or settlement fact,
consider whether one lifecycle controller can replace them. Preserve separate
machinery when it protects synchronous publication and rollback, callback containment,
first-terminal-outcome arbitration, worker/process ownership, or dispose-to-quiescence.

## Hand-rolled code versus a dependency

Introducing a dependency can be a valid simplification move. For protocol parsers,
framers, retry/backoff loops, glob matchers, diff engines, and similar infrastructure:

- Read the hand-rolled implementation and name the exact surface the package covers.
  Residual semantics the package does not cover count against the swap.
- Check package maintenance, adoption, transitive footprint, and supported runtime;
  prefer a platform builtin when it meets the contract.
- Read relevant ADRs and dependency policy before proposing a seam collapse or
  replacement. A recorded rationale must be answered by stronger evidence.
- Weigh net deletion: implementation plus dedicated tests and docs, minus the glue
  code and new maintenance burden. Moving complexity behind a wrapper is not a win.

## Prove or reject each candidate

Classify consumers before proposing anything:

- **Production corpus:** runtime source, loader/config paths, examples used as smoke
  paths, scripts invoked by production or release workflows, and wire formats.
- **Non-production corpus:** tests, README/docs, snapshots, generated expected
  outputs, comments, and historical notes.
- **Ambiguous corpus:** examples, scripts, dynamic registries, reflection, package
  exports, and string-based event/config references. Inspect before classifying.

Use `rg` first. Search the exact symbol, event name, package name, config key, wire
string, and method with both `.name(` and `name(` forms. Then read the callers. A
static tool can help find candidates but cannot replace understanding public
interfaces, dynamic names, loaders, tests, docs, and compatibility behavior.

Reject or downgrade a candidate when:

- a production caller exists and the change would be a feature decision rather than
  cleanup;
- an ADR, domain model, compatibility contract, or hard-won defensive pattern
  explicitly justifies the design and new evidence does not beat that reason;
- removal causes unrelated churn without reducing the public surface or required
  behavior;
- the idea is correct but too small to justify a durable simplification proposal;
- evidence is missing for dynamic, serialized, reflected, generated, or external use.

## Read existing records without creating a parallel system

Read relevant ADRs, `CONTEXT.md`, issue files, and existing local artifacts to find
the current owner of a decision. Do not create, edit, archive, consolidate, or delete
those records during this audit. Do not write a separate durable note, TODO/FIXME/XXX,
PRD, issue, code comment, commit, or generated report into the repository.

When an old record appears superseded, report that as a candidate observation only:
name the current owner, the surviving behavior or compatibility obligation, the
missing rationale, and the evidence still needed. Leave retention and migration to
the repository's existing documentation workflow.

When the user explicitly asks to reduce or coalesce repository records, or when the
selected simplification makes an owning record obsolete, audit only the directly
affected record chain. Do not turn every simplification survey into a repository-wide
record cleanup. For each chain:

1. Identify the current owner from shipped code, configuration, generated catalogs,
   package docs, newer ADRs, issue files, and inbound links. Dates and titles are
   discovery hints, not proof.
2. Classify the old record as fully or partially superseded. Surviving behavior,
   current contracts, durable formats, compatibility obligations, or an independently
   current rejected alternative make it partial.
3. For full supersession, report every unique rationale, alternative, consequence,
   shipped verification fact, and named coverage gap that the current owner would
   need to carry. A list of deleted implementation mechanics is not enough.
4. Repair or enumerate inbound links in the proposed follow-up. Do not edit or delete
   the records during this skill.
5. Search exact filenames, symbols, config keys, event names, and wire strings after
   the proposed change would be implemented. Keep partial supersessions linked and
   current.

An added-then-removed feature qualifies as full supersession only when it is absent
from production code, configuration, schemas, durable and wire formats, migration,
compatibility behavior, current documentation, and supported tests. Preserve why it
was introduced, why that motivation no longer justified it, alternatives to removal,
the capability given up, conditions for reintroduction, and evidence that removal is
complete. A current negative design decision may still need its own ADR even when the
implementation is gone.

Reject consolidation when the removal affects only one transport, default,
implementation, or presentation of a surviving feature, when persisted data or
compatibility handling remains, or when the proposed owner would not prevent
accidental reintroduction.

## Fold another PR or branch into the audit

When the user asks to import simplification ideas from another PR or branch, compare
that branch with its common base (normally `origin/master`), not with the current PR
branch. Treat each candidate as evidence to classify, not as an instruction to port.

- Keep non-overlapping candidates that meet this skill's evidence bar.
- Merge overlapping material into the existing candidate or ADR owner.
- Reject duplicate or lower-confidence proposals instead of preserving a count.
- Report which candidates were retained, merged, or excluded and why.
- Do not close PRs, rewrite branches, modify issue files, or update PR bodies here.

For every retained cross-branch candidate, include the independent diff range, the
production and non-production consumers checked, the net deletion, and the next
workflow that should own implementation.

## Return the candidate report

Return at most five candidates, ordered by evidence strength and net deletion. If no
candidate survives the evidence gate, say so and name the areas inspected. For each
candidate use this structure:

```text
Candidate: <action-oriented title>

Evidence
- Production consumers: <paths or none found>
- Non-production consumers: <tests/docs/examples>
- Ambiguous or dynamic consumers checked: <paths and result>
- Governing ADR/domain/compatibility constraint: <path or none>

Proposed simplification
<what to remove, fold, demote, or replace>

Net deletion
<implementation, tests, docs, dependency, or maintenance paths actually removed>

What it gives up
<capability, compatibility, observability, or future option that would disappear>

Risks
<behavior, public-surface, migration, dependency, or reintroduction risks>

Confidence: <Strong | Worth exploring | Speculative>
Recommended next workflow: <implement | to-issues | improve-codebase-architecture | grilling | domain-modeling>
```

Do not present a candidate as approved work. Do not write implementation instructions
that silently choose product intent. The report is a decision input for the user.

## Route the selected candidate

After the user selects a candidate, check whether they requested exploration,
planning, or implementation. Selection alone does not authorize a code change.
For already authorized follow-up work, continue the appropriate model-invoked
workflow; otherwise recommend the useful next action:

- deletion, folding, demotion, or dependency replacement: `to-issues` or `implement`;
- a changed module, interface, seam, adapter, or architecture shape:
  `improve-codebase-architecture` or `grilling`;
- a hard-to-reverse, surprising trade-off: `domain-modeling` to decide whether an
  ADR is warranted;
- old documentation or decision-record cleanup: the existing documentation workflow.

Do not invoke a user-invoked target automatically. Do not invoke `wayfinder` for a
bounded simplification candidate; recommend it only when the selected work reveals
material cross-session decision fog that changes destination, scope, architecture,
major risk, or acceptance.

## Validation discipline

Before returning the report, run a cold-start audit of each candidate:

- Can a fresh implementer reproduce the consumer search from the cited paths?
- Did the candidate account for configuration, registry, dynamic, serialized, wire,
  reflected, generated, and compatibility use?
- Is the claimed net deletion larger than the replacement glue and maintenance cost?
- Is the strongest counterargument stated in `What it gives up` or `Risks`?
- Did the report preserve existing ADRs and domain terms instead of making a new
  architecture decision?

If any answer is no, downgrade or remove the candidate. Return the report only after
this audit. The audit itself stays read-only; separately authorized follow-up
work belongs to its selected workflow.
