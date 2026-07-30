"""Standalone Pipeline Execution Benchmark Script.

Measures processing throughput and duration across subsystems.
"""

import json
import platform
import sys
import time
from typing import Any
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


def get_environment_metadata() -> dict[str, Any]:
    """Capture environmental metadata for benchmark reproducibility."""
    return {
        "execution_environment": "Local Development / Automated Test",
        "python_version": sys.version.split()[0],
        "operating_system": platform.platform(),
        "architecture": platform.machine(),
        "processor": platform.processor() or "x86_64/ARM",
    }


def run_pipeline_benchmark(iterations: int = 100) -> float:
    """Run pipeline benchmark over N iterations and return average duration in ms."""
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
    a_orch = AnalyticsOrchestrator()
    g_orch = GeneratorOrchestrator()
    r_orch = RendererOrchestrator()

    for _ in range(iterations):
        c_snap = c_orch.collect_user_snapshot("octocat")
        a_snap = a_orch.analyze_snapshot(c_snap)
        p_model = g_orch.generate_presentation_model(a_snap, c_snap)
        r_orch.render_presentation_model(p_model)

    total_time_ms = (time.perf_counter() - start_time) * 1000.0
    return total_time_ms / iterations


if __name__ == "__main__":
    env_meta = get_environment_metadata()
    print("=== Environment Metadata ===")
    print(json.dumps(env_meta, indent=2))
    avg_duration = run_pipeline_benchmark(50)
    print(f"\nPipeline Benchmark: {avg_duration:.2f} ms per run (50 iterations)")
