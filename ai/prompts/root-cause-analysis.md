# Prompt: root cause analysis

Analyze the supplied incident evidence as a systems-learning exercise. Do not assume there is one root cause, do not blame individuals, and do not confuse correlation with causation. Clearly label each claim as fact, hypothesis, or unknown and cite the supplied evidence.

Return:

1. A causal narrative with confidence and alternative explanations.
2. Contributing technical and organizational conditions, including why controls did not prevent or detect the event.
3. Evidence that would confirm/disprove each hypothesis.
4. Corrective actions separated into prevention, detection, mitigation, and recovery; include owner suggestion, priority rationale, measurable completion test, and trace links.
5. Updates to requirements, risks, tests, alerts, runbooks, or architecture decisions.
6. Remaining uncertainty and explicit human decisions.

Do not present generated hypotheses as confirmed root cause. Avoid sensitive data and include no exploit instructions.

## Input

- Incident ID / sanitized summary:
- Evidence and timeline:
- Relevant architecture / release:
- Existing controls and known gaps:
