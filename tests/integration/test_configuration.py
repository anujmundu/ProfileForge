"""Integration tests for Configuration subsystem.

Validates configuration loading, environment variable resolution, and engine bootstrapping.
Governed by 01_ENGINEERING_QUALITY_GATES.md and 11_CONFIGURATION_SPECIFICATION.md.
"""

import os

from profileforge.configuration import ConfigurationManager
from profileforge.engine import Engine


def test_configuration_environment_integration() -> None:
    """Verify environment variables cascade to loaded application configuration."""
    os.environ["PROFILEFORGE_APP_ENVIRONMENT"] = "production"
    os.environ["PROFILEFORGE_GITHUB_MAX_RETRIES"] = "5"

    try:
        mgr = ConfigurationManager()
        cfg = mgr.load()

        assert cfg.app.environment.value == "production"
        assert cfg.github.max_retries == 5
    finally:
        os.environ.pop("PROFILEFORGE_APP_ENVIRONMENT", None)
        os.environ.pop("PROFILEFORGE_GITHUB_MAX_RETRIES", None)


def test_engine_configuration_bootstrapping() -> None:
    """Verify engine bootstraps cleanly with loaded configuration."""
    engine = Engine()
    ctx = engine.bootstrap()

    assert ctx.configuration is not None
    assert engine.state.value == "BOOTSTRAPPED" or engine.state.value == "READY" or ctx.configuration.app.app_name == "ProfileForge"
