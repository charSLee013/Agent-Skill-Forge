# Student Page Boundary

Student pages are for learning. Backstage artifacts are for proof, governance, and audit.

## Student-Facing Content

Student pages should include:

- What to remember now.
- Why this matters.
- Where it sits in the course map.
- Plain-language explanation.
- Examples or diagrams that serve the explanation.
- Retrieval/practice prompts.
- Next action.

## Backstage Content

Keep these outside the main student narrative by default:

- Local filesystem paths.
- Line numbers.
- Agent logs.
- Subagent reports.
- Phase review notes.
- Source matrix filenames.
- Governance document names.
- Audit-report voice.
- Raw issue/task-management notes.

Backstage content belongs in `artifacts/`, `proof/`, `manifest.json`, or a collapsed evidence appendix.

## Evidence Appendix

If a student page needs evidence:

- Keep the main text explanatory.
- Put detailed anchors in a collapsed appendix.
- Label claim types in learner-friendly language.
- Avoid making the appendix required for basic comprehension.

## Clean Page Test

Ask:

- Would this page make sense if printed for a learner?
- Can the learner follow it without knowing the agent workflow?
- Are implementation anchors serving understanding rather than showing work?
- Is any backstage artifact name leaking into the main narrative?

If no, repair before delivery.
