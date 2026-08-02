---
name: teach
description: Create editorially designed, learner-facing static HTML courses with supporting Markdown, capability-driven structure, source fidelity, subject-native visuals, purposeful interaction, browser review, and Standard or Ultra quality profiles. Use when a learner needs a concept, skill, paper, repository, research topic, or multi-step subject organized into a complete course.
---

# Teach

## Outcome Contract

- **Outcome**: a learner can move from the stated starting point to an observable domain capability through a coherent static course.
- **Done when**: the declared publication opens at its delivery target, carries the full learning path without JavaScript, and passes the applicable editorial, fidelity, visual, interaction, and accessibility gates.
- **Evidence**: the Course Contract, domain sources, checked derivations or observations, rendered pages, exercised interactions, and capstone rubric.
- **Output**: learner-facing HTML and supporting Markdown only. Keep research notes, screenshots, review traces, and process commentary outside the publication unless the Course Contract names them as deliverables.

## Core Stance

Teach capability, not topic coverage. Build the shortest dependency path that lets the learner explain, reconstruct, compare, diagnose, and apply the subject with evidence.

- Standard and Ultra share one editorial, visual, motion, accessibility, and fidelity floor.
- Ultra adds research depth, coverage, specialist collaboration, tracer approval, and independent review.
- Treat templates as compositional skeletons. Derive the finished design from the subject and learner.
- Let prose carry explanation. Let visuals expose relationships. Let motion reveal a change that is difficult to understand from a static state.
- Prefer fewer, stronger representations. Decoration does not count as instruction.

## Preflight

Inspect the request, supplied material, local artifacts, and available sources before asking questions. Resolve reversible details from evidence. Ask once only when learner, target capability, source authority, delivery target, or scope would change the course trunk.

Draft a Course Contract containing:

- quality profile, learner, starting point, prerequisite gap, and target use;
- observable capability, graduation artifact, scope, and deferred topics;
- main trunk, dependency order, practice path, feedback, and capstone;
- evidence ecology, source strategy, and fidelity risks;
- editorial voice, paragraph rhythm, terminology, and reading density;
- visual thesis, representation inventory, motion purpose, and static equivalents;
- page topology, delivery target, enhancement policy, and verification mode.

Complete preflight when every field is supported by available evidence or one explicit user decision.

## Quality Profiles

Use **Standard** by default. It delivers a complete professional course through one primary Agent workflow.

Recommend **Ultra** for comprehensive, research-grade, exceptionally dense, or publication-critical instruction. Start it only after the user accepts the additional research and review effort. Then read `references/ultra-workflow.md` before dispatching specialists.

## Course Workflow

1. **Build the evidence base.** Research domain facts, formulas, data, standards, examples, expert tasks, and prerequisite gaps. Read `references/evidence-sources.md`. Complete this step when every consequential claim has an evidence role and scope.
2. **Architect the capability path.** Define the main trunk, dependency graph, page responsibilities, practice progression, and graduation task. Read `references/course-composition.md` and use `templates/structured-object-map.md` for structured subjects. Complete this step when every page unlocks a named next capability.
3. **Set the editorial direction.** Read `references/editorial-direction.md`. Establish voice, terminology, lesson arcs, paragraph responsibilities, and density before drafting. Complete this step when one representative explanation reads as a coherent argument rather than a sequence of sections.
4. **Set the visual and motion direction.** Read `references/visual-motion-direction.md`. Choose a representation for each learning bottleneck and specify applicable mechanisms with `templates/mechanism-visual-spec.md`. Complete this step when every visual has a claim and every motion has a state change plus a static equivalent.
5. **Build the tracer.** For a multi-page course, build the course map, one edited long-form lesson, one reference page, one key mechanism visual, and one applicable practice or interaction state. For a single-page course, use the complete page. Start from the templates, then replace their placeholders and neutral skeleton with the declared subject-native system.
6. **Review the tracer.** Read `references/browser-review.md` and run its gates in order. Standard expands after the tracer passes. Ultra presents the passing tracer for one user calibration.
7. **Expand the course.** Preserve the accepted vocabulary, evidence roles, editorial rhythm, visual grammar, navigation, and static baseline across coherent learning arcs. Complete expansion when every Course Contract object exists in the publication.
8. **Review the final publication.** Traverse all pages and run deep checks on representative and high-risk states. Use `references/independent-review.md` for meaningful evidence or multi-page risk and every Ultra tracer and final review. Complete the run only after repairs pass the affected gates.

## Hard Rules

- Preserve the depth of every declared explanation, formula, derivation, table, worked example, evidence item, activity, feedback path, and capstone requirement.
- Put primary explanations, default examples, source links, and ordinary navigation in HTML. JavaScript may add manipulation, state, scoring, persistence, or synchronized views.
- Ground factual claims in current sources or recorded observations. Label sourced facts, derivations, observations, teaching reconstructions, and transfer guidance distinctly.
- Match the learner's register without flattening the author's or domain's voice. Edit for meaning, paragraph logic, and rhythm before polishing sentences.
- Derive color, typography, spatial grammar, imagery, diagrams, and motion from the subject's objects and relationships. A reusable theme is not a visual thesis.
- Give time-based mechanisms play, pause, step, reset, keyboard operation, visible focus, reduced-motion behavior, and a complete static reading path.
- Keep temporary work under `${TMPDIR:-/tmp}/teach-{unique-id}/` only when research artifacts, intermediate drafts, screenshots, browser profiles, fixtures, or specialist work require isolation. Remove the owned directory after verification.

## Gotchas

| Symptom | Repair |
|---|---|
| Every lesson repeats Purpose, Explanation, Remember, and Next Action | Give the page an editorial arc shaped by its learning responsibility. |
| Paragraphs are individually correct but feel unrelated | Repair the handoff between the previous close and current opening before rewriting sentences. |
| The visual system could label any unrelated course | Rebuild it from domain objects, evidence types, learner actions, and reading conditions. |
| Animation adds movement without changing understanding | Replace it with a static representation or animate the exact state transition at issue. |
| A polished shell hides thin explanations or practice | Audit Course Contract objects in the generated HTML, not the source template. |
| Review notes, screenshots, and gate logs appear beside lessons | Keep process evidence temporary unless the Course Contract makes it learner-facing. |
| The course works only with JavaScript | Restore the explanation, default state, interpretation, and navigation to HTML. |

## Output

Default to a reading-first multi-page static directory with a course map, lessons, references or deep dives, source notes, shared presentation assets, a domain-native capstone, and its rubric. Use a single page when the Course Contract shows that splitting would weaken the learning path.

Adapt filenames and page types to the subject. Ship no template placeholders, empty generic sections, authoring instructions, debug output, or review scaffolding.

For returning learners, use `MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `GLOSSARY-FORMAT.md`, and `LEARNING-RECORD-FORMAT.md` only when persistent learning state is part of the request.

## Completion

Finish when every declared artifact exists, every page fulfills its assigned responsibility, the static path preserves the full educational meaning, practice and feedback support the target capability, the capstone measures that capability, and the declared delivery target passes `references/browser-review.md`.
