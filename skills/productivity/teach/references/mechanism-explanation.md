# Mechanism Explanation

Use this when teaching any nontrivial mechanism: procedure, loop, formula, protocol, state transition, optimization, layout, routing, interaction, data transformation, or causal chain.

## Required Structure

Never present code, equations, pseudocode, or diagrams alone.

Explain in this order:

1. Name the mechanism.
2. Define the object being changed or reasoned about.
3. Define every variable, state, role, or input that appears.
4. Explain the initial state.
5. Explain one step.
6. Explain the whole process.
7. Explain how parameters, constraints, or context affect behavior.
8. Explain failure modes or boundaries.
9. Add code, equation, pseudocode, or diagram only after the explanation.
10. Add a retrieval prompt asking the learner to restate the mechanism.

## Visual Spec Trigger

Write a visual spec before producing HTML when the mechanism is dynamic, spatial, temporal, multi-dimensional, stateful, interactive, or hard to inspect from prose alone.

Ask:

- What changes over time or steps?
- What dimensions or axes matter?
- What variables or states must remain visible?
- What can the learner compare or manipulate?
- What misconception should the visual prevent?
- Is a table, static diagram, animation, interaction, or text derivation sufficient?
- What fallback explains the same mechanism without the visual?

## Completion Rule

A mechanism page is incomplete if a learner sees code, equations, or a diagram before they know what the variables, states, one-step update, and whole-process purpose mean.
