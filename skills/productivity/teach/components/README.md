# Component Palette

Named visual patterns for the learning bottlenecks a course has to get past. Read `../references/visual-motion-direction.md` first — it decides *which* representation a bottleneck needs. This file says which component implements that choice and which variables to fill.

## Selector

| Learning bottleneck | Component | Demonstrates |
|---|---|---|
| Sequence, timing, causal handoff | `sequence-view/` | Participant lanes with messages advancing one step at a time |
| Hierarchy, containment, dependency | `diagram/` | Node graph where focusing a node reveals what it depends on |
| Stepwise reconstruction, comparison | `card-walkthrough/` | Narrative sidebar paired with a stepping detail pane |
| Whole-system structure | `svg-architecture/` | Inline SVG topology with an indicator travelling the active path |
| Formula or parameter exploration | `mechanism-animation/` | Controlled variables driving synchronized readouts and a plot |

Each component is one self-contained `index.html`. Copy it into the course's assets, replace the demonstration content with the subject's own objects, and set the variables below.

## Shared variables

Every component reads these from `:root`. They are the same names the course's `assets/course.css` defines, so a component dropped into a course inherits the course's visual thesis instead of carrying its own palette.

| Variable | Carries |
|---|---|
| `--color-domain-primary` | The subject's principal object or actor |
| `--color-evidence` | Sourced facts, citations, measured values |
| `--color-practice` | Learner actions and exercises |
| `--color-warning` | Boundaries, failure states, invalid input |
| `--font-step-0` … `--font-step-4` | Type scale, fixed `rem` steps |
| `--measure` | Reading width for prose |

A component may add variables for its own geometry (lane height, node radius). Those stay local; the six above are the contract.

## Filling the variables from a visual thesis

The thesis names the subject's objects and the relationships a learner must perceive. Map them in this order:

1. Assign `--color-domain-primary` to the object the learner tracks through the mechanism.
2. Assign `--color-evidence` where the course shows sourced or measured values, so evidence stays visually distinct from teaching reconstruction.
3. Assign `--color-practice` to anything the learner operates.
4. Reserve `--color-warning` for real boundaries — invalid ranges, failure modes, unsupported cases. Reusing it decoratively destroys its signal.
5. Set the type scale from reading conditions, then set `--measure` from the densest prose the page carries.

Keep `font-size` on the fixed `rem` steps. Viewport units resize type against the reading distance the thesis assumed.

## Contract every component satisfies

1. Colors and type sizes come from custom properties. Literal values appear only in the `:root` block.
2. Under `prefers-reduced-motion: reduce`, continuous movement becomes a discrete jump to the target state — not a shortened animation.
3. Time-based mechanisms carry play, pause, step, and reset, each with an accessible name, keyboard operation, and visible focus.
4. One `state` object and one `render()` function drive readouts, labels, visual state, and prose together, so no control can leave the surrounding explanation stale.
