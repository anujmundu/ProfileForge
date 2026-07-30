"""Publisher Abstraction and Local FileSystem Publisher.

Defines BasePublisher contract and LocalFileSystemPublisher implementation.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

from abc import ABC, abstractmethod

from profileforge.automation.artifact_manager import ArtifactManager
from profileforge.automation.exceptions import PublishingError
from profileforge.automation.models import PublishResult
from profileforge.renderers import RenderedArtifacts


class BasePublisher(ABC):
    """Abstract contract enforced across all publisher implementations."""

    @abstractmethod
    def publish(
        self, rendered_artifacts: RenderedArtifacts, output_dir: str
    ) -> PublishResult:
        """Publish rendered artifacts to target destination."""
        raise NotImplementedError


class LocalFileSystemPublisher(BasePublisher):
    """Concrete publisher writing rendered artifacts to local filesystem."""

    def publish(
        self, rendered_artifacts: RenderedArtifacts, output_dir: str
    ) -> PublishResult:
        """Publish rendered artifacts to local output directory."""
        try:
            manager = ArtifactManager(output_dir=output_dir, overwrite=True)
            manifests = manager.store_artifacts(rendered_artifacts)

            return PublishResult(
                success=True,
                published_path=str(manager.output_dir.resolve()),
                artifacts_published_count=len(manifests),
                publisher_name="local_filesystem",
            )
        except Exception as exc:
            raise PublishingError(
                f"Failed to publish artifacts to '{output_dir}': {exc}"
            ) from exc
