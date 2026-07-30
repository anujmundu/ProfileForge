"""Engine Subsystem.

Application lifecycle, orchestration, dependency injection, and pipeline execution.
Governed by 06_ENGINE_LIFECYCLE_SPECIFICATION.md.
"""

from profileforge.engine.context import ExecutionContext
from profileforge.engine.diagnostics import EngineDiagnostics
from profileforge.engine.engine import Engine
from profileforge.engine.exceptions import (
    BootstrapError,
    DependencyError,
    EngineError,
    InitializationError,
    LifecycleError,
)
from profileforge.engine.health import EngineHealth
from profileforge.engine.lifecycle import LifecyclePhase, LifecycleState
from profileforge.engine.registry import DependencyRegistry

__all__ = [
    "BootstrapError",
    "DependencyError",
    "DependencyRegistry",
    "Engine",
    "EngineDiagnostics",
    "EngineError",
    "EngineHealth",
    "ExecutionContext",
    "InitializationError",
    "LifecycleError",
    "LifecyclePhase",
    "LifecycleState",
]
