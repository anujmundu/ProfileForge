# Collectors Subsystem API (`profileforge.collectors`)

The Collectors subsystem retrieves raw GitHub data and builds canonical domain models.

---

## Primary Classes

### `CollectorOrchestrator`
Master coordinator assembling the canonical `CollectionSnapshot`.

```python
class CollectorOrchestrator:
    def __init__(self, client: GitHubClient | None = None) -> None: ...
    def collect_user_snapshot(self, username: str) -> CollectionSnapshot: ...
```

### `CollectionSnapshot`
Immutable composite container holding user profile, repository list, language stats, and contributions.

```python
class CollectionSnapshot(BaseModel):
    username: str
    user: User
    repositories: RepositoryCollection
    languages: LanguageCollection
    contributions: ContributionCollection
```
