---
name: pr
description: Draft or update a pull request description when the user has asked for PR text or creation, using only observed behavior, validation, and actual merge risks. Does not authorize PR mutation by itself.
license: MIT
---

# Pull Request Description

Explain the change for a reviewer, not the agent's process. This skill formats
a PR description when the task already calls for one. It does not authorize
creating, editing, pushing, or merging a pull request.

Adapted from Matt Pocock's `pr` and DeepSeek Harness's
`dsh-pr-description`; use the consuming repository's PR template and issue
conventions when present, not their project-specific sections or gates.

Read the actual diff, user request or issue, and checks that ran. Present:

1. **Why and what:** the user-visible change, with the smallest useful view of
   the affected behavior or interface. A concise paragraph often suffices;
   use a diagram only if it clarifies the change.
2. **Evidence:** the relevant commands or observations and their actual results.
   Separate passing checks, failed checks, pending CI, and unverified runtime
   conditions. Never use file hashes or process exit alone as behavioral proof.
3. **Merge risk:** affected consumers, compatibility, irreversible actions, or
   migrations only when the diff actually has them. State unresolved risks
   rather than filling a template with invented assurances.

Follow the existing PR template without adding a compulsory issue reference,
AI-usage estimate, GIF, or full test matrix. If the user requests an update,
re-read the current diff and description first so stale claims are removed.
