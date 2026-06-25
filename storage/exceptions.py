class StorageError(Exception):
    """Base storage exception."""


class StorageNotConfigured(StorageError):
    """Provider is not configured."""


class StorageUnavailable(StorageError):
    """Provider cannot be reached."""


class UploadFailed(StorageError):
    """Upload failed."""


class DownloadFailed(StorageError):
    """Download failed."""