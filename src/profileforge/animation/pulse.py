"""Pulse Animation Primitive.

Produces SMIL pulsing opacity primitives.
Governed by 10_ANIMATION_ENGINE_SPECIFICATION.md.
"""

from profileforge.animation.models import AnimationPrimitive


class PulsePrimitive:
    """Factory for creating pulsing opacity animation primitives."""

    @staticmethod
    def create(
        primitive_id: str = "pulse_glow",
        min_opacity: float = 0.4,
        max_opacity: float = 1.0,
        duration: str = "2.0s",
        begin: str = "0s",
    ) -> AnimationPrimitive:
        """Create pulsing opacity animation primitive."""
        return AnimationPrimitive(
            primitive_id=primitive_id,
            name="Pulse Glow",
            attribute_name="opacity",
            from_value=str(min_opacity),
            to_value=str(max_opacity),
            duration=duration,
            begin=begin,
            repeat_count="indefinite",
            fill="freeze",
        )
