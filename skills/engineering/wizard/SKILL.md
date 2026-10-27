---
name: wizard
description: Generate a user-requested script for a concrete sequence of human-only setup, migration, or credential actions.
license: MIT
argument-hint: "Which human-only procedure needs a guided script?"
disable-model-invocation: true
---

# Human-Operated Wizard

Generate a small script only when the user explicitly wants a reusable guide
for a human-only procedure. Adapted from Matt Pocock's `wizard`; do not import
its shell framework or create a new project setup system by default.

Inspect the consuming project's existing configuration, CLI, and documented
procedure. Define the ordered steps, where each value comes from, its owner,
whether it is secret, and what action could be irreversible. Use verified
current instructions; ask about an unknown critical dashboard action rather
than inventing clicks or fields.

Create one bounded script at the path requested by the user, or the project's
existing script location, only after the procedure and its output are clear.
If no durable path was requested or established, use a temporary path and
report it; do not create a new repository script location as a side effect.
Keep secrets out of command logs, shell history, and the generated script;
never embed values or print them. Confirm before concrete irreversible steps,
make reruns explicit, and leave unrelated files unchanged. A generated script
is not permission to execute it, commit it, push it, or write credentials to a
remote service.

Check shell syntax and review every command and secret destination statically.
Run a safe local fixture only when one already exists. Report what still needs
human execution and what could not be verified without it.
