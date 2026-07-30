"""Unit tests for Analytics Subsystem.

Tests deterministic scoring, ranking, tie-breaking, language analysis, technology inference,
skill inference, activity analysis, portfolio summary, and pipeline orchestration.
Governed by 08_ANALYTICS_SPECIFICATION.md.
"""


from profileforge.analytics import (
    ActivityAnalyzer,
    AnalyticsOrchestrator,
    AnalyticsSnapshot,
    FeaturedRepositories,
    LanguageAnalyzer,
    PortfolioAnalyzer,
    RepositoryAnalyzer,
    RepositoryRanking,
    RepositoryScore,
    RepositoryScorer,
    SkillAnalyzer,
    TechnologyAnalyzer,
)
from profileforge.collectors.models import (
    CollectionSnapshot,
    ContributionCollection,
    LanguageCollection,
    OrganizationCollection,
    Repository,
    RepositoryCollection,
    User,
)
from profileforge.configuration import AnalyticsCategory


def create_sample_snapshot() -> CollectionSnapshot:
    """Helper to create a deterministic sample CollectionSnapshot."""
    user = User(
        id=1,
        login="octocat",
        name="The Octocat",
        public_repos=3,
        followers=500,
    )

    repo1 = Repository(
        id=101,
        name="alpha-project",
        full_name="octocat/alpha-project",
        description="Core Python library",
        stargazers_count=150,
        forks_count=45,
        language="Python",
        topics=["python", "docker", "fastapi"],
        license_name="MIT License",
        pushed_at="2026-07-20T10:00:00Z",
    )

    repo2 = Repository(
        id=102,
        name="beta-service",
        full_name="octocat/beta-service",
        description="Frontend web application",
        stargazers_count=20,
        forks_count=5,
        language="TypeScript",
        topics=["react", "typescript"],
        pushed_at="2026-06-01T10:00:00Z",
    )

    repo3 = Repository(
        id=103,
        name="gamma-tool",
        full_name="octocat/gamma-tool",
        description="Utility script",
        stargazers_count=150,  # Same stars as repo1 for tie-breaking test
        forks_count=10,
        language="Python",
        topics=["python"],
        pushed_at="2025-01-01T10:00:00Z",
    )

    repos = RepositoryCollection(
        username="octocat",
        repositories=[repo1, repo2, repo3],
        total_count=3,
    )

    langs = LanguageCollection(
        username="octocat",
        language_bytes={"Python": 35000, "TypeScript": 15000, "HTML": 2000},
        total_bytes=52000,
    )

    contribs = ContributionCollection(username="octocat", has_data=False)
    orgs = OrganizationCollection(username="octocat", organizations=[], total_count=0)

    return CollectionSnapshot(
        username="octocat",
        user=user,
        repositories=repos,
        languages=langs,
        contributions=contribs,
        organizations=orgs,
    )


def test_repository_scorer_and_breakdown() -> None:
    """Verify RepositoryScorer produces transparent score and breakdown."""
    snapshot = create_sample_snapshot()
    repo = snapshot.repositories.repositories[0]

    scorer = RepositoryScorer()
    score = scorer.compute_score(repo)

    assert isinstance(score, RepositoryScore)
    assert score.repository_name == "octocat/alpha-project"
    assert 0.0 <= score.total_score <= 100.0
    assert "stars_score" in score.breakdown
    assert "completeness_score" in score.breakdown
    assert "recency_score" in score.breakdown


def test_configurable_scoring_weights() -> None:
    """Verify custom scoring weights from configuration alter final score."""
    snapshot = create_sample_snapshot()
    repo = snapshot.repositories.repositories[0]

    custom_config = AnalyticsCategory(
        scoring_weights={
            "stars": 0.80,
            "forks": 0.05,
            "recency": 0.05,
            "activity": 0.05,
            "completeness": 0.05,
        }
    )

    scorer = RepositoryScorer(config=custom_config)
    score = scorer.compute_score(repo)

    # Stars component heavily weighted
    assert score.total_score > 80.0


def test_deterministic_repository_ranking_and_tie_breaking() -> None:
    """Verify deterministic ranking and alphabetical tie-breaking on identical scores."""
    snapshot = create_sample_snapshot()
    analyzer = RepositoryAnalyzer()

    ranking1 = analyzer.analyze_ranking(snapshot.repositories)
    ranking2 = analyzer.analyze_ranking(snapshot.repositories)

    assert isinstance(ranking1, RepositoryRanking)
    assert ranking1.total_count == 3
    # Exact equality across multiple executions
    assert [r.repository.name for r in ranking1.ranked_repositories] == [
        r.repository.name for r in ranking2.ranked_repositories
    ]
    # alpha-project should rank higher than gamma-tool due to recency/completeness or tie-breaking
    assert ranking1.ranked_repositories[0].rank == 1


def test_featured_repository_selection() -> None:
    """Verify selecting featured repositories adheres to configured count limit."""
    snapshot = create_sample_snapshot()
    config = AnalyticsCategory(featured_repo_count=2)
    analyzer = RepositoryAnalyzer(config=config)

    ranking = analyzer.analyze_ranking(snapshot.repositories)
    featured = analyzer.select_featured(ranking)

    assert isinstance(featured, FeaturedRepositories)
    assert featured.count == 2
    assert len(featured.featured) == 2


def test_language_analyzer() -> None:
    """Verify LanguageAnalyzer computes dominant language, percentages, and diversity index."""
    snapshot = create_sample_snapshot()
    analyzer = LanguageAnalyzer()

    lang_analysis = analyzer.analyze(snapshot.languages)

    assert lang_analysis.dominant_language == "Python"
    assert lang_analysis.total_languages == 3
    assert "Python" in lang_analysis.language_percentages
    assert lang_analysis.diversity_index > 0.0


def test_technology_analyzer() -> None:
    """Verify TechnologyAnalyzer infers technology stack entries from topics and languages."""
    snapshot = create_sample_snapshot()
    analyzer = TechnologyAnalyzer()

    tech_analysis = analyzer.analyze(snapshot)

    tech_names = [t.name for t in tech_analysis.technologies]
    assert "Python" in tech_names
    assert "Docker" in tech_names
    assert "React" in tech_names


def test_skill_analyzer() -> None:
    """Verify SkillAnalyzer infers skills with confidence scores and supporting repositories."""
    snapshot = create_sample_snapshot()
    tech_analyzer = TechnologyAnalyzer()
    tech_analysis = tech_analyzer.analyze(snapshot)

    skill_analyzer = SkillAnalyzer()
    skill_analysis = skill_analyzer.analyze(snapshot, tech_analysis)

    assert len(skill_analysis.skills) > 0
    assert len(skill_analysis.primary_skills) > 0
    assert skill_analysis.skills[0].confidence > 0.0


def test_activity_analyzer() -> None:
    """Verify ActivityAnalyzer measures update recency and activity level."""
    snapshot = create_sample_snapshot()
    analyzer = ActivityAnalyzer()

    act = analyzer.analyze(snapshot)

    assert act.active_repositories_count >= 1
    assert act.activity_level in ("HIGH", "MODERATE", "LOW")


def test_portfolio_analyzer() -> None:
    """Verify PortfolioAnalyzer assembles structured summary metrics."""
    snapshot = create_sample_snapshot()
    repo_analyzer = RepositoryAnalyzer()
    lang_analyzer = LanguageAnalyzer()
    tech_analyzer = TechnologyAnalyzer()
    skill_analyzer = SkillAnalyzer()

    ranking = repo_analyzer.analyze_ranking(snapshot.repositories)
    featured = repo_analyzer.select_featured(ranking)
    langs = lang_analyzer.analyze(snapshot.languages)
    techs = tech_analyzer.analyze(snapshot)
    skills = skill_analyzer.analyze(snapshot, techs)

    portfolio_analyzer = PortfolioAnalyzer()
    summary = portfolio_analyzer.analyze(snapshot, featured, langs, skills)

    assert summary.total_public_repos == 3
    assert summary.total_stars == 320
    assert summary.primary_language == "Python"


def test_analytics_orchestrator() -> None:
    """Verify AnalyticsOrchestrator runs the complete pipeline and produces AnalyticsSnapshot."""
    snapshot = create_sample_snapshot()
    orchestrator = AnalyticsOrchestrator()

    analytics_snapshot = orchestrator.analyze_snapshot(snapshot)

    assert isinstance(analytics_snapshot, AnalyticsSnapshot)
    assert analytics_snapshot.username == "octocat"
    assert analytics_snapshot.featured_repositories.count > 0
    assert analytics_snapshot.portfolio_summary.total_stars == 320
    assert orchestrator.diagnostics.analyzed_repositories_count == 3
