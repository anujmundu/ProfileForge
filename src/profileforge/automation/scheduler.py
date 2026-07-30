"""Scheduler Abstraction Implementation.

Defines BaseScheduler contract and ManualScheduler implementation.
No platform-specific crons or GitHub Actions. Pure abstraction.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TypeVar

from profileforge.automation.exceptions import SchedulerError

T = TypeVar("T")


class BaseScheduler(ABC):
    """Abstract contract for automation execution scheduling."""

    @abstractmethod
    def schedule(self, trigger_fn: Callable[[], T]) -> T:
        """Schedule or trigger execution of workflow function."""
        raise NotImplementedError


class ManualScheduler(BaseScheduler):
    """Immediate manual execution scheduler."""

    def schedule(self, trigger_fn: Callable[[], T]) -> T:
        """Immediately trigger manual workflow execution."""
        try:
            return trigger_fn()
        except Exception as exc:
            raise SchedulerError(f"Manual execution failed: {exc}") from exc
