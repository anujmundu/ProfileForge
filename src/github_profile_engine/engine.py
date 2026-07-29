from __future__ import annotations

from pathlib import Path

from github_profile_engine.collectors.profile_collector import ProfileCollector
from github_profile_engine.generators.context_builder import ContextBuilder
from github_profile_engine.generators.generation_pipeline import GenerationPipeline
from github_profile_engine.models.generated_file import GeneratedFile
from github_profile_engine.models.profile import Profile
from github_profile_engine.models.profile_context import ProfileContext
from github_profile_engine.renderers.markdown_renderer import MarkdownRenderer
from github_profile_engine.services.configuration import ConfigurationLoader
from github_profile_engine.services.environment import get_github_token
from github_profile_engine.services.file_writer import FileWriter
from github_profile_engine.services.github_client import GitHubClient


class ProfileEngine:
    """
    Coordinates the complete GitHub Profile Engine pipeline.

    Pipeline:
        Configuration
            ↓
        GitHub API
            ↓
        Collectors
            ↓
        Domain Models
            ↓
        Context Builder
            ↓
        Renderers
            ↓
        Generated Files
            ↓
        File Writer
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root

        self.config = ConfigurationLoader(project_root / "config").load_profile()

        self.github = GitHubClient(get_github_token())

        # Engine state
        self.profile: Profile | None = None
        self.context: ProfileContext | None = None
        self.generated_files: list[GeneratedFile] = []

    def collect(self) -> None:
        """
        Collect profile information from GitHub.
        """

        github_user = self.github.get_user(self.config.profile.github_username)

        self.profile = ProfileCollector.collect(github_user)

    def build_context(self) -> None:
        """
        Build the rendering context from the collected profile.
        """

        assert self.profile is not None

        self.context = ContextBuilder.build(self.profile)

    def generate(self) -> None:
        """
        Generate all output artifacts.
        """

        assert self.context is not None

        markdown_renderer = MarkdownRenderer(
            self.project_root / "templates" / "markdown"
        )

        pipeline = GenerationPipeline(
            renderers=[
                markdown_renderer,
            ]
        )

        self.generated_files = pipeline.generate(self.context)

    def run(self) -> None:
        """
        Execute the complete profile generation pipeline.
        """

        # ------------------------------------------------------------
        # Collect Data
        # ------------------------------------------------------------

        self.collect()

        # ------------------------------------------------------------
        # Build Rendering Context
        # ------------------------------------------------------------

        self.build_context()

        # ------------------------------------------------------------
        # Generate Output Artifacts
        # ------------------------------------------------------------

        self.generate()

        # ------------------------------------------------------------
        # Write Files
        # ------------------------------------------------------------

        for generated_file in self.generated_files:
            FileWriter.write(generated_file)

        # ------------------------------------------------------------
        # Console Summary
        # ------------------------------------------------------------

        assert self.context is not None

        print("=" * 72)
        print(self.context.profile.user.name)
        print("=" * 72)

        print(f"Followers     : {self.context.profile.user.followers}")
        print(f"Following     : {self.context.profile.user.following}")
        print(f"Repositories  : {self.context.profile.statistics.total_repositories}")
        print(f"Stars         : {self.context.profile.statistics.total_stars}")
        print(f"Forks         : {self.context.profile.statistics.total_forks}")

        print()

        print("=" * 72)
        print("Top Repositories")
        print("=" * 72)

        for repository in self.context.featured_repositories:
            print(f"{repository.name:<40}{repository.score:>6.2f}")

        print()

        print("Repositories")
        print("-" * 72)

        for repository in self.context.profile.repositories:
            print(f"{repository.name:<35}⭐ {repository.stars:<3}{repository.language}")

        print()

        print("=" * 72)
        print("Language Distribution")
        print("=" * 72)

        for language in self.context.languages:
            print(
                f"{language.name:<20}"
                f"{language.repositories:>3} repositories   "
                f"{language.percentage:>6.2f}%"
            )

        print()

        print("=" * 72)
        print("Generated Files")
        print("=" * 72)

        for generated_file in self.generated_files:
            print(f"✓ {generated_file.path}")

        print()

        self.github.close()
