# Subsystem Interactions & Contract Boundaries

ProfileForge enforces strict architectural boundaries across all 9 subsystems.

---

## Allowed vs Prohibited Interactions

| Source Subsystem | Allowed Downstream Target | Prohibited Target | Rationale |
| :--- | :--- | :--- | :--- |
| **Configuration** | `Engine`, `GitHub` | `Collectors`, `Analytics`, `Renderers` | Configuration provides settings to low-level client & engine; higher subsystems receive config via context. |
| **Engine** | `GitHub`, `Collectors` | `Renderers`, `Automation` | Engine handles lifecycle and dependencies; it does not perform rendering or output generation. |
| **GitHub** | `Collectors` | `Analytics`, `Generators`, `Renderers` | REST API communication is strictly isolated within the GitHub subsystem. |
| **Collectors** | `Analytics` | `Renderers`, `Automation` | Collectors assemble raw data snapshots without scoring or rendering. |
| **Analytics** | `Generators` | `Renderers`, `GitHub` | Analytics computes mathematical scores without presentation formatting. |
| **Generators** | `Renderers` | `Automation` | Generators build presentation-independent models without Markdown/HTML formatting. |
| **Renderers** | `Animation`, `Automation` | `GitHub`, `Analytics` | Renderers transform presentation models into output formats without business logic. |
| **Automation** | All Subsystems (Orchestration) | None | Automation coordinates stage execution without introducing domain logic. |
