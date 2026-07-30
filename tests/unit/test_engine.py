"""Unit tests for Engine Subsystem.

Tests bootstrap, configuration integration, lifecycle transitions, state machine violations,
dependency registry, execution context, diagnostics, health reporting, and shutdown.
"""

from typing import Any

import pytest

from profileforge import __version__
from profileforge.configuration import ProfileForgeConfiguration
from profileforge.engine import (
    DependencyError,
    DependencyRegistry,
    Engine,
    EngineDiagnostics,
    EngineError,
    EngineHealth,
    ExecutionContext,
    InitializationError,
    LifecycleError,
    LifecyclePhase,
    LifecycleState,
)


def test_successful_bootstrap() -> None:
    """Verify successful engine bootstrap sequence."""
    engine = Engine()
    assert engine.state == LifecycleState.CREATED

    context = engine.bootstrap(env_overrides={})
    assert engine.state == LifecycleState.BOOTSTRAPPING
    assert isinstance(context, ExecutionContext)
    assert context.application_version == __version__
    assert engine.registry.has("configuration")
    assert engine.registry.has("diagnostics")


def test_valid_lifecycle_transitions() -> None:
    """Verify sequential lifecycle execution through all states."""
    engine = Engine()
    engine.bootstrap(env_overrides={})
    assert engine.state == LifecycleState.BOOTSTRAPPING

    engine.initialize()
    assert engine.state == LifecycleState.READY

    engine.run_pipeline()
    assert engine.state == LifecycleState.COMPLETED

    engine.shutdown()
    assert engine.state == LifecycleState.EXIT


def test_invalid_lifecycle_transition_raises_error() -> None:
    """Verify attempting invalid state transitions raises LifecycleError."""
    engine = Engine()

    # Cannot jump from CREATED directly to RUNNING
    with pytest.raises(LifecycleError):
        engine._state_machine.transition_to(LifecycleState.RUNNING)

    # Cannot run pipeline before bootstrapping/initializing
    with pytest.raises(EngineError):
        engine.run_pipeline()


def test_dependency_registration_and_retrieval() -> None:
    """Verify dependency registration, lookup by name, and lookup by type class."""
    registry = DependencyRegistry()
    dummy_config = ProfileForgeConfiguration()

    registry.register("my_config", dummy_config, instance_type=ProfileForgeConfiguration)

    assert registry.has("my_config")
    assert registry.has_type(ProfileForgeConfiguration)
    assert registry.get("my_config") == dummy_config
    assert registry.get_by_type(ProfileForgeConfiguration) == dummy_config


def test_duplicate_dependency_registration_raises_error() -> None:
    """Verify registering duplicate dependency name or type raises DependencyError."""
    registry = DependencyRegistry()
    registry.register("service1", "instance1", instance_type=str)

    with pytest.raises(DependencyError):
        registry.register("service1", "instance2")

    class ServiceType:
        pass

    s1 = ServiceType()
    s2 = ServiceType()
    registry.register("s1", s1, instance_type=ServiceType)

    with pytest.raises(DependencyError):
        registry.register("s2", s2, instance_type=ServiceType)


def test_empty_dependency_name_raises_error() -> None:
    """Verify registering dependency with empty name raises DependencyError."""
    registry = DependencyRegistry()
    with pytest.raises(DependencyError):
        registry.register("", "value")


def test_unregistered_dependency_retrieval_raises_error() -> None:
    """Verify retrieving non-existent dependency raises DependencyError."""
    registry = DependencyRegistry()
    with pytest.raises(DependencyError):
        registry.get("non_existent")

    with pytest.raises(DependencyError):
        registry.get_by_type(ProfileForgeConfiguration)


def test_graceful_shutdown() -> None:
    """Verify graceful shutdown clears registry and reaches EXIT state."""
    engine = Engine()
    engine.bootstrap(env_overrides={})
    engine.initialize()
    engine.run_pipeline()

    assert len(engine.registry.registered_names) > 0
    engine.shutdown()

    assert engine.state == LifecycleState.EXIT
    assert len(engine.registry.registered_names) == 0


def test_execution_context_creation() -> None:
    """Verify ExecutionContext immutability and attributes."""
    config = ProfileForgeConfiguration()
    ctx = ExecutionContext.create(configuration=config)

    assert ctx.application_version == __version__
    assert ctx.environment == config.app.environment
    assert isinstance(ctx.diagnostics, EngineDiagnostics)

    with pytest.raises(AttributeError):
        ctx.application_version = "2.0.0"  # type: ignore[misc]


def test_diagnostics_generation() -> None:
    """Verify EngineDiagnostics collects transition events and timing summary."""
    engine = Engine()
    engine.bootstrap(env_overrides={})
    engine.initialize()
    engine.run_pipeline()
    engine.shutdown()

    summary = engine.diagnostics.get_summary()

    assert summary["total_transitions"] > 0
    assert "total_duration_ms" in summary
    assert "phase_durations_ms" in summary
    assert LifecyclePhase.BOOTSTRAP.value in summary["phase_durations_ms"]


def test_health_reporting() -> None:
    """Verify EngineHealth report format and status."""
    engine = Engine()
    engine.bootstrap(env_overrides={})
    engine.initialize()

    health = engine.get_health()

    assert isinstance(health, EngineHealth)
    assert health.healthy is True
    assert health.lifecycle_state == LifecycleState.READY
    assert "configuration" in health.initialized_components
    assert health.configuration_status == "LOADED"

    health_dict: dict[str, Any] = health.to_dict()
    assert health_dict["healthy"] is True
    assert health_dict["lifecycle_state"] == "READY"


def test_initialize_without_bootstrap_raises_error() -> None:
    """Verify initialize() raises InitializationError if not bootstrapped."""
    engine = Engine()
    with pytest.raises(InitializationError):
        engine.initialize()
