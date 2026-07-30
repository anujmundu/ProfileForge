"""Pytest configuration and shared test fixtures for ProfileForge."""

import pytest


@pytest.fixture
def package_name() -> str:
    """Fixture returning the canonical package name."""
    return "profileforge"
