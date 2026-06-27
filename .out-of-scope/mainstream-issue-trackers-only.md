# External issue tracker integrations are out of scope

`setup-matt-pocock-skills` only offers first-class support for the local `.codex/agents/` issue workspace. Requests to add external issue tracker integrations are out of scope.

## Why this is out of scope

Every external issue tracker backend hard-codes a CLI or API shape into the skills (commands, flags, output parsing). Each backend is permanent maintenance surface — it has to keep working as the tool evolves, and it has to keep being tested against `/to-prd`, `/to-issues`, `/triage`, and friends.

The core workflow now avoids that surface entirely: PRDs, issues, and triage notes are local markdown under `.codex/agents/`. Teams that need external syncing can build it outside the core skills.

## Prior requests

- #99 — "Add dex as an issue tracker backend"
