---
name: wayfinder
description: Plan work that spans multiple agent sessions while material decisions remain unresolved. Use only when a destination can be named but the route is still unclear and direct planning or implementation would require guessing.
disable-model-invocation: true
---

# Wayfinder

Use this skill as a user-invoked decision-map phase for genuinely large work. It creates a low-resolution map and sharp decision issues in the local .codex/agents/ workspace, then resolves one decision issue at a time until the route is clear.

Wayfinder plans by default. It does not implement the destination, create an implementation PRD, or split implementation slices until its map is clear.

## Entry gate

Enter only when all of these are true:

- the work is likely to span more than one agent session;
- a destination can be stated, but the route is not yet clear;
- an unresolved decision or investigation could change scope, architecture, major risk, or acceptance;
- no existing map already covers the destination;
- entering to-prd or implement now would force a material guess.

Bypass Wayfinder for a clear bounded request, a small documentation or metadata change, an already approved PRD or issue, a known bug path, or work that merely looks long but has no decision fog. Use grill-with-docs, to-prd, to-issues, or implement directly.

Before writing anything, read the relevant CONTEXT.md, ADRs, existing local issue artifacts, and any existing map. If a map already exists, use its work mode instead of creating another one.

## Local artifacts

Use one feature directory:

    .codex/agents/work/<feature-slug>/
    +-- MAP.md
    +-- issues/
        +-- 01-<decision>.md
        +-- 02-<decision>.md

MAP.md contains only:

- Destination: what reaching the end of the map means;
- Notes: domain language, skills, and standing constraints;
- Decisions so far: one-line gists with links to resolved decision issues;
- Not yet specified: in-scope uncertainty that is not sharp enough to make an issue;
- Out of scope: work explicitly ruled out.

Each decision issue contains:

- Wayfinder type: research, prototype, grilling, or task;
- Wayfinder status: open, claimed, resolved, or out-of-scope;
- Claimed by when work is claimed;
- Blocked by with local issue numbers when applicable;
- a Question heading;
- an Answer heading after resolution.

Keep the existing Status triage field separate. Add or change it only when the decision issue is deliberately handed to triage. Do not introduce tracker labels or change the meaning of ready-for-agent.

## Chart the map

1. Establish the destination from the user's goal, acceptance boundary, non-goals, and known constraints.
2. Explore breadth-first. Find the decisions that can change the destination, scope, architecture, major risk, or acceptance. Do not solve every branch before creating the map.
3. If the route is already clear, stop without creating a map and recommend the smallest next workflow.
4. Keep only questions that are sharp enough to state now as decision issues. Put foreseeable but unclear questions in Not yet specified; do not pre-slice the fog.
5. Show the proposed destination, first decision issues, dependencies, risk, and expected evidence. Write MAP.md and decision issues only after the user approves that scope.
6. Create only the issues that are currently sharp. Record blockers with Blocked by and stop charting. Do not resolve issues, implement the destination, or dispatch a batch of research work during charting.

## Work through the map

1. Load MAP.md, then read only the selected decision issue and the linked context needed for it.
2. Choose the user-named issue, or the first open, unblocked, unclaimed issue in numeric order.
3. Claim it before doing work by writing Wayfinder status: claimed and Claimed by.
4. Use one smallest applicable existing workflow for the question:
   - grilling or grill-with-docs for a material user decision or domain term;
   - zoom-out for unfamiliar callers and module boundaries;
   - codebase-design for an explicit interface or architecture decision;
   - diagnosing-bugs for an uncertain failure or root-cause decision;
   - prototype for a behavior, state, or UI decision that needs a concrete artifact;
   - an approved research capability for an external fact that blocks the decision;
   - a manual task only when a prerequisite must be completed before a decision can be made.
5. Keep the work limited to the question. Use existing commands and artifacts first. Put temporary experiments and research artifacts under the system temporary directory, not in the repository.
6. Record the answer, relevant non-sensitive evidence, unresolved uncertainty, and any newly sharp question. Set the issue to resolved or out-of-scope, then update Decisions so far or Out of scope in the map.
7. Create only newly surfaced issues that are now precise and in scope. Do not reopen resolved decisions without recording the changed premise.
8. Stop after one decision issue in the session. Recommend the next frontier issue or the next workflow; do not automatically chain multiple user-invoked skills or dispatch parallel subagents.

Research work requires an explicit user-approved question and scope. Use an existing specialized research capability only when it matches the subject. Keep one research issue in progress at a time and return its evidence before creating another.

## Exit to delivery

The map is clear only when:

- every created decision issue is resolved or out-of-scope;
- no open, unblocked, unclaimed frontier issue remains;
- the destination, scope, non-goals, major risks, and acceptance boundary are stable;
- the map contains decisions and pointers, not implementation detail;
- the next delivery workflow is explicit.

Then recommend exactly one handoff:

- use to-prd when a formal specification still needs to be synthesized;
- use to-issues when the approved plan needs independently verifiable implementation slices;
- use implement when the destination is already bounded and approved;
- use real-path-verification only later, when implementation acceptance requires real or production-equivalent execution.

Wayfinder may identify the next skill, but it does not invoke the next phase automatically.

## Boundaries

- Keep all artifacts in the local .codex/agents/ workspace.
- Use the existing local fields and file relationships; do not add another tracker, label family, dependency system, or vendor-specific setup command.
- Do not create tests, harnesses, CLIs, production changes, commits, or unrelated issues as part of charting.
- A task issue may perform an explicitly authorized prerequisite, but it is not permission to deliver the destination.
- Preserve project rules, user-approved scope, and the safety gates of any workflow used to resolve a decision.
