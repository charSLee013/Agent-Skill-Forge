# Evidence Layer

The evidence layer prevents a course from turning useful inference into fake fact.

## Claim Layers

Every strong claim in complex modes must use one of these layers:

| Layer | Meaning | Student-Page Rule |
|---|---|---|
| `paper_fact` | Directly supported by the target paper/report/source. | Can appear as fact with clear wording. |
| `lineage_context` | Related work, ecosystem context, or historical background. | Must not imply the target source used it. |
| `course_reconstruction` | Teacher's restructuring to make evidence learnable. | Must be signaled as explanation, not original claim. |
| `engineering_transfer` | Applying course understanding to the learner's system. | Must be separated from source facts. |
| `unknown` | Public evidence is missing, ambiguous, or insufficient. | Must be stated as boundary or omitted. |

## Source Matrix First

For `deep-paper`, `repo-course`, `research-route`, and `long-course`, create or update `artifacts/source-matrix.md` before writing student-facing pages.

Required fields:

- `claim_id`
- `claim`
- `layer`
- `source`
- `anchor`
- `evidence_summary`
- `boundary`
- `confidence`
- `used_in`
- `misread_risk`
- `review_status`

## Anchors

Use the strongest available anchor:

- Papers: page, section, figure, table, equation, appendix.
- Repos: file path, function/class/module, commit if relevant.
- External docs: URL and heading.
- Experiments: run ID, command, dataset, metric, output path.

Backstage anchors may include local paths and line numbers. Student pages should not expose them by default.

## Visible Evidence

For `evidence-intensive`, `report-grade`, and `expert-audited` work, major student-facing claims need learner-friendly visible evidence. Use a compact claim/evidence/boundary/confidence block in the main page or near the relevant section.

Detailed anchors still belong in the source matrix or collapsed appendix. The learner should not need raw paths, line numbers, or audit notes to understand why a claim is credible.

## Strong Claim Test

A claim is "strong" if a learner may use it to make a technical, research, implementation, or evaluation decision. Strong claims need a source matrix entry.

Examples:

- "The paper proves X beats Y on metric Z" -> strong.
- "This repo's request flow goes through module A before B" -> strong.
- "This design likely transfers to your system" -> strong.
- "Remember this term" -> usually not strong unless contested.

## Boundary Language

Use plain boundary language:

- "The paper reports..."
- "The related work suggests..."
- "For learning, we reconstruct this as..."
- "For your system, this transfers only if..."
- "The public report does not say..."

Do not let citations hide inference. A cited paragraph can support the evidence, but the layer tells the learner what kind of statement it is.
