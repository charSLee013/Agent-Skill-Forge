---
name: real-path-verification
description: Verify an approved behavior through an existing real runtime path or a production-equivalent replay. Use during implement when an acceptance criterion explicitly requires production, real traffic, canary, shadow, replay, migration, release verification, or end-to-end evidence. Do not use for routine unit, smoke, mock, minimal-repro, documentation, or trivial-edit work.
---

# Real Path Verification

Verify the requested behavior at the runtime path that the acceptance criterion actually describes. This is an implement support phase, not a replacement for diagnosis, planning, or ordinary checks.

Read `implement`'s `references/evidence.md` when evaluating a behavior claim.
Locate the owner through host-discovered skill paths or the repository plugin
manifest. Reading the reference does not start an implementation task.

## Entry contract

Run when the user explicitly requests verification of a named behavior through
a real runtime path, a parent criterion has `real-path` evidence, or a `target`
criterion names an approved real runtime path as its source. An ordinary
natural-language request need not be converted into a PRD first.

Consume the current request's goal, scope, acceptance conditions, oracle,
environment, risk decision, and known runtime entrypoint, including any
formal work item when present. Do not re-interview, repartition the work,
or expand the scope.

## Safety gate

Before an action that can change shared or production state, send consequential
external traffic, incur material cost, expose sensitive data, or require
production credentials, show the user:

- the exact environment and runtime path;
- the expected side effect, traffic volume, cost, and data exposure;
- the rollback, cleanup, and stop condition;
- the observable result that will decide the conclusion;
- the remaining uncertainty.

If the current request already records the user's concrete risk choice and the
actual action has not widened, consume that choice instead of asking again.
Ask again only when the actual environment, side effect, traffic, cost, or data
exposure differs. Ordinary reversible local checks and read-only inspection of
an existing command need no separate safety presentation.

## Evidence boundary

Return a conclusion, not a verification transcript. Do not create a run directory, stored bundle, raw response capture, replay copy, generated summary, verification file, or artifact path merely to document verification. Do not write experiment artifacts into the repository or modify production code.

Use existing runtime output, telemetry, trace or request IDs, and observation links directly. Do not preserve raw command output, response bodies, logs, or payloads solely to make the result look auditable.

Only if an existing entrypoint cannot execute without a temporary input or output file, create the smallest necessary file under the system temporary directory and arrange cleanup before invocation. Remove it on every reachable success, failure, timeout, interruption, or observation-read path; if that cleanup cannot be guaranteed, do not use the file-dependent invocation. Do not report its path. Retain material only when the user explicitly requests it or an external compliance obligation requires it; that retention is not a default skill artifact.

## Workflow

1. Read the user's request and any parent criteria to identify the behavior and final oracle. If the requested outcome or necessary observation is unclear, resolve that material gap before taking a consequential runtime action; do not invent a formal work item.
2. Locate an existing runnable entrypoint: project command, deployed endpoint, CLI, browser flow, captured production trace, or approved replay command. Do not create a Python test, temporary harness, mock service, or new runner when no entrypoint exists.
3. If no suitable entrypoint exists, stop. Report the missing environment, command, data, credentials, traffic, or equivalence evidence needed; do not substitute a smoke test.
4. A production runtime observation, or an equivalent path with relevant parity established, can satisfy a real-path criterion. Staging, unit, mock, smoke, tracer, and minimal-repro results are supporting only; leave a real-path criterion unverified when they are the strongest available observation.
5. Run the existing path in the declared environment. Observe only the facts needed for the conclusion: actual oracle value, environment, version or deploy, time window, existing trace/request ID or observation link, and any applicable side-effect cleanup result.
6. Compare observed behavior with every selected acceptance criterion. A SHA-256 match, passing process exit, HTTP 2xx, or smoke result cannot establish business success without observing the criterion's behavioral oracle. Hashes may still establish asset integrity when integrity itself is the question.
7. Return the conclusion first, followed only by its minimum necessary basis:

   - `Conclusion`: passed, failed, or unverified.
   - `Oracle`: expected value compared with observed value.
   - `Source`: environment, version or deploy, time window, and an existing trace/request ID or observation link when available.
   - `Side effect and cleanup`: only when applicable.
   - `Unverified boundary`: only when one remains.

## Completion

The verification phase is complete only when:

- every selected criterion maps to an oracle, environment, observation, and conclusion;
- a production observation or relevant parity-established equivalent path supports every passed real-path criterion;
- all non-read-only actions have a recorded risk choice and cleanup/rollback result;
- missing parity, failed checks, and unverified claims are explicit;
- no repository file, test file, harness, verification artifact, commit, or unrelated issue was added.
