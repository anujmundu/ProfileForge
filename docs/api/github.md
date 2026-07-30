# GitHub Integration Subsystem API (`profileforge.github`)

The GitHub Integration subsystem handles all REST API communication with GitHub.

---

## Primary Classes

### `GitHubClient`
Low-level HTTP client with rate-limiting awareness, link header pagination, and response caching.

```python
class GitHubClient:
    def __init__(self, config: GitHubConfig | None = None) -> None: ...
    def get_user_profile(self, username: str) -> GitHubUserModel: ...
    def get_user_repositories(self, username: str) -> list[GitHubRepositoryModel]: ...
    def get_repository_languages(self, owner: str, repo: str) -> GitHubLanguageStatsModel: ...
```

### `ResponseCache`
In-memory TTL cache for HTTP responses.

```python
class ResponseCache:
    def get(self, key: str) -> Any | None: ...
    def set(self, key: str, value: Any, ttl_seconds: float) -> None: ...
```
