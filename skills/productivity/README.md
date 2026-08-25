# Productivity

General planning, learning, communication, and workflow tools.

## User-invoked

Reachable only when you type them (`disable-model-invocation: true`).

- **[grill-me](./grill-me/SKILL.md)** — finds a plan's main trunk with focused questions and reversible defaults; use it for general single-session clarification, not durable project-doc updates; it requires a stated goal and exits with an executable plan.
- **[handoff](./handoff/SKILL.md)** — compacts the current conversation for another agent or session; use it for context transfer, not replanning or implementation; it requires current state and open work and exits with a continuation document.
- **[to-questionnaire](./to-questionnaire/SKILL.md)** — turns a knowledge gap into a questionnaire for one informed person; use it for asynchronous discovery, not planning or a grill session; it requires a recipient and needed outcomes and exits with one Markdown questionnaire.
- **[i-have-adhd](./i-have-adhd/SKILL.md)** — shapes every response into an action-first ADHD-friendly form; use it as a manually enabled session mode, not a task workflow; it requires no arguments and exits only on `normal mode` or `stop adhd mode`.
- **[ponytail](./ponytail/SKILL.md)** — constrains approved code work to the smallest correct implementation by preferring existing mechanisms, stdlib, native features, and installed dependencies; use it as a manually enabled implementation rule, not for solution exploration; it takes no arguments and exits only on `/ponytail off`, `stop ponytail`, or `normal mode`.
- **[prepare-goals](./prepare-goals/SKILL.md)** — turns approved long-running work into bounded Codex Goal launchers; use it for work expected to take hours or days, not ordinary execution or unresolved planning; it requires a clear outcome and verification path and exits without starting Goal mode.
- **[prose-standard](./prose-standard/SKILL.md)** — preserves complete technical contracts while reviewing, writing, restoring, or trimming prose; use it for explicit documentation, comments, prompts, diagnostics, or visible-string work, not natural-language polish alone; it requires a scope and exits with edits or an audit report.
- **[trim-cot-leakage](./trim-cot-leakage/SKILL.md)** — removes design-session, PR, review, draft, and reasoning-transcript residue while preserving durable facts; use it for an explicit authoring-context audit, not generic shortening; it requires a scope and exits with edits or an audit report.
- **[doc-standards](./doc-standards/SKILL.md)** — audits documentation ownership, placement, source-of-truth boundaries, and agreement with current repository behavior; use it for an explicit documentation-system review, not prose polish or automatic rewriting; it requires a documentation scope and exits with findings or authorized edits.
- **[wait-what](./wait-what/SKILL.md)** — re-pitches the previous response with missing context and simpler language; use it for a one-response repair, not the persistent `i-have-adhd` mode; it requires a previous response and exits with a rewrite without changing repository files.
- **[writing-great-skills](./writing-great-skills/SKILL.md)** — defines how to write predictable agent-consumed documents; use it for skills and repository instruction maps, not product-rule persistence or installation; it requires a target document or behavior contract and exits with bounded prose that preserves the target's authority.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[grilling](./grilling/SKILL.md)** — resolves high-leverage decisions and backfills reversible details for a calling workflow; use it when key ambiguity exists, not as a user phase; it requires a goal and boundary and returns a decision trunk to its caller.
- **[humanizer](./humanizer/SKILL.md)** — rewrites existing prose to remove specific AI-writing patterns while preserving every claim, citation, and source boundary; use it for prose editing or review, not fact-checking, new content generation, or persistent conversation styling; it requires source text and exits with the rewrite shape appropriate to pasted, file, or embedded mode.
- **[teach](./teach/SKILL.md)** — builds editorially designed static HTML courses with subject-native visuals and supporting Markdown; use it for complete learning delivery, not a general summary or documentation page; it requires a learning goal, audience, and sources and exits with a Standard or Ultra course.
