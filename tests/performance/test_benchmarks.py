"""Performance benchmark tests establishing execution baselines.

Governed by 01_ENGINEERING_QUALITY_GATES.md.
"""

import time
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


def test_pipeline_performance_baseline() -> None:
    """Benchmark end-to-end processing pipeline execution speed."""
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

    start_time = time.perf_counter()

    c_orch = CollectorOrchestrator(client=mock_client)
    c_snap = c_orch.collect_user_snapshot("octocat")

    a_orch = AnalyticsOrchestrator()
    a_snap = a_orch.analyze_snapshot(c_snap)

    g_orch = GeneratorOrchestrator()
    p_model = g_orch.generate_presentation_model(a_snap, c_snap)

    r_orch = RendererOrchestrator()
    artifacts = r_orch.render_presentation_model(p_model)

    duration_ms = (time.perf_counter() - start_time) * 1000.0

    assert artifacts.total_count == 4
    # Ensure end-to-end execution completes within performance baseline threshold (e.g. < 500ms for in-memory pipeline)
    assert duration_ms < 500.0
