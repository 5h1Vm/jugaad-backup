from pathlib import Path

from .browser import NotionBrowser
from .api_inventory import build_inventory
from .api import NotionMetadataCollector
from .data_source_export import DataSourceExporter
from .data_source_rows import DataSourceRowsExporter
from .statistics import StatisticsCollector
from .manifest import ManifestBuilder


def collect(workspace, logger):

    workspace = Path(workspace)

    workspace.mkdir(
        parents=True,
        exist_ok=True
    )

    stats = {
        "status": "success",
        "items": {},
        "warnings": [],
        "errors": []
    }


    browser_exports = workspace / "browser"
    api_dir = workspace / "api"


    browser_exports.mkdir(
        parents=True,
        exist_ok=True
    )

    api_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    try:

        logger.info(
            "Browser Exports"
        )


        browser = NotionBrowser(
            logger
        )


        browser_count = browser.export_workspace(
            browser_exports
        )


        stats["items"]["browser_exports"] = (
            browser_count or 1
        )


        logger.success(
            "Browser export complete"
        )


        logger.info(
            "Building Inventory"
        )


        build_inventory(
            browser_exports,
            api_dir
        )


        logger.success(
            "Inventory complete"
        )


        logger.info(
            "Collecting Metadata"
        )


        meta = NotionMetadataCollector(
            api_dir
        )


        metadata = meta.collect_all()


        stats["items"].update(
            metadata
        )


        logger.success(
            "Metadata collected"
        )


        logger.info(
            "Exporting Data Sources"
        )


        exported = DataSourceExporter(
            api_dir
        ).export()


        stats["items"]["database_exports"] = (
            exported or 0
        )


        logger.success(
            "Data source export complete"
        )


        logger.info(
            "Exporting Rows"
        )


        rows = DataSourceRowsExporter(
            api_dir / "rows"
        ).export()


        stats["items"]["database_rows"] = (
            rows or 0
        )


        logger.success(
            "Rows export complete"
        )


        logger.info(
            "Collecting Statistics"
        )


        StatisticsCollector(
            api_dir
        ).collect()


        logger.success(
            "Statistics collected"
        )


        logger.info(
            "Building Manifest"
        )


        ManifestBuilder(
            workspace
        ).build()


        logger.success(
            "Manifest created"
        )


    except Exception as e:

        stats["status"] = "failed"

        stats["errors"].append(
            str(e)
        )

        logger.error(
            f"Notion failed: {e}"
        )


    logger.success(
        "Notion collection complete"
    )

    return stats