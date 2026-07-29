# Research

Research ingestion and paper-processing tools.

## Model-invoked

Model- or user-reachable when the task needs paper lookup, paper fetching, or reference-document generation.

- **[arxiv-lookup](./arxiv-lookup/SKILL.md)** — resolves arXiv metadata, IDs, and journal DOIs; use it to identify a paper, not fetch or convert its body; it requires a query or ID plus network access and exits with a stable identifier for a builder or research workflow.
- **[arxiv-doc-builder](./arxiv-doc-builder/SKILL.md)** — fetches arXiv source/PDF material and creates a Markdown reference document; use it for paper ingestion, not metadata-only lookup or course design; it requires an arXiv ID, network, and conversion tools and exits with material for deep reading or `teach`.
