from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from github_profile_engine.models.generated_file import GeneratedFile
from github_profile_engine.models.profile_context import ProfileContext
from github_profile_engine.renderers.base import Renderer


class MarkdownRenderer(Renderer):
    """
    Renders a README.md file from a Jinja2 template.
    """

    def __init__(self, template_directory: Path):
        self.environment = Environment(
            loader=FileSystemLoader(template_directory),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, context: ProfileContext) -> GeneratedFile:
        template = self.environment.get_template("README.md.j2")

        content = template.render(
            profile=context.profile,
            languages=context.languages,
            featured_repositories=context.featured_repositories,
        )

        return GeneratedFile(
            path=Path("README.md"),
            content=content,
        )
