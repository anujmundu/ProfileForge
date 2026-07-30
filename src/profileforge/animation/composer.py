"""Animation Composer Implementation.

Composes animation primitives and groups into AnimationDefinition objects containing valid SMIL SVG markup.
Governed by 10_ANIMATION_ENGINE_SPECIFICATION.md.
"""

from profileforge.animation.exceptions import CompositionError
from profileforge.animation.models import (
    AnimationConfiguration,
    AnimationDefinition,
    AnimationGroup,
    AnimationPrimitive,
)
from profileforge.animation.registry import AnimationRegistry


class AnimationComposer:
    """Composes primitives into SVG animation definitions."""

    def __init__(
        self,
        registry: AnimationRegistry | None = None,
        config: AnimationConfiguration | None = None,
    ) -> None:
        self._registry = registry or AnimationRegistry()
        self._config = config or AnimationConfiguration()

    def compose_definition(
        self,
        definition_id: str,
        svg_target_id: str,
        primitives: list[AnimationPrimitive],
    ) -> AnimationDefinition:
        """Compose a list of primitives into a valid AnimationDefinition.

        Args:
            definition_id: Unique string identifier for definition.
            svg_target_id: ID of the SVG element target.
            primitives: List of AnimationPrimitive objects.

        Returns:
            AnimationDefinition instance with combined SMIL markup string.

        Raises:
            CompositionError: If primitives list is empty or disabled in config.
        """
        if not self._config.enabled or self._config.reduced_motion:
            return AnimationDefinition(
                definition_id=definition_id,
                svg_target_id=svg_target_id,
                smil_markup="",
                primitives=[],
                enabled=False,
            )

        if not primitives:
            raise CompositionError("Cannot compose animation definition with zero primitives.")

        smil_elements = [p.to_smil_element() for p in primitives]
        smil_markup = "\n  ".join(smil_elements)
        primitive_ids = [p.primitive_id for p in primitives]
        config_hash = f"dur={self._config.duration_seconds}_timing={self._config.timing_preset.value}_easing={self._config.easing_preset.value}"

        return AnimationDefinition(
            definition_id=definition_id,
            svg_target_id=svg_target_id,
            smil_markup=smil_markup,
            primitives=primitives,
            primitive_ids=primitive_ids,
            config_hash=config_hash,
            enabled=True,
            metadata={"stagger_ms": self._config.stagger_interval_ms},
        )

    def compose_group_definition(
        self, definition_id: str, svg_target_id: str, group_id: str
    ) -> AnimationDefinition:
        """Compose registered group into AnimationDefinition."""
        group: AnimationGroup = self._registry.get_group(group_id)
        return self.compose_definition(
            definition_id=definition_id,
            svg_target_id=svg_target_id,
            primitives=group.primitives,
        )
