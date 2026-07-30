"""Markdown Renderer.

Renders PresentationModel into clean, formatted Markdown README.md artifact.
Governed by 09_RENDERING_SPECIFICATION.md.
"""

from jinja2 import Template

from profileforge.generators.models import PresentationModel
from profileforge.renderers.exceptions import MarkdownRenderError
from profileforge.renderers.models import MarkdownArtifact
from profileforge.renderers.renderer import BaseRenderer
from profileforge.renderers.template_loader import TemplateLoader


class MarkdownRenderer(BaseRenderer):
    """Concrete renderer for Markdown README artifacts."""

    def __init__(self, template_loader: TemplateLoader | None = None) -> None:
        self._template_loader = template_loader or TemplateLoader()

    def render(self, presentation_model: PresentationModel) -> MarkdownArtifact:
        """Render presentation model to MarkdownArtifact."""
        try:
            raw_template = self._template_loader.get_markdown_template()
            template = Template(raw_template, autoescape=False)

            rendered_content = template.render(
                profile=presentation_model.profile,
                statistics=presentation_model.statistics,
                featured_projects=presentation_model.featured_projects,
                technology_stack=presentation_model.technology_stack,
                timeline=presentation_model.timeline,
                achievements=presentation_model.achievements,
            )

            return MarkdownArtifact(
                identifier="readme_markdown",
                output_filename="README.md",
                content=rendered_content.strip(),
                metadata={"username": presentation_model.username},
            )
        except Exception as exc:
            raise MarkdownRenderError(
                f"Failed to render Markdown README for user '{presentation_model.username}': {exc}"
            ) from exc
