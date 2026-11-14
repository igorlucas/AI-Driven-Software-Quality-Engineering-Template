import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from run_quality_checks import run_quality_checks
from validate_traceability import build_report, validate_registry, write_report


def empty_registry():
    return {
        "version": 1,
        "requirements": [],
        "criteria": [],
        "risks": [],
        "tasks": [],
        "commits": [],
        "pull_requests": [],
        "tests": [],
        "evidence": [],
        "reports": [],
        "releases": [],
        "observations": [],
        "incidents": [],
        "defects": [],
        "lessons": [],
        "decisions": [],
    }


class TraceabilityValidationTests(unittest.TestCase):
    def test_quality_runner_runs_traceability_even_if_tests_fail(self):
        runner = Mock(side_effect=[Mock(returncode=1), Mock(returncode=0)])

        result = run_quality_checks("reports/generated", runner=runner)

        self.assertEqual(result, 1)
        self.assertEqual(runner.call_count, 2)

    def test_empty_template_is_valid(self):
        errors, warnings = validate_registry(empty_registry(), strict=True)

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_dangling_reference_is_an_error(self):
        data = empty_registry()
        data["requirements"] = [
            {
                "id": "REQ-001",
                "criteria": ["QA-999"],
                "risk_ids": [],
                "task_ids": [],
            }
        ]

        errors, _ = validate_registry(data)

        self.assertTrue(any("unknown criteria ID 'QA-999'" in error for error in errors))

    def test_incomplete_requirement_is_reported_as_a_gap(self):
        data = empty_registry()
        data["requirements"] = [
            {"id": "REQ-001", "status": "in_progress", "criteria": []}
        ]

        errors, warnings = validate_registry(data)

        self.assertEqual(errors, [])
        self.assertTrue(any("no acceptance criteria" in warning for warning in warnings))
        self.assertTrue(any("no risks" in warning for warning in warnings))

    def test_released_requirement_needs_complete_chain_in_strict_mode(self):
        data = empty_registry()
        data["requirements"] = [
            {
                "id": "REQ-001",
                "status": "released",
                "criteria": [],
                "risk_ids": [],
                "task_ids": [],
            }
        ]

        errors, warnings = validate_registry(data, strict=True)

        self.assertTrue(any("incomplete chain" in error for error in errors))
        self.assertTrue(any("no acceptance criteria" in warning for warning in warnings))

    def test_complete_released_chain_passes(self):
        data = empty_registry()
        data.update(
            {
                "requirements": [
                    {
                        "id": "REQ-001",
                        "status": "released",
                        "criteria": ["QA-001"],
                        "risk_ids": ["RISK-001"],
                        "task_ids": ["TASK-001"],
                    }
                ],
                "criteria": [
                    {
                        "id": "QA-001",
                        "requirement_id": "REQ-001",
                        "test_ids": ["TEST-001"],
                    }
                ],
                "risks": [
                    {
                        "id": "RISK-001",
                        "requirement_id": "REQ-001",
                        "task_ids": ["TASK-001"],
                    }
                ],
                "tasks": [
                    {
                        "id": "TASK-001",
                        "requirement_id": "REQ-001",
                        "risk_ids": ["RISK-001"],
                        "commit_ids": ["COMMIT-abcdef1"],
                        "pr_ids": ["PR-1"],
                    }
                ],
                "commits": [
                    {"id": "COMMIT-abcdef1", "task_ids": ["TASK-001"]}
                ],
                "pull_requests": [
                    {
                        "id": "PR-1",
                        "task_ids": ["TASK-001"],
                        "commit_ids": ["COMMIT-abcdef1"],
                    }
                ],
                "tests": [
                    {
                        "id": "TEST-001",
                        "criterion_ids": ["QA-001"],
                        "evidence_ids": ["EVID-001"],
                    }
                ],
                "evidence": [
                    {
                        "id": "EVID-001",
                        "test_ids": ["TEST-001"],
                        "report_ids": ["REPORT-001"],
                    }
                ],
                "reports": [
                    {
                        "id": "REPORT-001",
                        "evidence_ids": ["EVID-001"],
                        "release_ids": ["RELEASE-001"],
                    }
                ],
                "releases": [
                    {
                        "id": "RELEASE-001",
                        "report_ids": ["REPORT-001"],
                        "requirement_ids": ["REQ-001"],
                    }
                ],
            }
        )

        errors, warnings = validate_registry(data, strict=True)

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_strict_chain_rejects_non_reciprocal_links(self):
        data = empty_registry()
        data.update(
            {
                "requirements": [
                    {
                        "id": "REQ-001",
                        "status": "released",
                        "criteria": ["QA-001"],
                        "risk_ids": ["RISK-001"],
                        "task_ids": ["TASK-001"],
                    }
                ],
                "criteria": [
                    {
                        "id": "QA-001",
                        "requirement_id": "REQ-001",
                        "test_ids": ["TEST-001"],
                    }
                ],
                "risks": [
                    {
                        "id": "RISK-001",
                        "requirement_id": "REQ-001",
                        "task_ids": ["TASK-001"],
                    }
                ],
                "tasks": [
                    {
                        "id": "TASK-001",
                        "requirement_id": "REQ-001",
                        "risk_ids": ["RISK-001"],
                        "commit_ids": ["COMMIT-abcdef1"],
                        "pr_ids": ["PR-1"],
                    }
                ],
                "commits": [
                    {"id": "COMMIT-abcdef1", "task_ids": ["TASK-001"]}
                ],
                "pull_requests": [
                    {
                        "id": "PR-1",
                        "task_ids": ["TASK-001"],
                        "commit_ids": [],
                    }
                ],
                "tests": [
                    {
                        "id": "TEST-001",
                        "criterion_ids": ["QA-001"],
                        "evidence_ids": ["EVID-001"],
                    }
                ],
                "evidence": [
                    {
                        "id": "EVID-001",
                        "test_ids": ["TEST-001"],
                        "report_ids": ["REPORT-001"],
                    }
                ],
                "reports": [
                    {
                        "id": "REPORT-001",
                        "evidence_ids": ["EVID-001"],
                        "release_ids": ["RELEASE-001"],
                    }
                ],
                "releases": [
                    {
                        "id": "RELEASE-001",
                        "report_ids": ["REPORT-001"],
                        "requirement_ids": ["REQ-001"],
                    }
                ],
            }
        )

        errors, _ = validate_registry(data, strict=True)

        self.assertTrue(any("does not link a TASK-001 commit" in e for e in errors))

    def test_report_generation_includes_validation_evidence(self):
        data = empty_registry()
        errors, warnings = validate_registry(data, strict=True)
        report = build_report(
            data, errors, warnings, registry_sha256="registry-digest"
        )

        with tempfile.TemporaryDirectory() as directory:
            write_report(report, Path(directory))
            evidence = json.loads(
                (Path(directory) / "validation-evidence.json").read_text(
                    encoding="utf-8"
                )
            )

        self.assertEqual(evidence["result"], "passed")
        self.assertEqual(evidence["registry_sha256"], "registry-digest")
        self.assertTrue(evidence["report_sha256"])


if __name__ == "__main__":
    unittest.main()
