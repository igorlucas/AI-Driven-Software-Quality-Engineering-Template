# Security review guidance

Threat-model changed boundaries and data flows: authentication, authorization, input/output handling, secrets, sensitive data, dependencies, storage, logging, and abuse limits. Consider trust boundaries and failure modes, not only known vulnerability patterns.

- Verify authorization at the server-side operation and object boundary.
- Check validation, encoding, injection resistance, cryptographic use, secret handling, and privacy-minimizing logs.
- Assess dependency and configuration changes, default exposure, and privilege changes.
- Confirm security tests target the relevant threat and record their evidence.
- Link findings to risk/task IDs and note residual risk and accountable acceptance.

Keep reviews to authorized code and configuration. Do not run exploit attempts against live or third-party systems. Report a candidate issue with affected path/line, preconditions, impact, supporting code evidence, confidence, and a safe remediation; do not infer exploitability from pattern matching alone.
