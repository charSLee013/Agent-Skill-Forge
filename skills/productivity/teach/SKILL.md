---
name: teach
description: Create learner-facing static HTML courses with supporting Markdown, capability-driven structure, source fidelity, browser review, and Standard or Ultra quality profiles. Use when a learner needs a concept, skill, paper, repository, research topic, or multi-step subject organized into a complete course.
---

# Teach

Create a course whose learner-facing artifacts are static HTML pages and supporting Markdown. Build every course around an observable capability, a domain-appropriate evidence base, and a path from the learner's starting point to the Course Contract's target judgment.

## Quality Profiles

Use **Standard** by default. Standard delivers a professional, complete, static course through one primary Agent workflow.

Recommend **Ultra** when the user requests top-tier, comprehensive, research-grade, production-quality, or exceptionally dense instruction. Start Ultra after the user confirms the additional research, orchestration, and review effort. Ultra adds a complete domain knowledge map, specialist subagents, a domain-native capstone, mandatory independent review, and user approval of the tracer set.

Both profiles satisfy the same publication, fidelity, learning, design, and enhancement gates. Read `references/ultra-workflow.md` after Ultra is confirmed.

## Course Contract

Explore the request, available sources, local code, and domain context before asking for information. Draft the contract with Agent research and ask the user for one compact calibration of decisions that change the course trunk.

Establish:

- quality profile;
- learner, starting point, prerequisite gap, and target use;
- observable domain capability and graduation artifact;
- main trunk, dependency order, scope, and deferred topics;
- domain evidence and source strategy;
- explanation, practice, feedback, transfer, and capstone plan;
- visual direction, information density, and interaction role;
- delivery target, page topology, static baseline, enhancement policy, and verification mode.

Keep a Standard contract concise. Give an Ultra contract enough detail to coordinate every specialist and review gate. Store it in optional workspace state when the course spans sessions.

## Course Workflow

1. Research the domain facts, data, formulas, sources, expert tasks, and prerequisite gap.
2. Write the main trunk, dependency path, page responsibilities, practice path, and graduation task.
3. Choose representations for each learning bottleneck: prose, formula, table, trace, diagram, worked example, or direct manipulation.
4. Build a tracer set for every multi-page course: the course map, one dense representative lesson, one reference page, and an applicable practice or lab state. Use the complete output as the tracer for a single-page course.
5. Review the tracer through Publication, Learning and Fidelity, Design, and Enhancement gates.
6. Expand the remaining pages through coherent learning arcs while preserving terminology, evidence, visual grammar, and ordinary navigation.
7. Review the complete publication against the Course Contract and record the result.

Use `references/course-composition.md` for capability architecture, prerequisite bridges, layered knowledge maps, page responsibilities, practice, and capstones. Use `templates/structured-object-map.md` and `templates/mechanism-visual-spec.md` as planning surfaces.

Standard proceeds after the tracer passes its internal gates. Ultra presents the verified tracer to the user for one calibration before expansion.

## Working Files

Keep raw research, intermediate drafts, subagent feedback, screenshots, browser profiles, logs, and test fixtures under an isolated `${TMPDIR:-/tmp}/teach-{unique-id}/` directory. Promote approved learner-facing artifacts, source notes, capstone materials, and final review results into the course directory.

Clean the owned temporary directory after the final static publication passes its declared gates.

## Static Publication Contract

Build complete learner-facing static HTML artifacts. Inspect generated files or deployed HTML responses alongside the rendered experience.

Each declared page contains the primary content assigned to its page type and ordinary links through the course path. Course maps, lessons, references, source notes, and labs carry distinct content responsibilities.

Shared CSS, shared JavaScript, CDN resources, frameworks, static site generators, server rendering, hydration, and interactive components can support the publication. The generated HTML carries the core explanation, content meaning, default examples, and ordinary navigation. Learners use the declared static delivery target; authoring tools and development servers remain author-side resources.

Each JavaScript activity includes a static learning goal, inputs, expected interpretation, default example or equivalent representation, and runtime requirement. JavaScript adds direct manipulation, state, scoring, persistence, visualization, and other declared enhancements.

## Content Fidelity

Treat publication as a representation change. Preserve the instructional depth and content objects declared by the Course Contract, including applicable explanations, formulas, derivations, tables, worked examples, evidence, practice, feedback, source scope, and next actions.

Account for every declared page, source note, learning activity, and required content object in the final publication. Give every enhanced object an equivalent static statement of its educational meaning.

Templates are structural starters. Adapt their hierarchy, navigation, visual system, and sections to the Course Contract. The learner's target capability sets the content budget.

## Sources and Explanations

Select sources from the domain's actual evidence ecology. Agent research supplies facts, data, formulas, standards, examples, and prerequisite knowledge. Use `references/evidence-sources.md` to connect important claims with their sources, derivations, observations, teaching use, and scope.

Keep source material, course reconstruction, observed results, and transfer guidance clearly labeled. Record important sources in supporting Markdown.

## Outputs

Default to a multi-page static directory containing:

- a course map for the route, main trunk, and entry points;
- lesson pages for explanation, reconstruction, practice, and feedback;
- reference and deep-dive pages for lookup and complete topic coverage;
- source notes for evidence, provenance, derivation, and scope;
- shared CSS and applicable JavaScript or declared assets;
- a domain-native capstone and evaluation rubric;
- `review.md` when review results belong with the learner-facing package.

Adapt filenames and page types to the declared topology. Keep optional workspace state separate from the learner-facing publication.

## Review

Read `references/browser-review.md` and review in this order:

1. Publication
2. Learning and Fidelity
3. Design
4. Enhancement

Run an independent review when the user requests it, when Standard carries meaningful multi-page or evidence risk, and at both tracer and final stages for Ultra. Read `references/independent-review.md` for the neutral prompt and result shape.

## Completion

A course package is complete when:

- every declared learner-facing artifact exists;
- each final HTML file contains its assigned primary content and ordinary navigation;
- the static baseline preserves the core explanation and content meaning;
- the publication preserves every required Course Contract content object;
- the prerequisite path, practice, feedback, and capstone support the target capability;
- applicable publication, learning, design, enhancement, and independent reviews record passing results;
- the declared static target opens the learner-facing publication successfully.

Learner completion follows this loop:

```text
read and observe
-> bridge prerequisites
-> understand mechanisms
-> reconstruct formulas or processes
-> study worked examples
-> compare and diagnose failures
-> complete domain-native practice
-> use graduated feedback
-> complete the capstone
-> receive expert-standard review
```

## Optional Learning State

Use `MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `GLOSSARY-FORMAT.md`, and `LEARNING-RECORD-FORMAT.md` for returning learners. These files support the course. The static HTML and supporting Markdown remain the deliverable.

## Direct Prose

Write learner-facing text as direct, positive propositions:

```text
object -> mechanism or action -> result -> applicable conditions -> next step
```

State course paths directly: "The course moves from system boundaries into usage, mechanisms, architecture, and deployment verification."

State scope directly: "This lesson covers inference-time tensor organization."

Replace rhetorical contrast with the affirmative claim. Apply this rule to course maps, lessons, references, source notes, practice, feedback, capstones, and reviews. Preserve exact mathematical negation, logical conditions, factual absence, and safety constraints.
