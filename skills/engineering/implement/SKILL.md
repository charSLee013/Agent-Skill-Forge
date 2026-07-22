---
name: implement
description: "Implement a piece of work based on a PRD or set of issues."
disable-model-invocation: true
---

Implement the work described by the user in the PRD or issues.

Treat the user-approved PRD, issue, or task contract as the source of truth. Do not add adjacent behavior, refactors, tests, validation, documentation, or commits that are not required by it.

When an implementation issue has `Blocked by`, resolve each path from that issue's feature directory. A `decisions/` target requires `Wayfinder status: resolved`. An `issues/` target carrying both top-level Wayfinder fields is a legacy decision and uses the same oracle; every other `issues/` target requires `Completion: done`, with a missing field treated as `Completion: open`. Stop before implementation if any target is missing, ambiguous, outside the feature, or still blocked. Triage `Status` is not a completion oracle.

## Formal implementation issues

For an implementation issue, record the issue-start worktree before the first implementation change. Do not clean, stash, stage, or otherwise rewrite pre-existing user changes to make the baseline look clean. Use the setup-installed `Finalize Issue` entrypoint with the current session UUID: `python3 .codex/agents/runtime/support/scripts/finalize-issue.py begin --issue <path> --session-id <uuid>`. It records a private session receipt and a baseline section in the issue. If the entrypoint or current session UUID is unavailable, stop instead of inventing a baseline or editing `Completion` manually.

The baseline is attribution, not a cleanliness requirement. Continue to preserve pre-existing tracked and untracked work. During implementation, temporary exploration is allowed, but it has no claim on the final deliverable.

Run the existing checks relevant to the changed behavior. Do not create a test file for documentation, comments, copy, or non-behavioral metadata. Run the full suite only when repository policy, the task, or the breadth of the change requires it.

If the acceptance criteria require a real runtime path or production-equivalent proof, invoke /real-path-verification as the verification phase. If a parent work item has three or more slices, recommend one real-path run at final integration; do not run it once per slice unless the issue explicitly requires that.

## Finalize Issue

`Finalize Issue` is the only approved transition from `Completion: open` to `Completion: done`.

1. Run the entrypoint's `inspect` command for the same issue and session. Inspect its baseline-relative tracked files, non-ignored untracked files, file units, hunk units, and actual diff alongside the normal final worktree diff. Confirm that the Git index is unchanged from issue start and that ignored paths outside `.codex/` have returned to their baseline set.
2. Map every remaining file and hunk to approved scope, an acceptance criterion, or indispensable supporting implementation. Remove unmapped scratch files, debug scripts, temporary tests, unsolicited documentation, generated noise, unrelated hunks, and speculative abstractions. "Potentially useful" is not a mapping.
3. Audit public interfaces, dependencies, persistence, and error handling for unrequested parameters, options, environment variables, configuration keys, compatibility branches, packages, migrations, formats, durable state, or duplicated fallback and raise behavior.
4. Retain tests only for a named risk or acceptance requirement. After cleanup, rerun the required acceptance through the named interface. Unit, mock, or smoke evidence cannot replace a required real or production-equivalent path.
5. Request independent review when risk, breadth, or the acceptance contract warrants it. The main agent still owns scope, cleanup, acceptance, and proof.
6. Write `## Finalization proof` in the issue using the exact fields and delta-mapping grammar in `.codex/agents/issue-tracker.md`. Re-run `inspect` if cleanup or review changed the worktree.
7. Run the entrypoint's `finalize` command. It validates the current baseline-relative delta and proof, then atomically changes the existing completion oracle to `Completion: done`. Never make that edit directly.

The shared `Stop` hook is only a backstop. An active open issue may end a normal turn. An active done issue without a valid proof, with an unmapped unit, without its issue-key claim, or with post-proof, index, or ignored-path drift is blocked. A valid finalized issue is allowed and its temporary baseline receipt and claim are removed. With no active formal issue receipt, a direct small change uses an ordinary final diff check and does not enter this gate.

Before declaring done, inspect the final issue-attributable delta and map every acceptance criterion to evidence. Do not invoke another workflow to repair unrelated findings. Do not commit, stage unrelated changes, or delete existing files unless the user or task explicitly authorizes it.
