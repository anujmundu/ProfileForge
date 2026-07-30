# Observability & Diagnostics Guide

ProfileForge provides deep subsystem diagnostics telemetry across all execution stages.

---

## 1. Subsystem Telemetry Trackers

Each subsystem maintains a diagnostics object:
- **`ConfigurationDiagnostics`**: Config file loading & env override counts.
- **`EngineDiagnostics`**: Lifecycle state transition durations & phase timing.
- **`GitHubDiagnostics`**: Total HTTP requests, cache hits/misses, and rate limit status.
- **`CollectorDiagnostics`**: User, repository, and language collection counts.
- **`AnalyticsDiagnostics`**: Analytical scoring calculation time.
- **`GeneratorDiagnostics`**: Presentation model generation time.
- **`RendererDiagnostics`**: Artifact rendering count & durations.
- **`AnimationDiagnostics`**: SMIL animation primitives generated.
- **`AutomationDiagnostics`**: Total pipeline execution time and stage durations.

---

## 2. Accessing Diagnostics Telemetry

```python
from profileforge.automation import AutomationOrchestrator

orchestrator = AutomationOrchestrator()
report = orchestrator.execute_workflow("octocat")

# Get diagnostics summary dictionary
summary = orchestrator.diagnostics.get_summary()
print(summary)
```

Example Telemetry Output:
```json
{
  "total_execution_duration_ms": 142.5,
  "published_artifacts_count": 4,
  "stage_durations_ms": {
    "Load Configuration": 1.2,
    "Initialize Engine": 0.8,
    "Collect GitHub Data": 85.0,
    "Run Analytics": 5.4,
    "Generate Presentation Models": 4.1,
    "Render Artifacts": 15.2,
    "Store Artifacts": 12.0,
    "Publish Artifacts": 18.8
  }
}
```
