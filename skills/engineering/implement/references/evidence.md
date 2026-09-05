# Evidence for behavior claims

Use this reference during inspection, diagnosis, or implementation when a claim
needs verification. It is not an implementation entry point: a read-only request
remains read-only, and missing evidence does not authorize changing code or data.

Identify the observable claim and the evidence that could establish it. Trace
only the relevant parts of its causal path, such as configuration, registration,
model-visible instructions, invocation, permissions, and the actual result.
Separate inspected facts, inferences, and proposed actions.

Choose the least costly observation that is sufficient to answer the question:
source inspection, an existing check, a CLI invocation, or an authorized runtime
path. Decide what outcome would distinguish the plausible explanations. A
configuration value, passing unit test, process exit, or HTTP status proves only
what it directly observes; it is not automatically evidence of business success.

Use current tool schemas and existing entry points. Investigate a failed call's
actual error before concluding that a whole tool or environment is unavailable.
When reproduction is unavailable, source inspection and existing traces can
narrow the explanation; distinguish that inference from a reproduced result.

Reuse authorization already established for the concrete action. Resolve any
new material decision or unapproved side effect before executing it. Do not
introduce additional approval steps for hypothetical risks or routine read-only
inspection. Production and production-equivalent acceptance use the existing
real-path-verification discipline.

Report the conclusion with enough evidence to assess it and name what remains
unverified. If missing access or observations prevent a conclusion, explain the
specific gap and continue independent authorized work. Do not create a harness,
test, report file, or raw capture merely to make a claim appear more rigorous.
