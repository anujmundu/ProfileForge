"""Engine Bootstrap Implementation.

Coordinates application bootstrap, configuration loading, execution context creation,
and initial dependency registration.
Governed by 06_ENGINE_LIFECYCLE_SPECIFICATION.md.
"""

from pathlib import Path
from typing import Any

from profileforge.configuration import ConfigurationManager, ProfileForgeConfiguration
from profileforge.engine.context import ExecutionContext
from profileforge.engine.diagnostics import EngineDiagnostics
from profileforge.engine.exceptions import BootstrapError
from profileforge.engine.registry import DependencyRegistry


def bootstrap_engine(
    config_file: Path | str | None = None,
    env_overrides: dict[str, str] | None = None,
    raw_overrides: dict[str, Any] | None = None,
) -> tuple[ExecutionContext, DependencyRegistry]:
    """Execute the application bootstrap sequence.

    Args:
        config_file: Optional configuration file path.
        env_overrides: Optional environment overrides.
        raw_overrides: Optional raw dictionary overrides.

    Returns:
        Tuple containing (ExecutionContext, DependencyRegistry).

    Raises:
        BootstrapError: If configuration loading or bootstrap initialization fails.
    """
    diagnostics = EngineDiagnostics()
    registry = DependencyRegistry()

    try:
        # 1. Load validated configuration using ConfigurationManager
        config_mgr = ConfigurationManager(config_file=config_file)
        config: ProfileForgeConfiguration = config_mgr.load(
            env_overrides=env_overrides, raw_overrides=raw_overrides
        )

        # 2. Create immutable ExecutionContext
        context = ExecutionContext.create(
            configuration=config, diagnostics=diagnostics
        )

        # 3. Register foundational services into DependencyRegistry
        registry.register(
            "configuration_manager", config_mgr, instance_type=ConfigurationManager
        )
        registry.register(
            "configuration", config, instance_type=ProfileForgeConfiguration
        )
        registry.register(
            "diagnostics", diagnostics, instance_type=EngineDiagnostics
        )

        diagnostics.record_subsystem_status("configuration", initialized=True)

        return context, registry
    except Exception as exc:
        diagnostics.add_error(f"Bootstrap failed: {exc}")
        raise BootstrapError(f"Engine bootstrap failed: {exc}") from exc
