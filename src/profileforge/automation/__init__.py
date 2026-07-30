"""Automation and Execution Orchestration Subsystem.

Orchestrates complete ProfileForge execution pipeline across all subsystems.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md and 06_ENGINE_LIFECYCLE_SPECIFICATION.md.
"""

from profileforge.automation.artifact_manager import ArtifactManager
from profileforge.automation.cancellation import CancellationToken
from profileforge.automation.diagnostics import AutomationDiagnostics
from profileforge.automation.exceptions import (
    AutomationError,
    CancellationError,
    PublishingError,
    RetryError,
    SchedulerError,
    WorkflowError,
)
from profileforge.automation.models import (
    ArtifactManifest,
    AutomationConfiguration,
    ExecutionReport,
    ExecutionStage,
    PublishResult,
    StageStatus,
    WorkflowResult,
)
from profileforge.automation.orchestrator import AutomationOrchestrator
from profileforge.automation.publisher import (
    BasePublisher as Publisher,
)
from profileforge.automation.publisher import (
    LocalFileSystemPublisher,
)
from profileforge.automation.retry import (
    AutomationRetryPolicy as RetryPolicy,
)
from profileforge.automation.scheduler import (
    BaseScheduler as Scheduler,
)
from profileforge.automation.scheduler import (
    ManualScheduler,
)
from profileforge.automation.workflow import Workflow

__all__ = [
    "ArtifactManager",
    "ArtifactManifest",
    "AutomationConfiguration",
    "AutomationDiagnostics",
    "AutomationError",
    "AutomationOrchestrator",
    "CancellationToken",
    "CancellationError",
    "ExecutionReport",
    "ExecutionStage",
    "LocalFileSystemPublisher",
    "ManualScheduler",
    "PublishResult",
    "Publisher",
    "PublishingError",
    "RetryError",
    "RetryPolicy",
    "Scheduler",
    "SchedulerError",
    "StageStatus",
    "Workflow",
    "WorkflowError",
    "WorkflowResult",
]
