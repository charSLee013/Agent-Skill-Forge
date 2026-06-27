# Deep Paper Course

Use this mode for one or more papers, PDFs, technical reports, model reports, benchmark tables, or claims that depend on published evidence.

## Two-Stage Shape

1. Master the paper and evidence chain.
2. Only then transfer understanding to engineering, research planning, or system diagnosis.

Do not push the learner into engineering decisions before they can restate the paper's main line and evidence boundaries.

## Required Artifacts

- `course-map.html`: reading path and lesson sequence.
- `artifacts/source-matrix.md`: claim layer, source, anchor, boundary, confidence.
- `lessons/*.html`: layered explanations, not one giant summary.
- `reference/*.html`: tables, term maps, benchmark maps, or review cards.
- `artifacts/misconception-audits/*.md`: weak-reader and evidence review.
- `manifest.json` when there are multiple artifacts or phases.

## Reading Path

For each paper:

- Identify the question the paper tries to answer.
- Map the abstract/introduction to the method and evidence.
- Put key figures and tables into the source matrix or reading path.
- Explain evaluation dimensions and metric scales before comparing results.
- Mark which claims are paper facts versus reconstruction.

## Multi-Paper Courses

When multiple papers are involved:

- Separate target papers from lineage papers.
- Do not let lineage papers become proof that the target paper used a method.
- Build a concept graph only after each paper's core evidence is mapped.
- Track contradictions, incompatible metrics, and incomparable benchmark scales.

## Closed-Source Reports

Closed-source or incomplete reports need explicit public-boundary handling:

- What the report says.
- What it does not say.
- What related work can help explain.
- What related work cannot prove.
- What the course reconstructs for learning.

## Student Page Rules

Student pages should begin with:

- What to remember now.
- Why this section matters.
- How it connects to the paper's main evidence chain.
- What not to overclaim.

Avoid dumping figure/table anchors, local file names, or audit notes into the main narrative. Put detailed evidence in a collapsed appendix or backstage source matrix.
