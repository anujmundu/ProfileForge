"""Animation Orchestrator Implementation.

Coordinates animation configuration, registry lookup, and composition orchestration.
Governed by 10_ANIMATION_ENGINE_SPECIFICATION.md and 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

import time

from profileforge.animation.composer import AnimationComposer
from profileforge.animation.diagnostics import AnimationDiagnostics
from profileforge.animation.models import (
    AnimationConfiguration,
    AnimationDefinition,
)
from profileforge.animation.registry import AnimationRegistry
from profileforge.configuration import AnimationCategory


class AnimationOrchestrator:
    """Orchestrates animation definitions, configuration integration, and diagnostics."""

    def __init__(self, config: AnimationCategory | None = None) -> None:
        self._config_cat = config or AnimationCategory()
        self._animation_config = AnimationConfiguration(
            enabled=self._config_cat.enabled,
            timing_preset=self._config_cat.timing_preset,
            easing_preset=self._config_cat.easing_preset,
            stagger_interval_ms=self._config_cat.stagger_interval_ms,
            reduced_motion=self._config_cat.reduced_motion,
        )
        self._registry = AnimationRegistry()
        self._composer = AnimationComposer(
            registry=self._registry, config=self._animation_config
        )
        self._diagnostics = AnimationDiagnostics()

    @property
    def registry(self) -> AnimationRegistry:
        """Get the animation registry."""
        return self._registry

    @property
    def composer(self) -> AnimationComposer:
        """Get the animation composer."""
        return self._composer

    @property
    def diagnostics(self) -> AnimationDiagnostics:
        """Get subsystem diagnostics tracker."""
        return self._diagnostics

    @property
    def configuration(self) -> AnimationConfiguration:
        """Get active animation configuration."""
        return self._animation_config

    def create_card_entrance_animation(
        self, svg_target_id: str
    ) -> AnimationDefinition:
        """Helper to compose card entrance animation (Fade + Slide)."""
        start_time = time.perf_counter()

        fade = self._registry.get_primitive("fade_in")
        slide = self._registry.get_primitive("slide_up")

        definition = self._composer.compose_definition(
            definition_id=f"entrance_{svg_target_id}",
            svg_target_id=svg_target_id,
            primitives=[fade, slide],
        )

        duration_ms = (time.perf_counter() - start_time) * 1000.0
        self._diagnostics.generation_duration_ms += duration_ms
        self._diagnostics.registered_primitives_count = len(
            self._registry.registered_primitives
        )

        return definition
