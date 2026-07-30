"""Unit tests for SVG Animation Engine Subsystem.

Tests primitive registration, lookup, duplicate handling, composition into SMIL definitions,
disabled animation & reduced motion configuration, group composition, and orchestrator.
Governed by 10_ANIMATION_ENGINE_SPECIFICATION.md.
"""

import pytest

from profileforge.animation import (
    AnimationComposer,
    AnimationConfiguration,
    AnimationDefinition,
    AnimationGroup,
    AnimationOrchestrator,
    AnimationRegistry,
    CompositionError,
    RegistryError,
)
from profileforge.animation.fade import FadePrimitive
from profileforge.animation.slide import SlidePrimitive
from profileforge.configuration import AnimationCategory


def test_primitive_registration() -> None:
    """Verify default primitives are registered and custom primitives can be added."""
    registry = AnimationRegistry()

    assert registry.has_primitive("fade_in")
    assert registry.has_primitive("pulse_glow")
    assert registry.has_primitive("slide_up")
    assert len(registry.registered_primitives) >= 5

    custom = FadePrimitive.create(primitive_id="custom_fade", from_opacity=0.2)
    registry.register_primitive(custom)
    assert registry.has_primitive("custom_fade")


def test_duplicate_primitive_registration_raises_error() -> None:
    """Verify duplicate primitive registration raises RegistryError."""
    registry = AnimationRegistry()
    duplicate = FadePrimitive.create(primitive_id="fade_in")

    with pytest.raises(RegistryError):
        registry.register_primitive(duplicate)


def test_primitive_lookup() -> None:
    """Verify lookup by primitive ID."""
    registry = AnimationRegistry()
    fade = registry.get_primitive("fade_in")

    assert fade.primitive_id == "fade_in"
    assert fade.attribute_name == "opacity"
    assert "<animate" in fade.to_smil_element()


def test_unregistered_primitive_lookup_raises_error() -> None:
    """Verify lookup of non-existent primitive raises RegistryError."""
    registry = AnimationRegistry()
    with pytest.raises(RegistryError):
        registry.get_primitive("non_existent_primitive")


def test_animation_composition() -> None:
    """Verify composing primitives into valid SMIL AnimationDefinition."""
    fade = FadePrimitive.create("f1")
    slide = SlidePrimitive.create("s1")

    composer = AnimationComposer()
    definition = composer.compose_definition(
        definition_id="def_1",
        svg_target_id="card_1",
        primitives=[fade, slide],
    )

    assert isinstance(definition, AnimationDefinition)
    assert definition.enabled is True
    assert definition.svg_target_id == "card_1"
    assert 'attributeName="opacity"' in definition.smil_markup
    assert 'attributeName="y"' in definition.smil_markup


def test_disabled_animation_configuration() -> None:
    """Verify disabled config or reduced motion produces empty SMIL markup."""
    fade = FadePrimitive.create("f1")

    # 1. Disabled config
    disabled_cfg = AnimationConfiguration(enabled=False)
    composer_disabled = AnimationComposer(config=disabled_cfg)
    def_disabled = composer_disabled.compose_definition("d1", "t1", [fade])

    assert def_disabled.enabled is False
    assert def_disabled.smil_markup == ""

    # 2. Reduced motion config
    reduced_cfg = AnimationConfiguration(enabled=True, reduced_motion=True)
    composer_reduced = AnimationComposer(config=reduced_cfg)
    def_reduced = composer_reduced.compose_definition("d2", "t2", [fade])

    assert def_reduced.enabled is False
    assert def_reduced.smil_markup == ""


def test_empty_primitives_composition_raises_error() -> None:
    """Verify composing zero primitives raises CompositionError."""
    composer = AnimationComposer()
    with pytest.raises(CompositionError):
        composer.compose_definition("d1", "t1", primitives=[])


def test_group_registration_and_composition() -> None:
    """Verify registering and composing AnimationGroup."""
    registry = AnimationRegistry()
    fade = registry.get_primitive("fade_in")
    slide = registry.get_primitive("slide_up")

    group = AnimationGroup(
        group_id="entrance_group",
        description="Card entrance sequence",
        primitives=[fade, slide],
    )
    registry.register_group(group)
    assert registry.has_group("entrance_group")

    composer = AnimationComposer(registry=registry)
    def_group = composer.compose_group_definition("d_grp", "target_grp", "entrance_group")

    assert def_group.enabled is True
    assert len(def_group.primitives) == 2


def test_animation_orchestrator() -> None:
    """Verify AnimationOrchestrator integration with config category."""
    config_cat = AnimationCategory(enabled=True)
    orchestrator = AnimationOrchestrator(config=config_cat)

    card_anim = orchestrator.create_card_entrance_animation(svg_target_id="stats_card_1")

    assert card_anim.enabled is True
    assert card_anim.svg_target_id == "stats_card_1"
    assert orchestrator.diagnostics.registered_primitives_count >= 5


def test_deterministic_animation_output() -> None:
    """Verify identical inputs produce identical AnimationDefinition outputs."""
    orchestrator1 = AnimationOrchestrator()
    orchestrator2 = AnimationOrchestrator()

    anim1 = orchestrator1.create_card_entrance_animation("target_x")
    anim2 = orchestrator2.create_card_entrance_animation("target_x")

    assert anim1.smil_markup == anim2.smil_markup
    assert anim1.definition_id == anim2.definition_id


def test_animation_versioning_metadata() -> None:
    """Verify AnimationDefinition carries engine_version, config_hash, and primitive_ids."""
    orchestrator = AnimationOrchestrator()
    anim = orchestrator.create_card_entrance_animation("target_v")

    assert anim.engine_version == "0.1.0"
    assert "fade_in" in anim.primitive_ids
    assert "slide_up" in anim.primitive_ids
    assert anim.config_hash != ""

