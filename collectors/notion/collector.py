from pathlib import Path

from .browser import NotionBrowser
from .config import DOWNLOAD_DIR

from .api_inventory import build_inventory
from .api import NotionMetadataCollector
from .data_source_export import DataSourceExporter
from .data_source_rows import DataSourceRowsExporter
from .statistics import StatisticsCollector
from .manifest import ManifestBuilder


def collect(workspace):

    workspace = Path(workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    notion_dir = workspace / "notion"
    notion_dir.mkdir(parents=True, exist_ok=True)

    browser_exports = notion_dir / "browser"
    api_dir = notion_dir / "api"

    browser_exports.mkdir(parents=True, exist_ok=True)
    api_dir.mkdir(parents=True, exist_ok=True)

    print()
    print("=" * 60)
    print("Notion Collector")
    print("=" * 60)

    browser = NotionBrowser(DOWNLOAD_DIR)

    print("[+] Browser exports")

    browser.export_workspace()

    print("[+] Building inventory")

    build_inventory(
        browser_exports,
        api_dir
    )

    meta = NotionMetadataCollector(api_dir)

    meta.collect_pages()
    meta.collect_users()
    meta.collect_data_sources()

    DataSourceExporter(api_dir).export()

    rows_dir = api_dir / "rows"

    DataSourceRowsExporter(
        rows_dir
    ).export()

    StatisticsCollector(
        api_dir
    ).collect()

    ManifestBuilder(
        notion_dir
    ).build()

    return notion_dir
