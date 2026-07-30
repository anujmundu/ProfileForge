"""Fade Animation Primitive.

Produces SMIL opacity fade transition primitives.
Governed by 10_ANIMATION_ENGINE_SPECIFICATION.md.
"""

from profileforge.animation.models import AnimationPrimitive


class FadePrimitive:
    """Factory for creating opacity fade animation primitives."""

    @staticmethod
    def create(
        primitive_id: str = "fade_in",
        from_opacity: float = 0.0,
        to_opacity: float = 1.0,
        duration: str = "1.5s",
        begin: str = "0s",
    ) -> AnimationPrimitive:
        """Create opacity fade animation primitive."""
        return AnimationPrimitive(
            primitive_id=primitive_id,
            name="Fade In",
            attribute_name="opacity",
            from_value=str(from_opacity),
            to_value=str(to_opacity),
            duration=duration,
            begin=begin,
            repeat_count="1",
            fill="freeze",
        )
