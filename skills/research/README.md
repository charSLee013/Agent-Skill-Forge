# Research

Research ingestion, paper-processing, and explicitly requested research-loop tools.

## Model-invoked

Model- or user-reachable when the task needs paper lookup, paper fetching, or reference-document generation.

- **[arxiv-lookup](./arxiv-lookup/SKILL.md)** — resolves arXiv metadata, IDs, and journal DOIs; use it to identify a paper, not fetch or convert its body; it requires a query or ID plus network access and exits with a stable identifier for a builder or research workflow.
- **[arxiv-doc-builder](./arxiv-doc-builder/SKILL.md)** — fetches arXiv source/PDF material and creates a Markdown reference document; use it for paper ingestion, not metadata-only lookup or course design; it requires an arXiv ID, network, and conversion tools and exits with material for deep reading or `teach`.

## User-invoked

- **[research-loop](./research-loop/SKILL.md)** — designs and runs an auditable, iterative research-improvement loop with a protected judge, an open mutation surface, and a retained experiment ledger; invoke it explicitly when this operating model is wanted.
- **[antidetect-browser-lab](./antidetect-browser-lab/SKILL.md)** — installs or operates a user-owned Donut/Wayfern browser profile with an explicit proxy and loopback CDP; invoke it explicitly when this local browser workflow is wanted.
