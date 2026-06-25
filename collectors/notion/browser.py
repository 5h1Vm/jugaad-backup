from pathlib import Path

from playwright.sync_api import sync_playwright

from .config import (
    WORKSPACE_URL,
    PROFILE_DIR,
    EXPORT_TIMEOUT_MINUTES,
    BROWSER_EXECUTABLE,
)


EXPORT_TIMEOUT_MS = EXPORT_TIMEOUT_MINUTES * 60 * 1000
STEP_WAIT_MS = 1500


class NotionBrowser:

    def __init__(self, logger):

        self.logger = logger


    def _wait(self, page, ms=STEP_WAIT_MS):

        page.wait_for_timeout(ms)


    def _launch(self):

        playwright = sync_playwright().start()

        context = playwright.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            accept_downloads=True,
            executable_path=BROWSER_EXECUTABLE,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        page = (
            context.pages[0]
            if context.pages
            else context.new_page()
        )

        return playwright, context, page


    def _open_export_dialog(self, page):

        self.logger.info(
            "Opening workspace"
        )

        page.goto(
            WORKSPACE_URL,
            wait_until="domcontentloaded",
        )

        self._wait(
            page,
            3000
        )


        self.logger.info(
            "Opening actions menu"
        )

        page.locator(
            '[aria-label="Actions"]'
        ).click(
            timeout=30000
        )


        self._wait(page)


        self.logger.info(
            "Opening export dialog"
        )


        page.get_by_text(
            "Export",
            exact=True,
        ).click()


        page.wait_for_selector(
            '[role="dialog"][aria-label="Export"]',
            timeout=30000,
        )


        self._wait(
            page,
            2000
        )


    def _select_export_format(
        self,
        page,
        export_format,
    ):

        dialog = page.locator(
            '[role="dialog"][aria-label="Export"]'
        )


        self.logger.info(
            f"Selecting format: {export_format}"
        )


        current = dialog.get_by_role(
            "button",
            name="HTML"
        )


        if current.count() == 0:

            current = dialog.get_by_role(
                "button",
                name="Markdown & CSV"
            )


        if current.count() == 0:

            current = dialog.get_by_role(
                "button",
                name="PDF"
            )


        if current.count() == 0:

            raise RuntimeError(
                "Export format selector not found"
            )


        current.first.click()


        page.wait_for_timeout(
            1500
        )


        page.get_by_text(
            export_format,
            exact=True,
        ).click()


        page.wait_for_timeout(
            2000
        )


        self.logger.success(
            f"Selected format: {export_format}"
        )



    def _select_default_view(self, page):

        dialog = page.locator(
            '[role="dialog"][aria-label="Export"]'
        )


        try:

            default_button = dialog.get_by_role(
                "button",
                name="Default view",
            )


            if default_button.count():

                self.logger.info(
                    "Default view already selected"
                )

                return


            self.logger.info(
                "Selecting default database view"
            )


            current = dialog.get_by_role(
                "button",
                name="Current view"
            )


            if current.count() == 0:

                current = (
                    dialog.locator('[role="button"]')
                    .filter(
                        has_text="Current view"
                    )
                    .first
                )


            current.click()


            self._wait(
                page,
                1500
            )


            default_view = dialog.get_by_role(
                "menuitem",
                name="Default view"
            )


            if default_view.count() == 0:

                default_view = page.get_by_role(
                    "menuitem",
                    name="Default view"
                )


            if default_view.count() == 0:

                self.logger.warning(
                    "Default view not found"
                )

                return


            default_view.click()


            self.logger.success(
                "Default view selected"
            )


        except Exception as e:

            self.logger.warning(
                f"Default view selection failed: {e}"
            )



    def _enable_subpages(self,page):

        self.logger.info(
            "Checking Include Subpages"
        )


        switches = page.locator(
            'input[role="switch"]'
        )


        count = switches.count()


        if count < 1:

            raise RuntimeError(
                "No export switches found"
            )


        switch = switches.nth(0)


        if not switch.is_checked():

            switch.click(
                force=True
            )


        if switch.is_checked():

            self.logger.success(
                "Include Subpages enabled"
            )

        else:

            raise RuntimeError(
                "Failed enabling Include Subpages"
            )



    def _configure_export(
        self,
        page,
        export_format,
    ):


        self.logger.info(
            f"Configuring {export_format}"
        )


        self._select_export_format(
            page,
            export_format
        )


        self._select_default_view(
            page
        )


        self._enable_subpages(
            page
        )


        self._wait(
            page,
            2000
        )


        self.logger.success(
            "Export configuration complete"
        )



    def _download_export(
        self,
        page,
        download_dir: Path,
        export_format,
    ):


        dialog = page.locator(
            '[role="dialog"][aria-label="Export"]'
        )


        button = (
            dialog.locator('[role="button"]')
            .filter(
                has_text="Export"
            )
        )


        self.logger.info(
            "Starting export"
        )


        with page.expect_download(
            timeout=EXPORT_TIMEOUT_MS
        ) as dl:

            button.last.click()


        download = dl.value


        download_dir = Path(download_dir)

        download_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        if export_format == "Markdown & CSV":

            filename = "markdown_export.zip"

        elif export_format == "HTML":

            filename = "html_export.zip"

        else:

            filename = download.suggested_filename



        target = download_dir / filename


        download.save_as(
            str(target)
        )


        self.logger.success(
            f"Downloaded {filename}"
        )


        return target



    def _run_export(
        self,
        export_format,
        download_dir,
    ):


        playwright = None
        context = None


        try:

            playwright, context, page = self._launch()


            self._open_export_dialog(
                page
            )


            self._configure_export(
                page,
                export_format
            )


            return self._download_export(
                page,
                download_dir,
                export_format
            )


        finally:


            if context:

                context.close()


            if playwright:

                playwright.stop()



    def export_markdown_csv(
        self,
        download_dir,
    ):


        return self._run_export(
            "Markdown & CSV",
            download_dir
        )



    def export_html(
        self,
        download_dir,
    ):


        return self._run_export(
            "HTML",
            download_dir
        )



    def export_workspace(
        self,
        download_dir,
    ):


        markdown = self.export_markdown_csv(
            download_dir
        )


        html = self.export_html(
            download_dir
        )


        return {
            "markdown_csv": markdown,
            "html": html,
        }