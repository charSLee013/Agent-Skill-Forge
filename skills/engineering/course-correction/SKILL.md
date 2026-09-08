---
name: course-correction
description: Stop and repair agent work when execution has drifted beyond the user's goal, produced unauthorized artifacts, or continued after the useful work was done. Use when the agent or user notices scope creep, test-project bloat, tool fixation, weak delegation, or a partial result being presented as completion.
---

# Course Correction

Stop the drifting work immediately. This skill is for a general execution failure,
not for one file type or one testing style. It applies when the agent has started
serving its own process instead of the user's outcome: for example, an experiment
keeps growing after it answered the question, a temporary harness becomes a
project, repeated checks add no evidence, a subagent's weak result is forwarded,
or local progress is presented as the completed task.

## Name the failure plainly

State the actual failure in one or two sentences. Use direct language such as:
"I expanded the work beyond your request and created artifacts that were not part
of the agreed deliverable." Do not defend the choice, blame the tool, describe
the failure as inevitable, or bury the apology under a process report.

Separate four facts:

- the user's requested outcome and acceptance boundary;
- the last useful work that supports that outcome;
- the agent-added work that does not belong to it;
- what remains unknown, incomplete, or unverified.

Apologize directly for the agent's mistake. The apology must be short and factual;
the repair is the evidence of accountability.

## Stop the cause, not only the symptom

Before cleanup, stop the behavior that caused the drift:

- end the runaway experiment, repeated test loop, polling process, or delegation;
- stop creating new files, reports, fixtures, wrappers, or phases;
- return to the approved goal and decide whether the useful work already answers it;
- do not start a replacement harness merely to justify the cleanup.

If the user asks for diagnosis only, keep the repository unchanged. If the user
asks for repair, continue with the smallest authorized repair after cleanup.

## Clean safely

Compare the current state with the task-start baseline and inspect every candidate
artifact before removing it. Delete only files, directories, processes, or external
resources that this agent created during the drift and that have no approved
deliverable role. This includes oversized temporary test projects, generated logs,
scratch scripts, redundant reports, and abandoned fixtures when ownership is clear.

Never delete pre-existing user work, ambiguous files, shared infrastructure, or an
artifact that may contain user data. If ownership is uncertain, leave it in place,
identify it precisely, and ask or report the boundary. Do not use a broad recursive
cleanup command against a project root or home directory.

After cleanup, check that the intended source changes and user-owned changes remain,
that no process from the drift is still running, and that no temporary reference
was left in the deliverable.

## Verify without relapsing

Use the existing acceptance check or the cheapest sufficient observation. Do not
create a new test project, harness, mock, report, or benchmark unless the user has
explicitly authorized that artifact and it is necessary for the agreed acceptance.
Do not repeat a passing check without a new change, failure, or unresolved concern.

If the task is now complete, report the result and the evidence. If it is not
complete, report the exact unfinished condition and stop. Never call cleanup a
successful implementation, never claim a check that was not run, and never use a
partial check to imply full acceptance.

## Final response

Use the user's language and keep the response concise:

1. direct apology for the specific execution mistake;
2. what was stopped and what agent-owned artifacts were removed;
3. what intended work remains and what evidence supports it;
4. any files left because ownership was uncertain, or any unresolved blocker.

Do not provide a long justification, a self-congratulatory recovery story, or a
new menu of options. A failed repair is a failed repair; say so plainly.
