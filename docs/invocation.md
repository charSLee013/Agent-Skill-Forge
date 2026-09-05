# Model-invoked vs user-invoked

Every `SKILL.md` in this repo is a skill. The one axis that splits them is **invocation** — who can reach it. Each skill records this policy twice because Claude and Codex read different metadata:

- **User-invoked** — reachable **only by the human typing its name**. Set `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. The `description` is **human-facing**: a one-line summary read by a person browsing commands. Strip trigger lists ("Use when the user says…"). An optional `argument-hint` improves command input guidance without changing invocation authority.
- **Model-invoked** — reachable by **model or user**. Omit both `disable-model-invocation` and the Codex `policy` block. The `description` is **model-facing** and keeps rich trigger phrasing ("Use when the user wants…, mentions…, asks for…") so auto-invocation fires. The test for whether a skill should stay model-invoked: _could the model usefully reach for this autonomously?_ (Reuse is the reason to extract a skill, not the test.)

The two metadata surfaces must agree. Model invocation selects a capability; it
does not authorize its side effects. `grilling`, `implement`, `to-prd`,
`to-issues`, and `wayfinder` are model-invoked and may continue already requested
work across phases. A phase change alone is not a reason to wait for another
command. A read-only request or a request to review a draft still limits what
may happen next. Other explicitly manual skills retain their restrictions.

Bucket `README.md`s and the top-level `README.md` identify each skill's invocation mode. `scripts/test-skill-registry.sh` checks the shipped directory, manifest, README, sidecar, and invocation-policy sets together.

## Dependencies between them

Dependencies are expressed in prose, but the verb carries authority:

- **Invoke** — the current skill may execute the target only when the target is model-invoked.
- **Recommend** — propose a next action when it is outside current authorization
  or the target is user-invoked. Continue independent authorized work when possible.

`/skill` syntax is a reference, not permission to execute. A user-invoked skill
may invoke a model-invoked skill, but another workflow cannot activate a manual
skill on its own. Missing workspace configuration uses the shipped on-demand
defaults; it does not require invoking `setup-agent-skills`.

## Shared references

References live inside their owning skill and can be read without invoking that
skill. Resolve an owner's directory from the host's discovered skill paths. In
a source checkout, resolve it from `.claude-plugin/plugin.json`. The installer
flattens the three buckets into sibling skill directories, so a cross-bucket
relative source path is not a portable installed reference. Never assume a
particular user's home directory. Report an unavailable required reference
instead of claiming that it was read.

## Passive vs active domain work

Merely _reading_ `CONTEXT.md` for vocabulary is a one-line prose pointer, not the `domain-modeling` skill. Only the active build/sharpen discipline (challenge terms, edge-case scenarios, write ADRs, update `CONTEXT.md` inline) is `domain-modeling`.
