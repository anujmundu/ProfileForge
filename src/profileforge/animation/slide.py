"""Slide Animation Primitive.

Produces SMIL position translation slide primitives.
Governed by 10_ANIMATION_ENGINE_SPECIFICATION.md.
"""

from profileforge.animation.models import AnimationPrimitive


class SlidePrimitive:
    """Factory for creating translation slide animation primitives."""

    @staticmethod
    def create(
        primitive_id: str = "slide_up",
        attribute_name: str = "y",
        from_val: int = 20,
        to_val: int = 0,
        duration: str = "1.0s",
        begin: str = "0s",
    ) -> AnimationPrimitive:
        """Create translation slide animation primitive."""
        return AnimationPrimitive(
            primitive_id=primitive_id,
            name="Slide Up",
            attribute_name=attribute_name,
            from_value=str(from_val),
            to_value=str(to_val),
            duration=duration,
            begin=begin,
            repeat_count="1",
            fill="freeze",
        )
