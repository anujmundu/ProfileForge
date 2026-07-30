"""Engine Orchestrator Implementation.

Coordinates lifecycle state transitions, phase execution, dependency registration,
diagnostics tracking, health reporting, and graceful shutdown.
Governed by 06_ENGINE_LIFECYCLE_SPECIFICATION.md.
"""

from pathlib import Path
from typing import Any

from profileforge.engine.bootstrap import bootstrap_engine
from profileforge.engine.context import ExecutionContext
from profileforge.engine.diagnostics import EngineDiagnostics
from profileforge.engine.exceptions import EngineError, InitializationError
from profileforge.engine.health import EngineHealth
from profileforge.engine.lifecycle import LifecyclePhase, LifecycleState, StateMachine
from profileforge.engine.registry import DependencyRegistry


class Engine:
    """The central orchestrator of the ProfileForge platform application lifecycle."""

    def __init__(self) -> None:
        self._state_machine = StateMachine(initial_state=LifecycleState.CREATED)
        self._context: ExecutionContext | None = None
        self._registry: DependencyRegistry | None = None
        self._diagnostics: EngineDiagnostics = EngineDiagnostics()

    @property
    def state(self) -> LifecycleState:
        """Get current state of the Engine state machine."""
        return self._state_machine.current_state

    @property
    def context(self) -> ExecutionContext:
        """Get the execution context.

        Raises:
            EngineError: If engine has not been bootstrapped.
        """
        if self._context is None:
            raise EngineError("Engine has not been bootstrapped. Call bootstrap() first.")
        return self._context

    @property
    def registry(self) -> DependencyRegistry:
        """Get the dependency registry.

        Raises:
            EngineError: If engine has not been bootstrapped.
        """
        if self._registry is None:
            raise EngineError("Engine has not been bootstrapped. Call bootstrap() first.")
        return self._registry

    @property
    def diagnostics(self) -> EngineDiagnostics:
        """Get engine diagnostics collector."""
        return self._diagnostics

    def _transition_to(self, new_state: LifecycleState) -> None:
        """Helper to record transition and update state machine."""
        old_state = self._state_machine.current_state
        self._state_machine.transition_to(new_state)
        self._diagnostics.record_transition(from_state=old_state, to_state=new_state)

    def bootstrap(
        self,
        config_file: Path | str | None = None,
        env_overrides: dict[str, str] | None = None,
        raw_overrides: dict[str, Any] | None = None,
    ) -> ExecutionContext:
        """Bootstrap the application, load configuration, and create context.

        Args:
            config_file: Optional configuration file path.
            env_overrides: Optional environment overrides.
            raw_overrides: Optional raw dictionary overrides.

        Returns:
            Immutable ExecutionContext instance.
        """
        self._transition_to(LifecycleState.BOOTSTRAPPING)
        self._diagnostics.timing_tracker.start_phase(LifecyclePhase.BOOTSTRAP)

        try:
            ctx, reg = bootstrap_engine(
                config_file=config_file,
                env_overrides=env_overrides,
                raw_overrides=raw_overrides,
            )
            self._context = ctx
            self._registry = reg
            self._diagnostics = ctx.diagnostics

            self._diagnostics.timing_tracker.complete_phase(LifecyclePhase.BOOTSTRAP)
            self._diagnostics.timing_tracker.complete_phase(
                LifecyclePhase.CONFIGURATION_LOADING
            )
            return self._context
        except Exception:
            self._transition_to(LifecycleState.FAILED)
            raise

    def initialize(self) -> None:
        """Initialize dependencies, services, and subsystems in order."""
        if self._context is None or self._registry is None:
            raise InitializationError(
                "Cannot initialize engine: Engine must be bootstrapped first."
            )

        self._transition_to(LifecycleState.INITIALIZING)

        try:
            # Phase 3: Dependency Initialization
            self._diagnostics.timing_tracker.start_phase(
                LifecyclePhase.DEPENDENCY_INITIALIZATION
            )
            self._diagnostics.record_subsystem_status("registry", initialized=True)
            self._diagnostics.timing_tracker.complete_phase(
                LifecyclePhase.DEPENDENCY_INITIALIZATION
            )

            # Phase 4: Service Initialization
            self._diagnostics.timing_tracker.start_phase(
                LifecyclePhase.SERVICE_INITIALIZATION
            )
            self._diagnostics.record_subsystem_status("services", initialized=True)
            self._diagnostics.timing_tracker.complete_phase(
                LifecyclePhase.SERVICE_INITIALIZATION
            )

            # Phase 5: Subsystem Initialization
            self._diagnostics.timing_tracker.start_phase(
                LifecyclePhase.SUBSYSTEM_INITIALIZATION
            )
            self._diagnostics.record_subsystem_status("subsystems", initialized=True)
            self._diagnostics.timing_tracker.complete_phase(
                LifecyclePhase.SUBSYSTEM_INITIALIZATION
            )

            self._transition_to(LifecycleState.READY)
        except Exception as exc:
            self._transition_to(LifecycleState.FAILED)
            raise InitializationError(f"Engine initialization failed: {exc}") from exc

    def run_pipeline(self) -> None:
        """Coordinate pipeline execution, asset generation, and publication."""
        if self.state != LifecycleState.READY:
            raise EngineError(
                f"Cannot run pipeline: Engine state must be READY (current state: {self.state.value})."
            )

        try:
            # Phase 6: Pipeline Execution
            self._transition_to(LifecycleState.RUNNING)
            self._diagnostics.timing_tracker.start_phase(
                LifecyclePhase.PIPELINE_EXECUTION
            )
            self._diagnostics.timing_tracker.complete_phase(
                LifecyclePhase.PIPELINE_EXECUTION
            )

            # Phase 7: Output Generation
            self._transition_to(LifecycleState.GENERATING)
            self._diagnostics.timing_tracker.start_phase(
                LifecyclePhase.OUTPUT_GENERATION
            )
            self._diagnostics.timing_tracker.complete_phase(
                LifecyclePhase.OUTPUT_GENERATION
            )

            # Phase 8: Publication
            self._transition_to(LifecycleState.PUBLISHING)
            self._diagnostics.timing_tracker.start_phase(LifecyclePhase.PUBLICATION)
            self._diagnostics.timing_tracker.complete_phase(
                LifecyclePhase.PUBLICATION
            )

            self._transition_to(LifecycleState.COMPLETED)
        except Exception as exc:
            self._transition_to(LifecycleState.FAILED)
            raise EngineError(f"Pipeline execution failed: {exc}") from exc

    def shutdown(self) -> None:
        """Execute graceful shutdown sequence and release resources."""
        # Shutdown phase can transition from COMPLETED or FAILED
        if self.state in (LifecycleState.COMPLETED, LifecycleState.FAILED):
            self._transition_to(LifecycleState.SHUTDOWN)
        elif self.state != LifecycleState.SHUTDOWN and self.state != LifecycleState.EXIT:
            # Force transition if in intermediate state
            self._state_machine._current_state = LifecycleState.SHUTDOWN
            self._diagnostics.record_transition(
                from_state=self.state, to_state=LifecycleState.SHUTDOWN
            )

        self._diagnostics.timing_tracker.start_phase(LifecyclePhase.SHUTDOWN)

        if self._registry is not None:
            self._registry.clear()

        self._diagnostics.timing_tracker.complete_phase(LifecyclePhase.SHUTDOWN)
        self._diagnostics.timing_tracker.complete_all()

        # Transition to EXIT
        self._transition_to(LifecycleState.EXIT)

    def get_health(self) -> EngineHealth:
        """Generate Engine health audit report."""
        initialized_comps = (
            self._registry.registered_names if self._registry is not None else []
        )
        has_config = (
            self._context is not None and self._context.configuration is not None
        )
        config_status = "LOADED" if has_config else "NONE"
        duration_ms = self._diagnostics.timing_tracker.get_summary()[
            "total_duration_ms"
        ]
        is_healthy = self.state not in (LifecycleState.FAILED,)

        return EngineHealth(
            lifecycle_state=self.state,
            initialized_components=initialized_comps,
            configuration_status=config_status,
            startup_duration_ms=duration_ms,
            healthy=is_healthy,
            warnings_count=len(self._diagnostics.warnings),
            errors_count=len(self._diagnostics.errors),
        )
