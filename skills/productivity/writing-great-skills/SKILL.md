---
name: writing-great-skills
description: Reference for writing goal-directed agent-consumed documents, including skills and repository instruction maps.
license: MIT
argument-hint: "Which agent-consumed document or behavior contract should be written or reviewed?"
disable-model-invocation: true
---

# Writing Great Skills

Write instructions that keep the agent accountable for the user's outcome while
letting it choose methods from the evidence. Preserve goals, priorities, hard
constraints, authorization boundaries, factual honesty, and delivery obligations.
Let investigation depth, tools, experiment order, and resource allocation adapt
to the task. Consistency means respecting these commitments across runs; it does
not require taking the same process every time.

This guidance incorporates Matt Pocock's `writing-for-agents` and the
model-facing `agent-experience` principles from
`deepseek-ai/deepseek-harness@22ddee3792402c3e70ec5f86a63c3e3e895a2f60`.
It does not require either upstream runtime or documentation structure.

This skill supplies writing reference within the requested scope. `AGENTS.md`
owns repository-wide operating constraints and navigation. Product behavior,
feature scope, and task decisions belong in their owning specification, ADR,
issue, or code. A correction from one task stays local unless the user requests
a broader instruction change.

When writing a skill, also read
[`SKILL-MECHANICS.md`](SKILL-MECHANICS.md) for packaging and invocation.

## Choose the right constraints

Use a fixed sequence where an operation depends on an earlier result: for
example, create and verify a migration destination before switching its callers,
then remove the old form after those callers have moved. Explain the dependency
so the order remains meaningful when circumstances change.

For diagnosis, research, and design, state the useful methods, when each applies,
and how to choose the next action. A diagnostic loop can move between source
inspection, traces, reproduction, and measurement as uncertainty changes. It
need not complete every method or explain why every unused suggestion was skipped.

Match detail to consequences. Keep strict permission and data-protection rules
where they prevent concrete harm. Avoid turning one convenient tool, past
failure, or example into a universal prerequisite. Check competing explanations
and edge cases before prescribing a method.

## Context pointers and progressive disclosure

A context pointer names material outside the current context and says when to
read it. Skill descriptions and navigation entries in `AGENTS.md` are pointers.
Name each materially different case that should reach the target, collapse
synonyms, and keep definitions in the target. Sharpen an unreliable pointer
before moving its whole reference inline.

Always-loaded text spends context on every run. Hidden material without a
pointer makes the human remember it. Spend context where autonomous discovery
matters and rely on manual selection where human judgment should control entry.

Apply DeepSeek Harness's portable `agent-experience` principle: disclose purpose,
available actions, and critical constraints first, with a reliable path to
conditional detail. Bound tool results, identify truncation, and point to further
results. Judge total work: shortening a pointer at the cost of repeated searches
or missed constraints is a regression. Do not copy DSH schemas or its loader.

## Information ownership

Keep what every execution needs in the entrypoint. Place substantial
branch-specific material in a reference and link it where the branch becomes
relevant. Steps, definitions, and conditional guidance may coexist; a reference
skill does not need an execution sequence.

Keep a concept's definition, conditions, exceptions, and caveats together.
Choose one owner for shared meanings and let consumers link to it with only the
reminders their task needs. Avoid parallel definitions that drift independently.

## Completion criteria

Describe the required end state and the observations needed to establish it.
Cover every requested result, including combined behavior across subtasks and
any explicit limits on what may be claimed. Completion does not mean using every
suggested tool or exhausting every possible experiment.

A diagnostic task may finish with a supported, qualified explanation when the
necessary runtime evidence is unavailable. A migration may require every caller
to move and the old form to disappear. Write these distinct obligations directly
instead of fitting both into one phase template. Keep unmet requirements visible
and continue independent authorized work when one part is blocked.

## When to split

Split by branch when substantial detail applies to only some runs, and by
invocation when a capability needs independent discovery; see
[`SKILL-MECHANICS.md`](SKILL-MECHANICS.md). Split by sequence only when a real
dependency or context boundary makes separate instructions useful. A long task
alone does not justify more skills, phases, or approval gates. Each split must
earn the pointer and human memory it adds.

## Wording and pruning

Use familiar concepts to anchor behavior. Repeat a useful term where needed,
without repeating its definition. State the desired action; reserve prohibitions
for concrete boundaries and pair them with the permitted path forward.

Review each passage for its effect on decisions. Remove duplicate definitions,
stale compatibility, and advice that changes nothing. Keep environment facts
only when looking them up repeatedly costs more than maintaining the reference.
Preserve operational knowledge and source attribution when pruning prose.

Read the complete revised path and try realistic examples and counterexamples.
Check whether the instructions preserve the goal, permit an appropriate method,
and support an honest completion claim. Keyword checks and file presence cannot
establish these properties; distinguish a scenario walkthrough from an actually
executed behavioral evaluation.
