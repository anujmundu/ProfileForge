# Testing & Validation Workflow

ProfileForge uses Pytest and pytest-cov for automated test execution.

---

## Running Test Suites

```bash
# Run all unit, integration, e2e, resilience, regression, and performance tests
pytest

# Run tests with code coverage report
pytest --cov=src

# Run specific test directories
pytest tests/unit
pytest tests/integration
pytest tests/e2e
pytest tests/resilience
pytest tests/regression
pytest tests/performance
```

---

## Test Directory Organization

- `tests/unit/`: Subsystem unit tests.
- `tests/integration/`: Cross-subsystem interaction tests.
- `tests/e2e/`: Full pipeline end-to-end runs with mock clients.
- `tests/resilience/`: Fault injection, retry policies, and cancellation tests.
- `tests/regression/`: Determinism and snapshot schema tests.
- `tests/performance/`: Baseline timing tests.
