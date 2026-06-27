# Source Matrix

Use this backstage ledger for strong claims in complex teaching work. Student pages may summarize from it, but should not expose this file by default.

| claim_id | claim | layer | source | anchor | evidence_summary | boundary | confidence | used_in | misread_risk | review_status |
|---|---|---|---|---|---|---|---|---|---|---|
| C-0001 | Replace with one strong claim. | paper_fact | Source title or path. | Section/Figure/Table/Page/Function. | What the source directly supports. | What this does not prove. | high | lessons/0001-example.html | How a learner may overread it. | pending |

## Allowed Layers

- `paper_fact`
- `lineage_context`
- `course_reconstruction`
- `engineering_transfer`
- `unknown`

## Review Rules

- Every strong student-facing claim needs a row.
- `unknown` claims should usually appear as boundaries, not positive assertions.
- `lineage_context` must not imply the target paper or repo used that method.
- `course_reconstruction` must be worded as teaching explanation.
- `engineering_transfer` must state the condition required for transfer.
