# Long-Course Proof

Use long-course proof when the work spans phases, many artifacts, source matrices, HTML, subagent review, or later engineering/research transfer.

## Required State

Maintain:

- Frozen learning contract.
- Rigor contract when using evidence-intensive or stricter profiles.
- Structured object map when the subject has internal structure.
- Phase plan and gate criteria.
- `manifest.json`.
- `artifacts/source-matrix.md`.
- `artifacts/misconception-audits/`.
- `proof/` outputs for screenshots, link checks, validation logs, or final checks.
- Learning records and glossary updates.

## Phase Gate

Each phase must define:

- Goal.
- Inputs.
- Outputs.
- Validation command or manual proof.
- Gate reviewer lens.
- Pass/fail result.

Do not proceed past a failed gate. Repair first.

## Manifest Role

The manifest is the artifact survival contract. It should list required files, type, audience, status, last validation, and proof references.

If a new artifact is created, update the manifest before claiming the phase is complete.

## Final Proof Loop

Before success:

1. Stop adding scope.
2. Update final documentation or manifest state.
3. Run deterministic validators.
4. Check required artifacts still exist on disk.
5. Record proof output in `proof/` or equivalent governance directory.

Do not claim success because a file existed earlier in the session.
