---
name: real-path-verification
description: Verify an approved behavior through an existing real runtime path or a production-equivalent replay. Use during implement when the task requires production, real traffic, canary, shadow, replay, migration, release verification, explicit end-to-end acceptance, or final integration of a work item with three or more slices. Do not use for routine unit, smoke, mock, minimal-repro, documentation, or trivial-edit work.
---

# Real Path Verification

Verify the requested behavior at the runtime path that the acceptance criterion actually describes. This is an implement support phase, not a replacement for diagnosis, planning, or ordinary checks.

## Entry contract

Run only when the parent implement flow has established one of these:

- the acceptance criterion explicitly requires a real path or production-equivalent proof;
- the task requires production traffic, canary, shadow, replay, migration, release verification, or explicit end-to-end acceptance;
- a parent work item has three or more slices and the final integration point has recommended this verification.

For three or more slices, recommend one run at the complete integration point. Do not run this once per slice unless an issue explicitly says that the slice is an independently deployed unit with its own real-path acceptance.

Consume the parent task's existing goal, scope, non-goals, acceptance criteria, oracle, environment, risk decision, and known runtime entrypoint. Do not re-interview, repartition the work, or expand the scope.

## Safety gate

Before any action that can write data, send traffic, incur material cost, expose sensitive data, change shared state, or require production credentials, show the user:

- the exact environment and runtime path;
- the expected side effect, traffic volume, cost, and data exposure;
- the rollback, cleanup, and stop condition;
- the evidence that will be collected;
- the remaining uncertainty.

If issue slicing already recorded the user's risk choice and the actual action has not widened, consume that choice instead of asking again. Ask again only when the actual environment, side effect, traffic, cost, or data exposure differs. A read-only local inspection of an existing command does not need this gate.

Use the current system temporary directory for experiment state. Set `run_dir` to a unique `real-path-verification/<timestamp>-<task-slug>` subdirectory under `TMPDIR` when it is set, otherwise under `/tmp`.

Keep logs, captured responses, replay inputs, parity notes, command output, and generated summaries under that directory. Do not write experiment artifacts into the repository or modify production code.

## Workflow

1. Read the parent acceptance criteria and identify the final oracle. If no criterion names the behavior and its evidence, stop and report the contract gap.
2. Locate an existing runnable entrypoint: project command, deployed endpoint, CLI, browser flow, captured production trace, or approved replay command. Do not create a Python test, temporary harness, mock service, or new runner when no entrypoint exists.
3. If no suitable entrypoint exists, stop. Report the missing environment, command, data, credentials, traffic, or equivalence evidence needed; do not substitute a smoke test.
4. Classify the strongest available proof:
   - E0 production: controlled production traffic, canary, or shadow with observable results;
   - E1 equivalent: production capture/replay or an environment with a written parity check for all failure-relevant semantics;
   - E2 staging: useful runtime evidence with unproven parity;
   - E3 supporting: unit, mock, smoke, tracer, or minimal reproduction.
5. Run the existing path in the declared environment. Preserve the exact command, build/version, configuration identity, input identity, timestamp, and relevant output.
6. Compare observed behavior with every selected acceptance criterion. Do not convert a passing process exit, HTTP 2xx, or smoke result into a business success without checking the criterion's oracle.
7. Collect the complete evidence bundle in the temporary run directory: commands, logs, traces or request IDs, input/output references, environment and version metadata, parity matrix, risk approval, rollback/cleanup result, failures, and known gaps. Redact secrets and sensitive payloads, but do not hide non-sensitive evidence.
8. Return the evidence bundle paths and contents summary to the user. Put the conclusion in a separate final field; return the evidence first so the user can audit the conclusion.

## Completion

The verification phase is complete only when:

- every selected criterion maps to an oracle, environment, and artifact;
- the artifact identifies the strongest proof level E0 through E3;
- all non-read-only actions have a recorded risk choice and cleanup/rollback result;
- the temporary run directory and evidence paths are returned;
- missing parity, failed checks, and unverified claims are explicit;
- no repository file, test file, harness, commit, or unrelated issue was added.

E0 or E1 can satisfy a real-path/production-equivalent acceptance criterion. E2 and E3 remain supporting evidence and must be reported as insufficient when that criterion requires real execution.
