# Renderers Subsystem API (`profileforge.renderers`)

The Renderers subsystem transforms `PresentationModel` objects into concrete output artifacts.

---

## Primary Classes

### `RendererOrchestrator`
Master renderer coordinator rendering Markdown, theme-driven SVG cards, and JSON snapshots.

```python
class RendererOrchestrator:
    def render_presentation_model(
        self, model: PresentationModel
    ) -> RenderedArtifacts: ...
```

### `MarkdownRenderer`
Renders GitHub profile README.md markdown content.

```python
class MarkdownRenderer:
    def render(self, model: PresentationModel) -> MarkdownArtifact: ...
```

### `SVGRenderer`
Renders theme-styled visual SVG stats and tech stack cards.

```python
class SVGRenderer:
    def render(self, model: PresentationModel) -> list[SVGArtifact]: ...
```

### `JSONRenderer`
Renders JSON snapshot of the presentation model.

```python
class JSONRenderer:
    def render(self, model: PresentationModel) -> JSONArtifact: ...
```
