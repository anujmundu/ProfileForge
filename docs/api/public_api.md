# Public API Reference Overview

ProfileForge exports a clean, strongly-typed public API under top-level package namespace imports.

---

## Subsystem API References

- [Configuration API](configuration.md) — Settings loading, YAML parsing, and environment variable resolution.
- [Engine API](engine.md) — State machine lifecycle management, dependency injection, and health auditing.
- [GitHub API](github.md) — REST API client, Link header pagination, rate limiting, and response caching.
- [Collectors API](collectors.md) — Raw snapshot assembly for user, repository, language, and contribution data.
- [Analytics API](analytics.md) — Repository scoring, Shannon language diversity index, and technology inference.
- [Generators API](generators.md) — Presentation-independent model creation for profile, stats, tech stack, and timeline.
- [Renderers API](renderers.md) — Output rendering for Markdown README, theme-driven SVG cards, and JSON snapshots.
- [Animation API](animation.md) — SMIL SVG animation primitives, primitive registry, and composer.
- [Automation API](automation.md) — 8-stage workflow pipeline, artifact manager, retries, cancellation, and execution reports.
