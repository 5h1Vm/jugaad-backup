from pathlib import Path

from .api_inventory import build_inventory
from .browser import NotionBrowser
from .config import DOWNLOAD_DIR


def collect(workspace):

    workspace = Path(workspace)

    workspace.mkdir(
        parents=True,
        exist_ok=True
    )

    export_dir = (
        workspace / "export"
    )

    export_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    inventory_dir = (
        workspace / "inventory"
    )

    inventory_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    print("[+] Notion collector")

    browser = NotionBrowser(
        DOWNLOAD_DIR
    )

    inventory_file = (
        build_inventory(
            export_dir,
            inventory_dir
        )
    )

    return {
        "browser": browser,
        "inventory_file": inventory_file
    }