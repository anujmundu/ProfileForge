# ProfileForge 🚀

> **Enterprise-Grade GitHub Profile & Portfolio Automation Platform**
>
> Deterministic data collection, scoring analytics, presentation-independent content generation, theme-driven SVG & Markdown rendering, SMIL animation, and workflow orchestration.

---

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Checked: MyPy Strict](https://img.shields.io/badge/mypy-strict-brightgreen.svg)](https://mypy.readthedocs.io/)
[![Coverage: 94%](https://img.shields.io/badge/coverage-94%25-success.svg)](https://pytest.org/)

---

## 📖 Architecture Overview

ProfileForge is designed around strict subsystem separation of concerns. Data flows strictly in one direction from raw GitHub API signals down to rendered output artifacts:

```text
Configuration (YAML / Env)
       ↓
    Engine (Bootstrapping & Lifecycle)
       ↓
GitHub Integration (REST API Client, Rate Limiting & Caching)
       ↓
  Collectors (Profile, Repositories, Languages, Contributions)
       ↓
   Analytics (Repository Scoring, Shannon Diversity, Tech Inference)
       ↓
  Generators (Presentation Models for Profile, Stats, Tech Stack)
       ↓
   Renderers (Markdown, Theme-Driven SVG Cards, JSON Snapshots)
       ↓
   Animation (SMIL SVG Primitive Registry & Composer)
       ↓
  Automation (8-Stage Workflow, ArtifactManager, Retry Policy & Publishers)
```

---

## ✨ Key Features

- 🎯 **100% Deterministic Execution**: Pure mathematical scoring, Shannon language entropy, and reproducible presentation models.
- 🎨 **Theme-Driven SVG Cards**: Sleek dark mode, custom color palettes, modern typography, and SMIL SVG micro-animations (`reduced_motion` accessible).
- 🛡️ **Production Quality Gates**: 100% MyPy strict type safety, zero Ruff lint warnings, 94% test code coverage across 100+ unit, integration, e2e, and resilience tests.
- 🔒 **Provenanced Execution Reports**: SHA-256 artifact manifests, ISO 8601 execution telemetry, and cooperative cancellation tokens.

---

## ⚡ Quick Start

```bash
# 1. Install ProfileForge
pip install -e .

# 2. Set your GitHub Personal Access Token (optional, for higher rate limits)
export GITHUB_TOKEN="ghp_your_github_token_here"

# 3. Run full automated pipeline via Python API
python -c "from profileforge.automation import AutomationOrchestrator; orchestrator = AutomationOrchestrator(); report = orchestrator.execute_workflow('octocat'); print(report)"
```

Generated artifacts are published to `./dist/`:
- `./dist/README.md`
- `./dist/stats_card.svg`
- `./dist/tech_card.svg`
- `./dist/profileforge.json`

---

## 📚 Documentation Index

- [Architecture Guide](docs/architecture/overview.md)
- [Execution Pipeline](docs/architecture/execution_pipeline.md)
- [Public API Reference](docs/api/public_api.md)
- [Installation Guide](docs/guides/installation.md)
- [Configuration Guide](docs/guides/configuration.md)
- [Troubleshooting Guide](docs/guides/troubleshooting.md)
- [Observability & Diagnostics](docs/operations/observability.md)
- [Contributor Guide](docs/development/contributing.md)

---

## 🤝 Contributing

We welcome community contributions! Please read our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting Pull Requests.

---

## 📄 License

ProfileForge is released under the [MIT License](LICENSE).
