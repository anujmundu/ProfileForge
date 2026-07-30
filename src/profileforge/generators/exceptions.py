"""Generators Subsystem Exception Hierarchy.

Governed by 09_RENDERING_SPECIFICATION.md and 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

from profileforge.exceptions import ProfileForgeError


class GeneratorError(ProfileForgeError):
    """Base exception for all Generators subsystem errors."""


class ProfileGenerationError(GeneratorError):
    """Raised when profile presentation model generation fails."""


class StatisticsGenerationError(GeneratorError):
    """Raised when statistics presentation model generation fails."""


class FeaturedGenerationError(GeneratorError):
    """Raised when featured projects presentation model generation fails."""


class TimelineGenerationError(GeneratorError):
    """Raised when timeline presentation model generation fails."""


class TechnologyGenerationError(GeneratorError):
    """Raised when technology stack presentation model generation fails."""
