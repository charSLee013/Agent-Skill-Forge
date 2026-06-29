# Repo Course

Use this mode when the repository itself is the learning object.

## Order Of Work

1. Build a repo truth map from the actual code.
2. Derive a structured object map from the truth map.
3. Convert that object map into a learner-facing course.
4. Keep implementation evidence backstage by default.

Do not write a course from memory or from README claims alone.

## Repo Truth Map

Capture:

- Entrypoints and primary user flows.
- Core modules and ownership boundaries.
- Data/control flow.
- Key abstractions and invariants.
- Tests and validation commands.
- Known gaps, uncertainty, or stale docs.

The truth map may use local paths, line numbers, symbols, and commands. It belongs in `artifacts/` or collapsed evidence appendices, not the main student narrative.

## Structured Object Map

Do not organize the main student narrative by filesystem tree unless the filesystem is itself the concept being taught.

Derive the course structure from the subject:

- Interfaces and contracts.
- Representations and states.
- Processes and flows.
- Constraints and invariants.
- Operating environment.
- Verification and failure modes.
- Unknowns and evidence boundaries.

Use `structured-object-map.md` for report-grade courses.

## Student Course

Convert the truth map into:

- A course map.
- Lessons organized by mental model, workflow, and decision points.
- Reference pages for architecture terms, flows, APIs, commands, and debugging paths.
- Retrieval prompts that ask the learner to explain behavior without staring at paths.
- Visible evidence boxes for major implementation claims when using an evidence-intensive or stricter profile.

## Boundaries

Student pages must avoid:

- Path-and-line dumps as the core explanation.
- Audit or code review voice unless the task is explicitly evaluative.
- Unsupported architecture judgments.
- Mixing source-supported repo facts with suggested refactors.
- Treating folder order as the default teaching order.

When making a judgment, use the fixed evidence layers. Repository observations that are directly supported by source code should use `paper_fact` with a code anchor; teaching explanations should use `course_reconstruction`; system advice should use `engineering_transfer`; uncertainty should use `unknown`.
