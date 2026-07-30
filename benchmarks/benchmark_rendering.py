"""Standalone Rendering Benchmark Script.

Measures rendering throughput for Markdown, SVG visual cards, and JSON snapshots.
"""

import json
import platform
import sys
import time
from typing import Any

from profileforge.generators.models import (
    AchievementsModel,
    FeaturedProjectsModel,
    PresentationModel,
    ProfileModel,
    StatisticsModel,
    TechnologyStackModel,
    TimelineModel,
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


def run_rendering_benchmark(iterations: int = 100) -> float:
    """Run rendering benchmark over N iterations and return average duration in ms."""
    model = PresentationModel(
        username="octocat",
        profile=ProfileModel(username="octocat", display_name="The Octocat"),
        statistics=StatisticsModel(total_stars=150),
        featured_projects=FeaturedProjectsModel(),
        technology_stack=TechnologyStackModel(),
        timeline=TimelineModel(),
        achievements=AchievementsModel(),
    )

    r_orch = RendererOrchestrator()
    start_time = time.perf_counter()

    for _ in range(iterations):
        r_orch.render_presentation_model(model)

    total_time_ms = (time.perf_counter() - start_time) * 1000.0
    return total_time_ms / iterations


if __name__ == "__main__":
    env_meta = get_environment_metadata()
    print("=== Environment Metadata ===")
    print(json.dumps(env_meta, indent=2))
    avg_duration = run_rendering_benchmark(100)
    print(f"\nRendering Benchmark: {avg_duration:.2f} ms per run (100 iterations)")
