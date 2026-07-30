# Analytics Subsystem API (`profileforge.analytics`)

The Analytics subsystem transforms raw collection snapshots into deterministic engineering insights.

---

## Primary Classes

### `AnalyticsOrchestrator`
Master analytics coordinator producing `AnalyticsSnapshot`.

```python
class AnalyticsOrchestrator:
    def analyze_snapshot(self, snapshot: CollectionSnapshot) -> AnalyticsSnapshot: ...
```

### `RepositoryScorer`
Calculates mathematical quality scores for repositories based on stars, forks, and recency.

```python
class RepositoryScorer:
    def calculate_score(self, repo: Repository) -> RepositoryScore: ...
```

### `LanguageAnalyzer`
Computes Shannon language diversity index and byte percentage distribution.

```python
class LanguageAnalyzer:
    def analyze(self, languages: LanguageCollection) -> LanguageAnalysis: ...
```
