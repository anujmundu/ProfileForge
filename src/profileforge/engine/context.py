"""Immutable Execution Context for Engine Subsystem.

Container passed throughout the Engine rather than relying on global state.
Governed by 06_ENGINE_LIFECYCLE_SPECIFICATION.md.
"""

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from profileforge import __version__
from profileforge.configuration import ExecutionEnvironment, ProfileForgeConfiguration
from profileforge.engine.diagnostics import EngineDiagnostics


@dataclass(frozen=True)
class ExecutionContext:
    """Immutable execution context passed across lifecycle phases."""

    execution_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    startup_timestamp: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
    application_version: str = field(default_factory=lambda: __version__)
    environment: ExecutionEnvironment = ExecutionEnvironment.DEVELOPMENT
    configuration: ProfileForgeConfiguration = field(
        default_factory=ProfileForgeConfiguration
    )
    diagnostics: EngineDiagnostics = field(default_factory=EngineDiagnostics)

    @classmethod
    def create(
        cls,
        configuration: ProfileForgeConfiguration,
        diagnostics: EngineDiagnostics | None = None,
    ) -> "ExecutionContext":
        """Factory method to construct an ExecutionContext from configuration."""
        diag = diagnostics if diagnostics is not None else EngineDiagnostics()
        return cls(
            environment=configuration.app.environment,
            application_version=configuration.app.version,
            configuration=configuration,
            diagnostics=diag,
        )
