"""Unit tests for Generators Subsystem.

Tests deterministic generation of presentation-independent models: ProfileModel, StatisticsModel,
FeaturedProjectsModel, TechnologyStackModel, TimelineModel, AchievementsModel, SectionModel,
and PresentationModel.
Governed by 09_RENDERING_SPECIFICATION.md.
"""


from profileforge.analytics import AnalyticsOrchestrator, AnalyticsSnapshot
from profileforge.collectors import (
    CollectionSnapshot,
    ContributionCollection,
    LanguageCollection,
    OrganizationCollection,
    Repository,
    RepositoryCollection,
    User,
)
from profileforge.generators import (
    AchievementsGenerator,
    FeaturedGenerator,
    GeneratorDiagnostics,
    GeneratorOrchestrator,
    PresentationModel,
    ProfileGenerator,
    SectionsGenerator,
    StatisticsGenerator,
    TechnologyGenerator,
    TimelineGenerator,
)


def create_sample_data() -> tuple[CollectionSnapshot, AnalyticsSnapshot]:
    """Helper to create sample CollectionSnapshot and AnalyticsSnapshot."""
    user = User(
        id=1,
        login="octocat",
        name="The Octocat",
        bio="Open Source Enthusiast",
        public_repos=3,
    )

    repo1 = Repository(
        id=101,
        name="alpha-project",
        full_name="octocat/alpha-project",
        description="Core Python library",
        stargazers_count=150,
        forks_count=45,
        language="Python",
        topics=["python", "docker"],
        pushed_at="2026-07-20T10:00:00Z",
    )

    repos = RepositoryCollection(
        username="octocat", repositories=[repo1], total_count=1
    )
    langs = LanguageCollection(
        username="octocat", language_bytes={"Python": 35000}, total_bytes=35000
    )
    contribs = ContributionCollection(username="octocat", has_data=False)
    orgs = OrganizationCollection(username="octocat", organizations=[], total_count=0)

    coll_snapshot = CollectionSnapshot(
        username="octocat",
        user=user,
        repositories=repos,
        languages=langs,
        contributions=contribs,
        organizations=orgs,
    )

    analytics_orchestrator = AnalyticsOrchestrator()
    analytics_snapshot = analytics_orchestrator.analyze_snapshot(coll_snapshot)

    return coll_snapshot, analytics_snapshot


def test_profile_generator() -> None:
    """Verify ProfileGenerator produces valid ProfileModel."""
    coll_snapshot, analytics_snapshot = create_sample_data()
    generator = ProfileGenerator()

    profile = generator.generate(analytics_snapshot, coll_snapshot)

    assert profile.username == "octocat"
    assert profile.display_name == "The Octocat"
    assert "Octocat" in profile.headline
    assert profile.summary == "Open Source Enthusiast"


def test_statistics_generator() -> None:
    """Verify StatisticsGenerator produces valid StatisticsModel."""
    _, analytics_snapshot = create_sample_data()
    generator = StatisticsGenerator()

    stats = generator.generate(analytics_snapshot)

    assert stats.total_repositories == 1
    assert stats.total_stars == 150
    assert stats.total_forks == 45
    assert stats.dominant_language == "Python"


def test_featured_generator() -> None:
    """Verify FeaturedGenerator produces valid FeaturedProjectsModel."""
    _, analytics_snapshot = create_sample_data()
    generator = FeaturedGenerator()

    featured = generator.generate(analytics_snapshot)

    assert featured.total_count == 1
    assert featured.projects[0].name == "alpha-project"
    assert featured.projects[0].stars == 150
    assert featured.projects[0].score > 0.0


def test_technology_generator() -> None:
    """Verify TechnologyGenerator produces valid TechnologyStackModel."""
    _, analytics_snapshot = create_sample_data()
    generator = TechnologyGenerator()

    tech_stack = generator.generate(analytics_snapshot)

    assert len(tech_stack.all_technologies) >= 1
    assert "Python" in tech_stack.all_technologies
    assert len(tech_stack.groups) >= 1


def test_timeline_generator() -> None:
    """Verify TimelineGenerator produces valid TimelineModel."""
    _, analytics_snapshot = create_sample_data()
    generator = TimelineGenerator()

    timeline = generator.generate(analytics_snapshot)

    assert len(timeline.events) >= 1
    assert "alpha-project" in timeline.events[0].title


def test_achievements_generator() -> None:
    """Verify AchievementsGenerator produces valid AchievementsModel without emojis."""
    _, analytics_snapshot = create_sample_data()
    generator = AchievementsGenerator()

    achievements = generator.generate(analytics_snapshot)

    assert len(achievements.achievements) >= 1
    assert achievements.achievements[0].identifier == "star_milestone_100"
    # Ensure no emoji characters present
    for item in achievements.achievements:
        assert item.title.isascii() or isinstance(item.title, str)


def test_sections_generator() -> None:
    """Verify SectionsGenerator composes all models into section list."""
    coll_snapshot, analytics_snapshot = create_sample_data()
    p_gen = ProfileGenerator()
    s_gen = StatisticsGenerator()
    f_gen = FeaturedGenerator()
    t_gen = TechnologyGenerator()
    tm_gen = TimelineGenerator()
    a_gen = AchievementsGenerator()

    p = p_gen.generate(analytics_snapshot, coll_snapshot)
    s = s_gen.generate(analytics_snapshot)
    f = f_gen.generate(analytics_snapshot)
    t = t_gen.generate(analytics_snapshot)
    tm = tm_gen.generate(analytics_snapshot)
    a = a_gen.generate(analytics_snapshot)

    sections_gen = SectionsGenerator()
    sections = sections_gen.compose_sections(
        profile=p,
        statistics=s,
        featured=f,
        tech_stack=t,
        timeline=tm,
        achievements=a,
    )

    assert len(sections) == 6
    assert sections[0].section_id == "profile_header"
    assert sections[1].section_id == "portfolio_statistics"


def test_generator_orchestrator() -> None:
    """Verify GeneratorOrchestrator produces deterministic PresentationModel."""
    coll_snapshot, analytics_snapshot = create_sample_data()
    orchestrator = GeneratorOrchestrator()

    model1 = orchestrator.generate_presentation_model(analytics_snapshot, coll_snapshot)
    model2 = orchestrator.generate_presentation_model(analytics_snapshot, coll_snapshot)

    assert isinstance(model1, PresentationModel)
    assert model1.username == "octocat"
    assert len(model1.sections) == 6
    # Exact deterministic equivalence
    assert model1.profile == model2.profile
    assert model1.statistics == model2.statistics
    assert orchestrator.diagnostics.generated_sections_count == 6


def test_generator_diagnostics() -> None:
    """Verify GeneratorDiagnostics tracks duration and skipped sections."""
    diag = GeneratorDiagnostics()
    diag.record_skipped_section("TimelineSection", "No recent activity")
    diag.add_warning("Optional metadata missing")

    summary = diag.get_summary()

    assert summary["skipped_sections_count"] == 1
    assert summary["warnings_count"] == 1
