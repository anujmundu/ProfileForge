# Execution Pipeline Specification

The ProfileForge automation pipeline executes in 8 sequential, deterministic stages managed by `Workflow`.

---

## 8-Stage Execution Workflow

```text
Stage 1: Load Configuration
   ├── ConfigurationManager loads profileforge.yaml & environment variables
   └── Returns validated AppConfig

Stage 2: Initialize Engine
   ├── Engine bootstraps dependency registry and lifecycle manager
   └── Transitions state to READY

Stage 3: Collect GitHub Data
   ├── CollectorOrchestrator queries GitHub API via GitHubClient
   └── Assembles immutable CollectionSnapshot

Stage 4: Run Analytics
   ├── AnalyticsOrchestrator calculates repository scores & Shannon entropy
   └── Returns immutable AnalyticsSnapshot

Stage 5: Generate Presentation Models
   ├── GeneratorOrchestrator builds semantic PresentationModel
   └── Produces pure data objects for Profile, Stats, Tech Stack, & Timeline

Stage 6: Render Artifacts
   ├── RendererOrchestrator renders Markdown, SVG Cards, & JSON Snapshots
   └── Returns RenderedArtifacts collection

Stage 7: Store Artifacts
   ├── ArtifactManager writes output files to target directory
   └── Calculates SHA-256 checksums for ArtifactManifest

Stage 8: Publish Artifacts
   ├── LocalFileSystemPublisher publishes dist output files
   └── Generates ExecutionReport telemetry
```

---

## Stage Telemetry Contract (`ExecutionStage`)

Every stage records uniform execution telemetry:
- `stage_name`: Descriptive name of stage.
- `status`: Stage status (`PENDING`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`).
- `started_at`: UTC ISO timestamp when stage started.
- `completed_at`: UTC ISO timestamp when stage completed.
- `duration_ms`: Duration in milliseconds.
- `diagnostics`: Extensible telemetry dictionary.
