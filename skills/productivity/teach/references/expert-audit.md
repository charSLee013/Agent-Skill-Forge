# Expert Audit

Use expert audit for `report-grade` and `expert-audited` courses, and for any artifact that must survive a serious reader's objections.

## Lenses

Add these to the standard misconception audit:

| Lens | Question | Blocks When |
|---|---|---|
| Skeptical expert reader | Why should I believe this, and what exactly is the boundary? | Major claims lack visible evidence, precision, or boundary language. |
| Subject reviewer | Would a reader familiar with this subject reject the artifact as shallow, imprecise, or structurally wrong? | The artifact substitutes surface coverage for the subject's real structure. |

## Hard Failure Conditions

Fail the phase when:

- Main pages lack a clear claim summary or scope.
- Major claims lack visible evidence.
- Structure follows artifact order or file paths instead of the subject's learning structure.
- Code, formulas, diagrams, or procedures appear without variable/state/step explanation.
- Dynamic or multi-dimensional mechanisms lack a visual, table, step trace, or explicit reason why prose is enough.
- Boundaries are vague negations instead of positive scope and evidence limits.
- The audit passes without naming any concrete risk or hard fix.

## Repair Rule

Repair blocking issues before creating more course material. Do not mark the issue as a future improvement when it affects the learner's ability to trust, restate, or transfer the material.
