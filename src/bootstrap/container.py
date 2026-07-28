"""
Application composition root.

This module is responsible for constructing and wiring together
the application's dependency graph.
"""

from src.core.application import app
from src.dashboard.builder import DashboardBuilder
from src.dashboard.generator import DashboardGenerator
from src.github.api import GitHubClient
from src.github.collectors import GitHubCollector
from src.github.statistics import StatisticsEngine
from src.renderer.engine import RenderingEngine
from src.services.profile_service import ProfileService


def build_dashboard_generator() -> DashboardGenerator:
    """
    Construct and configure the dashboard generator.

    Returns:
        Fully configured DashboardGenerator instance.
    """

    github_config = app.config.load_github()

    github_client = GitHubClient(github_config)

    collector = GitHubCollector(github_client)

    statistics = StatisticsEngine()

    profile_service = ProfileService(
        collector=collector,
        statistics=statistics,
    )

    builder = DashboardBuilder()

    renderer = RenderingEngine()

    return DashboardGenerator(
        profile_service=profile_service,
        builder=builder,
        renderer=renderer,
    )