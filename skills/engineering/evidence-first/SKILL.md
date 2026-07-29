---
name: evidence-first
description: Use when a request spans user intent, configuration, prompts, tools, permissions, runtime behavior, or multiple implementation layers and the agent must establish the task contract and verify the claimed behavior before changing anything.
---

# Evidence First

Turn an ambiguous or multi-layer request into a small, checkable contract before acting. Use this as a light guidance layer; let task-specific skills own their detailed workflow.

## 1. Freeze the contract

Read the request, applicable instructions, relevant files, and existing decisions before proposing work.

Write down, in compact form:

- **Goal**: the user-visible outcome, in the user's terms.
- **Scope**: files, systems, and behaviors included.
- **Non-goals**: adjacent work that stays untouched.
- **Acceptance**: what must be observably true when done.
- **Constraints**: permissions, compatibility, cost, safety, and repository rules.

Ask a question only when its answer can change the goal, scope, risk, or acceptance. Discover facts from the workspace or authoritative sources; choose reversible details explicitly and record the default.

When present, current approved ADRs and issue slices govern decisions, scope, dependencies, and acceptance. Archived, superseded, rejected, and out-of-scope records are historical context unless the user explicitly reactivates them. Preserve approved vertical slices instead of silently merging or repartitioning them.

Completion criterion: one concise goal, bounded scope, and an acceptance check exist; unresolved decisions that could change them are surfaced.

## 2. Trace the causal chain

Reason from first principles: start with the requested observation and trace backward to the state, decision, input, and owner that could produce it.

For claims about support or behavior, check each applicable layer:

```text
configuration -> runtime registration -> model-visible contract -> real invocation -> permission/result
```

Separate **fact**, **inference**, and **proposal**. Treat a configuration value, parser success, registry entry, or local unit test as evidence for only that layer, never as proof of the layers after it. Use the current tool schema and source of truth; do not invent interfaces from memory.

Completion criterion: every acceptance claim has an identified owner and evidence layer, or is explicitly marked unconfirmed.

## 3. Choose the smallest oracle

Before changing anything, select the smallest existing check that can distinguish the leading explanations and observe the acceptance behavior. Prefer, in order: an existing integration or end-to-end check, a real CLI or HTTP path, a focused test, then a read-only inspection. Create a new harness only when no existing path can answer the acceptance question and the task authorizes it.

State the expected result before running the check. A passing parse, build, or process exit is supporting evidence unless it observes the user's acceptance criterion directly.

Evidence-first does not prescribe TDD or require a new test. Add a test only when it is the smallest authorized oracle or the accepted work item requires durable regression coverage.

Completion criterion: one named command, test, request, or inspection has an expected observable result and has been run when the task allows execution.

## 4. Execute within the contract

Make the smallest change that satisfies the frozen contract. Keep ownership clear: the execution agent edits only the approved scope and does not silently widen it.

When a tool call fails, preserve the original error and reassess that call's assumptions. Do not infer that the whole tool surface, repository, or environment is unavailable; do not switch to a guessed namespace or replacement workflow without evidence.

Keep task-specific product scope, decisions, findings, and progress in their owning Goal, PRD, issue, or task context. Do not move dynamic task facts into `AGENTS.md` or another static instruction source.

If new evidence changes the goal, scope, risk, or acceptance, pause and restate the contract before continuing.

Completion criterion: every changed behavior is inside scope, and no unapproved branch was introduced to compensate for an unverified assumption.

## 5. Close with evidence

Re-run the selected oracle and map each acceptance item to its observed result. Report:

- **Conclusion**: confirmed, unconfirmed, or blocked.
- **Evidence**: exact files, symbols, commands, requests, or outputs.
- **Remaining uncertainty**: the layer or assumption not proven.
- **Next action**: only when the conclusion is unconfirmed or blocked.

Do not call behavior supported or complete when a required layer remains unverified.

Completion criterion: the final report contains an evidence-backed conclusion for every acceptance item, with gaps named rather than implied away.

## Keep it light

For a simple, single-layer request with an obvious acceptance check, answer or act directly. Do not create plans, reports, subagents, or extra artifacts merely to perform this skill.
