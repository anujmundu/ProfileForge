from __future__ import annotations

from github_profile_engine.analytics.language_analyzer import LanguageAnalyzer
from github_profile_engine.analytics.repository_ranker import RepositoryRanker
from github_profile_engine.models.profile import Profile
from github_profile_engine.models.profile_context import ProfileContext


class ContextBuilder:
    """
    Converts the Profile domain model into
    a renderer-friendly ProfileContext.
    """

    @staticmethod
    def build(profile: Profile) -> ProfileContext:
        ranked = RepositoryRanker.rank(profile.repositories)

        featured = ranked[:6]

        languages = LanguageAnalyzer.analyze(profile.repositories)

        return ProfileContext(
            profile=profile,
            featured_repositories=featured,
            languages=languages,
        )
