"""Engineering Skill Inference Engine.

Infers skills with explicit confidence levels, supporting repositories, and rationale.
No machine learning. Purely deterministic and explainable.
Governed by 08_ANALYTICS_SPECIFICATION.md.
"""

from profileforge.analytics.models import InferredSkill, SkillAnalysis, TechnologyAnalysis
from profileforge.collectors.models import CollectionSnapshot


class SkillAnalyzer:
    """Analyzer for inferring engineering skills from technologies and repositories."""

    def analyze(
        self, _snapshot: CollectionSnapshot, tech_analysis: TechnologyAnalysis
    ) -> SkillAnalysis:
        """Infer skills from technology analysis and repository metadata."""
        skills: list[InferredSkill] = []

        for tech in tech_analysis.technologies:
            conf = min(1.0, round(tech.confidence, 2))
            reason = f"Inferred from usage across {len(tech.source_repos)} repository(ies)."
            skills.append(
                InferredSkill(
                    name=f"{tech.name} Engineering",
                    category=tech.category,
                    confidence=conf,
                    supporting_repositories=tech.source_repos,
                    reason=reason,
                )
            )

        # Sort by confidence descending, then name ascending
        skills.sort(key=lambda s: (-s.confidence, s.name.lower()))
        primary = [s.name for s in skills[:5]]

        return SkillAnalysis(skills=skills, primary_skills=primary)
