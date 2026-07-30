"""Canonical Animation Models.

Immutable animation primitive, group, and definition models for SVG artifacts.
Exposes pure animation metadata without SVG layout information.
Governed by 10_ANIMATION_ENGINE_SPECIFICATION.md and 04_DOMAIN_MODEL_SPECIFICATION.md.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from profileforge import __version__
from profileforge.configuration import EasingPreset, TimingPreset


class AnimationConfiguration(BaseModel):
    """Immutable operational configuration settings for SVG animations."""

    model_config = ConfigDict(frozen=True)

    enabled: bool = True
    duration_seconds: float = Field(default=1.5, gt=0.0)
    timing_preset: TimingPreset = TimingPreset.NORMAL
    easing_preset: EasingPreset = EasingPreset.EASE_IN_OUT
    stagger_interval_ms: int = Field(default=100, ge=0)
    reduced_motion: bool = False


class AnimationPrimitive(BaseModel):
    """Low-level reusable SMIL SVG animation primitive."""

    model_config = ConfigDict(frozen=True)

    primitive_id: str
    name: str
    attribute_name: str
    from_value: str
    to_value: str
    duration: str = "1.5s"
    begin: str = "0s"
    repeat_count: str = "indefinite"
    fill: str = "freeze"

    def to_smil_element(self) -> str:
        """Render primitive to a valid SMIL SVG element string."""
        return (
            f'<animate attributeName="{self.attribute_name}" '
            f'from="{self.from_value}" to="{self.to_value}" '
            f'dur="{self.duration}" begin="{self.begin}" '
            f'repeatCount="{self.repeat_count}" fill="{self.fill}" />'
        )


class AnimationGroup(BaseModel):
    """Group of primitives combined into a semantic animation sequence."""

    model_config = ConfigDict(frozen=True)

    group_id: str
    description: str = ""
    primitives: list[AnimationPrimitive] = Field(default_factory=list)


class AnimationDefinition(BaseModel):
    """Composed SVG animation definition ready for SVG renderer insertion."""

    model_config = ConfigDict(frozen=True)

    definition_id: str
    svg_target_id: str
    smil_markup: str
    primitives: list[AnimationPrimitive] = Field(default_factory=list)
    primitive_ids: list[str] = Field(default_factory=list)
    engine_version: str = __version__
    config_hash: str = ""
    enabled: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)
