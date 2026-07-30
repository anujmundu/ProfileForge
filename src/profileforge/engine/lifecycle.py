"""Engine Lifecycle State Machine and Phase Definitions.

Governed by 06_ENGINE_LIFECYCLE_SPECIFICATION.md.
"""

from enum import Enum
from typing import ClassVar

from profileforge.engine.exceptions import LifecycleError


class LifecycleState(str, Enum):
    """Execution states of the Engine state machine."""

    CREATED = "CREATED"
    BOOTSTRAPPING = "BOOTSTRAPPING"
    INITIALIZING = "INITIALIZING"
    READY = "READY"
    RUNNING = "RUNNING"
    GENERATING = "GENERATING"
    PUBLISHING = "PUBLISHING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SHUTDOWN = "SHUTDOWN"
    EXIT = "EXIT"


class LifecyclePhase(str, Enum):
    """The 9 canonical execution lifecycle phases."""

    BOOTSTRAP = "BOOTSTRAP"
    CONFIGURATION_LOADING = "CONFIGURATION_LOADING"
    DEPENDENCY_INITIALIZATION = "DEPENDENCY_INITIALIZATION"
    SERVICE_INITIALIZATION = "SERVICE_INITIALIZATION"
    SUBSYSTEM_INITIALIZATION = "SUBSYSTEM_INITIALIZATION"
    PIPELINE_EXECUTION = "PIPELINE_EXECUTION"
    OUTPUT_GENERATION = "OUTPUT_GENERATION"
    PUBLICATION = "PUBLICATION"
    SHUTDOWN = "SHUTDOWN"


class StateMachine:
    """Enforces valid state transitions in the Engine lifecycle."""

    # Allowed state transition map
    ALLOWED_TRANSITIONS: ClassVar[dict[LifecycleState, set[LifecycleState]]] = {
        LifecycleState.CREATED: {LifecycleState.BOOTSTRAPPING, LifecycleState.FAILED},
        LifecycleState.BOOTSTRAPPING: {LifecycleState.INITIALIZING, LifecycleState.FAILED},
        LifecycleState.INITIALIZING: {LifecycleState.READY, LifecycleState.FAILED},
        LifecycleState.READY: {LifecycleState.RUNNING, LifecycleState.FAILED},
        LifecycleState.RUNNING: {LifecycleState.GENERATING, LifecycleState.FAILED},
        LifecycleState.GENERATING: {LifecycleState.PUBLISHING, LifecycleState.FAILED},
        LifecycleState.PUBLISHING: {LifecycleState.COMPLETED, LifecycleState.FAILED},
        LifecycleState.COMPLETED: {LifecycleState.SHUTDOWN},
        LifecycleState.FAILED: {LifecycleState.SHUTDOWN},
        LifecycleState.SHUTDOWN: {LifecycleState.EXIT},
        LifecycleState.EXIT: set(),
    }

    def __init__(self, initial_state: LifecycleState = LifecycleState.CREATED) -> None:
        self._current_state: LifecycleState = initial_state

    @property
    def current_state(self) -> LifecycleState:
        """Get the current state."""
        return self._current_state

    def transition_to(self, new_state: LifecycleState) -> None:
        """Transition to a new state if valid.

        Args:
            new_state: The target LifecycleState.

        Raises:
            LifecycleError: If the transition is invalid.
        """
        allowed = self.ALLOWED_TRANSITIONS.get(self._current_state, set())
        if new_state not in allowed:
            raise LifecycleError(
                f"Invalid state transition: Cannot transition from {self._current_state.value} to {new_state.value}."
            )
        self._current_state = new_state
