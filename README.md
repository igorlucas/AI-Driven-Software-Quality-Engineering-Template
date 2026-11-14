# AI-Native Software Engineering & Quality Framework

This repository is a reusable framework for building software with quality evidence throughout the lifecycle—not a testing phase or a post-development QA handoff. Requirements, risks, delivery work, code changes, tests, evidence, reports, releases, and production observations are connected by stable IDs.

The framework combines human-readable working templates with a machine-readable traceability registry, a local validator/report generator, and a GitHub Actions gate. It does not assume a particular application stack or claim that a passing framework check proves product quality.

## Start here

1. Copy the framework into the product repository (or use this repository as the project quality system). Keep the platform-neutral `automation/` command and choose the matching CI adapter: `.github/workflows/quality.yml`, `.gitlab-ci.yml`, `bitbucket-pipelines.yml`, or `azure-pipelines.yml`.
2. Record business goals, features, constraints, assumptions, open questions, and acceptance criteria using [requirements/template.md](requirements/template.md).
3. Identify and assess risks using [risks/template.md](risks/template.md); design positive, negative, boundary, exploratory, security, and performance tests with [test-design/template.md](test-design/template.md).
4. Add lifecycle records and stable IDs to [traceability/records.json](traceability/records.json). Link acceptance criteria to requirements, risks and tasks; connect delivery artifacts as they are created.
5. Develop and validate continuously. Attach test output, screenshots, and other sanitized evidence to evidence records. Review and release decisions must point to evidence and unresolved risk.
6. Run `python3 automation/run_quality_checks.py`. The command runs the framework tests and strict registry validation, then generates a report and digest-based manifest. The CI adapter for your platform uploads those artifacts.
7. Record post-release observations and feed incidents, recurring defects, and decisions back into [knowledge/](knowledge/).

Read [quality-system.md](quality-system.md) for lifecycle gates, evidence rules, and the migration path. AI prompt templates live in [ai/prompts/](ai/prompts/).

## Gap analysis: current template → target framework

| Current strength or gap | Why it matters / problem solved | AI-native and traceability improvement | Quality engineering improvement |
|---|---|---|---|
| Existing `QA-nnn` criteria, stage cases, and evidence folders | These are a strong starting point, but a criterion is not connected to its source requirement, risk, delivery change, release, or production outcome. | Preserve QA IDs and add a normalized registry linking requirement → risk → task → commit → PR → test → evidence → report → release. | Enables impact analysis and supports evidence-based acceptance instead of relying on a matrix status alone. |
| Activity and closure guidance is mostly prose | A markdown-only process can drift, and the original workflow depends on manual cross-checking. | Store links in JSON and validate IDs/references automatically in local runs and pull requests. | Detects broken links and incomplete release chains early; generated reports expose open traceability gaps. |
| Requirements are implicit in a matrix row | Goals, assumptions, constraints, and questions can be lost or mistaken for acceptance criteria. | Add a dedicated requirement template and an AI analysis prompt that returns criteria, risks, edge cases, dependencies, and questions for human review. | Makes testable intent and uncertainty visible before implementation. |
| Deferred risks are tracked in one generic table | Impact, probability, priority, mitigation, owner, and validation strategy are not consistently captured. | Give risks stable IDs and an explicit template with assessment and disposition fields. | Helps teams choose proportionate validation and make release risk acceptance explicit. |
| Test design is largely functional and stage-based | Boundary, negative, exploratory, security, and performance ideas can be missed. | Add a reusable per-criterion test-design template and prompt; connect test records to criteria and evidence. | Broadens coverage without confusing “test exists” with “test passed.” |
| Reviews are not first-class lifecycle artifacts | Code, security, architecture, and maintainability concerns may not be reviewed consistently or tied back to risk. | Add focused AI-assisted review prompts and human decision guidance; record review actions as tasks/PR evidence. | Makes review repeatable while keeping humans accountable for risk and merge decisions. |
| Evidence and reports are manually recorded | Manual report assembly is slow and can omit IDs, context, or unresolved risks. | Generate machine-readable and Markdown traceability reports in CI and publish them as workflow artifacts. | Reproducible validation snapshots improve auditability; artifacts remain separate from product test evidence. |
| Production evidence is a folder placeholder | Release validation, incidents, regressions, and recurring defects do not reliably feed back into planning. | Add production observation and knowledge templates linked to releases, requirements, and follow-up tasks. | Extends quality into operations and creates a learning loop. |
| No defined AI collaboration layer | Prompts and expected output are ad hoc, making results inconsistent and hard to review. | Add prompt templates for requirements, risks, tests, reviews, incidents, and root cause analysis with explicit human verification. | Promotes structured assistance without treating generated content as validated fact. |
| Original guidance pauses code changes during proof and repeats all closed-stage tests | This encourages a late QA phase and can make feedback unnecessarily expensive. | Replace phase separation with short feedback loops and risk-based regression selection, while retaining evidence and revalidation on change. | Findings can be fixed during development; the final evidence must correspond to the final commit/build. |

### Critical limitations to keep visible

- The validator proves registry integrity and selected traceability rules—not that requirements are correct, tests are meaningful, evidence is authentic, or software is secure.
- Empty records are accepted as an unconfigured template. Teams must populate requirements and define product-specific CI tests and thresholds.
- A GitHub Actions run can validate declared data and archive a digest-based manifest for that check; it cannot invent trustworthy product evidence or infer a release decision.
- AI output is a draft. A qualified person must confirm requirement interpretation, risk ratings, review findings, root causes, and release acceptance.
- Markdown evidence can become stale. Record commit/build/environment/time, sanitize data, and retain source output where possible.

## Target repository structure

```text
.
├── .github/workflows/quality.yml   GitHub Actions adapter
├── .gitlab-ci.yml                  GitLab CI adapter
├── bitbucket-pipelines.yml         Bitbucket Pipelines adapter
├── azure-pipelines.yml             Azure Pipelines adapter
├── ai/prompts/                     reusable AI collaboration prompts
├── automation/                     traceability validator and tests
├── cases/                          existing executable/manual QA cases
├── evidence/                       sanitized test and production evidence
├── inventory/                      existing stage/matrix planning (migration bridge)
├── knowledge/                      incidents, lessons, defects, decisions
├── production/                     observations and post-release validation
├── reports/                        validation, release, and generated reports
├── releases/                       release records and checklist
├── requirements/                   goals, features, assumptions, constraints
├── reviews/                         code, security, architecture, maintainability
├── risks/                           assessed risks and mitigations
├── test-design/                     per-criterion scenario design
├── traceability/records.json        machine-readable lifecycle graph
└── work-items/                      development and remediation task templates
```

## Naming conventions

- Stable uppercase IDs, zero-padded and never reused: `REQ-001`, `QA-001`, `RISK-001`, `TASK-001`, `TEST-001`, `EVID-001`, `REPORT-001`, `RELEASE-001`, `OBS-001`, `INC-001`, `DEC-001`, `LESSON-001`, `DEFECT-001`.
- Commits use `COMMIT-<7-to-40-character-sha>`; `PR-<number>` means a pull request or merge request, regardless of provider.
- Evidence files use `<EVID-ID>_<QA-ID>_<YYYY-MM-DD>_<result>.<ext>`; result is `passed`, `failed`, or `deferred`. Include commit/build and environment in the evidence record.
- Templates use `template.md`; completed records use `<ID>_<short-kebab-title>.md`. Keep secrets, credentials, and unredacted personal/customer data out of this repository.
- One registry record per artifact; reference IDs rather than copying lifecycle data between records. Preserve IDs when artifacts move or are renamed.

## Platform portability

The lifecycle model, JSON registry, Python validator, Markdown templates, and AI prompts are platform-neutral. The runner requires Python 3.11+ and standard-library modules only; it does not call GitHub APIs. CI-specific files are adapters that run the same `python automation/run_quality_checks.py` command and publish `reports/generated/`.

| Provider | Adapter |
|---|---|
| GitHub Actions | `.github/workflows/quality.yml` |
| GitLab CI | `.gitlab-ci.yml` |
| Bitbucket Pipelines | `bitbucket-pipelines.yml` |
| Azure Pipelines | `azure-pipelines.yml` |
| Other CI (for example Jenkins, CircleCI, Buildkite, TeamCity) | Invoke the same runner command and archive `reports/generated/` |

These adapters run framework checks only. Add the product's own build/test/deploy jobs in the provider's native pipeline. For Azure Repos Git, configure the pipeline as a required branch-policy build validation: Azure Repos does not use YAML `pr:` triggers in the same way as GitHub/Bitbucket.

## Recommended GitHub Actions

The CI files are thin adapters over `automation/run_quality_checks.py`, the platform-neutral command for traceability validation, Python unit tests, report/evidence generation, and artifact publication. GitHub Actions is not required: use the GitLab, Bitbucket, or Azure adapter, or call the same command from another CI runner. Extend the adapter with the product's existing build/test jobs and stack-appropriate checks, for example:

- Unit, integration, contract, and end-to-end tests with coverage thresholds.
- Lint, formatting, type checks, dependency/license policy, secret scanning, and static analysis.
- API/schema compatibility and migration checks.
- Risk-based security analysis and performance smoke tests; run heavier tests on schedule or release candidates.
- Build provenance/SBOM, artifact signing, deployment approvals, and post-deployment smoke checks.
- A release gate that requires linked evidence and explicit acceptance of open risks.

Pin third-party actions to reviewed immutable SHAs in production, apply minimal permissions, and avoid exposing secrets to untrusted pull-request code. No product-specific test commands are assumed by this generic template.

## Opportunities for AI automation

The current implementation automates registry checks, report generation, and provenance for that validation. Product-specific teams can add the following as opt-in steps:

- Draft structured requirements and acceptance criteria from approved discovery notes; create issues only after owner review.
- On pull requests, suggest affected requirement/risk IDs and identify missing registry links; CI—not the model—enforces ID and chain integrity.
- Generate candidate test cases or test scaffolds from accepted criteria, then require normal code review and execution.
- Summarize test results into evidence metadata (commit, environment, test IDs, artifact digest); retain raw sanitized test output as the source.
- Recommend regression scope from changed files, task/criterion links, and risk, while allowing engineers to expand it and keeping a full-suite path.
- Draft code/security/architecture review findings with file/line evidence; require a human to confirm findings and decide merge readiness.
- Summarize sanitized production observations and incident timelines into candidate incident, defect, risk, and follow-up records; incident leads confirm impact and root cause.
- Assemble release reports from CI artifacts and list unresolved criteria/risks; protected environment approvals remain an accountable human decision.

Use explicit data handling, provenance, prompt/version tracking, and human approval at every consequential boundary. Do not grant a model deployment, risk-acceptance, merge, or incident-closure authority by default.

## Migration plan

1. Adopt the framework and keep the existing `cases/`, `evidence/`, `reports/`, and `inventory/` content. Their current `QA-nnn` identifiers remain valid.
2. For each existing matrix row, create a `REQ` record for its source business need and a `QA` criterion record. Record unknown sources as open questions rather than inventing intent.
3. Create risk and task records; connect existing test paths, evidence, and reports. Add commits and PR references when verifiable; do not fabricate historical links.
4. Map each existing stage to a release/checkpoint only when its completion evidence supports it. Mark gaps as open or deferred, with owner/condition where known.
5. Keep requirements in active states during migration, fix malformed IDs and dangling links, and mark a requirement `released` only after the strict CI gate confirms its full lifecycle chain.
6. Add product-specific test/build/security jobs and publish generated reports as CI artifacts. Review the process after the first delivery and feed operational learnings back into the templates.

## Framework maturity

The repository is a framework baseline, not a universal 10/10 guarantee. Industry alignment requires adapting controls to the product, threat model, regulatory obligations, and runtime. A team should claim a requirement is released only when the traceability chain and product-specific validation are actually demonstrated.
