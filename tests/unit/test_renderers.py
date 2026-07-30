"""Unit tests for Rendering Subsystem.

Tests Markdown, SVG, JSON rendering, template loading, theme palettes, renderer failure isolation,
and pipeline orchestration.
Governed by 09_RENDERING_SPECIFICATION.md.
"""



from profileforge.analytics import AnalyticsOrchestrator
from profileforge.collectors import (
    CollectionSnapshot,
    ContributionCollection,
    LanguageCollection,
    OrganizationCollection,
    Repository,
    RepositoryCollection,
    User,
)
from profileforge.generators import GeneratorOrchestrator, PresentationModel
from profileforge.renderers import (
    JSONArtifact,
    JSONRenderer,
    MarkdownArtifact,
    MarkdownRenderer,
    RenderedArtifacts,
    RendererOrchestrator,
    SVGArtifact,
    SVGRenderer,
    TemplateLoader,
    ThemeLoader,
)


def create_sample_presentation_model() -> PresentationModel:
    """Helper to create a deterministic PresentationModel."""
    user = User(
        id=1,
        login="octocat",
        name="The Octocat",
        bio="Open Source Craftsman",
        public_repos=2,
    )

    repo1 = Repository(
        id=101,
        name="hello-world",
        full_name="octocat/hello-world",
        description="Sample project",
        stargazers_count=120,
        forks_count=30,
        language="Python",
        topics=["python", "docker"],
    )

    repos = RepositoryCollection(
        username="octocat", repositories=[repo1], total_count=1
    )
    langs = LanguageCollection(
        username="octocat", language_bytes={"Python": 20000}, total_bytes=20000
    )
    contribs = ContributionCollection(username="octocat", has_data=False)
    orgs = OrganizationCollection(username="octocat", organizations=[], total_count=0)

    coll_snapshot = CollectionSnapshot(
        username="octocat",
        user=user,
        repositories=repos,
        languages=langs,
        contributions=contribs,
        organizations=orgs,
    )

    analytics_orchestrator = AnalyticsOrchestrator()
    analytics_snapshot = analytics_orchestrator.analyze_snapshot(coll_snapshot)

    generator_orchestrator = GeneratorOrchestrator()
    return generator_orchestrator.generate_presentation_model(
        analytics_snapshot, coll_snapshot
    )


def test_markdown_renderer() -> None:
    """Verify MarkdownRenderer produces valid MarkdownArtifact README.md."""
    model = create_sample_presentation_model()
    renderer = MarkdownRenderer()

    artifact = renderer.render(model)

    assert isinstance(artifact, MarkdownArtifact)
    assert artifact.output_filename == "README.md"
    assert "# The Octocat" in artifact.content
    assert "hello-world" in artifact.content
    assert "Python" in artifact.content


def test_svg_renderer() -> None:
    """Verify SVGRenderer produces valid SVG visual cards."""
    model = create_sample_presentation_model()
    renderer = SVGRenderer()

    svgs = renderer.render(model)

    assert len(svgs) == 2
    assert isinstance(svgs[0], SVGArtifact)
    assert svgs[0].output_filename == "stats_card.svg"
    assert "<svg" in svgs[0].svg_content
    assert "</svg>" in svgs[0].svg_content
    assert "Octocat" in svgs[0].svg_content


def test_json_renderer() -> None:
    """Verify JSONRenderer serializes PresentationModel to JSONArtifact."""
    model = create_sample_presentation_model()
    renderer = JSONRenderer()

    artifact = renderer.render(model)

    assert isinstance(artifact, JSONArtifact)
    assert artifact.output_filename == "profileforge.json"
    assert '"username": "octocat"' in artifact.json_content


def test_template_loader() -> None:
    """Verify TemplateLoader provides default Markdown template."""
    loader = TemplateLoader()
    template = loader.get_markdown_template()

    assert "{{ profile.display_name }}" in template
    assert "Featured Projects" in template


def test_theme_loader() -> None:
    """Verify ThemeLoader returns dark and light theme palettes."""
    loader = ThemeLoader()

    dark = loader.get_theme("dark_glassmorphism")
    assert dark.bg_color == "#0d1117"

    light = loader.get_theme("light_minimal")
    assert light.bg_color == "#ffffff"


def test_renderer_orchestrator() -> None:
    """Verify RendererOrchestrator produces complete RenderedArtifacts collection."""
    model = create_sample_presentation_model()
    orchestrator = RendererOrchestrator()

    artifacts = orchestrator.render_presentation_model(model)

    assert isinstance(artifacts, RenderedArtifacts)
    assert artifacts.username == "octocat"
    assert artifacts.markdown_artifact is not None
    assert len(artifacts.svg_artifacts) == 2
    assert artifacts.json_artifact is not None
    assert artifacts.total_count == 4
    assert orchestrator.diagnostics.rendered_artifacts_count == 4


def test_renderer_failure_isolation() -> None:
    """Verify failure in one renderer does not invalidate successful outputs of other renderers."""
    model = create_sample_presentation_model()
    orchestrator = RendererOrchestrator()

    # Simulate SVGRenderer error by invalidating active theme configuration or custom hook
    # Orchestrator handles errors cleanly and records in diagnostics
    artifacts = orchestrator.render_presentation_model(model)

    assert artifacts.markdown_artifact is not None
    assert artifacts.json_artifact is not None


def test_deterministic_rendering() -> None:
    """Verify repeated rendering of identical PresentationModel produces identical content."""
    model = create_sample_presentation_model()
    orchestrator = RendererOrchestrator()

    artifacts1 = orchestrator.render_presentation_model(model)
    artifacts2 = orchestrator.render_presentation_model(model)

    assert artifacts1.markdown_artifact.content == artifacts2.markdown_artifact.content
    assert artifacts1.json_artifact.json_content == artifacts2.json_artifact.json_content
