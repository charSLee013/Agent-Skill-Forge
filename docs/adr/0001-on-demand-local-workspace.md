# On-demand local workspace

Planning artifacts live under the consuming project's private `.codex/agents/`
workspace. Creating a requested specification, task breakdown, or decision map
does not require running a separate setup workflow.

Existing local workspace, label, and domain configuration takes precedence.
When configuration is absent, consumers read the shipped conventions in
`setup-agent-skills/issue-tracker-local.md`, `triage-labels.md`, and `domain.md`.
They create only the authorized artifact and necessary directories. Ambiguous
custom labels, output collisions, and unresolved task decisions still require
clarification; a missing configuration file alone does not.

For Git repositories, use the local exclude file located by Git to keep
`.codex/agents/` private. Do not rewrite project Agent instructions or create
empty configuration as a side effect of planning.

`setup-agent-skills` remains manually selected for explicit customization and
legacy decision-layout migration. The existing issue fields, dependency meaning,
and legacy reading support remain intact.

This replaces the earlier hard-dependency setup requirement. Default conventions
are sufficient for ordinary planning; requiring full setup also imposed changes
to project instructions that the planning task did not need.
