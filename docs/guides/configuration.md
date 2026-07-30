# Configuration Guide

ProfileForge supports file-based configuration (`profileforge.yaml`) and environment variable overrides (`PROFILEFORGE_*`).

---

## Precedence Hierarchy

```text
Environment Variables (PROFILEFORGE_*)
         ↓
YAML Configuration File (profileforge.yaml)
         ↓
Default Application Configuration
```

---

## Sample `profileforge.yaml`

```yaml
app:
  app_name: "ProfileForge"
  environment: "production"
  log_level: "INFO"

github:
  max_retries: 3
  timeout_seconds: 30.0
  cache_ttl_seconds: 3600

analytics:
  min_stars_threshold: 0
  max_featured_repositories: 6

rendering:
  theme: "dark"
  enable_animation: true

automation:
  output_dir: "./dist"
  overwrite_existing: true
  max_retries: 3
```

---

## Environment Variable Overrides

Override any configuration parameter using single underscore syntax:

```bash
export PROFILEFORGE_APP_ENVIRONMENT="production"
export PROFILEFORGE_GITHUB_MAX_RETRIES="5"
export PROFILEFORGE_RENDERING_THEME="light"
```
