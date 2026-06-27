# Local Issue Workspace: Codex Agents

Issues, PRDs, and triage notes for this repo live as local markdown files under `.codex/agents/`.

## Conventions

- One feature per directory: `.codex/agents/work/<feature-slug>/`
- The PRD is `.codex/agents/work/<feature-slug>/PRD.md`
- Implementation issues are `.codex/agents/work/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading
- `.codex/` is private local agent state. Keep it out of git with `.git/info/exclude`.

## When a skill says "publish to the local issue workspace"

Create a new file under `.codex/agents/work/<feature-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the local path directly.
