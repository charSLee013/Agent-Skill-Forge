# Course Composition

Compose the course from the learner's target capability and the subject's internal structure. The course map shows the main trunk, prerequisite entry points, deep dives, references, practice, and graduation task.

## Domain Capability Model

Infer the target domain's expert work before dividing the course into pages:

- expert tasks and decisions;
- evidence, standards, tools, and observations used in those decisions;
- prerequisite knowledge and embodied skills;
- common novice errors and expert failure diagnoses;
- the final artifact that demonstrates expert judgment.

Use domain-native evidence. A research course may culminate in a top-tier peer review. A cooking course may culminate in execution, sensory diagnosis, recipe adaptation, and food-safety reasoning. A codebase course may culminate in architecture review, failure reproduction, repair, and verification.

## Learner Path

Build the learner completion loop declared in `SKILL.md` into the package.

Map the learner's current abilities against the target task. Add a diagnostic entry point, prerequisite bridge, or narrower milestone wherever the dependency path needs support.

## Course Architecture

Write one memorable main trunk. Map prerequisite and concept dependencies. Assign every page one distinct learning responsibility within that route.

Place explanation, evidence, practice, feedback, and transfer where they serve the dependency path. Vary page structure according to its role: orientation, foundation, mechanism, evidence, practice, transfer, synthesis, reference, deep dive, or capstone.

For Ultra, organize broad coverage in layers:

- **Core Path**: the progression every learner follows;
- **Prerequisite Bridge**: mathematics, vocabulary, tools, procedures, and intuition;
- **Deep Dives**: derivations, implementation, history, edge cases, and advanced mechanisms;
- **Reference Atlas**: terminology, formulas, standards, parameters, and comparisons;
- **Evidence Map**: claims, sources, observations, derivations, and scope;
- **Expert Branches**: disputes, alternatives, open questions, and further inquiry.

The Core Path carries progression. The surrounding layers provide complete topic coverage and multiple entry points.

## Structured Subjects

For repositories, systems, protocols, papers, workflows, tools, and physical practices, map the dimensions that shape expert judgment:

- purpose and outcomes;
- interfaces and inputs;
- representations and vocabulary;
- processes and state changes;
- constraints and environment;
- evidence and verification;
- failure modes and repairs;
- expert comparisons and open questions.

Use `templates/structured-object-map.md` as the planning surface.

## Mechanisms and Representations

For each meaningful mechanism, identify the learner's hardest relationship. Explain the object, inputs, variables, initial state, one step, whole process, constraints, and failure modes.

Choose the representation that builds the needed intuition:

- prose for purpose, causality, and conditions;
- formulas for precise relationships;
- variable tables for symbols, shapes, units, and roles;
- traces for temporal or procedural change;
- diagrams for structure, space, and dependency;
- worked examples for concrete reconstruction;
- direct manipulation for variable changes, state transitions, and comparisons.

An interactive mechanism synchronizes controls, numerical readouts, visual state, textual interpretation, and a meaningful default example. Its static representation preserves the learning goal, variables, default state, formula or process, expected interpretation, and scope. Use `templates/mechanism-visual-spec.md` to plan it.

## Practice and Feedback

Move practice from recall toward expert judgment:

1. retrieve the main idea;
2. reconstruct a mechanism or procedure;
3. apply it to a worked case;
4. compare alternatives;
5. diagnose a failure;
6. adapt the idea to a new context;
7. produce a domain-native artifact.

Provide graduated feedback through hints, diagnostic rules, partial solutions, worked expert examples, rubrics, and self-review prompts. Package optional prompts that let a returning learner request an independent Agent review of an open-ended artifact.

## Capstone

Define one authentic expert task. Supply inputs, constraints, expected artifacts, evaluation dimensions, common failure patterns, staged checkpoints, and an expert-quality example or review.

The capstone demonstrates the Course Contract capability. Its rubric evaluates domain judgment, evidence use, mechanism understanding, execution quality, diagnosis, communication, and transfer.

## Page Responsibility

Give each page:

- a place in the main trunk;
- one primary learning responsibility;
- required prerequisite links;
- assigned content objects;
- evidence and scope;
- practice or learner action;
- ordinary previous, map, and next navigation;
- a clear handoff to the next capability.

Keep implementation anchors and detailed provenance in supporting Markdown. Keep learner-facing explanations direct, positive, concrete, and scoped.
