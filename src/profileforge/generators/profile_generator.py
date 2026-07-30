"""Profile Presentation Generator.

Generates ProfileModel from AnalyticsSnapshot.
Exposes presentation-independent semantic data only.
"""

from profileforge.analytics import AnalyticsSnapshot
from profileforge.collectors import CollectionSnapshot
from profileforge.generators.models import ProfileModel


class ProfileGenerator:
    """Generator for user profile presentation model."""

    def generate(
        self, analytics: AnalyticsSnapshot, collection: CollectionSnapshot
    ) -> ProfileModel:
        """Generate ProfileModel."""
        u = collection.user
        headline = (
            f"{u.name} - Software Engineer"
            if u.name
            else f"{u.login} - Software Developer"
        )

        return ProfileModel(
            username=analytics.username,
            display_name=u.name or u.login,
            headline=headline,
            summary=u.bio or "Software Engineer & Open Source Contributor",
            location=u.location,
            company=u.company,
            avatar_url=u.avatar_url,
            profile_url=u.html_url,
        )
