"""Automation Domain Models.

Immutable execution results, stage tracking, manifests, and reporting models.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md and 04_DOMAIN_MODEL_SPECIFICATION.md.
"""

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from profileforge import __version__


class StageStatus(StrEnum):
    """Operational status of a workflow stage."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class AutomationConfiguration(BaseModel):
    """Operational settings for automation pipeline execution."""

    model_config = ConfigDict(frozen=True)

    output_dir: str = "./dist"
    overwrite_existing: bool = True
    max_retries: int = Field(default=3, ge=0)
    retry_backoff_factor: float = Field(default=1.5, ge=1.0)
    publisher_type: str = "local_filesystem"


class ExecutionStage(BaseModel):
    """Execution status and timing telemetry for a single workflow stage."""

    model_config = ConfigDict(frozen=True)

    stage_name: str
    status: StageStatus = StageStatus.PENDING
    started_at: str = ""
    completed_at: str = ""
    duration_ms: float = 0.0
    error_message: str | None = None
    diagnostics: dict[str, Any] = Field(default_factory=dict)


class ArtifactManifest(BaseModel):
    """File manifest metadata for generated and stored artifacts."""

    model_config = ConfigDict(frozen=True)

    output_path: str
    filename: str
    size_bytes: int = 0
    checksum_sha256: str = ""
    artifact_type: str = "generic"


class PublishResult(BaseModel):
    """Result of publishing rendered artifacts to a publishing destination."""

    model_config = ConfigDict(frozen=True)

    success: bool
    published_path: str
    artifacts_published_count: int = 0
    publisher_name: str = "local_filesystem"
    error_message: str | None = None


class WorkflowResult(BaseModel):
    """Overall execution result of the end-to-end automation workflow."""

    model_config = ConfigDict(frozen=True)

    success: bool
    username: str
    stages: list[ExecutionStage] = Field(default_factory=list)
    manifests: list[ArtifactManifest] = Field(default_factory=list)
    publish_result: PublishResult | None = None
    total_duration_ms: float = 0.0


class ExecutionReport(BaseModel):
    """Comprehensive execution report summarizing an automated run."""

    model_config = ConfigDict(frozen=True)

    workflow_id: str
    username: str
    version: str = __version__
    config_hash: str = ""
    execution_mode: str = "manual"
    start_timestamp: str = ""
    end_timestamp: str = ""
    result: WorkflowResult
    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
    metadata: dict[str, Any] = Field(default_factory=dict)
