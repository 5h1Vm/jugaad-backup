from pathlib import Path

from .config import (
    REPOSITORY_PATH,
    BACKBLAZE_ENABLED,
    USB_ENABLED,
    USB_LABEL,
    USB_BACKUP_PATH,
)

from .mount import find_mountpoint
from .rclone import Rclone


class SyncEngine:

    def __init__(self):

        self.repository = Path(REPOSITORY_PATH)

    def sync(self):

        self.sync_usb()

        self.sync_backblaze()

    def sync_usb(self):

        if not USB_ENABLED:
            return

        mount = find_mountpoint(USB_LABEL)

        if mount is None:
            print("[Sync] USB not connected")
            return

        destination = mount / USB_BACKUP_PATH

        print(f"[Sync] Repository -> USB ({destination})")

        Rclone.sync(
            str(self.repository),
            str(destination),
        )

    def sync_backblaze(self):

        if not BACKBLAZE_ENABLED:
            return

        print("[Sync] Repository -> Backblaze")

        Rclone.sync(
            str(self.repository),
            "BACKBLAZE_REMOTE",
        )
