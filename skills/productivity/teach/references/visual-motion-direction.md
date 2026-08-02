# Visual and Motion Direction

## Outcome Contract

- **Outcome**: the visual system makes the subject's structure and changes easier to perceive.
- **Done when**: every content-bearing visual states a learning claim, every motion reveals a meaningful transition, and the static, reduced-motion, keyboard, desktop, and mobile paths preserve the same interpretation.
- **Evidence**: the Course Contract, representation inventory, mechanism specs, rendered tracer states, and browser review.

## Visual Thesis

Derive one visual thesis from:

- domain objects and their shapes, materials, scales, or boundaries;
- relationships the learner must compare, trace, or manipulate;
- evidence types such as code, measurements, sources, specimens, or timelines;
- learner actions such as diagnose, assemble, tune, classify, or reconstruct;
- reading conditions, density, delivery target, and accessibility needs.

Write the thesis as a claim about perception, not a style label. Example shape: "The course treats the protocol as messages crossing trust boundaries, so topology, direction, and state are the stable visual grammar."

Derive typography, spacing, color roles, imagery, diagrams, and interaction from that thesis. A preset theme, decorative effect, or technology choice cannot substitute for it.

## Representation Picker

| Relationship to reveal | Primary representation |
|---|---|
| Hierarchy, containment, or dependency | labeled structure diagram or nested map |
| Process, causality, or branching | flow or decision path |
| Sequence, timing, or handoff | trace, timeline, or sequence view |
| Topology, routes, or boundaries | network or spatial map |
| State, variable change, or feedback | state model, synchronized controls, or plotted transition |
| Comparison across repeated fields | table, aligned small multiples, or matrix |
| Exact reconstruction | worked example with visible intermediate states |

Use the smallest representation that exposes the relationship. Pair it with prose that explains how to read it and what judgment it enables.

## Compositional System

- Establish stable roles for navigation, body prose, evidence, definitions, warnings, practice, feedback, and status.
- Set reading width from content type. Prose, code, tables, and diagrams may need different tracks.
- Make typography express hierarchy through size, weight, spacing, and role. Do not use viewport units such as `vw` or `vi` in `font-size`; use fixed `rem` steps and media-query breakpoints when the type scale must change.
- Assign colors semantically and verify contrast in every state.
- Use real subject assets when inspection matters. Label diagrams and data views precisely.
- Give fixed-format boards, traces, controls, and diagrams stable dimensions and responsive constraints.
- Keep page shells consistent while allowing each page responsibility to determine composition.

## Motion Purpose Gate

Animate only when a learner must perceive sequence, causality, state change, spatial transformation, synchronization, or comparison over time.

Before implementation, state:

- the visual claim;
- initial state, transition, and resulting state;
- learner-controlled and system-controlled variables;
- the observation the learner should make;
- why static juxtaposition alone is insufficient;
- the static and reduced-motion equivalents.

Use a static representation when the purpose cannot be stated precisely.

## State Storyboard

For time-based mechanisms, storyboard named states before writing animation code:

1. establish the objects and initial conditions;
2. expose one transition at a readable pace;
3. synchronize active visual state, values, labels, and explanation;
4. pause at the consequential result;
5. let the learner replay, step, reset, or compare.

Keep narration, labels, and visual emphasis aligned to the same state. Never rely on transient color or motion as the only carrier of meaning.

## Interaction Contract

- Provide play, pause, step, and reset for instructional timelines.
- Give every control a visible label or accessible name, keyboard operation, focus state, and stable hit area.
- Keep numerical readouts, diagrams, text interpretation, and controls synchronized.
- Define valid ranges, boundary behavior, errors, empty states, and recovery.
- Avoid autoplay when it competes with reading or bypasses learner control.
- Preserve complete explanation, default state, and navigation without JavaScript.
- Under `prefers-reduced-motion`, replace continuous movement with discrete state changes or static comparison.

## Browser Review

Inspect representative and boundary states at desktop and narrow mobile widths. Check text wrapping, overflow, collision, clipping, label placement, control stability, focus order, console output, asset loading, resize behavior, and the no-JavaScript path.

For canvas or generated visuals, verify meaningful pixels and labels rather than treating a non-empty element as proof. Capture screenshots of initial, transitional, result, error, and reduced-motion states when they carry different interpretations.

## Gotchas

| What happened | Repair |
|---|---|
| The same palette and card treatment appears in every subject | Return to the visual thesis and domain objects. |
| Every page contains a diagram | Keep only representations that expose a learning bottleneck. |
| Motion looks polished but teaches no transition | Replace it with a static comparison or redesign around named states. |
| Controls change graphics while prose stays stale | Drive readouts, labels, visual state, and interpretation from one state model. |
| Mobile layout hides labels or changes the mechanism | Add stable dimensions, responsive constraints, and an alternate composition. |
| Reduced motion only shortens duration | Replace movement with discrete states or simultaneous comparison. |

## Completion

Complete the direction when the tracer visibly belongs to its subject, each representation has a learning claim, each animation has a justified state transition, and all declared browser paths preserve the same educational meaning.
