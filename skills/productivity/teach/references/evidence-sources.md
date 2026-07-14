# Evidence and Sources

Connect every important course claim to the strongest domain-appropriate material. Agent research supplies the evidence base and records its provenance in supporting Markdown.

## Domain Evidence Ecology

Choose sources according to the expert task:

- local code, tests, runtime traces, and release artifacts for repository behavior;
- target papers, primary datasets, and official implementations for research claims;
- official documentation and standards for interfaces and procedures;
- primary records and source criticism for historical claims;
- authoritative recipes, food science, safety guidance, and kitchen trials for cooking;
- professional standards, measured outcomes, and observed practice for applied skills;
- trusted high-signal communities for practical context and unresolved questions.

Use the Course Contract to define the applicable evidence ecology before research expands.

## Source Note

Create `sources/{slug}.md` with:

```md
# {Source title}

## Source
{URL, path, identifier, version, date, or repository reference.}

## Role
{source | derived | observed | context | explanation | transfer}

## What It Supports
{The precise claim, behavior, definition, formula, data point, or example.}

## Teaching Use
{The lesson, explanation, comparison, exercise, or capstone that uses it.}

## Scope
{The setting, audience, version, assumptions, and applicable conditions.}
```

## Evidence Roles

- `source`: the cited material states or demonstrates the claim directly;
- `derived`: the course calculates or reconstructs the result from cited inputs;
- `observed`: a recorded experiment, execution, measurement, or inspection produced the result;
- `context`: surrounding history, terminology, or related work;
- `explanation`: a course reconstruction that makes the material learnable;
- `transfer`: guidance applied to the learner's target situation.

Place the role beside the relevant claim or content object.

## Formula and Data Fidelity

For formulas, record variables, shapes or units, assumptions, derivation source, one checked example, and scope. Use a worked reconstruction when the formula carries a learning dependency.

For data, record provenance, version or date, collection conditions, transformations, and whether the values are sourced, derived, observed, or synthetic. Give synthetic examples an explicit teaching role.

For repository configurations, distinguish reusable defaults, example values, runtime observations, and released model settings through their evidence roles and source paths.

## Positive Scope Language

Use direct statements:

- "This source supports the documented interface."
- "This derivation follows from the cited variables and assumptions."
- "This observation comes from the recorded execution."
- "This reconstruction teaches the mechanism."
- "This comparison applies to the source's stated conditions."
- "This transfer supports systems with the same constraint."

Record open evidence questions as research tasks. Give the learner a clear view of established facts, course derivations, observations, and transfer guidance.
