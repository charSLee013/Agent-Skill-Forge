# Task Modes

Use task modes to avoid applying the lightweight lesson workflow to a research-grade course.

## Mode Selection

| Mode | Fit | Do Not Use When |
|---|---|---|
| `concept` | The learner needs one idea explained and remembered. | The user asks for complete mastery, papers, repo archaeology, or a multi-artifact course. |
| `skill` | The learner needs practice, feedback, and transfer to action. | The task is mostly evidence reconstruction or source-bound research. |
| `deep-paper` | The input is one or more papers, PDFs, technical reports, figures, tables, benchmarks, or closed-source model reports. | The user only wants a surface summary. |
| `repo-course` | A codebase is the object being taught. | The request is only code review or refactoring. |
| `research-route` | The user wants a path toward research, reproduction, open problems, or system migration. | There is no research or transfer goal. |
| `long-course` | The course spans phases, many artifacts, HTML proof, subagent review, or final artifact survival. | A single low-stakes lesson is enough. |

## Routing Rules

- If the user says "complete", "deep", "from shallow to deep", "paper", "PDF", "repo", "research", "migration", "proof", or "weak reader", prefer the more rigorous mode.
- `long-course` is a governance wrapper. It can wrap `deep-paper`, `repo-course`, or `research-route`.
- Do not ask the user to choose a mode unless two modes imply materially different deliverables.

## Lightweight Modes

For `concept` and `skill`:

- Keep the workspace stateful: mission, resources, learning records, glossary, notes.
- Use trusted sources, but do not force a full source matrix unless the claims are high-stakes or contested.
- Prefer short reachable lessons, retrieval prompts, worked examples, and immediate feedback.
- Record demonstrated understanding, corrected misconceptions, and mission shifts in `learning-records/`.

## Complex Modes

For `deep-paper`, `repo-course`, `research-route`, and `long-course`:

- Build the truth layer before student pages.
- Maintain an explicit evidence layer for strong claims.
- Separate learner-facing pages from backstage artifacts.
- Run misconception audit before moving to the next phase.
- Verify HTML artifacts if generated.
- Maintain a manifest and final proof loop when the course has multiple artifacts.

## Complete Mastery

"Complete mastery" never means one giant document. It means a navigable course bundle:

- Course map
- Layered lessons
- Reference pages
- Retrieval/review prompts
- Evidence/source matrix
- Misconception audits
- Manifest
- Proof artifacts
