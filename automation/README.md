# Automation entry point

The framework's CI-neutral command is:

```sh
python automation/run_quality_checks.py
```

It runs the validator's unit tests and strict traceability validation, generating the Markdown/JSON report and validation-evidence manifest under `reports/generated/`. Both checks run even if the tests fail, so CI can still publish the traceability report.

The GitHub Actions, GitLab CI, Bitbucket Pipelines, and Azure Pipelines files are thin platform adapters around this command. Use the adapter for your CI provider or invoke the same command in another runner and archive `reports/generated/`. Add product-specific build, test, security, and deployment checks separately; this command validates the framework, not the product.

## Focused test example

Tests use the standard-library `unittest` runner:

```python
import unittest
from validate_traceability import validate_registry


class RegistryExample(unittest.TestCase):
    def test_empty_template_is_valid(self):
        registry = {
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

        errors, warnings = validate_registry(registry)

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
```

The repository's real fixtures are in [test_validate_traceability.py](test_validate_traceability.py). Run a focused test without executing the complete suite:

```sh
python3 -m unittest automation/test_validate_traceability.py
```
