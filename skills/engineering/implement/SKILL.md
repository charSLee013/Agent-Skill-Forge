---
name: implement
description: "Implement a piece of work based on a PRD or set of issues."
disable-model-invocation: true
---

Implement the work described by the user in the PRD or issues.

Treat the user-approved PRD, issue, or task contract as the source of truth. Do not add adjacent behavior, refactors, tests, validation, documentation, or commits that are not required by it.

When an implementation issue has `Blocked by`, resolve each path from that issue's feature directory. A `decisions/` target requires `Wayfinder status: resolved`. An `issues/` target carrying both top-level Wayfinder fields is a legacy decision and uses the same oracle; every other `issues/` target requires `Completion: done`, with a missing field treated as `Completion: open`. Stop before implementation if any target is missing, ambiguous, outside the feature, or still blocked. Triage `Status` is not a completion oracle.

Run the existing checks relevant to the changed behavior. Do not create a test file for documentation, comments, copy, or non-behavioral metadata. Run the full suite only when repository policy, the task, or the breadth of the change requires it.

If the acceptance criteria require a real runtime path or production-equivalent proof, invoke /real-path-verification as the verification phase. If a parent work item has three or more slices, recommend one real-path run at final integration; do not run it once per slice unless the issue explicitly requires that.

Before declaring done, inspect the final diff and map every acceptance criterion to evidence. If the source is an implementation issue, add or change its field to `Completion: done` only after that evidence is complete. Do not invoke another workflow to repair unrelated findings. Do not commit, stage unrelated changes, or delete existing files unless the user or task explicitly authorizes it.
