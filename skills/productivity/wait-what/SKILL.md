---
name: wait-what
description: Re-pitch the previous response with the missing context and simpler language.
argument-hint: "Which part of the previous response did not land?"
disable-model-invocation: true
---

# Wait, What?

Re-pitch the immediately preceding assistant response. Supply the minimum
context needed to understand it, use the user's language and familiar wording,
and preserve every factual claim, condition, exception, and uncertainty from
the original response.

Use the user's arguments to focus the rewrite. Do not ask what was confusing
when the arguments or conversation already make that clear.

Read `grilling`'s `references/communication.md` for user-facing replies. Locate
the owner through the host's discovered skill paths, or the repository plugin
manifest when working from source. Reading the reference does not start grilling.

Only when the explanation depends on project terminology, use its established vocabulary:

1. If a root `CONTEXT-MAP.md` exists, read it and follow the relevant pointer to
   the applicable `CONTEXT.md`.
2. Otherwise, if a root `CONTEXT.md` exists, read it.
3. Otherwise, use terminology already present in the conversation and relevant
   repository files.

Reading vocabulary is passive. Do not create or modify `CONTEXT.md`,
`CONTEXT-MAP.md`, ADRs, issues, `AGENTS.md`, or other repository files.

Return only the rewritten explanation. This skill ends after that response and
does not alter the style of later messages.
