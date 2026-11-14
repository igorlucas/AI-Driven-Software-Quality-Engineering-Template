#!/usr/bin/env python3
"""Run the framework's platform-neutral tests and traceability gate."""

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_quality_checks(report_dir, runner=subprocess.run):
    test_result = runner(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "automation",
            "-p",
            "test_*.py",
        ],
        cwd=ROOT,
        check=False,
    )
    traceability_result = runner(
        [
            sys.executable,
            "automation/validate_traceability.py",
            "--strict",
            "--report-dir",
            str(report_dir),
        ],
        cwd=ROOT,
        check=False,
    )
    return 0 if test_result.returncode == traceability_result.returncode == 0 else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("reports/generated"),
        help="Directory for generated report and validation evidence.",
    )
    args = parser.parse_args(argv)
    return run_quality_checks(args.report_dir)


if __name__ == "__main__":
    raise SystemExit(main())
