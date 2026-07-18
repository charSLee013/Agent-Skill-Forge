# Local Issue Workspace: Codex Agents

Decision maps, issues, PRDs, and triage notes for this repo live as local markdown files under `.codex/agents/`.

## Conventions

- One feature per directory: `.codex/agents/work/<feature-slug>/`
- The PRD is `.codex/agents/work/<feature-slug>/PRD.md`
- Implementation issues are `.codex/agents/work/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading
- `.codex/` is private local agent state. Keep it out of git with `.git/info/exclude`.

## When a skill says "publish to the local issue workspace"

Create a new file under `.codex/agents/work/<feature-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant issue"

Read the file at the referenced path. The user will normally pass the local path directly.

## Wayfinding operations

Wayfinding is a user-invoked decision-map phase for work that spans sessions and still has material decisions open. It uses the same local workspace; it does not add another tracker.

- Map: .codex/agents/work/<feature-slug>/MAP.md
- Decision issues: .codex/agents/work/<feature-slug>/issues/<NN>-<slug>.md
- Map sections: Destination, Notes, Decisions so far, Not yet specified, and Out of scope
- Decision fields: Wayfinder type (research, prototype, grilling, or task), Wayfinder status (open, claimed, resolved, or out-of-scope), optional Claimed by, and Blocked by
- If an issue is intentionally handed to triage, its existing Status line remains the triage state. Wayfinder status must not replace or reinterpret it.
- A decision issue is unblocked when every referenced issue in Blocked by has Wayfinder status: resolved.
- The frontier is the first open, unblocked, unclaimed decision issue by number. Claim it by writing Wayfinder status: claimed and Claimed by before doing work.
- Resolve an issue by appending the answer under an Answer heading, recording non-sensitive evidence paths or references, setting Wayfinder status: resolved, and adding a one-line gist with a link to the issue under Decisions so far in MAP.md.
- If a decision is outside the destination, set Wayfinder status: out-of-scope and record the reason under Out of scope instead of resolving it as part of the route.

Use only the local .codex/agents/ workspace and the existing triage state machine. Do not add a second status machine or another tracker.
