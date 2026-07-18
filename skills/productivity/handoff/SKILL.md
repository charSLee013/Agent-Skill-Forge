---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

If a Wayfinder map exists, include its path, current decision issue, Wayfinder status, and next frontier. Reference the map instead of copying its decisions into the handoff.

Include the next task's objective, scope, non-goals, decisions, open questions, changed files, verification state, and exact artifact paths needed to continue. Do not prescribe a skill list unless the user explicitly asks for routing advice; the next agent should choose the smallest applicable flow from the handoff.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
