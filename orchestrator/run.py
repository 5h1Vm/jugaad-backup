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

from lib.logger import Logger


def run_notion(workspace, logger):

    from collectors.notion.collector import collect

    collect(
        str(workspace),
        logger
    )


def run_cloudflare(workspace, logger):

    from collectors.cloudflare.collector import collect

    collect(
        str(workspace),
        logger
    )


def run_m365(workspace, logger):

    from collectors.m365.collector import collect

    collect(
        str(workspace),
        logger
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

    logger = Logger(
        day_dir / "logs"
    )

    logger.info(
        f"Workspace: {day_dir}"
    )


    if (
        CFG.get(
            "ENABLE_M365",
            "false"
        ).lower()
        == "true"
    ):

        logger.section(
            "Microsoft 365"
        )

        logger.info(
            "Starting collector"
        )

        run_m365(
            day_dir / "m365",
            logger
        )

        logger.end_section()



    if (
        CFG.get(
            "ENABLE_CLOUDFLARE",
            "false"
        ).lower()
        == "true"
    ):

        logger.section(
            "Cloudflare"
        )

        logger.info(
            "Starting collector"
        )

        run_cloudflare(
            day_dir / "cloudflare",
            logger
        )

        logger.end_section()



    if (
        CFG.get(
            "ENABLE_NOTION",
            "false"
        ).lower()
        == "true"
    ):

        logger.section(
            "Notion"
        )

        logger.info(
            "Starting collector"
        )

        try:

            run_notion(
                day_dir / "notion",
                logger
            )

        except Exception as e:

            logger.error(
                f"Notion failed: {e}"
            )

        logger.end_section()



    logger.section(
        "Manifest"
    )

    logger.info(
        "Building"
    )

    manifest = build_manifest(
        day_dir
    )

    logger.end_section()



    logger.section(
        "Archive"
    )

    logger.info(
        "Building"
    )

    archive = build_archive(
        today
    )

    logger.end_section()



    logger.section(
        "Verification"
    )

    logger.info(
        "Verifying archive"
    )

    verify_archive(
        today
    )

    logger.end_section()



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


    logger.info(
        "Backup complete"
    )

    logger.info(
        f"Archive: {archive}"
    )

    logger.info(
        f"Manifest: {manifest_target}"
    )



    logger.section(
        "Cleanup"
    )


    deleted = cleanup_workspace()


    for item in deleted:

        logger.info(
            f"Removed {item}"
        )


    logger.end_section()


    logger.finish()



if __name__ == "__main__":

    main()