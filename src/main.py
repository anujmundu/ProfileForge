"""
Application entry point.

Generates the GitHub profile dashboard SVG.
"""

from pathlib import Path

from src.core.application import app
from src.dashboard.builder import DashboardBuilder
from src.dashboard.generator import DashboardGenerator
from src.github.api import GitHubClient
from src.github.collectors import GitHubCollector
from src.github.statistics import StatisticsEngine
from src.renderer.engine import RenderingEngine
from src.services.profile_service import ProfileService


def main() -> None:
    """Generate the GitHub dashboard SVG."""

    logger = app.logger

    logger.info("Loading GitHub configuration...")

    github_config = app.config.load_github()

    logger.info("Creating application services...")

    github_client = GitHubClient(github_config)

    collector = GitHubCollector(github_client)

    statistics = StatisticsEngine()

    profile_service = ProfileService(
        collector=collector,
        statistics=statistics,
    )

    builder = DashboardBuilder()

    renderer = RenderingEngine()

    generator = DashboardGenerator(
        profile_service=profile_service,
        builder=builder,
        renderer=renderer,
    )

    logger.info("Generating dashboard...")

    svg = generator.generate()

    output_path = Path("dashboard.svg")

    output_path.write_text(
        svg,
        encoding="utf-8",
    )

    logger.info(
        "Dashboard written to '%s'.",
        output_path.resolve(),
    )


if __name__ == "__main__":
    main()