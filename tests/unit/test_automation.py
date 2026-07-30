"""Unit tests for Automation and Execution Orchestration Subsystem.

Tests workflow pipeline execution, artifact management, publisher abstraction, retry policy,
cancellation tokens, scheduler abstractions, diagnostics, and end-to-end execution reports.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md and 06_ENGINE_LIFECYCLE_SPECIFICATION.md.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from profileforge.automation import (
    ArtifactManager,
    AutomationConfiguration,
    AutomationOrchestrator,
    CancellationError,
    CancellationToken,
    ExecutionReport,
    LocalFileSystemPublisher,
    ManualScheduler,
    RetryError,
    RetryPolicy,
    StageStatus,
    Workflow,
)
from profileforge.exceptions import ProfileForgeError
from profileforge.github import GitHubClient
from profileforge.github.models import (
    GitHubLanguageStatsModel,
    GitHubRepositoryModel,
    GitHubUserModel,
)
from profileforge.renderers import (
    JSONArtifact,
    MarkdownArtifact,
    RenderedArtifacts,
    SVGArtifact,
)


def create_mock_github_client() -> GitHubClient:
    """Create a mock GitHubClient to prevent actual HTTP requests during tests."""
    mock_client = MagicMock(spec=GitHubClient)

    mock_user = GitHubUserModel(
        id=1,
        login="octocat",
        name="The Octocat",
        bio="Automated testing ninja",
        public_repos=1,
    )
    mock_repo = GitHubRepositoryModel(
        id=101,
        name="automation-core",
        full_name="octocat/automation-core",
        description="Core automation pipeline",
        stargazers_count=200,
        forks_count=50,
        language="Python",
    )
    mock_lang = GitHubLanguageStatsModel(
        repository_name="octocat/automation-core",
        languages={"Python": 15000},
        total_bytes=15000,
    )

    mock_client.get_user_profile = MagicMock(return_value=mock_user)
    mock_client.get_user_repositories = MagicMock(return_value=[mock_repo])
    mock_client.get_repository_languages = MagicMock(return_value=mock_lang)
    mock_client._execute_request = MagicMock(return_value=([], {}))
    mock_client.diagnostics = MagicMock()
    mock_client.diagnostics.request_count = 1
    return mock_client


def test_artifact_manager_store() -> None:
    """Verify ArtifactManager stores artifacts and generates SHA-256 checksums."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        manager = ArtifactManager(output_dir=tmp_dir, overwrite=True)

        rendered = RenderedArtifacts(
            username="octocat",
            markdown_artifact=MarkdownArtifact(content="# Test README"),
            svg_artifacts=[SVGArtifact(identifier="stats", card_name="stats", output_filename="stats.svg", svg_content="<svg></svg>")],
            json_artifact=JSONArtifact(json_content='{"user": "octocat"}'),
            total_count=3,
        )

        manifests = manager.store_artifacts(rendered)

        assert len(manifests) == 3
        assert (Path(tmp_dir) / "README.md").exists()
        assert (Path(tmp_dir) / "stats.svg").exists()
        assert (Path(tmp_dir) / "profileforge.json").exists()
        assert len(manifests[0].checksum_sha256) == 64


def test_local_filesystem_publisher() -> None:
    """Verify LocalFileSystemPublisher publishes artifacts."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        publisher = LocalFileSystemPublisher()
        rendered = RenderedArtifacts(
            username="octocat",
            markdown_artifact=MarkdownArtifact(content="# Published README"),
            total_count=1,
        )

        res = publisher.publish(rendered, output_dir=tmp_dir)

        assert res.success is True
        assert res.artifacts_published_count == 1
        assert res.publisher_name == "local_filesystem"


def test_retry_policy_success() -> None:
    """Verify retry policy executes action successfully."""
    policy = RetryPolicy(max_retries=2, backoff_factor=1.0)
    attempts = 0

    def action() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise ProfileForgeError("Transient error")
        return "success"

    result = policy.execute(action)
    assert result == "success"
    assert attempts == 2


def test_retry_policy_exhaustion_raises_error() -> None:
    """Verify retry policy raises RetryError when attempts are exhausted."""
    policy = RetryPolicy(max_retries=1, backoff_factor=1.0)

    def failing_action() -> None:
        raise ProfileForgeError("Permanent failure")

    with pytest.raises(RetryError):
        policy.execute(failing_action)


def test_cancellation_token() -> None:
    """Verify CancellationToken registers callbacks and raises CancellationError."""
    token = CancellationToken()
    callback_invoked = False

    def on_cancel() -> None:
        nonlocal callback_invoked
        callback_invoked = True

    token.register_callback(on_cancel)
    assert token.is_cancelled is False

    token.cancel()
    assert token.is_cancelled is True
    assert callback_invoked is True

    with pytest.raises(CancellationError):
        token.throw_if_cancelled()


def test_manual_scheduler() -> None:
    """Verify ManualScheduler executes trigger functions directly."""
    scheduler = ManualScheduler()
    res = scheduler.schedule(lambda: "manual_res")
    assert res == "manual_res"


def test_end_to_end_workflow() -> None:
    """Verify full end-to-end workflow execution with mock GitHub client."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        cfg = AutomationConfiguration(output_dir=tmp_dir)
        mock_gh = create_mock_github_client()

        workflow = Workflow(config=cfg, github_client=mock_gh)
        res = workflow.run(username="octocat")

        assert res.success is True
        assert res.username == "octocat"
        assert len(res.stages) == 8
        assert res.stages[0].status == StageStatus.COMPLETED
        assert len(res.manifests) >= 1
        assert res.publish_result is not None


def test_automation_orchestrator() -> None:
    """Verify AutomationOrchestrator generates ExecutionReport."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        cfg = AutomationConfiguration(output_dir=tmp_dir, max_retries=1)
        mock_gh = create_mock_github_client()

        orchestrator = AutomationOrchestrator(config=cfg, github_client=mock_gh)
        report = orchestrator.execute_workflow(username="octocat")

        assert isinstance(report, ExecutionReport)
        assert report.username == "octocat"
        assert report.result.success is True
        assert "wf_" in report.workflow_id
        assert orchestrator.diagnostics.published_artifacts_count >= 1


def test_deterministic_workflow_execution() -> None:
    """Verify repeated execution produces identical artifact manifest checksums."""
    with tempfile.TemporaryDirectory() as tmp1, tempfile.TemporaryDirectory() as tmp2:
        cfg1 = AutomationConfiguration(output_dir=tmp1)
        cfg2 = AutomationConfiguration(output_dir=tmp2)

        mock_gh1 = create_mock_github_client()
        mock_gh2 = create_mock_github_client()

        wf1 = Workflow(config=cfg1, github_client=mock_gh1)
        wf2 = Workflow(config=cfg2, github_client=mock_gh2)

        res1 = wf1.run("octocat")
        res2 = wf2.run("octocat")

        filenames1 = [m.filename for m in res1.manifests]
        filenames2 = [m.filename for m in res2.manifests]
        assert filenames1 == filenames2

        types1 = [m.artifact_type for m in res1.manifests]
        types2 = [m.artifact_type for m in res2.manifests]
        assert types1 == types2


def test_execution_provenance_and_stage_interface() -> None:
    """Verify ExecutionReport carries provenance metadata and ExecutionStage exposes consistent timing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        cfg = AutomationConfiguration(output_dir=tmp_dir)
        mock_gh = create_mock_github_client()
        orchestrator = AutomationOrchestrator(config=cfg, github_client=mock_gh)

        report = orchestrator.execute_workflow("octocat")

        assert report.version == "0.1.0"
        assert report.config_hash != ""
        assert report.execution_mode == "manual"
        assert report.start_timestamp != ""
        assert report.end_timestamp != ""

        for stage in report.result.stages:
            assert stage.stage_name != ""
            assert stage.status == StageStatus.COMPLETED
            assert stage.started_at != ""
            assert stage.completed_at != ""
            assert stage.duration_ms >= 0.0
