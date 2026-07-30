"""Resilience tests for Retry policies and backoff behavior.

Governed by 01_ENGINEERING_QUALITY_GATES.md and 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

import pytest

from profileforge.automation import RetryPolicy
from profileforge.automation.exceptions import RetryError
from profileforge.exceptions import ProfileForgeError


def test_retry_policy_exponential_backoff() -> None:
    """Verify retry policy retries transient failures."""
    policy = RetryPolicy(max_retries=2, backoff_factor=1.1)
    attempts = 0

    def transient_action() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise ProfileForgeError("Transient failure")
        return "success"

    res = policy.execute(transient_action)
    assert res == "success"
    assert attempts == 2


def test_retry_policy_exhaustion() -> None:
    """Verify RetryError is raised when max_retries is reached."""
    policy = RetryPolicy(max_retries=1, backoff_factor=1.0)

    def failing_action() -> None:
        raise ProfileForgeError("Permanent failure")

    with pytest.raises(RetryError):
        policy.execute(failing_action)
