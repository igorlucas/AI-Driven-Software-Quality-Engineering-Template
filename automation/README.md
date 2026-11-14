# Automation entry point

The framework's CI-neutral command is:

```sh
python automation/run_quality_checks.py
```

It runs the validator's unit tests and strict traceability validation, generating the Markdown/JSON report and validation-evidence manifest under `reports/generated/`. Both checks run even if the tests fail, so CI can still publish the traceability report.

The GitHub Actions, GitLab CI, Bitbucket Pipelines, and Azure Pipelines files are thin platform adapters around this command. Use the adapter for your CI provider or invoke the same command in another runner and archive `reports/generated/`. Add product-specific build, test, security, and deployment checks separately; this command validates the framework, not the product.
