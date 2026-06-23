from datetime import date

from pathlib import Path

import shutil

from .config import (
    WORKSPACE,
    BACKUP_TARGET,
    CFG
)

from .cleanup import cleanup_workspace
from .manifest import build_manifest
from .archive import build_archive
from .verify import verify_archive

def run_cloudflare(workspace):

    from collectors.cloudflare.collector import collect

    print(
        "[+] Running Cloudflare collector"
    )

    collect(
        str(workspace)
    )

def run_m365(workspace):

    from collectors.m365.collector import collect

    collect(
        str(workspace)
    )

def main():

    today = str(
        date.today()
    )

    day_dir = (
        WORKSPACE /
        today
    )

    day_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        f"[+] Workspace: {day_dir}"
    )

    #
    # Collectors
    #

    if (
        CFG.get(
            "ENABLE_M365",
            "false"
        ).lower()
        == "true"
    ):

        print(
            "[+] Running M365 collector"
        )

        run_m365(
            day_dir / "m365"
        )

    if CFG["ENABLE_CLOUDFLARE"] == "true":

    	run_cloudflare(
            day_dir / "cloudflare"
        )


    #
    # Manifest
    #

    print(
        "[+] Building manifest"
    )

    manifest = build_manifest(
        day_dir
    )

    #
    # Archive
    #

    print(
        "[+] Building archive"
    )

    archive = build_archive(
        today
    )

    #
    # Verify
    #

    print(
        "[+] Verifying archive"
    )

    verify_archive(
        today
    )

    #
    # Store manifest
    #

    manifest_target = (
        BACKUP_TARGET /
        "manifests" /
        f"{today}.manifest.json"
    )

    manifest_target.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.copy2(
        manifest,
        manifest_target
    )

    print(
        "[+] Backup complete"
    )

    print(
        f"[+] Archive: {archive}"
    )

    print(
        f"[+] Manifest: {manifest_target}"
    )

    print(
        "[+] Cleanup"
    )

    deleted = cleanup_workspace()

    for item in deleted:

        print(
            f"[+] Removed {item}"
    )


if __name__ == "__main__":

    main()
