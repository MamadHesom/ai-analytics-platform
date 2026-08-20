# Contributing

Thank you for contributing to the AI-Powered Data Analytics Platform. Contributions should preserve the project’s emphasis on clear boundaries, reproducibility, and operational safety.

## Development workflow

Create a focused branch from `main`, install both requirement sets in a virtual environment, and copy `.env.example` to `.env`. Before opening a pull request, run the complete test suite and the same checks used by CI:

```bash
pip install -r python-backend/requirements.txt -r ml-module/requirements.txt
ruff check python-backend ml-module
ruff format --check python-backend ml-module
python -m compileall python-backend/app ml-module
pytest -q python-backend/tests
```

## Code expectations

New application code should use type annotations, small composable services, explicit error handling, and structured logging rather than ad-hoc `print` statements. API changes require updated Pydantic schemas and tests for valid and invalid requests. ML changes should document the target variable, preprocessing assumptions, random seed, and evaluation metrics.

Avoid committing credentials, customer data, generated model artifacts, or large datasets. Use synthetic fixtures or anonymized samples in tests. Changes that alter model behavior should include a short explanation of expected impact and a reproducible command.

## Pull requests

Pull requests should describe the problem, the approach, verification steps, and any operational considerations. Keep commits cohesive. Reviewers should be able to run the documented commands from a clean checkout and reproduce the result without access to private infrastructure.

## Reporting issues

Please include the smallest reproducible example, relevant request payloads with secrets removed, environment details, logs, and the expected versus observed behavior. Security issues should be reported privately to the maintainers rather than opened as public issues.
