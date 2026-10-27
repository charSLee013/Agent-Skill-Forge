---
name: code-review
description: Review current changes, a branch, or a PR for defects, regressions, scope drift, and missing behavioral evidence. Use when asked to review; a review request remains read-only.
license: MIT
---

# Code Review

Find actionable defects in the change the user named. Review does not authorize
fixes, a commit, or a new testing project.

Adapted from Matt Pocock's `code-review` and DeepSeek Harness's
`dsh-code-review`; preserve their separate requirement and engineering-quality
perspectives without importing their mandatory subagent or DSH review gates.

## Fix the comparison

Read the user's requested scope and inspect the working tree. For an explicit
commit, branch, or PR, resolve its actual base and head before examining its
diff. For an unspecified local review, include staged, unstaged, and relevant
untracked work; do not silently restrict review to committed changes. Report
an invalid or empty comparison rather than inventing a reference.

Read the originating request, issue, or specification when one exists. If no
specification exists, review observable behavior against the user's stated
intent and mark missing requirements as unknown rather than forcing a PRD.
Read relevant repository rules and affected callers before judging isolated
diff hunks.

## Judge two questions

1. **Behavior:** does the change actually satisfy its requested behavior,
   including errors, cancellation, compatibility, and relevant runtime paths?
   Identify omitted or unrelated behavior and evidence that fails to establish
   the acceptance condition.
2. **Engineering:** does it preserve the project's documented conventions and
   reasonable ownership, security, lifecycle, and maintenance properties?
   Check actual consumers before calling an abstraction necessary or dead.
   Distinguish a documented requirement from a judgment call.

For changed failure paths, read `error-handling` for the affected boundary;
for resource-owning or flaky tests, read `test-reliability`. For prose, consult
the relevant `prose-standard` or `doc-standards` reference through the host's
discovered skill paths. Reading a manual skill is not permission to invoke its
workflow or edit its files.

Report findings first, ordered by impact, with a precise path/line, causal
explanation, and evidence. Separate requirements, judgment calls, and test
gaps. If nothing actionable is found, say so and identify remaining coverage
limits. Do not claim independent subagent review unless it actually occurred.
