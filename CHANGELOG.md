# Changelog

All notable changes to the ProfileForge platform are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-07-30

### Added
- **Phase 1 — Workspace & Engineering Quality Gates**: Established MyPy strict mode, Ruff linting, Pytest test runner, and repository architecture specifications.
- **Phase 2 — Configuration Subsystem (`profileforge.configuration`)**: Implemented immutable `AppConfig`, `YAMLConfigLoader`, `EnvironmentResolver`, and `ConfigurationManager`.
- **Phase 3 — Engine Subsystem (`profileforge.engine`)**: Implemented 9-stage `LifecycleManager`, `EngineContext`, `DependencyRegistry`, `HealthAuditor`, and `Engine`.
- **Phase 4 — GitHub Integration Subsystem (`profileforge.github`)**: Implemented `GitHubClient`, rate limit awareness, HTTP Link header pagination, and in-memory TTL `ResponseCache`.
- **Phase 5 — Collectors Subsystem (`profileforge.collectors`)**: Implemented `CollectorOrchestrator`, `UserCollector`, `RepositoryCollector`, `LanguageCollector`, and canonical `CollectionSnapshot`.
- **Phase 6 — Analytics Subsystem (`profileforge.analytics`)**: Implemented deterministic repository scoring, featured repo selection, Shannon language entropy, and technology inference.
- **Phase 7 — Generators Subsystem (`profileforge.generators`)**: Implemented pure presentation models (`ProfileModel`, `StatisticsModel`, `FeaturedProjectsModel`, `TechnologyStackModel`).
- **Phase 8 — Rendering Subsystem (`profileforge.renderers`)**: Implemented `MarkdownRenderer`, `SVGRenderer` (with theme palettes), `JSONRenderer`, and `RendererOrchestrator`.
- **Phase 9 — SVG Animation Engine (`profileforge.animation`)**: Implemented SMIL animation primitives (`Fade`, `Pulse`, `Slide`, `Shimmer`, `Progress`), `AnimationRegistry`, `AnimationComposer`, and accessibility opt-out.
- **Phase 10 — Automation Subsystem (`profileforge.automation`)**: Implemented 8-stage `Workflow`, `ArtifactManager` with SHA-256 manifests, `LocalFileSystemPublisher`, `ManualScheduler`, `RetryPolicy`, `CancellationToken`, and `ExecutionReport`.
- **Phase 11 — System Hardening & Validation**: Created comprehensive integration, e2e, resilience, determinism, performance benchmark, and coverage validation suites (94% coverage across 106 tests).
- **Phase 12 — Documentation & DX**: Created architecture specifications, public API references, user guides, operational guides, and developer workflows.
