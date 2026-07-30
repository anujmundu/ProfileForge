"""Workflow Execution Pipeline.

Coordinates end-to-end execution across all ProfileForge subsystems.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md and 06_ENGINE_LIFECYCLE_SPECIFICATION.md.
"""

import time
from datetime import UTC, datetime

from profileforge.analytics import AnalyticsOrchestrator
from profileforge.automation.artifact_manager import ArtifactManager
from profileforge.automation.cancellation import CancellationToken
from profileforge.automation.diagnostics import AutomationDiagnostics
from profileforge.automation.exceptions import WorkflowError
from profileforge.automation.models import (
    ArtifactManifest,
    AutomationConfiguration,
    ExecutionStage,
    PublishResult,
    StageStatus,
    WorkflowResult,
)
from profileforge.automation.publisher import LocalFileSystemPublisher
from profileforge.collectors import (
    CollectionSnapshot,
    CollectorOrchestrator,
)
from profileforge.configuration import ConfigurationManager
from profileforge.engine import Engine
from profileforge.generators import GeneratorOrchestrator
from profileforge.github import GitHubClient
from profileforge.renderers import RendererOrchestrator


class Workflow:
    """Deterministic end-to-end ProfileForge execution pipeline."""

    def __init__(
        self,
        config: AutomationConfiguration | None = None,
        github_client: GitHubClient | None = None,
    ) -> None:
        self.config = config or AutomationConfiguration()
        self.github_client = github_client
        self.diagnostics = AutomationDiagnostics()

    def run(
        self, username: str, cancel_token: CancellationToken | None = None
    ) -> WorkflowResult:
        """Execute end-to-end pipeline for username.

        Args:
            username: Target GitHub username.
            cancel_token: Optional cooperative cancellation token.

        Returns:
            WorkflowResult summarizing execution stages, manifest, and publishing.
        """
        token = cancel_token or CancellationToken()
        stages: list[ExecutionStage] = []
        manifests: list[ArtifactManifest] = []
        publish_res: PublishResult | None = None
        pipeline_start = time.perf_counter()

        try:
            # Stage 1: Load Configuration
            token.throw_if_cancelled()
            st_start = datetime.now(UTC).isoformat()
            s1_start = time.perf_counter()
            cfg_mgr = ConfigurationManager()
            app_cfg = cfg_mgr.load()
            s1_dur = (time.perf_counter() - s1_start) * 1000.0
            st_end = datetime.now(UTC).isoformat()
            stages.append(
                ExecutionStage(
                    stage_name="Load Configuration",
                    status=StageStatus.COMPLETED,
                    started_at=st_start,
                    completed_at=st_end,
                    duration_ms=s1_dur,
                )
            )
            self.diagnostics.record_stage_duration("Load Configuration", s1_dur)

            # Stage 2: Initialize Engine
            token.throw_if_cancelled()
            st_start = datetime.now(UTC).isoformat()
            s2_start = time.perf_counter()
            engine = Engine()
            engine.bootstrap()
            s2_dur = (time.perf_counter() - s2_start) * 1000.0
            st_end = datetime.now(UTC).isoformat()
            stages.append(
                ExecutionStage(
                    stage_name="Initialize Engine",
                    status=StageStatus.COMPLETED,
                    started_at=st_start,
                    completed_at=st_end,
                    duration_ms=s2_dur,
                )
            )
            self.diagnostics.record_stage_duration("Initialize Engine", s2_dur)

            # Stage 3: Collect GitHub Data
            token.throw_if_cancelled()
            st_start = datetime.now(UTC).isoformat()
            s3_start = time.perf_counter()
            gh_client = self.github_client or GitHubClient(
                config=app_cfg.github
            )
            collector_orchestrator = CollectorOrchestrator(client=gh_client)
            coll_snapshot: CollectionSnapshot = (
                collector_orchestrator.collect_user_snapshot(username)
            )
            s3_dur = (time.perf_counter() - s3_start) * 1000.0
            st_end = datetime.now(UTC).isoformat()
            stages.append(
                ExecutionStage(
                    stage_name="Collect GitHub Data",
                    status=StageStatus.COMPLETED,
                    started_at=st_start,
                    completed_at=st_end,
                    duration_ms=s3_dur,
                )
            )
            self.diagnostics.record_stage_duration("Collect GitHub Data", s3_dur)

            # Stage 4: Run Analytics
            token.throw_if_cancelled()
            st_start = datetime.now(UTC).isoformat()
            s4_start = time.perf_counter()
            analytics_orchestrator = AnalyticsOrchestrator()
            analytics_snapshot = analytics_orchestrator.analyze_snapshot(
                coll_snapshot
            )
            s4_dur = (time.perf_counter() - s4_start) * 1000.0
            st_end = datetime.now(UTC).isoformat()
            stages.append(
                ExecutionStage(
                    stage_name="Run Analytics",
                    status=StageStatus.COMPLETED,
                    started_at=st_start,
                    completed_at=st_end,
                    duration_ms=s4_dur,
                )
            )
            self.diagnostics.record_stage_duration("Run Analytics", s4_dur)

            # Stage 5: Generate Presentation Models
            token.throw_if_cancelled()
            st_start = datetime.now(UTC).isoformat()
            s5_start = time.perf_counter()
            generator_orchestrator = GeneratorOrchestrator()
            presentation_model = (
                generator_orchestrator.generate_presentation_model(
                    analytics_snapshot, coll_snapshot
                )
            )
            s5_dur = (time.perf_counter() - s5_start) * 1000.0
            st_end = datetime.now(UTC).isoformat()
            stages.append(
                ExecutionStage(
                    stage_name="Generate Presentation Models",
                    status=StageStatus.COMPLETED,
                    started_at=st_start,
                    completed_at=st_end,
                    duration_ms=s5_dur,
                )
            )
            self.diagnostics.record_stage_duration(
                "Generate Presentation Models", s5_dur
            )

            # Stage 6: Render Artifacts
            token.throw_if_cancelled()
            st_start = datetime.now(UTC).isoformat()
            s6_start = time.perf_counter()
            renderer_orchestrator = RendererOrchestrator()
            rendered_artifacts = renderer_orchestrator.render_presentation_model(
                presentation_model
            )
            s6_dur = (time.perf_counter() - s6_start) * 1000.0
            st_end = datetime.now(UTC).isoformat()
            stages.append(
                ExecutionStage(
                    stage_name="Render Artifacts",
                    status=StageStatus.COMPLETED,
                    started_at=st_start,
                    completed_at=st_end,
                    duration_ms=s6_dur,
                )
            )
            self.diagnostics.record_stage_duration("Render Artifacts", s6_dur)

            # Stage 7: Store Artifacts
            token.throw_if_cancelled()
            st_start = datetime.now(UTC).isoformat()
            s7_start = time.perf_counter()
            art_mgr = ArtifactManager(
                output_dir=self.config.output_dir,
                overwrite=self.config.overwrite_existing,
            )
            manifests = art_mgr.store_artifacts(rendered_artifacts)
            s7_dur = (time.perf_counter() - s7_start) * 1000.0
            st_end = datetime.now(UTC).isoformat()
            stages.append(
                ExecutionStage(
                    stage_name="Store Artifacts",
                    status=StageStatus.COMPLETED,
                    started_at=st_start,
                    completed_at=st_end,
                    duration_ms=s7_dur,
                )
            )
            self.diagnostics.record_stage_duration("Store Artifacts", s7_dur)

            # Stage 8: Publish Artifacts
            token.throw_if_cancelled()
            st_start = datetime.now(UTC).isoformat()
            s8_start = time.perf_counter()
            publisher = LocalFileSystemPublisher()
            publish_res = publisher.publish(
                rendered_artifacts, self.config.output_dir
            )
            s8_dur = (time.perf_counter() - s8_start) * 1000.0
            st_end = datetime.now(UTC).isoformat()
            stages.append(
                ExecutionStage(
                    stage_name="Publish Artifacts",
                    status=StageStatus.COMPLETED,
                    started_at=st_start,
                    completed_at=st_end,
                    duration_ms=s8_dur,
                )
            )
            self.diagnostics.record_stage_duration("Publish Artifacts", s8_dur)
            self.diagnostics.published_artifacts_count = (
                publish_res.artifacts_published_count
            )

            total_dur = (time.perf_counter() - pipeline_start) * 1000.0
            self.diagnostics.total_execution_duration_ms = total_dur

            return WorkflowResult(
                success=True,
                username=username,
                stages=stages,
                manifests=manifests,
                publish_result=publish_res,
                total_duration_ms=total_dur,
            )

        except Exception as exc:
            total_dur = (time.perf_counter() - pipeline_start) * 1000.0
            self.diagnostics.total_execution_duration_ms = total_dur
            self.diagnostics.record_failure("Pipeline", str(exc))

            raise WorkflowError(
                f"Workflow execution failed for user '{username}': {exc}"
            ) from exc
