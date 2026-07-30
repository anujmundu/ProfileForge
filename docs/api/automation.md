# Automation Subsystem API (`profileforge.automation`)

The Automation subsystem coordinates the end-to-end ProfileForge execution pipeline.

---

## Key Classes

### `AutomationOrchestrator`
Master entrypoint for executing automated workflow runs.

```python
class AutomationOrchestrator:
    def __init__(
        self,
        config: AutomationConfiguration | None = None,
        github_client: GitHubClient | None = None,
    ) -> None: ...

    def execute_workflow(
        self, username: str, cancel_token: CancellationToken | None = None
    ) -> ExecutionReport: ...
```

### `Workflow`
8-stage deterministic execution pipeline.

```python
class Workflow:
    def run(
        self, username: str, cancel_token: CancellationToken | None = None
    ) -> WorkflowResult: ...
```

### `ArtifactManager`
Directory preparation, overwrite enforcement, and SHA-256 artifact manifest generation.

```python
class ArtifactManager:
    def store_artifacts(
        self, artifacts: RenderedArtifacts
    ) -> list[ArtifactManifest]: ...
```

### `CancellationToken`
Cooperative cancellation token supporting registered cleanup callbacks.

```python
class CancellationToken:
    def cancel(self) -> None: ...
    def throw_if_cancelled(self) -> None: ...
```
