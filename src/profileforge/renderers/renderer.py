"""Abstract Base Renderer Contract.

Defines common contract for all concrete renderers.
Governed by 09_RENDERING_SPECIFICATION.md.
"""

from abc import ABC, abstractmethod
from typing import Any

from profileforge.generators.models import PresentationModel


class BaseRenderer(ABC):
    """Abstract contract enforced across all renderers."""

    @abstractmethod
    def render(self, presentation_model: PresentationModel) -> Any:
        """Render presentation model into a concrete artifact."""
        raise NotImplementedError
