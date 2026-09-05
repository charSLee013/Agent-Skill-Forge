# Engineering

Use a clear coding request directly with `implement`. Clarify material choices
with `grilling` when needed, then continue work already authorized by the user.
Requested specifications, task decomposition, and cross-session decision maps
use `to-prd`, `to-issues`, and `wayfinder` respectively; they are not mandatory
stages of every change.

| Skill | Invocation | Purpose |
|---|---|---|
| [implement](./implement/SKILL.md) | Model or user | Complete requested code changes, fixes, or redesigns with relevant verification. |
| [to-prd](./to-prd/SKILL.md) | Model or user | Write a requested specification from established requirements. |
| [to-issues](./to-issues/SKILL.md) | Model or user | Split a clear plan into verifiable implementation issues. |
| [wayfinder](./wayfinder/SKILL.md) | Model or user | Maintain or resume authorized cross-session decision work. |
| [diagnosing-bugs](./diagnosing-bugs/SKILL.md) | Model or user | Diagnose a hard or uncertain failure within the requested scope. |
| [real-path-verification](./real-path-verification/SKILL.md) | Model or user | Verify an approved criterion through its selected real runtime path. |
| [domain-modeling](./domain-modeling/SKILL.md) | Model or user | Resolve domain terms and record authorized durable decisions. |
| [codebase-design](./codebase-design/SKILL.md) | Model or user | Provide module design methods for explicit interface or architecture work. |
| [resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md) | Model or user | Resolve an active merge or rebase conflict while preserving both intentions. |
| [triage](./triage/SKILL.md) | User only | Triage local issues while preserving separate implementation completion state. |
| [improve-codebase-architecture](./improve-codebase-architecture/SKILL.md) | User only | Report architecture opportunities and follow the user's selected scope. |
| [find-simplifications](./find-simplifications/SKILL.md) | User only | Audit evidence-backed simplification opportunities without changing code. |
| [setup-agent-skills](./setup-agent-skills/SKILL.md) | User only | Customize workspace configuration or migrate a legacy decision layout. |
| [issues-to-execution-brief](./issues-to-execution-brief/SKILL.md) | User only | Compile selected executable issues into a brief for a fresh session. |
| [prototype](./prototype/SKILL.md) | User only | Build a disposable executable experiment for a concrete design question. |
| [zoom-out](./zoom-out/SKILL.md) | User only | Map unfamiliar code and its callers in the surrounding system. |

Planning creates only requested artifacts under the private local
`.codex/agents/` workspace. Existing configuration takes precedence; shipped
defaults handle its absence. Explicit setup remains available for customization
and legacy layout migration.

Read-only verification can use `implement`'s `references/evidence.md` without
starting implementation. Resolve shared references through the host's skill
paths or the source plugin manifest, because installation flattens the buckets.

Model invocation does not authorize additional work. Continue across phases
when the user already requested the subsequent result; finish at the requested
deliverable or a real unresolved decision, permission, or dependency.
