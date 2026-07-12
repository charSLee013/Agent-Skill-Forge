---
name: teach
description: Create HTML courses with supporting Markdown sources, clear learning structure, browser review, and optional independent review. Use when a learner needs a concept, skill, paper, repository, research topic, or multi-step subject organized into a readable course.
---

# Teach

Create a course whose primary artifacts are HTML pages and supporting Markdown. Shape the course around the learner's goal, the subject's structure, and the evidence needed for confident use.

## Course Contract

Before writing pages, establish:

- learner and starting point;
- concrete outcome and target use;
- subject scope and available sources;
- output set: course map, lessons, references, source notes, and optional review;
- success signal: what the learner can explain, build, compare, or transfer.

Keep this contract short. Store it in optional workspace state when the course spans sessions.

## Compose the Course

Use one course workflow. Choose and order modules for the subject rather than following a fixed phase list.

Useful modules include:

- orientation: purpose, vocabulary, and the main line;
- foundations: prerequisites and representations;
- mechanism: objects, variables, states, steps, constraints, and failure modes;
- evidence: sources, observations, examples, and scope;
- practice: retrieval, worked examples, exercises, and feedback;
- transfer: application conditions and a concrete next action;
- synthesis: comparison, explanation, construction, or review.

Use `references/course-composition.md` when the subject has internal structure. Use `templates/structured-object-map.md` and `templates/mechanism-visual-spec.md` when they make the course easier to compose.

## Sources and Explanations

Use primary sources, official documentation, local code, papers, trusted references, or high-signal communities. Record important sources in `sources/*.md` with:

- what the source supports;
- how the course uses it;
- the scope of that support.

Use `references/evidence-sources.md` for source notes and positive scope language. Present the source, the teaching explanation, and any transfer guidance as distinct parts of the course.

## HTML and Markdown Outputs

Build a navigable set of:

- `course-map.html` for the route and main line;
- `lessons/*.html` for focused explanations and practice;
- `reference/*.html` for lookup material;
- `sources/*.md` for supporting source notes;
- `review.md` when an independent review is requested.

Student pages present the main line, memory target, purpose, explanation, evidence, practice, and next action. Detailed source notes remain in the supporting Markdown and can be linked from the relevant page.

## Browser Review

Use Chrome DevTools as the primary review surface whenever HTML is produced and the browser tool is available. Inspect desktop and mobile layouts, Console, Network, links, assets, text flow, tables, diagrams, and interactive states. Capture screenshots for important states. Record the result in the session or in `review.md`.

Read `references/browser-review.md` for the review checklist. When Chrome is unavailable, record the environment limitation and complete the content review explicitly.

## Independent Review

Run an independent subagent review when the user asks for it or when the course has multiple pages, technical evidence, or a meaningful risk of structural drift. Give the reviewer the raw HTML and Markdown artifacts plus the review request. Ask it to assess the main line, learner understanding, source scope, terminology, structure, and concrete repairs. Read `references/independent-review.md` for the review prompt and output shape.

## Optional Learning State

Use the workspace formats when the learner returns across sessions:

- `MISSION-FORMAT.md` for the learner's purpose and outcome;
- `RESOURCES-FORMAT.md` for curated sources;
- `GLOSSARY-FORMAT.md` for stable terminology;
- `LEARNING-RECORD-FORMAT.md` for demonstrated understanding and changed prerequisites.

These files support the course. The HTML and supporting Markdown remain the deliverable.

## Writing Style

Define roles, objects, processes, and scope positively. Prefer sentences such as:

- "This section explains..."
- "This source supports..."
- "This reconstruction is useful for..."
- "The next page develops..."

Use concrete scope statements when precision matters. Keep student pages readable, and keep implementation anchors in supporting Markdown.
