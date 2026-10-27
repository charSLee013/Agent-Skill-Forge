---
name: test-reliability
description: Design or diagnose an asynchronous, shared-resource, or flaky test when isolation, synchronization, teardown, or CI concurrency changes whether its result is trustworthy. Do not invoke for ordinary tests.
license: MIT
---

# Test Reliability

Make a test's observation trustworthy under the actual execution topology.
This is not a test-first workflow, a requirement to add a test, or a universal
test-suite gate. A diagnosis-only request stays read-only.

Adapted from DeepSeek Harness's `dsh-ci-test-reliability` at
`deepseek-ai/deepseek-harness@22ddee3792402c3e70ec5f86a63c3e3e895a2f60`.
Use the consuming project's runner, platforms, and CI configuration.

## Establish the topology

Inspect the relevant test runner and CI configuration. Identify which tests,
workers, processes, jobs, and hosts can overlap. For each acquired port, path,
database namespace, child process, timer, or global override, name its owner,
allocation, readiness signal, and completed cleanup signal. A separate test
process does not isolate a shared host resource.

Allocate a resource atomically through its owner, such as binding an ephemeral
port or creating a private temporary directory. Restore environment variables,
clock mocks, cwd, interceptors, and other process-global state to their exact
prior condition in the smallest scope, including on failure. Await teardown
until owned work can no longer affect another test.

Synchronize on an observable state or event rather than a sleep. Use a timeout
to bound the wait, not as proof that initialization or cleanup finished. Size
test and cleanup budgets against the actual runner; do not hide a reproducible
failure by raising timeouts, broad serialization, retries, or weaker assertions.

## Verify the claimed risk

Run the narrowest relevant check. When the defect crosses process boundaries,
check concurrent processes; when it concerns a race, establish the overlap;
when a rule rejects bad input, observe that its negative case fails. Stress
runs can support but do not replace a causal observation. Report actual runs,
skips, and remaining uncertainty without calling pending CI a pass.
