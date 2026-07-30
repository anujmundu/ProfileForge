# Contributing to ProfileForge

Thank you for considering contributing to ProfileForge!

ProfileForge is governed by strict architectural principles, engineering quality gates, and type safety rules.

---

## 🛠️ Development Setup

1. **Clone Repository**:
   ```bash
   git clone https://github.com/anujmundu/anujmundu.git
   cd anujmundu
   ```

2. **Create Virtual Environment & Install Dependencies**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Run Quality Gates**:
   ```bash
   ruff check src tests benchmarks
   mypy src --strict
   pytest --cov=src
   ```

---

## 📐 Architectural Principles

- **Strict Subsystem Isolation**: Data flows strictly downwards (`Configuration -> Engine -> GitHub -> Collectors -> Analytics -> Generators -> Renderers -> Animation -> Automation`). Never add upward or circular dependencies.
- **100% Type Safety**: All source code must pass `mypy src --strict` with zero type errors or `type: ignore` comments.
- **Pure Presentation Models**: Generators must produce raw data objects without Markdown/HTML/SVG tags or emojis.
- **Zero Live Network Calls in Tests**: All API interactions must use mocked HTTP clients or snapshots.

---

## 📝 Commit Conventions

We follow Conventional Commits format:
- `feat(subsystem)`: New capability or module.
- `fix(subsystem)`: Bug fix in existing module.
- `docs(subsystem)`: Documentation updates.
- `test(subsystem)`: Test suite additions or enhancements.
- `refactor(subsystem)`: Non-functional code cleanup.

Example: `feat(analytics): add Shannon language diversity index`
