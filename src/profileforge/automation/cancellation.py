"""Cooperative Cancellation Support.

Provides CancellationToken for graceful workflow cancellation without forced thread termination.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

import contextlib
from collections.abc import Callable

from profileforge.automation.exceptions import CancellationError


class CancellationToken:
    """Cooperative cancellation token storing cancellation status and cleanup callbacks."""

    def __init__(self) -> None:
        self._is_cancelled: bool = False
        self._callbacks: list[Callable[[], None]] = []

    @property
    def is_cancelled(self) -> bool:
        """Return true if cancellation was requested."""
        return self._is_cancelled

    def cancel(self) -> None:
        """Request cancellation and invoke registered cleanup callbacks."""
        if not self._is_cancelled:
            self._is_cancelled = True
            for cb in self._callbacks:
                with contextlib.suppress(Exception):
                    cb()

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register a cleanup callback invoked upon cancellation."""
        self._callbacks.append(callback)

    def throw_if_cancelled(self) -> None:
        """Raise CancellationError if cancellation was requested."""
        if self._is_cancelled:
            raise CancellationError("Workflow execution was cancelled.")
