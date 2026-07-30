"""Integration tests for ProfileForge end-to-end pipeline.

Validates subsystem contracts from Configuration through Collectors, Analytics, Generators, and Renderers.
Governed by 01_ENGINEERING_QUALITY_GATES.md and 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

from unittest.mock import MagicMock

from profileforge.analytics import AnalyticsOrchestrator
from profileforge.collectors import CollectorOrchestrator
from profileforge.generators import GeneratorOrchestrator
from profileforge.github import (
    GitHubClient,
    GitHubLanguageStatsModel,
    GitHubRepositoryModel,
    GitHubUserModel,
)
from profileforge.renderers import RendererOrchestrator


def create_mock_github_client() -> GitHubClient:
    """Create a mock GitHubClient for integration tests."""
    mock_client = MagicMock(spec=GitHubClient)
    mock_user = GitHubUserModel(
        id=1,
        login="octocat",
        name="The Octocat",
        bio="Integration Tester",
        public_repos=1,
    )
    mock_repo = GitHubRepositoryModel(
        id=101,
        name="integration-repo",
        full_name="octocat/integration-repo",
        description="Repo for integration tests",
        stargazers_count=100,
        forks_count=25,
        language="Python",
    )
    mock_lang = GitHubLanguageStatsModel(
        repository_name="octocat/integration-repo",
        languages={"Python": 10000},
        total_bytes=10000,
    )

    mock_client.get_user_profile = MagicMock(return_value=mock_user)
    mock_client.get_user_repositories = MagicMock(return_value=[mock_repo])
    mock_client.get_repository_languages = MagicMock(return_value=mock_lang)
    mock_client._execute_request = MagicMock(return_value=([], {}))
    mock_client.diagnostics = MagicMock()
    mock_client.diagnostics.request_count = 1
    return mock_client


def test_subsystem_contract_pipeline() -> None:
    """Verify data flows cleanly across all subsystem boundaries."""
    client = create_mock_github_client()

    # 1. Collectors
    collector_orchestrator = CollectorOrchestrator(client=client)
    coll_snapshot = collector_orchestrator.collect_user_snapshot("octocat")
    assert coll_snapshot.username == "octocat"
    assert coll_snapshot.user.name == "The Octocat"

    # 2. Analytics
    analytics_orchestrator = AnalyticsOrchestrator()
    analytics_snapshot = analytics_orchestrator.analyze_snapshot(coll_snapshot)
    assert analytics_snapshot.portfolio_summary.total_stars == 100

    # 3. Generators
    generator_orchestrator = GeneratorOrchestrator()
    presentation_model = generator_orchestrator.generate_presentation_model(
        analytics_snapshot, coll_snapshot
    )
    assert presentation_model.profile.display_name == "The Octocat"

    # 4. Renderers
    renderer_orchestrator = RendererOrchestrator()
    artifacts = renderer_orchestrator.render_presentation_model(presentation_model)
    assert artifacts.markdown_artifact is not None
    assert artifacts.total_count == 4
