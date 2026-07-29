from __future__ import annotations

from abc import ABC, abstractmethod

from github_profile_engine.models.generated_file import GeneratedFile
from github_profile_engine.models.profile_context import ProfileContext


class Renderer(ABC):
    """
    Base interface for every renderer.
    """

    @abstractmethod
    def render(
        self,
        context: ProfileContext,
    ) -> GeneratedFile:
        raise NotImplementedError
