# Coding Standards & Guidelines

All code in ProfileForge must strictly adhere to the following standards:

---

## 1. Type Safety
- **100% MyPy Strict Mode**: Run `mypy src --strict`.
- Every function argument and return type must be explicitly annotated.
- Do not use `Any` unless strictly necessary for generic wrapping.

---

## 2. Code Style & Formatting
- **Ruff Compliance**: Run `ruff check src tests benchmarks`.
- Follow PEP 8 naming conventions (snake_case for functions/variables, PascalCase for classes).

---

## 3. Immutability & Domain Models
- Use Pydantic `BaseModel` with `model_config = ConfigDict(frozen=True)` for domain models.
- Never mutate domain model instances in place; return new immutable objects.

---

## 4. Subsystem Isolation
- Maintain single directional dependency flow: `Configuration -> Engine -> GitHub -> Collectors -> Analytics -> Generators -> Renderers -> Animation -> Automation`.
- Never import a downstream subsystem into an upstream module.
