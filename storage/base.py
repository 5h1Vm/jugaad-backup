from abc import ABC, abstractmethod
from pathlib import Path


class StorageProvider(ABC):
    """
    Base interface implemented by every storage backend.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def enabled(self) -> bool:
        """
        Return True if this provider is configured
        and should receive backups.
        """
        ...

    @abstractmethod
    def healthcheck(self) -> bool:
        """
        Verify the provider is reachable.
        """
        ...

    @abstractmethod
    def upload(
        self,
        archive: Path,
        manifest: Path,
    ) -> bool:
        """
        Upload archive + manifest.
        """
        ...

    @abstractmethod
    def download(
        self,
        backup_name: str,
        destination: Path,
    ) -> bool:
        ...

    @abstractmethod
    def delete(
        self,
        backup_name: str,
    ) -> bool:
        ...

    @abstractmethod
    def exists(
        self,
        backup_name: str,
    ) -> bool:
        ...

    @abstractmethod
    def list_backups(self):
        ...