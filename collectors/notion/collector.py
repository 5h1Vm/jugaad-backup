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
        exist_ok=True,
    )


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


    logger.info(
        "Browser Exports"
    )


    browser = NotionBrowser(
        logger
    )


    browser.export_workspace(
        browser_exports
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
        "Collecting Pages"
    )


    meta = NotionMetadataCollector(
        api_dir
    )


    meta.collect_pages()


    logger.success(
        "Pages collected"
    )



    logger.info(
        "Collecting Users"
    )


    meta.collect_users()


    logger.success(
        "Users collected"
    )



    logger.info(
        "Collecting Data Sources"
    )


    meta.collect_data_sources()


    logger.success(
        "Data sources collected"
    )



    logger.info(
        "Exporting Data Sources"
    )


    DataSourceExporter(
        api_dir
    ).export()


    logger.success(
        "Data source export complete"
    )



    logger.info(
        "Exporting Rows"
    )


    rows_dir = api_dir / "rows"


    DataSourceRowsExporter(
        rows_dir
    ).export()


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


    logger.success(
        "Notion collection complete"
    )


    return workspace