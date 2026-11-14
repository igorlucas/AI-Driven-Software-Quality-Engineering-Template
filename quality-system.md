# Quality system

Quality is a continuous engineering property demonstrated by evidence. Planning, implementation, review, testing, release, and operations share one lifecycle record in `traceability/records.json`; `inventory/traceability-matrix.md` remains a useful human-readable view and migration bridge.

## Lifecycle and gates

| Lifecycle step | Minimum record | Exit evidence |
|---|---|---|
| Requirement | `REQ` with goals/context, constraints, assumptions, open questions, and linked `QA` criteria | Criteria are observable/testable; unresolved questions have owners or explicit acceptance |
| Risk | `RISK` linked to the requirement, with impact, probability, priority, strategy, and mitigation | Risk owner and response are known; residual risk is visible |
| Development | `TASK` linked to requirement and risks | Change is implemented and linked to commit(s) and a reviewed PR |
| Validation | `TEST` linked to acceptance criteria | Relevant automated/manual test result and regression scope are recorded |
| Evidence | `EVID` linked to test(s) | Sanitized, dated, reproducible artifact identifies commit/build and environment |
| Report | `REPORT` summarizes criteria, outcomes, failures, and accepted/deferred risks | Evidence links and disposition are reviewed |
| Release | `RELEASE` links report(s) and requirement(s) | Release approval and post-release validation plan are explicit |
| Production learning | `OBS` and relevant `INC`, `DEFECT`, `LESSON`, or `DEC` | Follow-up work is connected; findings update risks and requirements when appropriate |

The registry validator checks unique IDs and reference integrity. Strict checks for `released` requirements ensure a complete linked chain. A valid chain is necessary but does not prove the quality or authenticity of its contents.

## Evidence and closure

Every result records: criterion ID, method, result (`passed`, `failed`, `deferred`), timestamp, environment, commit/build, and evidence location. `covered` means a test file exists; it is not an execution result or acceptance.

- A failed check creates a defect or task and is fixed in the normal development loop. Re-run affected tests and capture evidence for the final commit/build; do not freeze product changes while a proof is underway.
- Select regression scope based on changed behavior, dependency graph, and risk. Run the full suite when the impact is broad or cannot be bounded.
- Use browser, API, usability, load, or security channels when they answer a relevant product question—not as ritualized channels for every criterion.
- A deferred proof includes the impediment, owner (when known), and the condition or date that makes validation possible. Unaccepted high risks block release.
- Evidence must be attributable and reproducible where feasible. Store links/metadata and sanitized outputs; never commit secrets, credentials, or raw customer data.

## AI collaboration and human accountability

Prompts under `ai/prompts/` request structured drafts and explicit uncertainty. Keep source context and output connected to stable IDs. Humans confirm scope, factual claims, severity, security findings, root cause, and acceptance decisions. Do not treat generated tests, summaries, or reviews as proof until executed or independently checked.

## Automation and continuous improvement

Run `python3 automation/run_quality_checks.py` locally. The GitHub Actions, GitLab CI, Bitbucket Pipelines, and Azure Pipelines adapters invoke the same command and publish its report plus digest manifest for the framework validation run. Any CI runner with Python 3.11+ can invoke the same command. In Azure Repos Git, use a branch-policy build validation for pull requests. The manifest is not evidence that product tests passed. Add product builds and tests to the relevant CI pipeline; this framework has no application code to test.

Incidents, production observations, recurring defects, lessons, and decisions belong under `knowledge/` or `production/`. Link observations to releases and follow-up tasks so operational evidence updates the next planning cycle.

## Migration from the original template

Keep the existing case, evidence, report, and inventory files. Retain `QA-nnn` IDs. Add requirement records for verified business intent, then link risks, tasks, commits, PRs, tests, evidence, reports, and releases as known. Unknown historical provenance remains unknown; do not fabricate traceability. The matrix remains a readable view, while the registry becomes the checked link index.
