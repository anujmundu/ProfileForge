# ProfileForge — GitHub Profile Engine

> A production-grade platform for creating self-updating GitHub profile READMEs, animated SVG graphics, and automated engineering portfolio dashboards.

---

## Architecture & Specifications

The platform is strictly defined by 14 locked constitutional specification documents:

- **[00 — Project Charter](docs/00_project_charter.md)**
- **[01 — Engineering Quality Gates](docs/01_engineering_quality_gates.md)**
- **[02 — Product Requirements Specification](docs/02_product_requirements_specification.md)**
- **[03 — System Architecture Specification](docs/03_system_architecture_spec.md)**
- **[04 — Domain Model Specification](docs/04_domain_model_specification.md)**
- **[05 — Repository Structure Specification](docs/05_repository_structure_specification.md)**
- **[06 — Engine Lifecycle Specification](docs/06_engine_lifecycle_specification.md)**
- **[07 — GitHub Integration Specification](docs/07_github_integration_specification.md)**
- **[08 — Analytics Specification](docs/08_analytics_specification.md)**
- **[09 — Rendering Specification](docs/09_rendering_specification.md)**
- **[10 — Animation Engine Specification](docs/10_animation_engine_specification.md)**
- **[11 — Configuration Specification](docs/11_configuration_specification.md)**
- **[12 — AI Development Constitution](docs/12_ai_development_constitution.md)**
- **[13 — Development Workflow Specification](docs/13_development_workflow.md)**

Operations & roadmap are tracked in:
- **[14 — Milestones](docs/14_milestones.md)**
- **[15 — Session State](docs/15_session_state.md)**

---

## Development Setup

```bash
# Install package in editable mode with development dependencies
pip install -e ".[dev]"

# Run code formatting check
ruff format --check src tests

# Run linting
ruff check src tests

# Run type checking
mypy src --strict

# Run test suite
pytest
```
