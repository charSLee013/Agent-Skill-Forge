# Agent Skill Forge

A neutral collection of agent skills loaded by supported agent runtimes. Skills are organized into buckets and consumed by per-repo configuration emitted by `/setup-agent-skills`.

## Language

**Local issue workspace**:
The repo-local `.codex/agents/` workspace that stores PRDs, implementation issues, and triage notes as markdown files.
_Avoid_: issue tracker, backlog manager, backlog backend, issue host

**Issue**:
A single tracked unit of work inside the **Local issue workspace** — a bug, task, PRD, or slice produced by `to-issues`.
_Avoid_: ticket (use only when quoting external systems that call them tickets)

**Triage role**:
A canonical state-machine label applied to an **Issue** during triage (e.g. `needs-triage`, `ready-for-agent`). Each role maps to a local status string via `.codex/agents/triage-labels.md`.

## Relationships

- A **Local issue workspace** holds many **Issues**
- An **Issue** carries one **Triage role** at a time

## Flagged ambiguities

- "issue tracker" previously meant multiple external and local storage surfaces. Resolved: these skills now use the **Local issue workspace** only.
- "backlog" was previously used to mean both the *tool* hosting issues and the *body of work* inside it — resolved: use **Local issue workspace** for the storage surface; "backlog" is no longer used as a domain term.
- "backlog backend" / "backlog manager" — resolved: collapsed into **Local issue workspace**.
