# Engine Subsystem API (`profileforge.engine`)

The Engine subsystem manages application lifecycle state transitions, dependency injection, and health checks.

---

## Primary Classes

### `Engine`
Master engine orchestrator managing the 9-stage lifecycle.

```python
class Engine:
    def bootstrap(self) -> EngineContext: ...
    def shutdown(self) -> None: ...
```

### `LifecycleManager`
Manages application state machine (`BOOTSTRAPPING`, `READY`, `RUNNING`, `SHUTTING_DOWN`).

```python
class LifecycleManager:
    @property
    def current_phase(self) -> LifecyclePhase: ...
    def transition_to(self, target_phase: LifecyclePhase) -> None: ...
```

### `DependencyRegistry`
In-memory service registry for dependency injection.

```python
class DependencyRegistry:
    def register(self, service_type: type, instance: Any) -> None: ...
    def resolve(self, service_type: type[T]) -> T: ...
```
