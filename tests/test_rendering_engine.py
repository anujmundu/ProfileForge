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
                name=f"Repository {i}",
                description="Example",
                language="Python",
                stars=i,
                forks=i,
                html_url="https://github.com/example",
            )
            for i in range(1, 5)
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

    texts = [element.text for element in root.iter() if element.tag.endswith("text")]

    assert "Anuj Mundu" in texts
    assert "AI Engineer" in texts
    assert "GitHub Statistics" in texts
    assert "Repositories : 2" in texts
    assert "Forks        : 7" in texts
    assert "Repository 1" in texts
    assert "Repository 2" in texts
    assert "Repository 3" in texts
    assert "Repository 4" in texts

    assert "Example" in texts
    assert "Language: Python" in texts

    assert "★ 1   Forks: 1" in texts
    assert "★ 2   Forks: 2" in texts
    assert "★ 3   Forks: 3" in texts
    assert "★ 4   Forks: 4" in texts
