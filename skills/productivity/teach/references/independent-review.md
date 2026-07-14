# Independent Review

Use a fresh reviewer for meaningful multi-page or evidence risk, user-requested review, and both Ultra tracer and final stages. Give the reviewer final learner-facing artifacts, supporting Markdown, and the minimum Course Contract context needed for the review.

## Review Prompt

```text
Read the supplied Course Contract, final HTML, and supporting Markdown as an
independent course reviewer.

Begin with the publication gate. Enumerate every declared learner-facing
artifact and determine whether each final HTML file contains its assigned
primary content and ordinary navigation through the declared static target.

Then report:

1. the course main trunk in three direct sentences;
2. the learner's starting point, prerequisite bridge, and first likely difficulty;
3. the path from explanation through practice, feedback, and capstone;
4. source support, evidence roles, formula or process fidelity, and scope;
5. content objects lost, compressed, or altered during publication;
6. terminology, structure, and evidence drift across pages;
7. visual hierarchy, scanability, subject fit, information density, and long-form quality;
8. the educational value and static meaning of enhanced interactions;
9. pages whose apparent completion comes from template structure while their
   assigned explanation, evidence, practice, feedback, or design remains thin;
10. rhetorical contrast that can become a direct positive proposition;
11. concrete repairs ordered by learner impact.

Separate sourced facts, derived results, observations, teaching explanations,
and transfer guidance. Return concise findings in Markdown.
```

## Review Result

Store an applicable final `review.md` with:

```md
# Course Review

## Publication

## Main Trunk and Prerequisites

## Learning and Content Fidelity

## Sources, Formulas, and Scope

## Design and Information Density

## Enhancement

## Direct Prose

## Capstone

## Repairs
```

Raw subagent review stays in the session temporary workspace. The final learner-facing review contains accepted findings, completed repairs, remaining limitations, and gate results.
