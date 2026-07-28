"""
Dashboard generation pipeline.

Coordinates the complete dashboard generation workflow:

GitHub
    ↓
ProfileService
    ↓
DashboardBuilder
    ↓
RenderingEngine
    ↓
SVG
"""

from src.dashboard.builder import DashboardBuilder
from src.renderer.engine import RenderingEngine
from src.services.profile_service import ProfileService


class DashboardGenerator:
    """Generate a complete SVG dashboard."""

    def __init__(
        self,
        profile_service: ProfileService,
        builder: DashboardBuilder,
        renderer: RenderingEngine,
    ) -> None:
        self._profile_service = profile_service
        self._builder = builder
        self._renderer = renderer

    def generate(self) -> str:
        """
        Generate the GitHub dashboard SVG.

        Returns:
            SVG document as a string.
        """

        dashboard_data = self._profile_service.build_dashboard()

        dashboard_view = self._builder.build(dashboard_data)

        return self._renderer.render(dashboard_view)