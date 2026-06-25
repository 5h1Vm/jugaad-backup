from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class BackupArtifact:
    """
    Represents one complete backup artifact produced by the
    archive pipeline.
    """

    day: str

    archive: Path

    sha256: Path

    manifest: Path | None = None

    report: Path | None = None

    size: int = 0

    @property
    def archive_name(self) -> str:

        return self.archive.name

    @property
    def checksum_name(self) -> str:

        return self.sha256.name

    @property
    def manifest_name(self) -> str | None:

        if self.manifest is None:
            return None

        return self.manifest.name
