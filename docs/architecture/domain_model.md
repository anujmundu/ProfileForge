# Domain Model Architecture

ProfileForge uses immutable Pydantic `BaseModel` classes with `frozen=True` to guarantee data integrity across subsystem boundaries.

---

## Primary Domain Models

### 1. Collection Models (`profileforge.collectors.models`)
- `User`: GitHub user profile data.
- `Repository`: Metadata for a single GitHub repository.
- `RepositoryCollection`: List of repositories collected for a user.
- `LanguageCollection`: Byte counts per language across user repositories.
- `ContributionCollection`: User contribution activity history.
- `CollectionSnapshot`: Immutable composite container holding all collected GitHub data.

### 2. Analytics Models (`profileforge.analytics.models`)
- `RepositoryScore`: Composite quality score computed for a repository.
- `LanguageAnalysis`: Shannon diversity index and language percentage breakdown.
- `TechnologyInference`: Frameworks, build systems, and libraries inferred from repository topics and files.
- `AnalyticsSnapshot`: Immutable container holding calculated portfolio insights.

### 3. Presentation Models (`profileforge.generators.models`)
- `ProfileModel`: User identity and profile bio representation.
- `StatisticsModel`: Aggregate statistics (total stars, forks, repos, dominant language).
- `FeaturedProjectsModel`: Curated list of top scored repositories.
- `TechnologyStackModel`: Categorized skills and technology categories.
- `TimelineModel`: Milestone timeline of public activity.
- `PresentationModel`: Master presentation-independent model consumed by all renderers.

### 4. Automation Models (`profileforge.automation.models`)
- `ExecutionStage`: Telemetry for a single workflow execution stage.
- `ArtifactManifest`: File manifest with SHA-256 checksum and size.
- `WorkflowResult`: Summary of workflow execution across all 8 stages.
- `ExecutionReport`: Complete provenanced execution report with UUID, versioning, and timing.
