---
name: trim-cot-leakage
description: Audit or fix prose that leaks design-session, PR, review, draft, or reasoning-transcript context instead of stating durable repository facts.
argument-hint: "Which prose scope should be checked for authoring-session residue?"
license: MIT
disable-model-invocation: true
---

# Trim chain-of-thought leakage

Chain-of-thought leakage is prose whose vantage is the authoring session rather
than the repository: it cites artifacts only that session could see, narrates a
change instead of the state, or argues with a reviewer who has left. The fix is
never deletion alone when a passage carries factual clauses: restate each so it
stands at HEAD, then delete the transcript around it. Delete a passage outright
only when it carries no fact, such as an audit code or control-flow narration.

This adaptation preserves the review core of
[`dsh-trim-cot-leakage`](https://github.com/deepseek-ai/deepseek-harness/blob/b150a551b8d465e31e418e1b2eaf5e79bbb7d28e/.agents/skills/dsh-trim-cot-leakage/SKILL.md)
while using this repository's `AGENTS.md`, ADRs, `CONTEXT.md`, README files, and
local `.codex/agents/` workspace as its durable records. It is guidance, not a
script.

Before deleting, preserve every surviving actor/action, condition or ordering,
modality, exception, ownership, failure, and consequence. For a broader review
of required prose coverage and placement, recommend `$prose-standard`; do not
invoke another user-invoked skill automatically.

## The one test

For every suspect passage ask: **could a reader at HEAD, with no access to any
session transcript, PR thread, or uncommitted draft, resolve every reference and
verify every claim?** If no, restate the surviving facts from the repository's
vantage and delete the rest. If yes, it is not leakage, however historical it
sounds.

Resolvability only clears this skill's bar. On current-state surfaces such as
READMEs, documentation, and JSDoc, a resolvable change story is still change
narration: state the current mechanism and keep history in the durable record
that owns it.

## Taxonomy

1. **Dead design-session citations**: `(decision 7)`, `(audit C2)`, `design
   section 4.7`, `plan section 1.4`, phase labels, or an unnamed design ledger.
   If a committed record owns the decision, cite it by name and path; otherwise
   delete the citation and restate its factual clause to stand alone.
2. **Stack and PR vantage**: "a later PR in this stack", "this PR adds", or
   "the previous commit". State the shipped mechanism or extension point;
   deferred work belongs in an existing issue or a deliberate TODO.
3. **Change narration and version stamps**: "used to", "no longer", "the old
   X", and indexical stamps such as "this cut", "today", or "now" contrasted
   with a past repository state. State present behavior. Turn a fixed regression
   into a present-tense counterfactual, never repo archaeology.
4. **Review choreography**: "rejected in review", "the reviewer confirmed",
   draft ordinals, or round attributions. Keep the decision and rationale as
   plain fact; delete who said it when.
5. **Reviewer-addressed justification**: "the cast is safe, it simply..." or
   "this is correct because...". State the invariant that makes the code safe,
   or delete the comment if the code already shows it.
6. **Restatement and derivation transcripts**: control-flow narration, test
   walkthroughs, and proofs of obvious branches. Delete them; keep only a
   non-obvious contract or invariant.
7. **Hedges and planning residue**: "probably fine for now", "should be
   enough", or an unowned deferral. Promote a real deferred obligation to an
   existing issue or deliberate TODO, restate an actual bound, or delete the
   hedge.
8. **Authoring-language slips**: untranslated working-language fragments or
   session separators in otherwise coherent prose. Translate or delete them.

## What is not leakage

Unaided citation passes fail in both directions by deleting durable references
and keeping dead ones. Apply these keep rules as written; the
[examples](references/examples.md) calibrate each.

- **Issue references:** issue identifiers and deliberate `TODO(owner):` markers
  resolve at HEAD. Keep them on any surface, including READMEs.
- **Merged-PR and issue citations inside ADRs or postmortems:** these can be
  durable evidence when the record is the authorized historical owner.
- **Suppression justifications:** lint, coverage-ignore, and empty-catch reasons
  are required prose. Fix a false reason; never delete it merely to shorten.
- **Counterfactual-present regression pins:** "without X, Y happens" and "a
  naive X would...".
- **Measured bounds:** measurements calibrating a constant; the provenance word
  `measured` is load-bearing.
- **Runtime old/new states:** "the old connection drains before the new one
  accepts" names live objects during handover, not repository history.
- **Historical stage names in a durable change-story:** the historical record
  may name a release stage, but indexical stamps such as "this cut" remain
  unsuitable durable prose.
- **External references:** standards sections, design-system frame names, and
  committed documents that own their section numbering.
- **Project voice and genre:** project "we" and an ADR's Alternatives Considered
  section are not leakage by themselves.

## Workflow

1. Require an explicit scope. Exclude `vendor/`, `node_modules/`, and generated
   or recorded fixtures and snapshots from edits. Respect any explicitly frozen
   history in the requested scope.
2. Audit read-only first: run the [recall batteries](references/recall-batteries.md)
   with `--hidden` when the scope may include `.codex/`, then judge every hit
   semantically. Batteries are probes, not the definition. Also read dense prose
   in scope without a pattern in hand.
3. Fix the owner first. For a generated catalog, edit source JSDoc or a generator
   template, then regenerate. For maintained language counterparts, update both.
   Treat model-visible wording as behavior: validate the rendered result or flag
   the need for snapshot-backed verification rather than silently rewording it.
4. Before deleting, enumerate a passage's propositions and check the
   [overcorrection traps](references/examples.md#overcorrection-traps). Do not
   flip an obligation into an endorsement, promote a hypothetical to a shipped
   feature, delete a true fact with its transcript, or drop provenance.
5. Re-run relevant batteries, confirm each remaining citation resolves at HEAD,
   and run narrow checks for every touched surface plus `git diff --check`.
   Report inspected scope, edits, deliberate keeps, deferred cases, and checks
   actually run.

Use the user's requested mode. In automatic mode, apply clear edits when the
task authorizes changes and report genuine borderline cases. In interactive
mode, present only proposition-preserving alternatives with their real tradeoff.
