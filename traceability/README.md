# Traceability registry

`records.json` is the machine-readable index of lifecycle artifacts. Human-readable specifications, cases, reports, and evidence stay in their working folders; registry entries point to them with stable IDs and paths/URLs.

## Linking model

`REQ → RISK → TASK → COMMIT → PR → TEST → EVIDENCE → REPORT → RELEASE → OBSERVATION`

Acceptance criteria (`QA`) are children of requirements and are linked to tests. Risks/tasks and test/evidence/report/release links are explicit; each record uses arrays for plural links and a singular field for its owning record. Knowledge records (incidents, defects, lessons, decisions) link to affected requirements, risks, tasks, releases, evidence, and one another as applicable.

Use the fields in existing examples/templates; add only useful metadata. Do not copy entire artifacts into the registry. Keep it valid JSON, with no comments or trailing commas.

## Record fields

Every record has `id` and should include a human-readable `title` plus a relative `path` or canonical `url` to its source artifact when one exists. Keep detailed content in the linked artifact. The validator checks IDs and the reference fields below; it does not validate all metadata or prose.

| Collection | Required lifecycle references |
|---|---|
| `requirements` | `status`, `criteria[]`, `risk_ids[]`, `task_ids[]` |
| `criteria` | `requirement_id`, `test_ids[]` |
| `risks` | `requirement_id`, `task_ids[]` |
| `tasks` | `requirement_id`, `risk_ids[]`, `commit_ids[]`, `pr_ids[]` |
| `commits` | `task_ids[]` |
| `pull_requests` | `task_ids[]`, `commit_ids[]` |
| `tests` | `criterion_ids[]`, `evidence_ids[]` |
| `evidence` | `test_ids[]`, `report_ids[]` |
| `reports` | `evidence_ids[]`, `release_ids[]` |
| `releases` | `report_ids[]`, `requirement_ids[]` |
| `observations` | `release_id`, and applicable requirement/risk/evidence/task/incident/defect ID arrays |
| `incidents` | `release_id`, and applicable requirement/risk/task/observation ID arrays |
| `defects` | `release_id`, and applicable requirement/risk/task/test/evidence ID arrays |
| `lessons` | applicable requirement/risk/task/incident ID arrays |
| `decisions` | `release_id`, and applicable requirement/risk/task ID arrays |

Reference arrays may be empty while work is in progress. For a released requirement, strict mode requires criteria, risk and task links and verifies the reciprocal path through tests, evidence, reports, releases, commits, and PRs.

## IDs and status

IDs are globally unique, uppercase prefixes with zero-padded numbers, except `COMMIT-<sha>` and `PR-<number>` (`PR` covers pull requests and merge requests). Never recycle an ID. For requirement status, use `draft`, `approved`, `in_progress`, `validated`, `released`, or `retired`. Mark a requirement `released` only after its criteria have test/evidence/report/release links, delivery tasks have commit and review-request links, and residual risks are dispositioned.

Run `python3 automation/validate_traceability.py --report-dir reports/generated` after editing. The checker rejects malformed/duplicate IDs and dangling references. It reports incomplete work as warnings; `--strict` rejects an incomplete chain for any requirement marked `released`.
