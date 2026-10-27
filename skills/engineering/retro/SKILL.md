---
name: retro
description: Examine a completed or interrupted coding session for concrete improvements to the agent's working environment.
license: MIT
argument-hint: "Which session or failure should be reviewed?"
disable-model-invocation: true
---

# Retrospective

The user has asked to examine how the work went. Deliver an evidence-backed
recommendation, not another implementation phase. Adapted from Matt Pocock's
`retro` while keeping this repository's authorization and artifact boundaries.

Read the specified session or current conversation, its actual diffs and
checks, and the applicable repository rules. Identify where navigation,
missing information, an ineffective check, oversized instructions, or a
repeated tool call materially changed the outcome. Separate a product bug
from an environment defect; a one-off mistake is not automatically a new
standing rule, hook, or harness.

For each supported candidate state what happened, the smallest intervention,
what it would have changed, and its ongoing maintenance cost. Check existing
tools and rules first. Prefer a narrow deterministic existing check for a
mechanical recurring failure; put genuine judgment in its owning guidance.
Only propose another skill when its independently discoverable job is not
already owned. An unsuccessful review must not be reported as completed work.

Return at most a few high-impact findings and any contrary evidence. Do not
write an AGENTS.md rule, test, issue, memory file, or report without the user's
separate authorization. No improvement candidate is a condition for declaring
the original coding task complete.
