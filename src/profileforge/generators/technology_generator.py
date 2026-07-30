"""Technology Stack Presentation Generator.

Generates TechnologyStackModel grouped by technology categories.
"""

from profileforge.analytics import AnalyticsSnapshot
from profileforge.generators.models import TechnologyGroup, TechnologyStackModel


class TechnologyGenerator:
    """Generator for grouped technology stack presentation model."""

    def generate(self, analytics: AnalyticsSnapshot) -> TechnologyStackModel:
        """Generate TechnologyStackModel."""
        category_map: dict[str, list[str]] = {}
        all_techs: list[str] = []

        for tech in analytics.technology_analysis.technologies:
            all_techs.append(tech.name)
            cat_name = tech.category.capitalize()
            category_map.setdefault(cat_name, []).append(tech.name)

        groups: list[TechnologyGroup] = [
            TechnologyGroup(category_name=cat, technologies=sorted(techs))
            for cat, techs in sorted(category_map.items())
        ]

        return TechnologyStackModel(
            groups=groups,
            all_technologies=sorted(all_techs),
        )
