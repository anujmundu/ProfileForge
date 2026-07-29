from __future__ import annotations

from github_profile_engine.models.generated_file import GeneratedFile
from github_profile_engine.models.profile_context import ProfileContext
from github_profile_engine.renderers.base import Renderer


class GenerationPipeline:
    """
    Executes all registered renderers.
    """

    def __init__(
        self,
        renderers: list[Renderer],
    ):
        self.renderers = renderers

    def generate(
        self,
        context: ProfileContext,
    ) -> list[GeneratedFile]:
        generated: list[GeneratedFile] = []

        for renderer in self.renderers:
            generated.append(renderer.render(context))

        return generated
