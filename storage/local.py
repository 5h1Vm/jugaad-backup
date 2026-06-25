import shutil
from pathlib import Path

from .base import StorageProvider
from .config import load_config
from .utils import sha256


class LocalStorage(StorageProvider):

    @property
    def name(self):

        return "Local"

    def enabled(self):

        cfg = load_config()

        return (
            cfg.get("LOCAL_ENABLED", "false").lower()
            == "true"
        )

    @property
    def root(self):

        cfg = load_config()

        return Path(
            cfg["LOCAL_PATH"]
        )

    def healthcheck(self):

        try:

            self.root.mkdir(
                parents=True,
                exist_ok=True
            )

            return True

        except Exception:

            return False

    def upload(
        self,
        archive,
        manifest,
    ):

        self.root.mkdir(
            parents=True,
            exist_ok=True
        )

        archive_dst = (
            self.root
            / "archives"
        )

        manifest_dst = (
            self.root
            / "manifests"
        )

        archive_dst.mkdir(
            exist_ok=True
        )

        manifest_dst.mkdir(
            exist_ok=True
        )

        archive_copy = (
            archive_dst
            / archive.name
        )

        manifest_copy = (
            manifest_dst
            / manifest.name
        )

        shutil.copy2(
            archive,
            archive_copy
        )

        shutil.copy2(
            manifest,
            manifest_copy
        )

        if (
            sha256(archive)
            != sha256(archive_copy)
        ):
            raise RuntimeError(
                "Archive verification failed"
            )

        if (
            sha256(manifest)
            != sha256(manifest_copy)
        ):
            raise RuntimeError(
                "Manifest verification failed"
            )

        return True

    def download(
        self,
        backup_name,
        destination,
    ):

        raise NotImplementedError

    def delete(
        self,
        backup_name,
    ):

        raise NotImplementedError

    def exists(
        self,
        backup_name,
    ):

        return (
            self.root
            / "archives"
            / backup_name
        ).exists()

    def list_backups(self):

        archive_dir = (
            self.root
            / "archives"
        )

        if not archive_dir.exists():
            return []

        return sorted(
            archive_dir.iterdir()
        )
