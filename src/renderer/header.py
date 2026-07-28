"""
Header renderer.
"""

from xml.etree.ElementTree import Element, SubElement

from src.dashboard.models import DashboardView


class HeaderRenderer:
    """Renders the profile header."""

    def render(
        self,
        svg: Element,
        dashboard: DashboardView,
    ) -> None:

        SubElement(
            svg,
            "text",
            {
                "x": "40",
                "y": "70",
                "font-size": "32",
                "font-weight": "bold",
            },
        ).text = dashboard.name or dashboard.username

        SubElement(
            svg,
            "text",
            {
                "x": "40",
                "y": "105",
                "font-size": "18",
            },
        ).text = dashboard.bio or ""