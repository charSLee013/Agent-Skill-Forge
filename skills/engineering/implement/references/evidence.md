# Evidence for behavior claims

Use this reference during inspection, diagnosis, or implementation when a claim
needs verification. A read-only request remains read-only. Evidence requirements
do not independently authorize changes to code, data, or external state.

Identify each acceptance condition and the observations needed to establish it.
Trace relevant parts of its causal path, such as configuration, registration,
instructions, invocation, permissions, and the actual result. Separate inspected
facts, inferences, and proposed actions.

## Describe what each observation establishes

These descriptions are complementary, not ranked levels:

- `static`: named checks or focused source/content review, with the predicate and
  limits stated. They can establish structural or interface properties within
  their coverage; they do not by themselves establish a runtime outcome.
- `real-path`: observation through the required real runtime path or a replay
  with relevant equivalence established. Name the path, environment, and business
  result to observe. Use `real-path-verification` for this work.
- `target`: a falsifiable measurement: metric or definition, direction or
  comparison, threshold or baseline, unit, source, and observation window.
  Establish whether the source must also satisfy a real-path requirement.

One condition may need several observations, and one issue may contain conditions
with different evidence. Record all necessary observations and their expected
results under that condition. Existing single `Evidence` entries remain valid;
no format conversion is required. A shared observation may support several
conditions if it actually covers them; retain the mapping to each condition.
A target measurement cannot replace an independent compatibility or correctness
check merely because it produces a number.

Choose the least costly sufficient set of observations. A configuration value,
passing unit test, process exit, or HTTP status proves only what it observes.
A SHA-256 checksum proves byte identity against its reference, not runtime
behavior. Use it for integrity when integrity is the actual question; observe
the requested outcome for behavioral acceptance.

## Obtain evidence within the task

Use current tool schemas and suitable existing entry points first. Investigate
a failed call's actual error before concluding that a tool or environment is
unavailable. When necessary and covered by the task, add a small invocation,
temporary input, or measurement helper. Judge auxiliary work by what it enables,
its cost, and its side effects, rather than its file type. Its output supports
only what it observes; a helper or mock cannot stand in for a required real path.
Do not create artifacts merely to make a claim look more rigorous.

Reuse established authorization for the concrete action. Resolve new material
decisions or unapproved side effects before executing them; routine reversible
support within the task needs no separate approval. Arrange cleanup and recovery
proportionate to consequences. Ordinary temporary files need reasonable cleanup;
sensitive data, production state, and shared resources need controls addressing
their actual exposure or disruption.

When reproduction is unavailable, source inspection and existing traces can
support an inference; distinguish it from an executed reproduction. Report the
conclusion with its evidence and unverified limits. If access, materials, or
runtime conditions are missing, identify the affected criterion and continue
independent authorized work. Never silently weaken the acceptance contract.

## Example: one result, several observations

Suppose a PRD requires: on workload W, improve throughput by at least 20% over
baseline B while keeping output correct and the public interface compatible.
The process must stay within 60 GB peak memory, with 30 minutes of total
experimental runtime shared across the feature. These numbers illustrate a
contract, not default thresholds or budgets.

The same acceptance condition can carry:

- `target`: completed work per second on W, candidate/B ≥ 1.20 during matched
  10-minute steady-state windows; observe total process peak memory ≤ 60 GB,
  including transient allocations. State environment and measurement sources.
- `real-path`: use the approved application path on W, observe completed output
  equivalent to B under the specified correctness contract, and establish any
  required replay parity. This path can also supply the throughput measurement.
- `static`: run the existing interface compatibility checks and inspect the
  public API changes against the stated compatibility predicate; record gaps
  those checks cannot cover.

If this is one coherent change, `to-issues` may keep it in
`issues/01-optimize.md`, which also owns combined feature acceptance. The triage
brief, execution brief, and any prepared Goal retain all three observations,
their expected results, and the one shared runtime budget. `implement` measures
performance, verifies real output, and checks compatibility before marking it
done; `implement-spec` compares the combined result with the original PRD.
A faster run does not discharge the output or interface requirements. If noise
prevents a supported performance conclusion within the remaining budget, report
that condition unverified rather than spending another full budget per issue.
