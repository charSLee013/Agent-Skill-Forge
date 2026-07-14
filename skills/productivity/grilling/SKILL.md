---
name: grilling
description: Find the decision trunk of a plan or design through a small number of high-leverage questions, then fill reversible details with explicit defaults. Use when the user wants to stress-test an idea before building or asks for a grill session.
---

# Grilling

Build enough shared understanding to continue planning, designing, or implementing with minimal user effort.

Think in four moves:

- **Trunk**: identify the few decisions that shape the whole plan.
- **Prune**: investigate discoverable facts and set aside low-impact branches.
- **Backfill**: choose explicit defaults for reversible details.
- **Calibrate**: let the user correct the defaults in one pass.

## 1. Find the trunk

Read the conversation, codebase, and available documents before asking for information. Derive the goal, success criteria, necessary preconditions, major constraints, and irreversible risks from first principles.

When the trunk is unclear, present two to four materially different scenarios. Put the recommended scenario first and explain the recommendation briefly. Ask the user to choose the closest fit. When the user has already supplied a clear scenario, adopt it and continue.

Complete this step when one working trunk is established.

## 2. Ask for leverage

Classify every candidate question before asking it:

| Candidate | Action |
|---|---|
| Its answer can change the goal, scope, architecture, major risk, irreversible trade-off, or acceptance criteria | Ask the user |
| The answer is available from code, documents, or prior context | Investigate |
| The choice is low-impact and easy to reverse | Backfill a reasonable default |
| The decision belongs to a later phase | Defer it explicitly |
| It conflicts with an established decision | Ask one repair question |
| Its answer would not materially change the plan | Prune it |

Ask exactly one highest-leverage question at a time. Include a recommended answer and a brief reason. Wait for the answer before continuing.

After each answer, quietly recompute what is established, what remains assumed, whether a conflict exists, and which unknown has the most decision leverage. Show the resulting recommendation or next question rather than the private reasoning process.

Complete this step when the goal, success criteria, trunk, core scope, major constraints, meaningful trade-offs, and irreversible risks are clear, and every remaining unknown can be investigated, backfilled, deferred, or changed cheaply. Use this completion criterion instead of a fixed question count.

## 3. Backfill and calibrate

Choose reasonable defaults for the remaining details. Present a compact decision summary under these headings:

- **Established trunk**
- **Backfilled defaults**
- **Deferred decisions**

Ask the user to identify only the defaults that do not fit. Apply those corrections, resolve any resulting trunk conflict with one question, and finish with a decision-ready summary.

## Strong negative feedback

When forceful user feedback indicates that the current answer or process missed their intent, pause the interview and repair it immediately:

1. Name the specific mistake, its behavioral cause, and the immediate correction in a compact response.
2. Apply the correction to the current work.
3. Distill one short, positive, observable rule that would prevent the same mistake.
4. Offer the exact rule and target path for persistence in the active project's `AGENTS.md`.

Ground the diagnosis in the preceding exchange. When the mismatch remains uncertain after reviewing it, state the most likely mismatch and ask one concise calibration question.

Persist a lesson only when it is reusable across later project work, useful to other agents, free of private or emotional details, and consistent with existing instructions. Check for duplication and conflicts first. Locate the nearest applicable `AGENTS.md`; when none exists, propose creating one at the project root. Write or create the file only after the user explicitly approves the exact rule and path.

When no active project exists, keep the lesson in the conversation and continue with the corrected behavior.
