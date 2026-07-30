"""Analytics Subsystem.

Transforms canonical collection data into deterministic engineering insights.
Governed by 08_ANALYTICS_SPECIFICATION.md.
"""

from profileforge.analytics.activity_analyzer import ActivityAnalyzer
from profileforge.analytics.diagnostics import AnalyticsDiagnostics
from profileforge.analytics.exceptions import (
    ActivityAnalysisError,
    AnalyticsError,
    LanguageAnalysisError,
    RepositoryAnalysisError,
    SkillInferenceError,
    TechnologyInferenceError,
)
from profileforge.analytics.language_analyzer import LanguageAnalyzer
from profileforge.analytics.models import (
    ActivityAnalysis,
    AnalyticsSnapshot,
    FeaturedRepositories,
    InferredSkill,
    InferredTechnology,
    LanguageAnalysis,
    PortfolioSummary,
    RankedRepository,
    RepositoryRanking,
    RepositoryScore,
    SkillAnalysis,
    TechnologyAnalysis,
)
from profileforge.analytics.orchestrator import AnalyticsOrchestrator
from profileforge.analytics.portfolio_analyzer import PortfolioAnalyzer
from profileforge.analytics.repository_analyzer import RepositoryAnalyzer
from profileforge.analytics.scoring import RepositoryScorer
from profileforge.analytics.skill_analyzer import SkillAnalyzer
from profileforge.analytics.technology_analyzer import TechnologyAnalyzer

__all__ = [
    "ActivityAnalysis",
    "ActivityAnalysisError",
    "ActivityAnalyzer",
    "AnalyticsDiagnostics",
    "AnalyticsError",
    "AnalyticsOrchestrator",
    "AnalyticsSnapshot",
    "FeaturedRepositories",
    "InferredSkill",
    "InferredTechnology",
    "LanguageAnalysis",
    "LanguageAnalysisError",
    "LanguageAnalyzer",
    "PortfolioSummary",
    "PortfolioAnalyzer",
    "RankedRepository",
    "RepositoryAnalysisError",
    "RepositoryAnalyzer",
    "RepositoryRanking",
    "RepositoryScore",
    "RepositoryScorer",
    "SkillAnalysis",
    "SkillInferenceError",
    "SkillAnalyzer",
    "TechnologyAnalysis",
    "TechnologyInferenceError",
    "TechnologyAnalyzer",
]
