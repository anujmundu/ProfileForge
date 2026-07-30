# SVG Animation Engine API (`profileforge.animation`)

The Animation Engine provides reusable SMIL animation primitives for SVG artifacts.

---

## Primary Classes

### `AnimationOrchestrator`
Master animation coordinator building SMIL animation definitions.

```python
class AnimationOrchestrator:
    def create_card_entrance_animation(
        self, target_id: str
    ) -> AnimationDefinition: ...
```

### `AnimationRegistry`
Central registry storing available SMIL primitive factories (`Fade`, `Pulse`, `Slide`, `Shimmer`, `Progress`).

```python
class AnimationRegistry:
    def register(self, name: str, primitive: SMILPrimitive) -> None: ...
    def get(self, name: str) -> SMILPrimitive: ...
```

### `AnimationComposer`
Composes multiple animation primitives into a single valid SMIL SVG definition.

```python
class AnimationComposer:
    def compose(
        self, primitives: list[SMILPrimitive], target_id: str
    ) -> AnimationDefinition: ...
```
