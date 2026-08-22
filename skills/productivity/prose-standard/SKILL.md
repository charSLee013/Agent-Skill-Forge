---
name: prose-standard
description: Review, write, restore, trim, or audit prose when documentation, comments, prompts, diagnostics, or visible strings must preserve a complete technical contract.
argument-hint: "Which prose scope should be audited or edited?"
license: MIT
disable-model-invocation: true
---

# Prose standard

Write enough to preserve the contract, then remove reasoning transcripts,
repetition, and decoration. A contract is an obligation, invariant,
precondition, postcondition, or compatibility promise that a caller, callee,
implementer, producer, or consumer relies on.

This adaptation preserves the editorial discipline of
[`dsh-prose-standard`](https://github.com/deepseek-ai/deepseek-harness/blob/b150a551b8d465e31e418e1b2eaf5e79bbb7d28e/.agents/skills/dsh-prose-standard/SKILL.md)
without importing DeepSeek Harness's separate documentation tree, Agent Notes,
or release gates. It is guidance, not a script.

Treat `contract`, `boundary`, `shape`, `surface`, `seam`, `gate`, and
`vocabulary` as terms to check before use, not banned words. First ask whether
the exact rule, API, field set, type, validation, timing point, component
split, or failure state states the fact better. Keep a term when it names the
exact technical subject, including caller/callee contracts and
security/process boundaries.

Comments describe non-obvious contracts or rationale that code cannot express;
they do not restate what code already implies. For a focused pass on
authoring-session residue, recommend `$trim-cot-leakage`; do not invoke another
user-invoked skill automatically.

## Inputs and exclusions

Require an explicit `scope`. If it is missing, report the required input and
stop; do not infer a repository-wide scope or begin an interview.

Accept `mode: automatic | interactive`; default to `automatic`. Enter
interactive mode only when the user explicitly requests questions or
calibration. `mode` controls questions, not write authority: review and audit
tasks report findings without editing; explicitly requested write, fix, or trim
tasks apply clear changes.

Always exclude `vendor/` and `node_modules/` from discovery, review, and edits,
even when the requested scope is the whole repository. Do not follow a symlink
into either directory. Put exclusions after inclusion globs so a later include
cannot re-admit them. If the requested scope contains only excluded material,
report that no eligible files remain.

Treat generated catalogs, snapshots, and fixtures as derivative. Edit the
owning source or scenario first, then regenerate the artifact. When a generator
extracts a summary from owner prose, make the extracted sentence complete for
that surface. When maintained language counterparts exist, update the
counterpart minimally and verify that their shared facts still agree.

## Preserve the complete proposition

Before editing, identify every proposition in the passage. Preserve each
relevant:

- actor and action;
- condition, timing, and ordering;
- modality such as must, may, or never;
- negative guarantee and exception;
- ownership, side effect, failure mode, and consequence.

Remove adjectives, repetition, and narration only when every factual clause
survives and the result is clearer. A smaller word count alone is not an
improvement.

Keep a complete local contract at the point of use: behavior, failure,
ownership, and consequence that a caller or maintainer needs there. Link to the
owning document for architecture, rationale, algorithms, history, or extended
examples. One explanation has one home; essential contract facts may repeat
locally.

Keep non-obvious rationale when omitting it could plausibly cause misuse or an
incorrect simplification. Otherwise state the consequence and link the rationale
home.

## Required coverage by prose location

This is not a one-way shortening pass. Add or restore prose when code, types,
and structure do not communicate a required contract below. Do not add a
comment when those facts are already obvious locally.

- **Public JSDoc:** caller-visible return distinctions, throws or rejections,
  side effects, ownership, timing, cancellation, and durability.
- **Internal comments:** non-local structure, invariants, race ordering,
  ownership, security boundaries, and surprising failure behavior. Delete
  control-flow narration and code restatement.
- **Module comments:** role, dependencies, responsibilities, and non-obvious
  architecture choices; link their durable owner.
- **Tests:** only non-obvious test design, such as why a fixture, assertion,
  platform accommodation, real entry path, or indirect observation is needed.
  Delete walkthroughs and inventories.
- **Cookbooks:** prerequisites, required actions, the real entry path,
  observable verification, and concise warnings.
- **READMEs:** consumer configuration, semantics, failures, limitations,
  extension points, and model-visible effects. Quote stable text the package
  owns; link generated catalogs and cross-package owners. Keep durable gaps and
  maintainer traps, not ordinary cleanup inventories.
- **ADRs and other durable decision records:** unique rationale, mechanisms,
  alternatives, consequences, shipped verification evidence, and named coverage
  gaps. Records of implemented decisions state shipped reality in the present
  tense; remove planning checklists, not evidence of what pins the decision.
- **Postmortems:** incident sequence, evidence, causal chain, impact, and
  prevention. Remove repeated persuasion or implementation detail that does not
  establish causality.
- **Skills and agent instructions:** behavioral guardrails and explicit scope
  limitations such as "guidance, not a script/checklist." Keep the workflow
  concise and link its source of truth.
- **Examples and configuration comments:** access limits, non-obvious wiring or
  load order, security stance, replay behavior, exceptions, and likely misuse.
  Do not narrate entries that the configuration already shows.
- **Prompts and visible strings:** treat wording as behavior. Inspect generated
  output and run behavior validation or state why no snapshot applies.
- **Diagnostics:** failing subject or path, violated rule, and non-obvious
  correction. Remove internal execution narration.

Preserve searchable mechanism names and meaningful modal, temporal, or negative
emphasis. Normalize decorative emphasis only.

## Workflow

1. Confirm scope, mode, branch or comparison base when relevant, and applicable
   `AGENTS.md` instructions. Do not inspect unrelated branches.
2. Read the owning code or document before judging a passage. Read `CONTEXT.md`,
   relevant ADRs, README files, and `.codex/agents/` material only when they
   govern the requested scope. For calibration or unfamiliar cases, read the
   [distilled examples](references/examples.md).
3. Inspect the requested scope, not only the largest files. Use searches and
   word counts to find candidates, then judge passages semantically.
4. Classify each candidate as keep, add, trim, restore, restructure, or defer.
   Apply clear changes only when the task authorizes edits; do not manufacture
   edits to satisfy a deletion target.
5. Update the owner before derivative artifacts. Re-check analogous passages
   after learning a new rule.
6. Run narrow checks for the touched surface, `git diff --check`, and behavior
   validation for visible strings. Verify the final diff contains no excluded
   path and report any accidental match instead of claiming a clean exclusion
   history.
7. Report inspected scope, clear changes, deliberate keeps, deferred cases, and
   checks actually run.

## Borderline decisions

A case is borderline only when at least two versions satisfy the
complete-proposition rule but trade accepted principles, and this skill does not
already resolve the tradeoff. A rewrite with one proposition-preserving answer
is not borderline.

In automatic mode, apply clear edits when authorized and report genuine
borderline cases without asking questions. Do not weaken a proposition to make
progress.

In interactive mode, group analogous passages under the governing principle.
Present two or three viable versions, recommend one, and state the factual or
structural difference. Do not offer inferior distractors.

After the user decides, apply the learned principle to analogous passages in
scope. Do not create a new tracker, note tree, archive, or standing style record
for a one-off prose decision.
