---
name: prototype
description: Build a throwaway prototype to flesh out a design — a runnable terminal app for state/business-logic questions, or several radically different UI variations toggleable from one route.
disable-model-invocation: true
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify which question is being answered — from the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). Build a tiny interactive terminal app that pushes the state machine through cases that are hard to reason about on paper.
- **"What should this look like?"** → [UI.md](UI.md). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.

The two branches produce very different artifacts — getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or component → UI) and state the assumption at the top of the prototype.

## Rules that apply to both

1. **Throwaway from day one, and clearly marked as such.** Locate prototype code close to where it will actually be used, but when a parent workflow such as Wayfinder supplies an isolation rule, isolation wins: use the system temporary directory or an isolated copy/worktree, and interpret co-location inside that copy. Modifying the current worktree or a real route requires explicit user approval with risk, cleanup, and stop conditions. Name the artifact so a casual reader can see it's a prototype, not production, and obey the host routing convention inside the isolated environment.
2. **One command to run.** Whatever the project's existing task runner supports — `pnpm <name>`, `python <path>`, `bun <path>`, etc. The user must be able to start it without thinking.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE — wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype _runnable_, no abstractions. The point is to learn something fast and then delete it. A prototype result is a design signal, not production acceptance.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Delete or hand off when done.** When the prototype has answered its question, delete it or hand the decision back to the explicitly selected implementation flow. Do not fold prototype code into production automatically.

## When done

Return the answer and the observations that support it to the user. Write a durable artifact (ADR, issue, or notes) only when the task explicitly requires one or the user selects that handoff. Do not create a placeholder or `NOTES.md` by default; delete the prototype after its decision has been handed back to the selected workflow.
