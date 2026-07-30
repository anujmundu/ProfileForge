# 05 — REPOSITORY STRUCTURE SPECIFICATION

> **Status:** Locked
>
> **Authority:** Repository Constitution
>
> This document defines the canonical repository organization for the GitHub Profile Platform.
>
> It specifies the ownership, responsibilities, dependency boundaries, naming conventions, and lifecycle of every directory within the repository.
>
> This document is considered immutable unless explicitly revised through an architectural decision.
>
> Every implementation performed by humans or AI assistants must comply with this specification.

---

# Purpose

The repository structure exists to provide a predictable, scalable, and maintainable foundation for the platform.

A well-defined structure ensures:

- architectural consistency
- simplified navigation
- reduced cognitive load
- improved onboarding
- deterministic AI-assisted development
- long-term maintainability
- clear ownership boundaries

The repository shall be organized according to architectural responsibilities rather than implementation technologies.

---

# Repository Philosophy

The repository represents a production software product.

Directories exist because they own a business or architectural responsibility.

Directories must never become collections of unrelated code.

Every file shall have one logical home.

If a file does not clearly belong to an existing subsystem, the architecture must be reviewed before implementation.

---

# Canonical Repository Layout

```text
.
├── .github/
│   ├── ai/
│   └── workflows/
│
├── assets/
│   ├── generated/
│   ├── templates/
│   ├── icons/
│   ├── themes/
│   └── animations/
│
├── config/
│
├── docs/
│
├── examples/
│
├── scripts/
│
├── src/
│
├── tests/
│
├── .gitignore
├── LICENSE
├── README.md
└── pyproject.toml
```

---

# Source Tree

The source code shall be organized as follows.

```text
src/

└── profileforge/
    │
    ├── engine/
    │
    ├── configuration/
    │
    ├── github/
    │
    ├── collectors/
    │
    ├── analytics/
    │
    ├── models/
    │
    ├── generators/
    │
    ├── renderers/
    │
    ├── animations/
    │
    ├── automation/
    │
    ├── services/
    │
    ├── cli/
    │
    ├── exceptions/
    │
    └── utilities/
```

The internal Python package name for this project shall be:

```text
profileforge
```

This package name is considered part of the public architecture.

It shall not be renamed after implementation begins without an approved architectural migration.

---

# Directory Responsibilities

## engine/

### Owns

- application lifecycle
- orchestration
- dependency initialization
- execution pipeline
- subsystem coordination
- shutdown sequence

### Must Never Contain

- GitHub API logic
- analytics
- rendering logic
- configuration parsing

---

## configuration/

### Owns

- configuration loading
- schema validation
- typed settings
- environment variables
- configuration defaults
- configuration merging

### Must Never Contain

- business logic
- rendering logic

---

## github/

### Owns

- GitHub API communication
- authentication
- API clients
- request execution
- response parsing
- rate-limit handling

### Must Never Contain

- analytics
- rendering
- profile generation

---

## collectors/

### Owns

- data acquisition
- normalization
- conversion into domain models

Collectors retrieve information.

Collectors do not analyze information.

---

## analytics/

### Owns

- repository scoring
- language analysis
- activity analysis
- contribution metrics
- engineering metrics
- skill inference
- project ranking
- research classification

Analytics enriches domain models.

Analytics never communicates directly with GitHub.

---

## models/

### Owns

The canonical domain models defined in:

> 04_DOMAIN_MODEL_SPECIFICATION.md

Models contain data only.

Business logic is prohibited.

---

## generators/

### Owns

- profile assembly
- rendering context creation
- asset planning
- output preparation

Generators convert domain models into rendering models.

---

## renderers/

### Owns

Generation of:

- Markdown
- SVG
- JSON
- HTML (future)
- PNG (future)
- PDF (future)

Renderers consume rendering models.

Renderers perform no analytics.

Renderers perform no GitHub communication.

---

## animations/

### Owns

- SVG animations
- timelines
- transitions
- motion definitions
- reusable animation primitives

Animations shall remain reusable across renderers.

---

## automation/

### Owns

- GitHub Actions
- scheduled execution
- repository events
- automation workflows

Automation contains orchestration only.

Business logic is prohibited.

---

## services/

Shared infrastructure services.

Examples include:

- logging
- filesystem
- caching
- dependency injection
- serialization
- validation

Services are infrastructure.

They are not business logic.

---

## cli/

### Owns

- command-line interface
- developer tools
- diagnostics
- local execution

---

## exceptions/

### Owns

- custom exception hierarchy
- error definitions
- domain exceptions

---

## utilities/

Utilities are reserved for:

- small
- generic
- stateless
- reusable helper functions

Utilities shall never become a dumping ground.

Every new utility requires architectural justification.

---

# Assets Structure

```text
assets/

generated/
```

Contains generated artifacts.

Examples:

- README assets
- generated SVGs
- dashboards
- graphs

Generated content may be overwritten.

---

```text
assets/

templates/
```

Contains rendering templates.

Templates are immutable inputs.

---

```text
assets/

icons/
```

Contains reusable icon assets.

---

```text
assets/

themes/
```

Contains theme definitions.

Themes are configuration.

They are not rendering logic.

---

```text
assets/

animations/
```

Contains reusable animation resources.

---

# Documentation Structure

```text
docs/

00_project_charter.md

01_engineering_quality_gates.md

02_product_requirements_specification.md

03_system_architecture_specification.md

04_domain_model_specification.md

05_repository_structure_specification.md

06_engine_lifecycle_specification.md

07_github_integration_specification.md

08_analytics_specification.md

09_rendering_specification.md

10_animation_engine_specification.md

11_configuration_specification.md

12_ai_development_constitution.md

13_development_workflow.md

14_milestones.md

15_session_state.md
```

Documents 00–13 are immutable architectural specifications.

Documents 14–15 are living documents that evolve throughout the project lifecycle.

---

# Testing Structure

```text
tests/

unit/

integration/

end_to_end/

fixtures/

snapshots/
```

Tests shall mirror the source hierarchy wherever practical.

Every subsystem shall have corresponding unit tests.

Integration tests shall verify subsystem interaction.

End-to-end tests shall validate complete execution pipelines.

---

# Naming Conventions

Directories:

- lowercase
- singular responsibility
- descriptive names

Python Modules:

- snake_case

Classes:

- PascalCase

Functions:

- snake_case

Constants:

- UPPER_SNAKE_CASE

Private Members:

- leading underscore

Configuration Files:

- snake_case

Documentation:

- numbered sequentially

---

# Ownership Rules

Every source file belongs to exactly one subsystem.

Ownership ambiguity is considered an architectural issue.

Subsystem ownership may not overlap.

No subsystem may directly modify another subsystem's internal state.

Communication shall occur only through documented interfaces.

---

# Dependency Rules

Allowed dependency direction:

```text
CLI

↓

Automation

↓

Engine

↓

Collectors

↓

Analytics

↓

Generators

↓

Renderers

↓

Outputs
```

Dependencies shall always point inward.

Reverse dependencies are prohibited.

Circular dependencies are prohibited.

Cross-layer shortcuts are prohibited.

---

# Repository Evolution Rules

Future directories may only be added if:

- a new architectural responsibility exists
- existing responsibilities cannot reasonably own the new functionality
- the addition has been documented
- the architecture specification has been updated

Directories shall never be created for convenience.

---

# Forbidden Practices

The following practices are prohibited:

- business logic inside renderers
- GitHub API code outside github/
- analytics inside collectors
- rendering inside analytics
- configuration parsing outside configuration/
- circular imports
- duplicated implementations
- utility dumping
- global mutable state
- hidden dependencies
- undocumented directories

---

# AI Development Rules

Before creating a new file, the AI assistant shall determine:

1. Which subsystem owns this functionality.
2. Whether a file already exists with this responsibility.
3. Whether the implementation violates dependency direction.
4. Whether the architecture specification already defines the location.

If any answer is uncertain, implementation shall stop until clarification is obtained.

The AI assistant shall never invent new top-level directories.

The AI assistant shall never relocate existing files without explicit architectural approval.

The AI assistant shall treat this repository layout as immutable.

---

# Success Criteria

The repository structure succeeds when:

- every file has a clear architectural home
- subsystem ownership is immediately obvious
- navigation is intuitive
- onboarding new contributors is straightforward
- AI assistants can place files without guessing
- future expansion occurs without repository reorganization

---

# Approval

This document defines the canonical repository organization of the GitHub Profile Platform.

All future implementation shall conform to this structure.

Architectural changes require an explicit revision to this specification before implementation may proceed.
