# Model-invoked vs user-invoked

Every `SKILL.md` in this repo is a skill. The one axis that splits them is **invocation** — who can reach it. Each skill records this policy twice because Claude and Codex read different metadata:

- **User-invoked** — reachable **only by the human typing its name**. Set `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. The `description` is **human-facing**: a one-line summary read by a person browsing commands. Strip trigger lists ("Use when the user says…"). An optional `argument-hint` improves command input guidance without changing invocation authority.
- **Model-invoked** — reachable by **model or user**. Omit both `disable-model-invocation` and the Codex `policy` block. The `description` is **model-facing** and keeps rich trigger phrasing ("Use when the user wants…, mentions…, asks for…") so auto-invocation fires. The test for whether a skill should stay model-invoked: _could the model usefully reach for this autonomously?_ (Reuse is the reason to extract a skill, not the test.)

The two metadata surfaces must agree. A user-invoked skill may invoke model-invoked skills, but it can never reach another user-invoked skill.

Bucket `README.md`s and the top-level `README.md` group entries into **User-invoked** and **Model-invoked**. `scripts/test-skill-registry.sh` checks the shipped directory, manifest, README, sidecar, and invocation-policy sets together.

## Dependencies between them

Dependencies are expressed in prose, but the verb carries authority:

- **Invoke** — the current skill may execute the target only when the target is model-invoked.
- **Recommend** — tell the user to explicitly run the target, then stop the current phase. Use this for every user-invoked target.

`/skill` syntax is a reference, not permission to execute. Write `recommend /setup-agent-skills and stop` when required local configuration is missing. Shared reference docs still live inside the skill that owns them; do not use a prose dependency to bypass invocation rules.

## Passive vs active domain work

Merely _reading_ `CONTEXT.md` for vocabulary is a one-line prose pointer, not the `domain-modeling` skill. Only the active build/sharpen discipline (challenge terms, edge-case scenarios, write ADRs, update `CONTEXT.md` inline) is `domain-modeling`.
