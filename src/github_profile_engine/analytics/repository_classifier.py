from __future__ import annotations

from github_profile_engine.models.repository import Repository


class RepositoryClassifier:
    """
    Simple rule-based repository classifier.

    This will later evolve into a richer classifier.
    """

    KEYWORDS = {
        "Artificial Intelligence": [
            "ai",
            "ml",
            "rag",
            "llm",
            "neural",
            "vision",
            "classification",
            "detection",
        ],
        "Web Development": [
            "react",
            "flask",
            "django",
            "website",
            "portfolio",
            "frontend",
            "backend",
        ],
        "Data Science": [
            "analysis",
            "prediction",
            "analytics",
            "pandas",
            "numpy",
        ],
    }

    @classmethod
    def classify(cls, repository: Repository) -> str:
        text = (f"{repository.name} {repository.description or ''}").lower()

        for category, keywords in cls.KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return category

        return "General"
