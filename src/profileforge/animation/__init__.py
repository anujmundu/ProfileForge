"""SVG Animation Engine Subsystem.

Provides reusable, optional SVG animation primitives and definitions for visual renderers.
Governed by 10_ANIMATION_ENGINE_SPECIFICATION.md.
"""

from profileforge.animation.composer import AnimationComposer
from profileforge.animation.diagnostics import AnimationDiagnostics
from profileforge.animation.exceptions import (
    AnimationError,
    CompositionError,
    ConfigurationError,
    RegistryError,
)
from profileforge.animation.models import (
    AnimationConfiguration,
    AnimationDefinition,
    AnimationGroup,
    AnimationPrimitive,
)
from profileforge.animation.orchestrator import AnimationOrchestrator
from profileforge.animation.registry import AnimationRegistry

__all__ = [
    "AnimationComposer",
    "AnimationConfiguration",
    "AnimationDefinition",
    "AnimationDiagnostics",
    "AnimationError",
    "AnimationGroup",
    "AnimationOrchestrator",
    "AnimationPrimitive",
    "AnimationRegistry",
    "CompositionError",
    "ConfigurationError",
    "RegistryError",
]
