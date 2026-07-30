"""Rendered Artifact Models.

Immutable artifact models produced by the Rendering subsystem.
Governed by 09_RENDERING_SPECIFICATION.md and 04_DOMAIN_MODEL_SPECIFICATION.md.
"""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MarkdownArtifact(BaseModel):
    """Rendered Markdown README output artifact."""

    model_config = ConfigDict(frozen=True)

    identifier: str = "readme_markdown"
    output_filename: str = "README.md"
    content: str
    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
    metadata: dict[str, Any] = Field(default_factory=dict)


class SVGArtifact(BaseModel):
    """Rendered SVG visual card output artifact."""

    model_config = ConfigDict(frozen=True)

    identifier: str
    card_name: str
    output_filename: str
    svg_content: str
    width: int = 800
    height: int = 400
    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )


class JSONArtifact(BaseModel):
    """Rendered JSON snapshot export artifact."""

    model_config = ConfigDict(frozen=True)

    identifier: str = "presentation_json"
    output_filename: str = "profileforge.json"
    json_content: str
    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )


class RenderedArtifacts(BaseModel):
    """Collection of all successfully rendered artifacts for a profile."""

    model_config = ConfigDict(frozen=True)

    username: str
    markdown_artifact: MarkdownArtifact | None = None
    svg_artifacts: list[SVGArtifact] = Field(default_factory=list)
    json_artifact: JSONArtifact | None = None
    total_count: int = 0
    rendered_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
