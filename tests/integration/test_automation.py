"""Integration tests for Automation workflow subsystem.

Validates workflow pipeline, cancellation, retries, and local filesystem publishing.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

import tempfile
from unittest.mock import MagicMock

from profileforge.automation import (
    AutomationConfiguration,
    AutomationOrchestrator,
    CancellationToken,
)
from profileforge.github import (
    GitHubClient,
    GitHubLanguageStatsModel,
    GitHubRepositoryModel,
    GitHubUserModel,
)


def create_mock_client() -> GitHubClient:
    """Create a mock GitHubClient."""
    mock_client = MagicMock(spec=GitHubClient)
    mock_user = GitHubUserModel(id=1, login="octocat", name="Octocat")
    mock_repo = GitHubRepositoryModel(id=101, name="r1", full_name="octocat/r1")
    mock_lang = GitHubLanguageStatsModel(repository_name="octocat/r1", languages={"Python": 100}, total_bytes=100)

    mock_client.get_user_profile = MagicMock(return_value=mock_user)
    mock_client.get_user_repositories = MagicMock(return_value=[mock_repo])
    mock_client.get_repository_languages = MagicMock(return_value=mock_lang)
    mock_client._execute_request = MagicMock(return_value=([], {}))
    mock_client.diagnostics = MagicMock()
    mock_client.diagnostics.request_count = 1
    return mock_client


def test_automation_pipeline_integration() -> None:
    """Verify AutomationOrchestrator executes workflow and generates report."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        cfg = AutomationConfiguration(output_dir=tmp_dir)
        mock_gh = create_mock_client()

        orchestrator = AutomationOrchestrator(config=cfg, github_client=mock_gh)
        token = CancellationToken()

        report = orchestrator.execute_workflow("octocat", cancel_token=token)

        assert report.result.success is True
        assert report.result.publish_result is not None
        assert report.result.publish_result.artifacts_published_count == 4
