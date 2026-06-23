from pathlib import Path

from playwright.sync_api import sync_playwright

from .export import (
    export_files,
    wait_for_new_export,
    wait_for_stable_file
)

from .config import (
    EXPORT_TIMEOUT_MINUTES,
    WORKSPACE_URL,
    PROFILE_DIR,
    PROFILE_NAME
)


class NotionBrowser:

    def __init__(self, download_dir: Path):
        self.download_dir = Path(download_dir)

    def _launch(self):
        playwright = sync_playwright().start()

        context = playwright.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            executable_path="/usr/bin/microsoft-edge"
        )

        page = context.new_page()

        return playwright, context, page

    def _open_export_dialog(self, page):

        page.goto(WORKSPACE_URL)

        page.wait_for_load_state("networkidle")

        page.locator('[aria-label="Actions"]').click()

        page.get_by_text("Export", exact=True).click()

        page.wait_for_selector(
            '[role="dialog"][aria-label="Export"]'
        )

    def _configure_export(
        self,
        page,
        export_format
    ):

        if export_format == "HTML":

            page.get_by_text("Markdown & CSV").click()

            page.get_by_text("HTML").click()

        # Include subpages
        switches = page.locator(
            'input[role="switch"]'
        )

        count = switches.count()

        for i in range(count):

            try:
                switches.nth(i).check()
            except Exception:
                pass

    def _run_export(self, export_format):

        existing = export_files(
            self.download_dir
        )

        known_count = len(existing)

        playwright = None
        context = None

        try:

            playwright, context, page = self._launch()

            self._open_export_dialog(page)

            self._configure_export(
                page,
                export_format
            )

            page.get_by_text(
                "Export",
                exact=True
            ).last.click()

            archive = wait_for_new_export(
                self.download_dir,
                known_count,
                EXPORT_TIMEOUT_MINUTES
            )

            if archive is None:
                raise RuntimeError(
                    f"No new export detected for {export_format}"
                )

            wait_for_stable_file(archive)

            return archive

        finally:

            if context:
                context.close()

            if playwright:
                playwright.stop()

    def export_markdown_csv(self):
        return self._run_export(
            "Markdown & CSV"
        )

    def export_html(self):
        return self._run_export(
            "HTML"
        )

    def export_workspace(self):

        return {
            "markdown_csv":
                self.export_markdown_csv(),
            "html":
                self.export_html()
        }