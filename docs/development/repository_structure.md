# Repository Structure & Subsystem Layout

```text
anujmundu/
├── benchmarks/             # Standalone performance benchmark scripts
├── docs/                   # Full documentation index
│   ├── api/                # Public API reference docs
│   ├── architecture/       # System architecture specifications
│   ├── development/        # Developer & contribution guides
│   ├── guides/             # User & configuration guides
│   └── operations/         # Observability & diagnostic guides
├── reports/
│   └── quality/            # Quality audit reports & production readiness checklist
├── src/
│   └── profileforge/       # Primary Python package
│       ├── analytics/      # Repository scoring & Shannon diversity analytics
│       ├── animation/      # SMIL SVG animation primitives & registry
│       ├── automation/     # Master workflow orchestration & artifact management
│       ├── collectors/     # Raw GitHub snapshot assembly
│       ├── configuration/  # YAML loader & environment resolver
│       ├── engine/         # Application lifecycle manager & dependency registry
│       ├── exceptions/     # Base ProfileForge error hierarchy
│       ├── generators/     # Semantic presentation-independent models
│       ├── github/         # REST API client, pagination, & response caching
│       └── renderers/      # Markdown, theme-driven SVG cards, & JSON renderers
├── tests/                  # Automated test suites
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── resilience/
│   ├── regression/
│   └── performance/
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
├── README.md
└── SECURITY.md
```
