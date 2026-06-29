from datetime import date

from .config import (
    WORKSPACE,
    CFG,
)

from .report import BackupReport
from .cleanup import cleanup_workspace
from .manifest import build_manifest
from .archive import build_archive
from .verify import verify_archive

from storage.manager import StorageManager

from lib.logger import Logger


def run_notion(workspace, logger):

    from collectors.notion.collector import collect

    return collect(
        str(workspace),
        logger,
    )


def run_cloudflare(workspace, logger):

    from collectors.cloudflare.collector import collect

    return collect(
        str(workspace),
        logger,
    )


def run_m365(workspace, logger):

    from collectors.m365.collector import collect

    return collect(
        str(workspace),
        logger,
    )


def process_collector_result(
    report,
    name,
    stats,
):

    if not stats:

        stats = {

            "status": "failed",

            "items": {},

            "warnings": [],

            "errors": [
                "Collector returned no statistics"
            ],
        }

    report.collector_finish(
        name,
        **stats,
    )

    for warning in stats.get(
        "warnings",
        [],
    ):

        report.warning(
            warning
        )

    for error in stats.get(
        "errors",
        [],
    ):

        report.error(
            error
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
        exist_ok=True,
    )

    logger = Logger(
        day_dir / "logs"
    )

    report = BackupReport()

    logger.info(
        f"Workspace: {day_dir}"
    )

    #
    # Microsoft 365
    #
    if CFG.get(
        "ENABLE_M365",
        "false",
    ).lower() == "true":

        logger.section(
            "Microsoft 365"
        )

        report.collector_start(
            "m365"
        )

        try:

            stats = run_m365(
                day_dir / "m365",
                logger,
            )

            process_collector_result(
                report,
                "m365",
                stats,
            )

        except Exception as e:

            logger.error(
                f"M365 failed: {e}"
            )

            report.error(
                str(e)
            )

            report.collector_finish(
                "m365",
                status="failed",
                items={},
                warnings=[],
                errors=[str(e)],
            )

        logger.end_section()

    #
    # Cloudflare
    #
    if CFG.get(
        "ENABLE_CLOUDFLARE",
        "false",
    ).lower() == "true":

        logger.section(
            "Cloudflare"
        )

        report.collector_start(
            "cloudflare"
        )

        try:

            stats = run_cloudflare(
                day_dir / "cloudflare",
                logger,
            )

            process_collector_result(
                report,
                "cloudflare",
                stats,
            )

        except Exception as e:

            logger.error(
                f"Cloudflare failed: {e}"
            )

            report.error(
                str(e)
            )

            report.collector_finish(
                "cloudflare",
                status="failed",
                items={},
                warnings=[],
                errors=[str(e)],
            )

        logger.end_section()

    #
    # Notion
    #
    if CFG.get(
        "ENABLE_NOTION",
        "false",
    ).lower() == "true":

        logger.section(
            "Notion"
        )

        report.collector_start(
            "notion"
        )

        try:

            stats = run_notion(
                day_dir / "notion",
                logger,
            )

            process_collector_result(
                report,
                "notion",
                stats,
            )

        except Exception as e:

            logger.error(
                f"Notion failed: {e}"
            )

            report.error(
                str(e)
            )

            report.collector_finish(
                "notion",
                status="failed",
                items={},
                warnings=[],
                errors=[str(e)],
            )

        logger.end_section()

    #
    # Manifest
    #
    logger.section(
        "Manifest"
    )

    manifest = build_manifest(
        day_dir
    )

    logger.end_section()

    #
    # Archive
    #
    logger.section(
        "Archive"
    )

    artifact = build_archive(
        day=today,
        manifest=manifest,
    )

    report.archive(
        file=artifact.archive.name,
        sha256=artifact.sha256.name,
        size=artifact.size,
    )

    logger.end_section()

    #
    # Verification
    #
    logger.section(
        "Verification"
    )

    try:

        verify_archive(
            artifact
        )

        report.verification(
            verified=True
        )

    except Exception as e:

        report.error(
            str(e)
        )

        report.verification(
            verified=False
        )

        raise

    logger.end_section()

    #
    # Storage
    #
    logger.section(
        "Storage"
    )

    storage = StorageManager()

    uploaded = storage.upload(
        artifact
    )

    if not uploaded:
        raise RuntimeError(
            "No storage backend successfully accepted this backup."
        )

    report.archive(
        uploaded_to=uploaded
    )

    logger.end_section()

    #
    # Cleanup
    #
    logger.section(
        "Cleanup"
    )

    deleted = cleanup_workspace()

    report.cleanup(
        removed=deleted
    )

    logger.end_section()

    #
    # Final report
    #
    report.finish()

    report.write(
        day_dir
    )

    logger.finish()


if __name__ == "__main__":

    main()