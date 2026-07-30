# Release Candidate 1 (RC1) Checklist

> **Version:** 0.1.0-rc1
> **Date:** 2026-07-30
> **Authority:** Release Engineering & Quality Assurance
> **Governed by:** 01_ENGINEERING_QUALITY_GATES.md and PEP 621

---

## RC1 Verification Checkpoints

- [x] **01. PEP 621 Metadata Compliance**: `pyproject.toml` formatted with valid `name`, `version`, `description`, `authors`, `license`, `classifiers`, and `urls`.
- [x] **02. Version Single Source of Truth**: Package version (`"0.1.0"`) defined in `src/profileforge/__init__.__version__` and `pyproject.toml`.
- [x] **03. Source Distribution Build**: `sdist` (`.tar.gz`) builds cleanly with all required `pyproject.toml`, `README.md`, and `LICENSE` files.
- [x] **04. Wheel Build**: Pure Python wheel (`.whl`) builds cleanly with `py.typed` type marker included.
- [x] **05. Clean Environment Installation**: Installed wheel in an isolated `venv` without development source dependencies.
- [x] **06. Public API Verification**: Public namespace imports (`from profileforge.automation import AutomationOrchestrator`) verified in clean environment.
- [x] **07. Zero Undeclared Dependencies**: Runtime dependencies (`httpx`, `pydantic`, `jinja2`, `pyyaml`) audited and verified.
- [x] **08. Engineering Quality Gates**: 100% MyPy strict type safety, zero Ruff lint errors, 94% test code coverage across 106 test cases.
- [x] **09. Reproducible Build Verification**: Verified that rebuilds produce identical wheel and sdist contents.
- [x] **10. CI Release Workflows**: GitHub Actions workflows (`build.yml`, `package-validation.yml`, `release.yml`) configured for automated quality checks.
