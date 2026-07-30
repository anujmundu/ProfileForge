# Generators Subsystem API (`profileforge.generators`)

The Generators subsystem builds presentation-independent content models.

---

## Primary Classes

### `GeneratorOrchestrator`
Master generator coordinator producing `PresentationModel`.

```python
class GeneratorOrchestrator:
    def generate_presentation_model(
        self, analytics: AnalyticsSnapshot, snapshot: CollectionSnapshot
    ) -> PresentationModel: ...
```

### `PresentationModel`
Immutable presentation-independent content model consumed by Renderers.

```python
class PresentationModel(BaseModel):
    username: str
    profile: ProfileModel
    statistics: StatisticsModel
    featured_projects: FeaturedProjectsModel
    technology_stack: TechnologyStackModel
    timeline: TimelineModel
```
