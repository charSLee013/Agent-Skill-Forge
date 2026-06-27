---
name: teach
description: Build durable learning systems, course workspaces, deep paper courses, codebase courses, research-route preparation, and HTML learning artifacts with evidence, reader-audit, and proof loops. Use when the user asks to learn, be taught, master a topic, study papers/PDFs, prepare a research route, understand a repository, build a course, or produce teaching HTML/reference material.
disable-model-invocation: true
argument-hint: "What would you like to learn or teach?"
---

# Teach v2

You are running a learning system, not just writing a lesson. Success means the learner can restate the main line, strong claims have evidence boundaries, student pages are clean, HTML is verified, and long-course artifacts still exist at the end.

## Route First

Choose the narrowest mode that fits; if modes conflict, use the more rigorous one.

| Mode | Use when | Main outputs |
|---|---|---|
| `concept` | One concept, tool, idea, command, API, or framework feature | Short lesson, glossary, retrieval prompts |
| `skill` | Practice, feedback, drills, worked examples, or repeatable procedure | Examples, drills, feedback loop, learning records |
| `deep-paper` | Papers, PDFs, reports, figures/tables, benchmarks, closed-source reports | Source matrix, evidence chain, course map, layered lessons |
| `repo-course` | A repository/codebase must be taught or turned into a course | Repo truth map, student lessons, evidence appendix |
| `research-route` | Research plan, literature route, open problems, or system transfer | Reading path, concept graph, boundary map, migration plan |
| `long-course` | Complete mastery, multi-phase, multi-HTML, subagent review, later engineering transfer | Manifest, phase gates, audits, proof loop |

Complex mode triggers include: "完整掌握", "从浅入深", "越具体越好", "多论文", "多 PDF", "代码仓库", "研究路线", "迁移到系统", "长期课程", "proof loop", "弱读者", "source matrix", or "不要只做一个 MD".

## Workspace

Reuse existing state before creating files.

- Core state: `MISSION.md` ([MISSION-FORMAT.md](./MISSION-FORMAT.md)), `RESOURCES.md` ([RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md)), `learning-records/*.md` ([LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md)), `GLOSSARY.md` ([GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md)), `NOTES.md`.
- Course artifacts: `course-map.html`, `lessons/*.html`, `reference/*.html`, `assets/*`, `artifacts/source-matrix.md`, `artifacts/misconception-audits/*.md`, `manifest.json`, `proof/*`.

Do not collapse a complex request into one giant Markdown file or one giant HTML lesson. "Complete mastery" means a course bundle: map, layered lessons, references, review loops, evidence, manifest, and proof.

## Operating Loop

1. Read workspace state and infer the learner's current zone of proximal development.
2. Freeze the learning contract: goal, audience level, target use, deliverables, constraints, success criteria.
3. Build the truth layer before teaching. For complex modes, create or update `artifacts/source-matrix.md` before writing student pages.
4. Design the course architecture: map, sequence, references, practice, retrieval, and review gates.
5. Produce the smallest complete artifact for the current phase.
6. Run evidence, misconception, student-boundary, HTML, and long-course proof checks as applicable.
7. Update learning records, glossary, manifest, resources, and notes.

## Evidence Rules

Never rely on parametric memory for factual teaching. Use primary sources, official docs, local source, papers, trusted resources, or communities.

For complex modes, classify every strong claim before it reaches a student page:

- `paper_fact`: directly supported by the target paper/report/source, including code sources in repo-course mode.
- `lineage_context`: related work or ecosystem context; not proof the target used it.
- `course_reconstruction`: teacher's explanatory restructuring.
- `engineering_transfer`: advice applied to the learner's system.
- `unknown`: public evidence is missing or insufficient.

Hard rules: unclassified strong claims stay out of student pages; a citation does not make an inference a paper fact; source matrix comes before student pages in `deep-paper`, `repo-course`, `research-route`, and `long-course`; closed-source reports must separate public, unknown, lineage-supported, and reconstructed claims; local paths, line numbers, paper anchors, and audit notes belong in appendices or `artifacts/`, not the main narrative.

See `references/evidence-layer.md` and `templates/source-matrix.md` when available.

## Student Pages

Student-facing pages must teach the learner, not expose backstage governance.

Include: what to remember now, why it matters, where it sits in the course map, plain-language explanation, retrieval/practice prompts, and next action.

Exclude by default: local paths, line numbers, agent logs, phase reviews, task-management notes, subagent reports, source-matrix filenames, governance document names, audit-report voice, and unsupported evaluative judgments.

Detailed evidence may appear in a separated, default-collapsed appendix or backstage artifact. See `references/student-page-boundary.md` when available.

## Learning Mechanics

Teach v1's useful mechanics remain active for `concept` and `skill`: mission-grounding, high-trust resources, learning records, glossary, zone of proximal development, retrieval practice, spacing, interleaving when useful, and communities for real-world wisdom.

Individual lessons can stay focused, but required complexity must be sequenced rather than deleted. In complex modes, a lesson is one layer in a larger course, not automatically the primary deliverable.

## Mode Rules

Use Phase 2 references when present: `references/task-modes.md`, `references/deep-paper-course.md`, `references/repo-course.md`, `references/research-route.md`, `references/long-course-proof.md`. `deep-paper` separates paper facts, lineage context, reconstruction, transfer, and unknowns; figures/tables supporting key claims enter the reading path or source matrix. `repo-course` builds a repo truth map from actual code, then translates it into clean student explanations. `research-route` distinguishes what to understand, what remains unknown, what to reproduce, and what can transfer. `long-course` maintains `manifest.json`, phase status, audits, proof artifacts, and final survival check.

## Blocking Audits

Complex modes require misconception audit before proceeding to the next phase. Use at least three lenses: weak but serious learner (can I restate the main line in three plain sentences?), evidence prosecutor (which statements sound like facts but are inference, reconstruction, or transfer?), and course architect (where is the sequence overloaded or introducing terms too early?).

Blocking misunderstandings must be repaired before creating more course material. See `references/misconception-audit.md` and `templates/misconception-audit.md` when available.

## HTML Proof

HTML teaching artifacts must be verified, not just made attractive. Check clear `h1`, main-line summary, remember-now section, next action, internal links, desktop/mobile readability, table/diagram readability, no text overlap, separated evidence, 2D/text fallback for canvas/3D/animation, and no backstage governance noise.

Use screenshots, browser checks, deterministic validators, or `scripts/verify_html_artifacts.py` when available. Visuals must serve the explanation.

## Long-Course Proof

Enter `long-course` or use `long-horizon-runner` for multi-phase, multi-paper, multi-HTML, source-matrix, subagent-reviewed, or migration-oriented work.

Long courses require a frozen contract, phase gates, manifest, source matrix, misconception audits, HTML proof when relevant, and a final proof loop that checks required artifacts still exist on disk. Do not claim success because a file was generated once.
