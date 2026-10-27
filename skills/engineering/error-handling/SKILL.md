---
name: error-handling
description: Analyze or design failure handling when a task involves partial effects, recovery, retries, background work, or user-visible error reports. Use only for the affected failure paths, not every routine edit.
license: MIT
---

# Error Handling

Determine what remains true after a failure before deciding to continue. This
discipline supports an authorized implementation, diagnosis, or review; it does
not authorize changes on a read-only request.

Adapted from DeepSeek Harness's `dsh-error-handling` at
`deepseek-ai/deepseek-harness@22ddee3792402c3e70ec5f86a63c3e3e895a2f60`.
Use the consuming project's error conventions, not DSH types or commands.

## Identify the boundary

- Name the operation, the owner of the state it changes, and the observable
  failure. Separate expected failures from unexpected defects without assuming
  every failure needs a new error type.
- Record whether effects are absent, partial, committed, or unknown. A caught
  exception or log line does not undo a mutation.
- Locate the owner of containment, cleanup, reporting, and any retry. Only the
  state owner can establish that dependent work is safe to continue.

## Choose the response

Reuse established structured errors when callers need to distinguish outcomes.
Preserve causes and handling-relevant details; do not branch on display text.
If the state is untrusted, stop dependent work or discard it. Retry only when
repetition is safe, cancellation is handled, and a finite operation has a
bounded attempt or time budget. Background work still owns its errors and
cleanup after its caller returns.

Report the affected operation, impact, uncertainty, and a safe next step at the
surface the user can actually observe. Do not claim a rollback, successful
retry, or safe continuation without evidence. Verify the resulting state and
visible outcome, not merely that an exception was caught.

For an implementation, change only the requested failure path and its direct
callers. For a review or diagnosis, report defects without editing. A missing
behavioral oracle remains unverified; it does not justify adding a new harness.
