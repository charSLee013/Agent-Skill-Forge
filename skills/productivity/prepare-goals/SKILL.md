---
name: prepare-goals
description: Prepare clear, long-running work as bounded Codex Goals with observable completion criteria.
argument-hint: "What long-running objective should be prepared?"
disable-model-invocation: true
---

# Prepare Goals

Turn approved work into one or more ready-to-paste Codex Goal launchers. Prepare the Goal contract; do not implement the work, change issue state, or start Goal mode.

Use Goal mode for an objective expected to require many steps or continue for hours or days. Keep ordinary bounded work as a direct task. If the outcome, constraints, or completion criteria still require a material decision, report the blocker instead of disguising planning as a Goal.

## 1. Establish Authority

Read the latest user request and the smallest set of current sources that govern it: the instruction chain, relevant approved PRD or plan, ADRs, implementation issues, and the affected repository state.

Apply these authority rules:

- The latest explicit user decision wins over older task documents.
- Current approved work items govern scope and acceptance. Archived, superseded, rejected, and out-of-scope records provide history only unless the user explicitly reactivates them.
- `AGENTS.md` governs stable repository instructions and maps. Keep task-specific outcomes, product scope, decisions, status, and progress in the Goal text or their owning work items; never propose adding them to `AGENTS.md`.
- Existing worktree changes belong to their current owner. Record only the overlap that affects Goal isolation; do not manufacture a full-repository hash inventory.
- Volatile Goal behavior comes from the current Codex surface and [official long-running work documentation](https://learn.chatgpt.com/docs/long-running-work), not an older packet template.

## 2. Classify The Work

Give every candidate task exactly one disposition:

- `ready`: one clear, durable outcome with bounded scope and observable completion evidence.
- `direct`: clear work small enough for normal execution; emit no Goal launcher.
- `blocked`: a missing decision, dependency, authority, permission, or verification path would force the executor to guess.
- `done`: current evidence already proves the requested end state.
- `excluded`: outside the user's stated task boundary.

For `blocked`, name the smallest decision or fact that unlocks the work. Do not turn a loose backlog, unresolved architecture question, or aspirational roadmap into a ready Goal.

## 3. Slice Durable Outcomes

One Goal owns one result and one stopping condition. Combine work only when all included items share the same delivered outcome, scope boundary, and verification closure. Otherwise split them and preserve dependency order.

When multiple Goals are independent, note that each belongs in a separate chat. For coding work, do not recommend parallel Goals against the same checkout when their write scopes can overlap; use isolated worktrees or run them sequentially.

Preserve the approved issue slices. Do not merge independent issues into a super-Goal merely because they share a PRD, and do not split one coherent vertical slice into layer-by-layer Goals.

## 4. Write Each Goal

Write each launcher as `/goal <objective>`, under the current 4,000-character objective limit. The objective must stand on its own and include only what changes execution:

1. **Outcome** - the observable result, not a list of activities.
2. **Authority** - exact current source paths or user decisions the executor must follow.
3. **Scope** - the owned behavior or paths, relevant non-goals, dependency order, and pre-existing changes that must be preserved.
4. **Constraints** - required compatibility, safety, architecture, tools, and explicitly rejected approaches.
5. **Verification** - tests, measurements, inspections, or review criteria that prove the end state.

Use task-appropriate evidence. TDD, fixed phase names, persistent progress ledgers, repository-wide hashes, and mandatory subagent review are not defaults; include one only when the governing work item or repository policy requires that exact mechanism.

Do not invent a token budget. Include one only when the user explicitly supplied it and the current Goal surface supports it.

## 5. Deliver

Return the launchers in the conversation by default. Write an `instruct.md` only when the user requested a file or named an output path. Do not create a nested packet or ledger tree unless separate durable handoff files are an explicit deliverable.

For multiple candidates, provide a compact inventory before the launchers:

| ID | Disposition | Outcome | Depends on | Authority |
| --- | --- | --- | --- | --- |
| G01 | ready | One durable result | none | Exact source path or user decision |

Then provide each `ready` launcher in dependency order in its own text block. List `blocked` work with its exact unlock condition and `direct` work with the normal execution boundary. Do not emit launchers for `done` or `excluded` work.

End after the prepared output. Starting `/goal` is a separate user action.

## Completion Check

- Every candidate task has exactly one disposition and every accepted criterion is covered once.
- Every `ready` launcher contains one outcome, relevant constraints, and observable verification.
- Dependencies and overlapping write scopes cannot silently race.
- Every launcher is below 4,000 characters and contains no unrelated backlog.
- No task-specific product rule or progress fact was moved into `AGENTS.md`.
- No additional ceremony was introduced without authority.
- Goal mode was not started.
