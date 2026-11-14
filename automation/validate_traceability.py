#!/usr/bin/env python3
"""Validate lifecycle references and generate a traceability report."""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "traceability" / "records.json"

ID_PATTERNS = {
    "requirements": r"REQ-\d{3,}",
    "criteria": r"QA-\d{3,}",
    "risks": r"RISK-\d{3,}",
    "tasks": r"TASK-\d{3,}",
    "commits": r"COMMIT-[0-9a-f]{7,40}",
    "pull_requests": r"PR-\d+",
    "tests": r"TEST-\d{3,}",
    "evidence": r"EVID-\d{3,}",
    "reports": r"REPORT-\d{3,}",
    "releases": r"RELEASE-\d{3,}",
    "observations": r"OBS-\d{3,}",
    "incidents": r"INC-\d{3,}",
    "defects": r"DEFECT-\d{3,}",
    "lessons": r"LESSON-\d{3,}",
    "decisions": r"DEC-\d{3,}",
}

REFERENCES = {
    "requirements": {
        "criteria": ("criteria", True),
        "risk_ids": ("risks", True),
        "task_ids": ("tasks", True),
    },
    "criteria": {
        "requirement_id": ("requirements", False),
        "test_ids": ("tests", True),
    },
    "risks": {
        "requirement_id": ("requirements", False),
        "task_ids": ("tasks", True),
    },
    "tasks": {
        "requirement_id": ("requirements", False),
        "risk_ids": ("risks", True),
        "commit_ids": ("commits", True),
        "pr_ids": ("pull_requests", True),
    },
    "commits": {"task_ids": ("tasks", True)},
    "pull_requests": {
        "task_ids": ("tasks", True),
        "commit_ids": ("commits", True),
    },
    "tests": {
        "criterion_ids": ("criteria", True),
        "evidence_ids": ("evidence", True),
    },
    "evidence": {
        "test_ids": ("tests", True),
        "report_ids": ("reports", True),
    },
    "reports": {
        "evidence_ids": ("evidence", True),
        "release_ids": ("releases", True),
    },
    "releases": {
        "report_ids": ("reports", True),
        "requirement_ids": ("requirements", True),
    },
    "observations": {
        "release_id": ("releases", False),
        "requirement_ids": ("requirements", True),
        "risk_ids": ("risks", True),
        "evidence_ids": ("evidence", True),
        "task_ids": ("tasks", True),
        "incident_ids": ("incidents", True),
        "defect_ids": ("defects", True),
    },
    "incidents": {
        "requirement_ids": ("requirements", True),
        "risk_ids": ("risks", True),
        "task_ids": ("tasks", True),
        "release_id": ("releases", False),
        "observation_ids": ("observations", True),
    },
    "defects": {
        "requirement_ids": ("requirements", True),
        "risk_ids": ("risks", True),
        "task_ids": ("tasks", True),
        "test_ids": ("tests", True),
        "evidence_ids": ("evidence", True),
        "release_id": ("releases", False),
    },
    "lessons": {
        "requirement_ids": ("requirements", True),
        "risk_ids": ("risks", True),
        "task_ids": ("tasks", True),
        "incident_ids": ("incidents", True),
    },
    "decisions": {
        "requirement_ids": ("requirements", True),
        "risk_ids": ("risks", True),
        "task_ids": ("tasks", True),
        "release_id": ("releases", False),
    },
}


def validate_registry(data, strict=False):
    errors = []
    warnings = []
    ids_by_collection = {}
    records_by_collection = {}
    global_ids = {}

    if not isinstance(data, dict):
        return ["Registry root must be a JSON object."], warnings
    if data.get("version") != 1:
        errors.append("Registry version must be 1.")

    for collection, pattern in ID_PATTERNS.items():
        records = data.get(collection)
        if not isinstance(records, list):
            errors.append(f"'{collection}' must be an array.")
            records = []
        ids = set()
        records_by_collection[collection] = {}
        for index, record in enumerate(records):
            location = f"{collection}[{index}]"
            if not isinstance(record, dict):
                errors.append(f"{location} must be an object.")
                continue
            record_id = record.get("id")
            if not isinstance(record_id, str) or not re.fullmatch(pattern, record_id):
                errors.append(f"{location}.id must match {pattern}.")
                continue
            if record_id in global_ids:
                errors.append(
                    f"Duplicate ID '{record_id}' in {location}; already used in "
                    f"{global_ids[record_id]}."
                )
                continue
            ids.add(record_id)
            global_ids[record_id] = location
            records_by_collection[collection][record_id] = record
        ids_by_collection[collection] = ids

    for collection, fields in REFERENCES.items():
        for record_id, record in records_by_collection.get(collection, {}).items():
            for field, (target_collection, is_plural) in fields.items():
                value = record.get(field, [] if is_plural else None)
                if is_plural:
                    if not isinstance(value, list):
                        errors.append(f"{record_id}.{field} must be an array.")
                        continue
                    references = value
                else:
                    if value is None or value == "":
                        continue
                    references = [value]
                for reference in references:
                    if not isinstance(reference, str):
                        errors.append(f"{record_id}.{field} entries must be strings.")
                    elif reference not in ids_by_collection.get(target_collection, set()):
                        errors.append(
                            f"{record_id}.{field} references unknown "
                            f"{target_collection} ID '{reference}'."
                        )

    if errors:
        return errors, warnings

    for requirement in records_by_collection.get("requirements", {}).values():
        if requirement.get("status") == "released":
            missing = []
            for field in ("criteria", "risk_ids", "task_ids"):
                if not requirement.get(field):
                    missing.append(field)
            for criterion_id in requirement.get("criteria", []):
                criterion = records_by_collection.get("criteria", {}).get(criterion_id, {})
                if criterion.get("requirement_id") != requirement["id"]:
                    missing.append(f"{criterion_id} does not link {requirement['id']}")
                if not criterion.get("test_ids"):
                    missing.append(f"{criterion_id} tests")
                for test_id in criterion.get("test_ids", []):
                    test = records_by_collection.get("tests", {}).get(test_id, {})
                    if criterion_id not in test.get("criterion_ids", []):
                        missing.append(f"{test_id} does not link {criterion_id}")
                    if not test.get("evidence_ids"):
                        missing.append(f"{test_id} evidence")
                    for evidence_id in test.get("evidence_ids", []):
                        evidence = records_by_collection.get("evidence", {}).get(
                            evidence_id, {}
                        )
                        if test_id not in evidence.get("test_ids", []):
                            missing.append(f"{evidence_id} does not link {test_id}")
                        if not evidence.get("report_ids"):
                            missing.append(f"{evidence_id} reports")
                        for report_id in evidence.get("report_ids", []):
                            report = records_by_collection.get("reports", {}).get(
                                report_id, {}
                            )
                            if evidence_id not in report.get("evidence_ids", []):
                                missing.append(
                                    f"{report_id} does not link {evidence_id}"
                                )
                            if not report.get("release_ids"):
                                missing.append(f"{report_id} releases")
                            for release_id in report.get("release_ids", []):
                                release = records_by_collection.get("releases", {}).get(
                                    release_id, {}
                                )
                                if report_id not in release.get("report_ids", []):
                                    missing.append(
                                        f"{release_id} does not link {report_id}"
                                    )
                                if requirement["id"] not in release.get(
                                    "requirement_ids", []
                                ):
                                    missing.append(
                                        f"{release_id} does not link {requirement['id']}"
                                    )
            for task_id in requirement.get("task_ids", []):
                task = records_by_collection.get("tasks", {}).get(task_id, {})
                if task.get("requirement_id") != requirement["id"]:
                    missing.append(f"{task_id} does not link {requirement['id']}")
                if not task.get("commit_ids"):
                    missing.append(f"{task_id} commits")
                if not task.get("pr_ids"):
                    missing.append(f"{task_id} pull requests")
                for commit_id in task.get("commit_ids", []):
                    commit = records_by_collection.get("commits", {}).get(commit_id, {})
                    if task_id not in commit.get("task_ids", []):
                        missing.append(f"{commit_id} does not link {task_id}")
                for pr_id in task.get("pr_ids", []):
                    pull_request = records_by_collection.get("pull_requests", {}).get(
                        pr_id, {}
                    )
                    if task_id not in pull_request.get("task_ids", []):
                        missing.append(f"{pr_id} does not link {task_id}")
                    if not set(task.get("commit_ids", [])).intersection(
                        pull_request.get("commit_ids", [])
                    ):
                        missing.append(f"{pr_id} does not link a {task_id} commit")
            for risk_id in requirement.get("risk_ids", []):
                risk = records_by_collection.get("risks", {}).get(risk_id, {})
                if risk.get("requirement_id") != requirement["id"]:
                    missing.append(f"{risk_id} does not link {requirement['id']}")
                if not set(requirement.get("task_ids", [])).intersection(
                    risk.get("task_ids", [])
                ):
                    missing.append(f"{risk_id} does not link a {requirement['id']} task")
                for task_id in risk.get("task_ids", []):
                    task = records_by_collection.get("tasks", {}).get(task_id, {})
                    if risk_id not in task.get("risk_ids", []):
                        missing.append(f"{task_id} does not link {risk_id}")
            if missing:
                message = (
                    f"{requirement['id']} is released with an incomplete chain: "
                    + ", ".join(sorted(set(missing)))
                    + "."
                )
                (errors if strict else warnings).append(message)

    for requirement in records_by_collection.get("requirements", {}).values():
        gaps = []
        field_names = {
            "criteria": "acceptance criteria",
            "risk_ids": "risks",
            "task_ids": "tasks",
        }
        for field, name in field_names.items():
            if not requirement.get(field):
                gaps.append(f"no {name}")
        for criterion_id in requirement.get("criteria", []):
            criterion = records_by_collection.get("criteria", {}).get(criterion_id, {})
            if not criterion.get("test_ids"):
                gaps.append(f"{criterion_id} has no tests")
            for test_id in criterion.get("test_ids", []):
                test = records_by_collection.get("tests", {}).get(test_id, {})
                if not test.get("evidence_ids"):
                    gaps.append(f"{test_id} has no evidence")
                for evidence_id in test.get("evidence_ids", []):
                    evidence = records_by_collection.get("evidence", {}).get(
                        evidence_id, {}
                    )
                    if not evidence.get("report_ids"):
                        gaps.append(f"{evidence_id} has no report")
                    for report_id in evidence.get("report_ids", []):
                        report = records_by_collection.get("reports", {}).get(
                            report_id, {}
                        )
                        if not report.get("release_ids"):
                            gaps.append(f"{report_id} has no release")
        for task_id in requirement.get("task_ids", []):
            task = records_by_collection.get("tasks", {}).get(task_id, {})
            if not task.get("commit_ids"):
                gaps.append(f"{task_id} has no commit")
            if not task.get("pr_ids"):
                gaps.append(f"{task_id} has no pull request")
        if gaps:
            warnings.append(
                f"{requirement['id']} traceability gaps: "
                + ", ".join(sorted(set(gaps)))
                + "."
            )

    return errors, warnings


def build_report(data, errors, warnings, registry_sha256=None):
    if not isinstance(data, dict):
        data = {}
    counts = {
        collection: len(records) if isinstance(records, list) else 0
        for collection in ID_PATTERNS
        for records in [data.get(collection, [])]
    }
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "valid": not errors,
        "counts": counts,
        "total_records": sum(counts.values()),
        "registry_sha256": registry_sha256,
        "errors": errors,
        "warnings": warnings,
    }


def write_report(report, report_dir):
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / "traceability-validation.json"
    markdown_path = report_dir / "traceability-validation.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Traceability validation",
        "",
        f"- Generated: {report['generated_at']}",
        f"- Result: {'PASS' if report['valid'] else 'FAIL'}",
        f"- Records: {report['total_records']}",
        "",
        "## Record counts",
        "",
        "| Collection | Records |",
        "|---|---:|",
    ]
    lines.extend(
        f"| {collection} | {count} |"
        for collection, count in report["counts"].items()
    )
    for title, key in (("Errors", "errors"), ("Warnings", "warnings")):
        lines.extend(["", f"## {title}", ""])
        lines.extend(f"- {item}" for item in report[key])
        if not report[key]:
            lines.append("- None")
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    evidence = {
        "kind": "framework-traceability-validation",
        "result": "passed" if report["valid"] else "failed",
        "generated_at": report["generated_at"],
        "registry_sha256": report["registry_sha256"],
        "report_sha256": hashlib.sha256(json_path.read_bytes()).hexdigest(),
        "repository_commit": os.environ.get("GITHUB_SHA"),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
    }
    (report_dir / "validation-evidence.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--report-dir", type=Path)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail when a requirement marked released has an incomplete lifecycle chain.",
    )
    args = parser.parse_args(argv)

    try:
        raw_registry = args.registry.read_bytes()
        data = json.loads(raw_registry)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not read registry {args.registry}: {error}", file=sys.stderr)
        return 2

    errors, warnings = validate_registry(data, strict=args.strict)
    report = build_report(
        data,
        errors,
        warnings,
        registry_sha256=hashlib.sha256(raw_registry).hexdigest(),
    )
    if args.report_dir:
        write_report(report, args.report_dir)

    print(
        f"Traceability: {'PASS' if report['valid'] else 'FAIL'} "
        f"({report['total_records']} records, "
        f"{len(errors)} errors, {len(warnings)} warnings)"
    )
    for message in errors + warnings:
        print(f"{'ERROR' if message in errors else 'WARNING'}: {message}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
