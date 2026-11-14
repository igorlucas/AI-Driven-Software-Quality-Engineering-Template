# Prompt: risk analysis

Act as a risk analyst for the supplied requirements, design, or change. Identify plausible product, security, privacy, reliability, delivery, and operational risks relevant to the context. Do not claim a vulnerability or impact without evidence; state uncertainty and assumptions.

For each candidate risk return:

- Stable candidate risk ID (or existing `RISK-nnn`) and linked requirement/criterion IDs.
- Cause → uncertain event → impact; affected users/assets and exposure window.
- Impact and probability with rationale, confidence, and evidence gaps.
- Suggested priority, validation strategy with a measurable oracle, mitigation, detection, recovery, owner, and review trigger.
- Residual risk and the decision that requires accountable human acceptance.

Also list edge cases, dependencies, and risks not assessable from the supplied context. Do not approve/accept a risk.

## Input

- Requirement/design/change:
- Threat and operating context:
- Existing risk register:
- Constraints and evidence:
