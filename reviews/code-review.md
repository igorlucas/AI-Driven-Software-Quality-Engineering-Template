# Code review guidance

Review the change against its requirement and acceptance criteria, not merely its apparent intent.

- Confirm behavior, edge cases, error handling, compatibility, and tests for changed logic.
- Check that tests would fail for the relevant regression and use meaningful assertions.
- Follow data and control flow across changed call sites; inspect adjacent code only as needed to verify the change.
- Check observability, accessibility, performance, and operational behavior where relevant.
- Confirm generated/AI-written code is understandable, maintainable, and consistent with repository patterns.
- Tie actionable findings to a requirement, risk, or task; record unresolved items and rationale.

AI review output must distinguish verified findings from questions and assumptions. Humans decide severity, merge readiness, and whether a concern is accepted.
