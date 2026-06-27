# HTML Quality Proof

HTML teaching artifacts must prove readability and learning value, not just visual effort.

## Required Checks

For each student-facing HTML artifact, verify:

- One clear `h1`.
- Main-line summary near the top.
- "Remember now" or equivalent memory target.
- Next action.
- Internal links resolve.
- Tables, diagrams, and callouts are readable.
- Desktop and mobile layouts do not overlap or hide text.
- Evidence is separated from the main narrative.
- Canvas/3D/animation has a 2D or text fallback.
- No backstage governance noise appears in the student narrative.

## Screenshot Proof

For important HTML artifacts, capture or inspect:

- Desktop viewport.
- Mobile viewport.
- Any interactive/canvas/3D state needed to prove nonblank rendering.

If Playwright is available, use it. If not, use deterministic HTML checks plus a browser inspection note.

## Visual Discipline

Borrow design-proof discipline without turning Teach into a design skill:

- Facts and evidence before visual polish.
- Visuals serve the main line.
- Avoid decorative slop: cards, gradients, icons, and animations must earn their place.
- Do not use 3D/canvas as the only carrier of an explanation.
- Prefer clear 2D diagrams or tables when they teach better.

## Failure Conditions

Block delivery when:

- The page is visually impressive but the learner cannot restate the point.
- Important text overlaps or is hidden.
- A table cannot be read on mobile.
- Links are broken.
- Local paths, logs, audits, or governance names leak into the main page.
- A canvas/3D area is blank or lacks fallback.
