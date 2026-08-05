# Browser Review

Review the learner-facing publication through four ordered gates. Keep evidence in the session workspace unless the Course Contract declares a review artifact.

## Opening the publication target

Take the first path that is available:

1. the project's existing browser automation path — Playwright, Puppeteer, or a chrome-devtools MCP server;
2. a local server such as `python3 -m http.server` or `npx serve`, then drive the page by hand;
3. `file://` opened directly, running each gate manually.

When none is reachable, finish the static inspections, report the course as **browser-unverified**, and list the gate items that went unrun.

## 1. Publication

1. Enumerate every learner-facing artifact in the Course Contract.
2. Inspect generated HTML, not only source templates, for assigned primary content and ordinary links.
3. Open the declared publication target and traverse every local course link.
4. Verify base paths, page titles, assets, local 404 behavior, and applicable CDN or CSP behavior.
5. Run `file://`, portability, connected-host, print, or offline checks when declared.

Pass when the final files carry the complete course path through the publication target.

## 2. Learning, Editorial, and Fidelity

Read the final HTML and supporting Markdown as the learner. Confirm:

- the main trunk is easy to restate and begins at the declared starting point;
- prerequisite bridges arrive before the mechanisms that use them;
- every page fulfills one distinct learning responsibility;
- explanations, evidence, practice, feedback, transfer, and capstone follow the dependency path;
- claims preserve evidence roles, terminology, formulas, data, and scope;
- every Course Contract content object survives publication;
- the capstone and rubric measure the target capability;
- lesson arcs vary with their responsibility rather than repeating template headings;
- paragraph openings follow prior conclusions and each paragraph advances one reasoning job;
- sentence rhythm, register, and terminology fit the learner and subject;
- summary echoes, generic transitions, inflated claims, and abstract filler have been removed.

Pass when a learner can reconstruct the argument and no editorial repair would change the intended meaning or evidence.

## 3. Visual System

Inspect desktop, narrow mobile, keyboard, reduced-motion, and declared print states. Confirm:

- the visual thesis is visibly derived from the subject's objects, evidence, and learner actions;
- `assets/course.css` exists, every page links it, and its custom properties carry the declared visual thesis;
- typography, spacing, and reading widths support long-form comprehension;
- `font-size` declarations use stable type steps rather than viewport units;
- navigation, evidence, warnings, practice, feedback, and status have stable roles;
- formulas, tables, code, diagrams, figures, and citations support scanning and comparison;
- content wraps without overlap, clipping, accidental horizontal scrolling, or layout shift;
- semantic color, labels, focus, and contrast remain legible in every state;
- no generic theme or decorative treatment substitutes for content structure.

Capture tracer and high-risk screenshots in the temporary workspace. Pass when each viewport preserves hierarchy, subject fit, and complete content meaning.

## 4. Interaction and Motion

Exercise every meaningful enhanced state:

- play, pause, step, reset, and direct-manipulation controls;
- synchronized values, labels, visual state, and textual interpretation;
- quizzes, hints, feedback, scoring, progress, and persistence;
- calculators, charts, diagrams, canvas, and responsive redraw;
- initial, transitional, result, empty, error, boundary, and recovery states;
- keyboard operation, visible focus, and accessible names;
- reduced-motion behavior;
- console errors, warnings, network failures, and missing assets.

For each animation, restate the learning claim and verify that the transition exposes it. For canvas or generated visuals, inspect meaningful pixels and labels. Pass when every declared state behaves correctly and readouts, labels, and text explanation stay synchronized throughout.

## Review Scope

Run all gates on the tracer. During final review, traverse every learner-facing page for publication and links, then inspect representative and high-risk pages deeply through the remaining gates.

Browser rendering is required for completion: a course that never rendered is unverified, however clean its source reads.
