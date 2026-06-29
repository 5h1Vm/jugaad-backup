import shutil

from pathlib import Path

from .artifact import BackupArtifact
from .base import StorageProvider
from .config import (
    USB_ENABLED,
    USB_LABEL,
    USB_BACKUP_PATH,
)
from .mount import find_mountpoint


class USBStorage(StorageProvider):

    name = "USB"

    def enabled(self) -> bool:

        return USB_ENABLED

    def _root(self) -> Path | None:

        mount = find_mountpoint(
            USB_LABEL
        )

        if mount is None:
            return None

        if USB_BACKUP_PATH:

            return mount / USB_BACKUP_PATH

        return mount / "HonestBackup"

    def healthcheck(self) -> bool:

        root = self._root()

        if root is None:
            return False

        root.mkdir(
            parents=True,
            exist_ok=True,
        )

        return root.exists()

    def upload(
        self,
        artifact: BackupArtifact,
    ) -> bool:

        root = self._root()

        if root is None:
            return False

        archives = root / "archives"
        hashes = root / "hashes"
        manifests = root / "manifests"

        archives.mkdir(
            parents=True,
            exist_ok=True,
        )

        hashes.mkdir(
            parents=True,
            exist_ok=True,
        )

        manifests.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._copy(
            artifact.archive,
            archives / artifact.archive.name,
        )

        self._copy(
            artifact.sha256,
            hashes / artifact.sha256.name,
        )

        if artifact.manifest is not None:

            self._copy(
                artifact.manifest,
                manifests / artifact.manifest.name,
            )

        return True

    def download(
        self,
        backup_name: str,
        destination: Path,
    ) -> bool:

        root = self._root()

        if root is None:
            return False

        source = (
            root
            / "archives"
            / f"{backup_name}.tar.zst.age"
        )

        if not source.exists():
            return False

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source,
            destination / source.name,
        )

        return True

    def delete(
        self,
        backup_name: str,
    ) -> bool:

        root = self._root()

        if root is None:
            return False

        removed = False

        for folder, ext in [

            ("archives", ".tar.zst.age"),

            ("hashes", ".sha256"),

            ("manifests", ".manifest.json"),

        ]:

            file = (
                root
                / folder
                / f"{backup_name}{ext}"
            )

            if file.exists():

                file.unlink()

                removed = True

        return removed

    def exists(
        self,
        backup_name: str,
    ) -> bool:

        root = self._root()

        if root is None:
            return False

        return (
            root
            / "archives"
            / f"{backup_name}.tar.zst.age"
        ).exists()

    def list_backups(self):

        root = self._root()

        if root is None:
            return []

        archives = root / "archives"

        if not archives.exists():
            return []

        return [

            file.name.replace(
                ".tar.zst.age",
                "",
            )

            for file in sorted(
                archives.glob("*.tar.zst.age")
            )

        ]

    def _copy(
        self,
        src: Path,
        dst: Path,
    ):

        if src.resolve() == dst.resolve():
            return

        shutil.copy2(
            src,
            dst,
        )