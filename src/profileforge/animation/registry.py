"""Animation Registry Implementation.

Centralized registration, validation, and retrieval of animation primitives and groups.
Governed by 10_ANIMATION_ENGINE_SPECIFICATION.md.
"""

from profileforge.animation.exceptions import RegistryError
from profileforge.animation.fade import FadePrimitive
from profileforge.animation.models import AnimationGroup, AnimationPrimitive
from profileforge.animation.progress import ProgressPrimitive
from profileforge.animation.pulse import PulsePrimitive
from profileforge.animation.shimmer import ShimmerPrimitive
from profileforge.animation.slide import SlidePrimitive


class AnimationRegistry:
    """Registry managing animation primitives and composed groups."""

    def __init__(self) -> None:
        self._primitives: dict[str, AnimationPrimitive] = {}
        self._groups: dict[str, AnimationGroup] = {}
        self._register_default_primitives()

    def _register_default_primitives(self) -> None:
        """Register built-in primitive factories."""
        self.register_primitive(FadePrimitive.create("fade_in"))
        self.register_primitive(PulsePrimitive.create("pulse_glow"))
        self.register_primitive(SlidePrimitive.create("slide_up"))
        self.register_primitive(ShimmerPrimitive.create("shimmer_sweep"))
        self.register_primitive(ProgressPrimitive.create("progress_reveal"))

    def register_primitive(self, primitive: AnimationPrimitive) -> None:
        """Register a new primitive.

        Raises:
            RegistryError: If primitive_id is empty or already registered.
        """
        if not primitive.primitive_id or not primitive.primitive_id.strip():
            raise RegistryError("Primitive ID cannot be empty.")

        if primitive.primitive_id in self._primitives:
            raise RegistryError(
                f"Primitive with ID '{primitive.primitive_id}' is already registered."
            )

        self._primitives[primitive.primitive_id] = primitive

    def get_primitive(self, primitive_id: str) -> AnimationPrimitive:
        """Retrieve primitive by ID.

        Raises:
            RegistryError: If primitive is not found.
        """
        if primitive_id not in self._primitives:
            raise RegistryError(f"No registered primitive found with ID '{primitive_id}'.")
        return self._primitives[primitive_id]

    def has_primitive(self, primitive_id: str) -> bool:
        """Check if primitive is registered."""
        return primitive_id in self._primitives

    def register_group(self, group: AnimationGroup) -> None:
        """Register an animation group.

        Raises:
            RegistryError: If group_id is already registered.
        """
        if not group.group_id or not group.group_id.strip():
            raise RegistryError("Group ID cannot be empty.")

        if group.group_id in self._groups:
            raise RegistryError(f"Animation group '{group.group_id}' is already registered.")

        self._groups[group.group_id] = group

    def get_group(self, group_id: str) -> AnimationGroup:
        """Retrieve animation group by ID.

        Raises:
            RegistryError: If group is not found.
        """
        if group_id not in self._groups:
            raise RegistryError(f"No registered animation group found with ID '{group_id}'.")
        return self._groups[group_id]

    def has_group(self, group_id: str) -> bool:
        """Check if group is registered."""
        return group_id in self._groups

    @property
    def registered_primitives(self) -> list[str]:
        """List registered primitive IDs."""
        return list(self._primitives.keys())
