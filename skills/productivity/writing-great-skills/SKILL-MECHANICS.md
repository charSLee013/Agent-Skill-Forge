# Skill Mechanics

This is the skill-specific branch of
[`writing-great-skills`](SKILL.md). The main file owns the writing principles;
this file owns packaging, invocation, and routing mechanics.

## Invocation

Choose invocation authority before writing the description. The repository
records the choice in both host metadata surfaces:

- A **model-invoked** skill is reachable by the model, the user, and other
  skills. Omit `disable-model-invocation` from `SKILL.md` and omit
  `policy.allow_implicit_invocation` from `agents/openai.yaml`. Its description
  is model-facing and names each materially different trigger branch.
- A **user-invoked** skill is reachable only when the human names it. Set
  `disable-model-invocation: true` in `SKILL.md` and
  `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Its
  description is a human-facing one-line summary without trigger lists.

A user-invoked skill may invoke a model-invoked skill. A user-invoked skill
cannot be invoked by another skill; another workflow may recommend it and stop,
leaving the invocation decision with the human.

Shared reference needed by multiple user-invoked skills belongs in a plain
reference file that each owner can point to. Do not duplicate it or bypass
invocation authority through prose.

## Descriptions

A model-facing description is the skill's always-loaded context pointer. State
what the skill does, front-load its leading word, and include one trigger per
branch. A user-facing description states the capability and omits autonomous
trigger language. An `argument-hint` may improve command input without changing
invocation authority.

## Splitting by invocation

Split a model-invoked skill only when a distinct behavior must be discovered on
its own or another model-invoked workflow must reach it. The new description
adds permanent context load, so independent reach must justify the split.

Keep manually selected modes and phase-changing workflows user-invoked. Do not
create an alias skill for a rename; retain the stable command or perform one
coordinated rename across every registry surface.

## Routing

When manual skills become hard to find, use the routing owner already chosen by
the repository, such as a README route map or command index. A repository that
deliberately owns a router skill may use one, but the router can only recommend
user-invoked skills. Keep one route owner instead of parallel routing systems.
