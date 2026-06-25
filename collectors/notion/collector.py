from pathlib import Path
from .browser import NotionBrowser
from .api_inventory import build_inventory
from .api import NotionMetadataCollector
from .data_source_export import DataSourceExporter
from .data_source_rows import DataSourceRowsExporter
from .statistics import StatisticsCollector
from .manifest import ManifestBuilder


def collect(workspace):
    workspace = Path(workspace)
    workspace.mkdir(
        parents=True,
        exist_ok=True,
    )

    browser_exports = workspace / "browser"
    api_dir = workspace / "api"

    browser_exports.mkdir(parents=True, exist_ok=True)
    api_dir.mkdir(parents=True, exist_ok=True)

    print()
    print("=" * 60)
    print("Notion Collector")
    print("=" * 60)

    browser = NotionBrowser()

    print("[+] Browser exports")

    browser.export_workspace(
        browser_exports
    )

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
        workspace
    ).build()

    return workspace
