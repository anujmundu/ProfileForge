"""Technology Stack Inference Engine.

Infers technologies from languages, repository topics, and metadata using deterministic rules.
Governed by 08_ANALYTICS_SPECIFICATION.md.
"""

from profileforge.analytics.models import InferredTechnology, TechnologyAnalysis
from profileforge.collectors.models import CollectionSnapshot


class TechnologyAnalyzer:
    """Analyzer for technology stack inference."""

    # Deterministic technology mapping rules (topic/keyword -> Tech metadata)
    TECH_MAP: dict[str, tuple[str, str]] = {
        "python": ("Python", "language"),
        "typescript": ("TypeScript", "language"),
        "javascript": ("JavaScript", "language"),
        "docker": ("Docker", "devops"),
        "kubernetes": ("Kubernetes", "devops"),
        "react": ("React", "frontend"),
        "vue": ("Vue.js", "frontend"),
        "fastapi": ("FastAPI", "backend"),
        "django": ("Django", "backend"),
        "postresql": ("PostgreSQL", "database"),
        "postgres": ("PostgreSQL", "database"),
        "mongodb": ("MongoDB", "database"),
        "redis": ("Redis", "database"),
        "pydantic": ("Pydantic", "library"),
        "httpx": ("HTTPX", "library"),
        "pytest": ("Pytest", "testing"),
    }

    def analyze(self, snapshot: CollectionSnapshot) -> TechnologyAnalysis:
        """Infer technologies from languages and repository topics across snapshot."""
        tech_repos: dict[str, set[str]] = {}
        tech_category: dict[str, str] = {}

        # 1. Infer from languages
        for lang in snapshot.languages.language_bytes:
            lang_key = lang.lower()
            if lang_key in self.TECH_MAP:
                tech_name, cat = self.TECH_MAP[lang_key]
            else:
                tech_name, cat = lang, "language"

            tech_category[tech_name] = cat
            tech_repos.setdefault(tech_name, set())

        # 2. Infer from repository topics & primary languages
        for repo in snapshot.repositories.repositories:
            for topic in repo.topics:
                topic_key = topic.lower()
                if topic_key in self.TECH_MAP:
                    tech_name, cat = self.TECH_MAP[topic_key]
                    tech_category[tech_name] = cat
                    tech_repos.setdefault(tech_name, set()).add(repo.name)

            if repo.language:
                tech_repos.setdefault(repo.language, set()).add(repo.name)

        tech_list: list[InferredTechnology] = []
        for tech_name, source_set in sorted(tech_repos.items()):
            cat = tech_category.get(tech_name, "general")
            confidence = min(1.0, round(0.7 + (len(source_set) * 0.1), 2))
            tech_list.append(
                InferredTechnology(
                    name=tech_name,
                    category=cat,
                    confidence=confidence,
                    source_repos=sorted(source_set),
                )
            )

        categories = sorted({t.category for t in tech_list})
        return TechnologyAnalysis(technologies=tech_list, top_categories=categories)
