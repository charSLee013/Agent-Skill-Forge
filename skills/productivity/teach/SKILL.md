---
name: teach
description: Create editorially designed, learner-facing static HTML courses with supporting Markdown, capability-driven structure, source fidelity, subject-native visuals, purposeful interaction, browser review, and Standard or Ultra quality profiles. Use when a learner needs a concept, skill, paper, repository, research topic, or multi-step subject organized into a complete course.
---

# Teach

## Outcome Contract

- **Outcome**: a learner can move from the stated starting point to an observable domain capability through a coherent static course.
- **Done when**: the declared publication opens at its publication target and passes the applicable editorial, fidelity, visual, interaction, and accessibility gates.
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

Inspect the request, supplied material, local artifacts, and available sources before asking questions. Resolve reversible details from evidence. Ask once only when learner, target capability, source authority, publication target, or scope would change the course trunk.

Draft a Course Contract containing:

- quality profile, learner, starting point, prerequisite gap, target use, and learning-state (boolean, whether the request maintains persistent learning state across sessions);
- observable capability, graduation artifact, scope, and deferred topics;
- main trunk, dependency order, practice path, feedback, and capstone;
- evidence ecology, source strategy, and fidelity risks;
- editorial voice, paragraph rhythm, terminology, and reading density;
- visual thesis, representation inventory, motion purpose, and state models and reduced-motion behavior;
- page topology, publication target, and verification path.

The **publication target** is the specific location the published course opens at, for example `file:///tmp/teach-abc/course-map.html` or `http://localhost:5500/`. Every review gate runs against this location. The verification path is the browser check against that location defined in `references/browser-review.md`.

The Contract also sets the course's depth floor, so hold it to three structural minimums. Every later gate measures the publication against this Contract, which means a thin Contract would otherwise pass every check.

- **Each page states one observable expert judgment**, written as "the learner can *verb* …" where the verb is `reconstruct`, `diagnose`, `compare`, `apply`, or `produce`. Rewrite `understand`, `know`, `learn`, and `be familiar with`: they name no act a reviewer could witness.
- **Each declared mechanism carries at least one worked example** with concrete input values, intermediate states, and the expected result.
- **The capstone names its evaluation dimensions** and the failure patterns that separate expert work from novice work. "Build an X" is a task, not a measure.

Complete preflight when every field is supported by available evidence or one explicit user decision, and the three minimums hold.

## Quality Profiles

Use **Standard** by default. It delivers a complete professional course through one primary Agent workflow.

Recommend **Ultra** for comprehensive, research-grade, exceptionally dense, or publication-critical instruction. Start it only after the user accepts the additional research and review effort. Then read `references/ultra-workflow.md` before dispatching specialists.

## Course Workflow

1. **Build the evidence base.** Research domain facts, formulas, data, standards, examples, expert tasks, and prerequisite gaps. Read `references/evidence-sources.md` and record each important source with `templates/source-notes.md`. Complete this step when every consequential claim has an evidence role and scope.
2. **Architect the capability path.** Define the main trunk, dependency graph, page responsibilities, practice progression, and graduation task. Read `references/course-composition.md` and use `templates/structured-object-map.md` for structured subjects. Complete this step when every page unlocks a named next capability.
3. **Set the editorial direction.** Read `references/editorial-direction.md`. Establish voice, terminology, lesson arcs, paragraph responsibilities, and density before drafting. Complete this step when one representative explanation reads as a coherent argument rather than a sequence of sections.
4. **Set the visual and motion direction.** Read `references/visual-motion-direction.md`. Choose a representation for each learning bottleneck, then pick the implementing pattern from `components/README.md` and specify applicable mechanisms with `templates/mechanism-visual-spec.md`. Write `assets/course.css` with the custom properties both the pages and the components read: `--color-domain-primary`, `--color-evidence`, `--color-practice`, `--color-warning`, `--font-step-0` through `--font-step-4`, and `--measure`. Complete this step when every visual has a claim, every motion has a state change plus a named state model, and every custom property traces back to a Course Contract visual thesis field.
5. **Build the tracer.** For a multi-page course, build the course map from `templates/course-map.html`, one edited long-form lesson from `templates/lesson.html`, one reference page from `templates/reference.html`, one key mechanism visual, and one applicable practice or interaction state. For a single-page course, use the complete page. Start from the templates, then replace their placeholders and neutral skeleton with the declared subject-native system.
6. **Review the tracer.** Read `references/browser-review.md` and run its gates in order. Standard expands after the tracer passes. Ultra presents the passing tracer for one user calibration.
7. **Expand the course.** Preserve the accepted vocabulary, evidence roles, editorial rhythm, visual grammar, navigation, and state models across coherent learning arcs. Complete expansion when every Course Contract object exists in the publication.
8. **Review the final publication.** Traverse all pages and run deep checks on representative and high-risk states. Use `references/independent-review.md` for meaningful evidence or multi-page risk and every Ultra tracer and final review. Complete the run only after repairs pass the affected gates.

## Hard Rules

- Preserve the depth of every declared explanation, formula, derivation, table, worked example, evidence item, activity, feedback path, and capstone requirement.
- Present primary explanations, worked examples, and source citations as readable text so a learner can read, search, and cite them. Let interaction give the learner ways to manipulate state, compare values, and get feedback.
- Ground factual claims in current sources or recorded observations. Label sourced facts, derivations, observations, teaching reconstructions, and transfer guidance distinctly.
- Match the learner's register without flattening the author's or domain's voice. Edit for meaning, paragraph logic, and rhythm before polishing sentences.
- Derive color, typography, spatial grammar, imagery, diagrams, and motion from the subject's objects and relationships. A reusable theme is not a visual thesis.
- Give time-based mechanisms play, pause, step, reset, keyboard operation, visible focus, reduced-motion behavior, and text explanation that stays synchronized with visual state.
- Keep temporary work under `${TMPDIR:-/tmp}/teach-{unique-id}/` only when research artifacts, intermediate drafts, screenshots, browser profiles, fixtures, or specialist work require isolation. Remove the owned directory after verification.

## Gotchas

| Symptom | Repair |
|---|---|
| Every lesson repeats Purpose, Explanation, Remember, and Next Action | Give the page an editorial arc shaped by its learning responsibility. |
| Paragraphs are individually correct but feel unrelated | Repair the handoff between the previous close and current opening before rewriting sentences. |
| The visual system could label any unrelated course | Rebuild it from domain objects, evidence types, learner actions, and reading conditions. |
| Animation adds movement without changing understanding | Replace it with a static representation or animate the exact state transition at issue. |
| A polished shell hides thin explanations or practice | Return to the Preflight minimums: the page's judgment verb, the mechanism's worked example, and the capstone's evaluation dimensions. A thin Contract cannot be repaired downstream. |
| Review notes, screenshots, and gate logs appear beside lessons | Keep process evidence temporary unless the Course Contract makes it learner-facing. |

## Output

Default to a reading-first multi-page static directory with a course map, lessons, references or deep dives, source notes, shared presentation assets, a domain-native capstone, and its rubric. Use a single page when the Course Contract shows that splitting would weaken the learning path.

Adapt filenames and page types to the subject. Ship no template placeholders, empty generic sections, authoring instructions, debug output, or review scaffolding.

When the Course Contract's `learning-state` field is true, read `references/learning-state.md` and maintain its persistent workspace for the returning learner.

## Completion

Finish when every declared artifact exists, every page fulfills its assigned responsibility, explanations and worked examples remain legible and citable in prose, practice and feedback support the target capability, the capstone measures that capability, and the declared publication target passes `references/browser-review.md`.
