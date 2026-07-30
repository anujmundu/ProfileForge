"""End-to-End test suite for ProfileForge platform.

Executes complete pipeline using mocked GitHub API responses to validate full production execution.
Governed by 01_ENGINEERING_QUALITY_GATES.md and 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

from profileforge.automation import AutomationConfiguration, AutomationOrchestrator
from profileforge.github import (
    GitHubClient,
    GitHubLanguageStatsModel,
    GitHubRepositoryModel,
    GitHubUserModel,
)


def test_full_platform_end_to_end_execution() -> None:
    """Execute end-to-end platform run and verify all generated output artifacts."""
    with tempfile.TemporaryDirectory() as output_dir:
        mock_client = MagicMock(spec=GitHubClient)
        mock_user = GitHubUserModel(
            id=1,
            login="monalisa",
            name="Mona Lisa Octocat",
            bio="Lead Developer at GitHub",
            company="GitHub",
            location="San Francisco",
            avatar_url="https://github.com/images/error/octocat_happy.gif",
            html_url="https://github.com/monalisa",
            public_repos=2,
        )
        mock_repo1 = GitHubRepositoryModel(
            id=201,
            name="smile-engine",
            full_name="monalisa/smile-engine",
            description="AI facial analysis",
            stargazers_count=500,
            forks_count=120,
            language="Python",
            topics=["ai", "computer-vision"],
        )
        mock_repo2 = GitHubRepositoryModel(
            id=202,
            name="canvas-db",
            full_name="monalisa/canvas-db",
            description="Vector graphics storage",
            stargazers_count=300,
            forks_count=45,
            language="Rust",
            topics=["rust", "database"],
        )
        mock_lang1 = GitHubLanguageStatsModel(
            repository_name="monalisa/smile-engine",
            languages={"Python": 30000},
            total_bytes=30000,
        )
        mock_lang2 = GitHubLanguageStatsModel(
            repository_name="monalisa/canvas-db",
            languages={"Rust": 25000},
            total_bytes=25000,
        )

        mock_client.get_user_profile = MagicMock(return_value=mock_user)
        mock_client.get_user_repositories = MagicMock(return_value=[mock_repo1, mock_repo2])
        mock_client.get_repository_languages = MagicMock(
            side_effect=[mock_lang1, mock_lang2]
        )
        mock_client._execute_request = MagicMock(return_value=([], {}))
        mock_client.diagnostics = MagicMock()
        mock_client.diagnostics.request_count = 3

        config = AutomationConfiguration(output_dir=output_dir, overwrite_existing=True)
        orchestrator = AutomationOrchestrator(config=config, github_client=mock_client)

        report = orchestrator.execute_workflow(username="monalisa")

        assert report.result.success is True
        assert report.username == "monalisa"
        assert len(report.result.manifests) == 4

        # Verify filesystem artifacts exist
        dist_path = Path(output_dir)
        readme_path = dist_path / "README.md"
        stats_svg_path = dist_path / "stats_card.svg"
        tech_svg_path = dist_path / "tech_card.svg"
        json_path = dist_path / "profileforge.json"

        assert readme_path.exists()
        assert stats_svg_path.exists()
        assert tech_svg_path.exists()
        assert json_path.exists()

        readme_content = readme_path.read_text(encoding="utf-8")
        assert "Mona Lisa Octocat" in readme_content
        assert "smile-engine" in readme_content
