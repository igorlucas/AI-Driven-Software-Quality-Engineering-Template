# Contributing

Thank you for improving the framework. Keep changes platform-neutral unless a provider-specific adapter is the subject of the change.

## Local validation

From the repository root, run:

```sh
python3 automation/run_quality_checks.py
```

The command runs the framework unit tests and strict traceability validation, then writes reports to `reports/generated/`.

On Windows, use `py -3.11 automation/run_quality_checks.py` when `py` is available.

## Change checklist

- Use stable IDs and reciprocal links in `traceability/records.json`.
- Keep Markdown links relative and verify that referenced files exist.
- Use evidence names and states described in [evidence/README.md](evidence/README.md).
- Do not commit secrets, tokens, personal data, or unredacted customer data.
- Add focused unit tests for validator or report behavior.
- Update [README.md](README.md) or the relevant README when commands or workflows change.

Before opening a pull request, run the local quality command and review `reports/generated/traceability-report.md`.
