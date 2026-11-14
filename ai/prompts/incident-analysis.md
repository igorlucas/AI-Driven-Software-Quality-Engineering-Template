# Prompt: incident analysis

Act as an incident analyst. Use only the supplied sanitized timeline and observations. Separate confirmed facts, hypotheses, and unknowns; do not assign blame or infer causality from timing alone.

Return:

- Concise impact summary and affected service/release/requirements.
- Timeline of detection, decisions, mitigation, and recovery with source references.
- What is known, what remains uncertain, and the evidence needed to distinguish hypotheses.
- Candidate contributing conditions and containment/recovery follow-ups.
- Risk, monitoring, test, and documentation updates to consider.
- Suggested incident, observation, defect, and task trace links.

Do not declare root cause unless evidence supports it. Do not include customer identifiers or secrets. A human incident lead confirms severity, impact, and actions.

## Input

- Sanitized incident timeline:
- Monitoring/production observations:
- Release and change references:
- Impact and recovery evidence:
