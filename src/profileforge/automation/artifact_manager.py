"""Artifact Manager Implementation.

Manages output directory preparation, file manifest generation, SHA-256 checksums, and overwrite policies.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md.
"""

import hashlib
from pathlib import Path

from profileforge.automation.models import ArtifactManifest
from profileforge.renderers import RenderedArtifacts


class ArtifactManager:
    """Centralized manager for stored output artifacts."""

    def __init__(self, output_dir: str = "./dist", overwrite: bool = True) -> None:
        self.output_dir = Path(output_dir)
        self.overwrite = overwrite

    def prepare_directory(self) -> Path:
        """Ensure output directory exists."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        return self.output_dir

    def store_artifacts(
        self, rendered_artifacts: RenderedArtifacts
    ) -> list[ArtifactManifest]:
        """Store rendered artifacts to filesystem and return manifests."""
        target_dir = self.prepare_directory()
        manifests: list[ArtifactManifest] = []

        # 1. Store Markdown README
        if rendered_artifacts.markdown_artifact:
            art = rendered_artifacts.markdown_artifact
            file_path = target_dir / art.output_filename
            manifests.append(
                self._write_file(
                    file_path, art.content, artifact_type="markdown"
                )
            )

        # 2. Store SVG visual cards
        for svg in rendered_artifacts.svg_artifacts:
            file_path = target_dir / svg.output_filename
            manifests.append(
                self._write_file(
                    file_path, svg.svg_content, artifact_type="svg"
                )
            )

        # 3. Store JSON presentation snapshot
        if rendered_artifacts.json_artifact:
            j_art = rendered_artifacts.json_artifact
            file_path = target_dir / j_art.output_filename
            manifests.append(
                self._write_file(
                    file_path, j_art.json_content, artifact_type="json"
                )
            )

        return manifests

    def _write_file(
        self, file_path: Path, content: str, artifact_type: str
    ) -> ArtifactManifest:
        """Write content to file and calculate SHA-256 manifest."""
        if file_path.exists() and not self.overwrite:
            content_bytes = file_path.read_bytes()
        else:
            content_bytes = content.encode("utf-8")
            file_path.write_bytes(content_bytes)

        checksum = hashlib.sha256(content_bytes).hexdigest()
        size_bytes = len(content_bytes)

        return ArtifactManifest(
            output_path=str(file_path.resolve()),
            filename=file_path.name,
            size_bytes=size_bytes,
            checksum_sha256=checksum,
            artifact_type=artifact_type,
        )
