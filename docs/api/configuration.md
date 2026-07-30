# Configuration Subsystem API (`profileforge.configuration`)

The Configuration subsystem loads, validates, and manages immutable application settings.

---

## Primary Classes

### `ConfigurationManager`
Central manager for loading configuration from YAML files and environment variable overrides.

```python
class ConfigurationManager:
    def __init__(self, config_path: str | Path | None = None) -> None: ...
    def load(self) -> AppConfig: ...
```

### `YAMLConfigLoader`
File loader for parsing `profileforge.yaml`.

```python
class YAMLConfigLoader:
    def load_file(self, file_path: str | Path) -> dict[str, Any]: ...
```

### `AppConfig`
Immutable root configuration model (`frozen=True`).

```python
class AppConfig(BaseModel):
    app: GeneralAppConfig
    github: GitHubConfig
    analytics: AnalyticsConfig
    rendering: RenderingConfig
    automation: AutomationConfig
```
