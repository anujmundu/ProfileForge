"""Animation Engine Subsystem Exception Hierarchy.

Governed by 10_ANIMATION_ENGINE_SPECIFICATION.md.
"""

from profileforge.exceptions import ProfileForgeError


class AnimationError(ProfileForgeError):
    """Base exception for all Animation Engine subsystem errors."""


class RegistryError(AnimationError):
    """Raised when animation primitive or group registration/lookup fails."""


class CompositionError(AnimationError):
    """Raised when animation composition fails."""


class ConfigurationError(AnimationError):
    """Raised when animation configuration or validation fails."""
