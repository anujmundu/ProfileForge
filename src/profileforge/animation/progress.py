"""Progress Animation Primitive.

Produces SMIL width progress reveal primitives.
Governed by 10_ANIMATION_ENGINE_SPECIFICATION.md.
"""

from profileforge.animation.models import AnimationPrimitive


class ProgressPrimitive:
    """Factory for creating progress bar reveal animation primitives."""

    @staticmethod
    def create(
        primitive_id: str = "progress_reveal",
        from_width: int = 0,
        to_width: int = 100,
        duration: str = "1.8s",
        begin: str = "0.2s",
    ) -> AnimationPrimitive:
        """Create progress reveal animation primitive."""
        return AnimationPrimitive(
            primitive_id=primitive_id,
            name="Progress Reveal",
            attribute_name="width",
            from_value=str(from_width),
            to_value=str(to_width),
            duration=duration,
            begin=begin,
            repeat_count="1",
            fill="freeze",
        )
