"""Automation Retry Policy Implementation.

Configurable exponential backoff retry execution wrapper.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

import time
from collections.abc import Callable
from typing import Any, TypeVar

from profileforge.automation.exceptions import RetryError
from profileforge.exceptions import ProfileForgeError

T = TypeVar("T")


class AutomationRetryPolicy:
    """Configurable exponential backoff retry execution handler."""

    def __init__(
        self,
        max_retries: int = 3,
        backoff_factor: float = 1.5,
        retryable_exceptions: tuple[type[Exception], ...] = (ProfileForgeError,),
    ) -> None:
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.retryable_exceptions = retryable_exceptions

    def execute(self, action: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute action with configurable exponential backoff retries.

        Raises:
            RetryError: If all retry attempts are exhausted.
        """
        last_exception: Exception | None = None
        delay = 0.5

        for attempt in range(1, self.max_retries + 2):
            try:
                return action(*args, **kwargs)
            except self.retryable_exceptions as exc:
                last_exception = exc
                if attempt > self.max_retries:
                    break
                time.sleep(delay)
                delay *= self.backoff_factor

        raise RetryError(
            f"Exhausted all {self.max_retries} retry attempts. Last error: {last_exception}"
        ) from last_exception
