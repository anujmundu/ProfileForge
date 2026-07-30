"""JSON Renderer.

Serializes PresentationModel into structured JSON artifact for debugging and export.
Governed by 09_RENDERING_SPECIFICATION.md.
"""

import json

from profileforge.generators.models import PresentationModel
from profileforge.renderers.exceptions import JSONRenderError
from profileforge.renderers.models import JSONArtifact
from profileforge.renderers.renderer import BaseRenderer


class JSONRenderer(BaseRenderer):
    """Concrete renderer for JSON presentation snapshot export."""

    def render(self, presentation_model: PresentationModel) -> JSONArtifact:
        """Render presentation model to JSONArtifact."""
        try:
            dumped_dict = presentation_model.model_dump()
            json_str = json.dumps(dumped_dict, indent=2)

            return JSONArtifact(
                identifier="presentation_json",
                output_filename="profileforge.json",
                json_content=json_str,
            )
        except Exception as exc:
            raise JSONRenderError(
                f"Failed to render JSON artifact for user '{presentation_model.username}': {exc}"
            ) from exc
