# Evidence

Evidence is a result of an execution tied to `TEST` and `QA` IDs in `traceability/records.json`. Store sanitized artifacts here; retain the ID, date, commit/build, environment, and result in the registry.

| Folder | What to store |
|---|---|
| `api/` | Automated test output and HTTP collection, when relevant |
| `stage-<n>/` | Screenshots and other stage evidence |
| `journeys/` | Exported journey video or image |
| `load/` | Load-test summary: thresholds, virtual users, duration |
| `security/` | Security proof that is not already inside a stage folder |
| `production/` | A dated note from the live environment: symptom and impact |
| `usability/` | Guided-session photo or video, with the script beside it |

File name: `<EVID-ID>_<QA-ID>_<YYYY-MM-DD>_<result>.<ext>`, with result `passed`, `failed`, or `deferred`.

Do not store passwords, tokens, personal/customer data, or full database exports. Redact and minimize evidence. A CI traceability report validates references only; it is not product test evidence.
