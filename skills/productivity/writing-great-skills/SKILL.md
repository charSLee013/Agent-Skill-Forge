---
name: writing-great-skills
description: Reference for writing and editing predictable agent-consumed documents, including skills and repository instruction maps.
argument-hint: "Which agent-consumed document or behavior contract should be written or reviewed?"
disable-model-invocation: true
---

# Writing Great Skills

An agent-consumed document exists to create **predictability** in a stochastic
system: the agent takes the same process on each run, rather than producing the
same output. Packaging differs between a skill, an `AGENTS.md` or `CLAUDE.md`,
and a document reached through a pointer; the writing levers are the same.

This skill supplies writing reference. It does not expand the requested scope or
authorize edits to another document. In particular:

- `AGENTS.md` owns repository-wide operating constraints and navigation.
- Product behavior, feature scope, and task decisions belong in the product,
  specification, ADR, issue, or code surface that owns them.
- A correction from one task remains local unless the user explicitly requests
  a repository-wide instruction change.

When the target is a skill, also read
[`SKILL-MECHANICS.md`](SKILL-MECHANICS.md) for frontmatter, invocation, and
routing mechanics.

## Context pointers

A **context pointer** is text already in the agent's context that names material
outside that context and states when to read it. A skill description is one. A
line in `AGENTS.md` that routes a task to another document is the same object.
The pointer's wording, not its target, determines when and how reliably the
agent follows it.

A pointer states what the material is and names each distinct **branch** that
should reach it. A branch is a materially different case handled by the target.
Every word in an always-loaded pointer spends attention on every turn, so:

- Front-load a leading word that names the behavior.
- Keep one trigger per branch; collapse synonyms for the same branch.
- Remove identity and explanation already carried by the target document.

Sharpen a weak pointer before moving its target inline. Inline only when the
material is required on every relevant path and the pointer still fires
unreliably.

## The two loads

Every document and pointer spends one of two budgets:

- **Context load** is always-loaded text in the model's context, such as an
  instruction-map entry or model-facing skill description.
- **Cognitive load** is what the human must remember: which documents or manual
  skills exist and when to reach for each.

Material behind a pointer reduces context load at the cost of the pointer.
Material with no pointer relies entirely on human memory. Spend context load
where autonomous discovery matters and cognitive load where human judgment
should retain control.

## Information hierarchy

Agent documents are built from **steps** and **reference**. The two mix freely:
all steps, all reference, or both. Place each item on the lowest rung that still
makes it reliably available:

1. **In-file step**: an ordered action the agent must perform.
2. **In-file reference**: a definition, rule, or fact consulted while acting.
   A flat peer set is valid when the document is all reference.
3. **Disclosed reference**: branch-specific material in another file, reached
   through a context pointer. It may be a sibling file or an external owner.

**Progressive disclosure** moves branch-specific reference down this hierarchy.
It protects the action path from unrelated material; it is not merely a token
optimization. Inline what every branch needs and disclose what only some
branches need.

**Co-location** governs material on the same rung. Keep a concept's definition,
rules, exceptions, and caveats together so one read supplies the complete
contract. Scattering fragments one meaning; duplication creates competing
owners for it.

**Sprawl** is a document that remains too long even when every line is live and
unique. Disclose by branch or sequence until each execution path carries only
what it needs.

## Steps and completion criteria

Every step ends on a **completion criterion**: the condition that distinguishes
done from unfinished. Strong criteria have two properties:

- **Clarity**: the agent can check whether the condition holds.
- **Demand**: the condition accounts for every required result, not merely a
  representative sample.

Demand drives **legwork**, the investigation and production performed within
the work. It is not step-bound: "every rule applied" binds flat reference just
as "every step done" binds a sequence, so an all-reference document can still
carry an exhaustive completion criterion. Visible **post-completion steps** can
pull attention forward and cause **premature completion** when the current
criterion is vague. Sharpen the criterion first. Split the sequence across a
real context boundary only when the criterion cannot be made clear and the rush
is observable.

A completion criterion owns the required outcome, not a universal verification
technique. Use the evidence required by the target repository, task, and risk.

## When to split

**Granularity** is how finely documents or skills are divided. Each split adds a
pointer or something the human must remember, so make the cut earn that load:

- **By sequence** when hiding later steps prevents premature completion.
- **By branch** when a substantial body of reference belongs to only some runs.
- **By invocation** when a skill must be discovered independently; see
  [`SKILL-MECHANICS.md`](SKILL-MECHANICS.md).

## Leading words

A **leading word** is a compact, pretrained concept that anchors behavior, such
as _lesson_, _fog of war_, or _tracer bullets_. Repeat the token where the same
behavior must be recruited; do not repeat its full definition. In a body it
anchors execution, and in flat reference it focuses attention on the class of
thing to inspect. In a pointer it anchors invocation.

Prefer a familiar concept over a coined term because a familiar word recruits
useful priors without a long definition. Replace repeated explanations with one
strong leading word only when it preserves the full meaning.

**Negation** is the neighboring failure mode: naming an unwanted behavior makes
it more available. State the positive target. Reserve prohibitions for hard
guardrails that cannot be expressed positively, and pair each with the desired
behavior.

## Pruning

- Keep each meaning in a **single source of truth**. **Duplication** raises
  maintenance cost and gives one rule accidental extra weight.
- Treat the environment as a source of truth. A document that repeats an easy
  lookup from configuration, directory layout, or command output is a **cache**;
  keep it only when the lookup is expensive enough to justify drift risk.
- Check **relevance**: every line must still bear on the document's behavior.
  Stale layers form **sediment**, making live rules harder to find.
- Run the **no-op check** sentence by sentence: would the agent behave
  differently without it? Delete a sentence that does not change behavior.
  This check is model-relative; settle uncertainty through observed behavior,
  not additional explanatory prose.
