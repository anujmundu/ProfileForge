"""Shimmer Animation Primitive.

Produces SMIL highlight shimmer sweep primitives.
Governed by 10_ANIMATION_ENGINE_SPECIFICATION.md.
"""

from profileforge.animation.models import AnimationPrimitive


class ShimmerPrimitive:
    """Factory for creating shimmer highlight animation primitives."""

    @staticmethod
    def create(
        primitive_id: str = "shimmer_sweep",
        duration: str = "2.5s",
        begin: str = "0.5s",
    ) -> AnimationPrimitive:
        """Create shimmer highlight animation primitive."""
        return AnimationPrimitive(
            primitive_id=primitive_id,
            name="Shimmer Sweep",
            attribute_name="opacity",
            from_value="0.3",
            to_value="1.0",
            duration=duration,
            begin=begin,
            repeat_count="indefinite",
            fill="freeze",
        )
