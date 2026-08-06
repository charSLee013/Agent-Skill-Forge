---
name: ponytail
description: >
  Constrains an approved coding task to the smallest implementation that is
  still correct. Use only when the user explicitly invokes Ponytail while
  implementing, fixing, refactoring, or reviewing code. It reuses existing
  mechanisms, standard libraries, native platform features, and installed
  dependencies before adding code. It does not explore product direction,
  reopen approved scope, weaken acceptance evidence, or impose TDD.
license: MIT
disable-model-invocation: true
---

# Ponytail

Implement the approved behavior with the least code that preserves correctness.
Small is a constraint on the solution, never on understanding or verification.

## Scope

Ponytail starts only when the user explicitly invokes it. Once invoked, it stays
active for every later response in the current project, including new tasks,
resume, clear, compact, and subagents. A topic change, session boundary, idle
time, malformed hook input, or execution error must never disable it. Only an
explicit `stop ponytail`, `normal mode`, or `/ponytail off` command may clear it.

The parent workflow owns product direction. Treat the current approved request
and any applicable issue, PRD, ADRs, non-goals, and acceptance evidence as fixed
input. Do not replace Wayfinder, reopen settled decisions, shrink requested
behavior, or invent adjacent work. If those inputs conflict or leave correctness
undefined, stop under the parent workflow instead of guessing.

## Order

Before editing:

1. Read the approved scope, constraints, and acceptance evidence.
2. Trace the affected runtime path, callers, state changes, and failure paths.
3. Identify the smallest change point that covers the complete behavior.

Then stop at the first option that satisfies the full contract:

1. Reuse an existing repository mechanism.
2. Use the standard library.
3. Use a native platform capability.
4. Use an already-installed dependency.
5. Write the minimum new code.

Fewer lines do not win when they obscure intent, mishandle an edge case, or
weaken the approved behavior. Prefer the smallest correct solution, not the
smallest-looking diff.

## Correctness

- Fix root causes at the shared change point after checking all relevant callers.
- Preserve validation at trust boundaries, security controls, accessibility,
  data-loss protection, required error handling, and explicit compatibility.
- Follow repository interfaces and patterns unless the approved work changes them.
- Do not introduce speculative abstractions, extension points, dependencies,
  configuration, compatibility branches, or documentation.
- Do not create a test merely because Ponytail is active. Use the acceptance
  evidence selected by the issue and parent workflow. Add or change tests only
  when that contract or the changed behavior requires them.
- Never delete existing tests or weaken an oracle to make the implementation smaller.

## Finish

Check the final delta twice:

1. Every changed line maps to approved behavior, indispensable support, or
   required evidence.
2. Removing anything else would break correctness, repository fit, or acceptance.

Remove debug output, scratch files, temporary checks, and speculative code before
delivery. Ponytail changes implementation size only; the parent workflow still
owns verification, staging, commits, and the final report.
