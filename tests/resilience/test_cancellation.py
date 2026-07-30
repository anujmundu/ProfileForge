"""Resilience tests for Cancellation Tokens.

Governed by 01_ENGINEERING_QUALITY_GATES.md and 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

import pytest

from profileforge.automation import CancellationToken
from profileforge.automation.exceptions import CancellationError


def test_cooperative_cancellation() -> None:
    """Verify CancellationToken triggers callbacks and raises CancellationError."""
    token = CancellationToken()
    cleaned_up = False

    def cleanup() -> None:
        nonlocal cleaned_up
        cleaned_up = True

    token.register_callback(cleanup)
    assert not token.is_cancelled

    token.cancel()
    assert token.is_cancelled
    assert cleaned_up

    with pytest.raises(CancellationError):
        token.throw_if_cancelled()
