---
name: issues-to-execution-brief
description: Compile selected implementation issues into one decision-complete execution brief for a fresh expert.
argument-hint: "Which issue paths or feature directory should be compiled?"
disable-model-invocation: true
---

# Issues to Execution Brief

Compile implementation issues into a cold-start brief for a fresh expert. Treat this
as semantics-preserving compilation: reorganize and co-locate source facts, but do not
make new product or architecture decisions, widen scope, or weaken evidence.

## Process

### 1. Resolve the source set

Use exact issue paths supplied by the user or already established in the conversation.
Read every selected issue in full, including comments. When given a feature directory,
select its open implementation issues under `issues/` and report completed issues as
excluded. Use tracker fields, not directory placement alone, to distinguish legacy
decision issues from implementation issues. If no executable issue remains, stop and
report that result. Do not silently choose between multiple features or similarly
named issues.

Read the local tracker conventions when present. Follow dependencies to their exact
paths, and read applicable `AGENTS.md`, domain context, maps, PRDs, and source files
named by the issues far enough to resolve their contracts. Prefer references by path
over copying whole documents into the brief.

Complete this step only when every selected issue has an exact path, current state,
and fully resolved dependency identity.

### 2. Build the contract ledger

Capture for every selected issue:

- why the change exists and the observable end state;
- required behavior and deliverables;
- dependency order;
- in-scope and excluded work;
- implementation constraints and preservation requirements;
- external calls, destructive effects, authorization, and safety gates;
- every acceptance criterion and its original evidence oracle;
- required completion report facts.

Trace each source acceptance criterion to exactly one place in the brief. Preserve
exact paths, identifiers, commands, limits, ordering rules, and evidence strength.
Keep qualitative review as direct inspection and real-path evidence as real-path
evidence; never replace either with length, keyword, score, mock, or structural
proxies.

Complete this step only when every source criterion and constraint is represented and
no source statements conflict. If authoritative documents conflict, identify the
paths and statements and stop.

### 3. Gate execution readiness

Order the selected issues topologically. An unresolved blocker inside the selected
set appears earlier in the brief. An unresolved blocker outside the selected set,
missing authority for a side effect, `needs-info` state, or unresolved product choice
blocks compilation; report the smallest set of facts or questions needed to proceed.

Treat the recipient as a fresh implementation agent unless the user names a human
recipient. Require `ready-for-agent` for the default recipient and `ready-for-human`
for a named human recipient when the tracker defines those states. A completed,
`wontfix`, `needs-triage`, `needs-info`, or recipient-incompatible issue is not
executable without explicit user direction.

Complete this step only when the recipient can execute the entire selected set without
inventing a decision or obtaining unstated authority.

### 4. Compile one execution brief

Return one copy-ready fenced text block in the user's language. State explicitly that
it is execution-requirement text, not a shell command. Consolidate multiple selected
issues into one brief by default and preserve their dependency order.

Use this section order, omitting only a section that is genuinely inapplicable:

```text
Task: <imperative title>

This is execution-requirement text for an implementation expert, not a shell command.

Background
<current state, root cause, downstream goal, and why the issue set exists>

Objective and completion boundary
<observable final state and the point at which work is complete>

Sources of truth and applicable rules
<exact issue and governing document paths, precedence, and required preflight reads>

Issue slices and execution order
1. <exact issue path>
   Dependency: <exact blocker path or none>
   Deliverable: <behavior to implement>
   Acceptance: <observable criteria and original evidence oracle>

Change scope
<approved files, systems, records, and behaviors>

Constraints and non-goals
<preservation rules, prohibited expansion, compatibility decisions, and exclusions>

Authorized side effects and safety gates
<network calls, writes, deletion, costs, environment, limits, and stop conditions>

Verification
<actual entrypoints, artifacts, state comparisons, direct content review, and final checks>

Completion report
<changed files, commands and outcomes, artifacts, side effects, and remaining risks>
```

Use commands only when the sources require them or repository inspection establishes
the exact command. Give the expert implementation instructions, not a request to
re-plan the approved issues. Do not modify or close issue files while producing the
brief.

Complete this step only when the result is one self-contained execution brief rather
than a summary, handoff note, plan, or command line.

### 5. Run the cold-start audit

Assume the recipient has the repository, the brief, and its referenced issue paths,
but none of the prior conversation. Check the brief against the contract ledger for:

- an unmapped acceptance criterion or non-goal;
- an omitted dependency, side effect, authorization, or stop condition;
- invented scope, compatibility, commands, or evidence;
- qualitative acceptance replaced by a mechanical proxy;
- wording that makes the recipient choose product intent;
- wording that could be mistaken for a terminal command.

Revise until all checks pass. When unblocked, output only the copy-ready brief. When
blocked, output only the blocking facts and questions; do not emit a partial brief.
