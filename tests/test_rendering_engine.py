"""Unit tests for the SVG rendering engine."""

from xml.etree.ElementTree import fromstring

from src.dashboard.models import DashboardView, RepositoryCard
from src.renderer.engine import RenderingEngine


def test_rendering_engine_generates_valid_svg():
    """RenderingEngine should produce a valid SVG document."""

    # Arrange
    dashboard = DashboardView(
        username="anujmundu",
        name="Anuj Mundu",
        bio="AI Engineer",
        total_repositories=2,
        total_stars=35,
        total_forks=7,
        repositories=[
            RepositoryCard(
                name="GitHub Profile",
                description="Profile Dashboard",
                language="Python",
                stars=35,
                forks=7,
                html_url="https://github.com/anujmundu",
            )
        ],
    )

    engine = RenderingEngine()

    # Act
    svg = engine.render(dashboard)

    # Assert
    root = fromstring(svg)

    # Verify the root element is an SVG.
    assert root.tag.endswith("svg")

    # Verify essential SVG attributes.
    assert "viewBox" in root.attrib
    assert root.attrib["width"] == "1200"
    assert root.attrib["height"] == "630"

    # Verify the SVG namespace is present.
    assert "xmlns" in svg