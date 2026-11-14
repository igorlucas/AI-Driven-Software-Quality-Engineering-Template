# Prompt: test design

Act as a quality engineer. Design tests for the supplied acceptance criteria and risk IDs. Do not claim a scenario has been executed or that coverage exists. Use only the supplied behavior; raise ambiguity instead of making it up.

For each criterion, propose applicable:

- Positive and negative scenarios.
- Boundary, state-transition, and invalid-data cases.
- Exploratory ideas that could reveal unmodeled behavior.
- Security concerns tied to trust boundaries.
- Performance/reliability concerns with candidate measurable thresholds.

For every scenario state preconditions, inputs, observable oracle, test level, data/setup needs, cleanup, and candidate automation/evidence. Explain categories that do not apply. Include dependencies, regression scope, and unresolved questions. Output structured markdown suitable for `test-design/template.md`; identify human decisions required.

## Input

- Requirement and criterion IDs/text:
- Risk IDs and mitigations:
- System/API/UI context:
- Existing tests and environment:
