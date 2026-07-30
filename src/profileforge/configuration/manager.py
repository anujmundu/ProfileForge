"""Configuration Manager Subsystem Entry Point.

Coordinates configuration discovery, loading, precedence merging, validation,
and immutable root configuration construction.
"""

from pathlib import Path
from typing import Any

from profileforge.configuration.defaults import get_default_configuration_dict
from profileforge.configuration.diagnostics import ConfigurationDiagnostics
from profileforge.configuration.environment import load_environment_variables
from profileforge.configuration.loader import deep_merge_dicts, load_yaml_file
from profileforge.configuration.models import ProfileForgeConfiguration
from profileforge.configuration.validator import validate_configuration_dict


class ConfigurationManager:
    """Orchestrates configuration discovery, loading, validation, and immutability."""

    def __init__(self, config_file: Path | str | None = None) -> None:
        self._config_file: Path | None = Path(config_file) if config_file else None
        self._sources_loaded: list[str] = ["defaults"]
        self._config: ProfileForgeConfiguration | None = None
        self._diagnostics: ConfigurationDiagnostics | None = None

    def load(
        self,
        env_overrides: dict[str, str] | None = None,
        raw_overrides: dict[str, Any] | None = None,
    ) -> ProfileForgeConfiguration:
        """Load, merge, validate, and freeze configuration.

        Precedence Order:
        1. Explicit raw overrides (e.g. CLI arguments)
        2. Environment variables (PROFILEFORGE_* / GITHUB_TOKEN)
        3. YAML Configuration file
        4. Default values

        Args:
            env_overrides: Optional dictionary simulating os.environ.
            raw_overrides: Optional dictionary of raw field overrides.

        Returns:
            Immutable ProfileForgeConfiguration instance.
        """
        # 1. Start with defaults dictionary
        merged = get_default_configuration_dict()

        # 2. Merge optional YAML configuration file
        if self._config_file:
            file_data = load_yaml_file(self._config_file)
            if file_data:
                merged = deep_merge_dicts(merged, file_data)
                self._sources_loaded.append(f"yaml:{self._config_file}")
        else:
            # Check default config locations: config/profileforge.yml or config/config.yml
            for default_path in [
                Path("config/profileforge.yml"),
                Path("config/profileforge.yaml"),
                Path("config/config.yml"),
            ]:
                if default_path.is_file():
                    file_data = load_yaml_file(default_path)
                    if file_data:
                        merged = deep_merge_dicts(merged, file_data)
                        self._sources_loaded.append(f"yaml:{default_path}")
                        self._config_file = default_path
                        break

        # 3. Merge Environment Variables
        env_data = load_environment_variables(env_overrides)
        if env_data:
            merged = deep_merge_dicts(merged, env_data)
            self._sources_loaded.append("environment")

        # 4. Merge explicit raw overrides (e.g. CLI flags)
        if raw_overrides:
            merged = deep_merge_dicts(merged, raw_overrides)
            self._sources_loaded.append("cli_overrides")

        # 5. Validate and construct immutable model
        self._config = validate_configuration_dict(merged)

        # 6. Build diagnostics instance
        self._diagnostics = ConfigurationDiagnostics(
            config=self._config,
            sources=self._sources_loaded,
            applied_overrides=merged,
        )

        return self._config

    @property
    def config(self) -> ProfileForgeConfiguration:
        """Get the current loaded configuration object.

        Raises:
            RuntimeError: If configuration has not been loaded yet.
        """
        if self._config is None:
            raise RuntimeError(
                "Configuration has not been loaded. Call load() before accessing config."
            )
        return self._config

    @property
    def diagnostics(self) -> ConfigurationDiagnostics:
        """Get diagnostics for the loaded configuration."""
        if self._diagnostics is None:
            raise RuntimeError(
                "Configuration has not been loaded. Call load() before accessing diagnostics."
            )
        return self._diagnostics
