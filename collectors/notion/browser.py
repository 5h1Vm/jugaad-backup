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

    def __init__(self):
        pass

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

        page = context.pages[0] if context.pages else context.new_page()
        return playwright, context, page

    def _open_export_dialog(self, page):
        print("[+] Opening workspace")

        page.goto(
            WORKSPACE_URL,
            wait_until="domcontentloaded",
        )

        self._wait(page, 3000)

        print("[+] Opening actions menu")

        page.locator('[aria-label="Actions"]').click(timeout=30000)

        self._wait(page)

        print("[+] Opening export dialog")

        page.get_by_text(
            "Export",
            exact=True,
        ).click()

        page.wait_for_selector(
            '[role="dialog"][aria-label="Export"]',
            timeout=30000,
        )

        self._wait(page, 2000)

    def _select_export_format(
        self,
        page,
        export_format,
    ):
        dialog = page.locator(
            '[role="dialog"][aria-label="Export"]'
        )

        print(
            f"[+] Switching export format -> {export_format}"
        )

        #
        # Current format selector
        #
        current = (
            dialog.get_by_role("button", name="HTML")
        )

        if current.count() == 0:
            current = (
                dialog.get_by_role(
                    "button",
                    name="Markdown & CSV",
                )
            )

        if current.count() == 0:
            current = (
                dialog.get_by_role(
                    "button",
                    name="PDF",
                )
            )

        if current.count() == 0:
            raise RuntimeError(
                "Could not locate export format selector"
            )

        current.first.click()

        page.wait_for_timeout(1500)

        #
        # Select desired option
        #
        option = page.get_by_text(
            export_format,
            exact=True,
        )

        option.click()

        page.wait_for_timeout(2000)

        print(
            f"[+] Selected format: {export_format}"
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
                print("[+] Default View already selected")
                return

            print("[+] Opening Database Views")

            current_view_button = dialog.get_by_role(
                "button",
                name="Current view",
            )

            if current_view_button.count() == 0:
                current_view_button = (
                    dialog.locator('[role="button"]')
                    .filter(has_text="Current view")
                    .first
                )

            current_view_button.click()

            self._wait(page, 1500)

            default_view = dialog.get_by_role(
                "menuitem",
                name="Default view",
            )

            if default_view.count() == 0:
                default_view = page.get_by_role(
                    "menuitem",
                    name="Default view",
                )

            if default_view.count() == 0:
                print("[!] Default View not found")
                return

            default_view.click()

            self._wait(page, 1500)

            print("[+] Default View selected")

        except Exception as e:
            print(f"[!] View selection error: {e}")

    def _enable_subpages(self, page):
        print("[+] Ensuring Include Subpages enabled")

        try:
            switches = page.locator(
                'input[role="switch"]'
            )

            count = switches.count()

            print(f"[+] Switch count: {count}")

            if count < 1:
                raise RuntimeError(
                    "No switches found in export dialog"
                )

            include_subpages = switches.nth(0)

            before = include_subpages.is_checked()
            print(f"[+] Current state: {before}")

            if not before:
                include_subpages.click(force=True)
                self._wait(page, 1000)

            after = include_subpages.is_checked()
            print(f"[+] Final state: {after}")

            if not after:
                raise RuntimeError(
                    "Failed to enable Include Subpages"
                )

        except Exception as e:
            print(f"[!] Include Subpages error: {e}")
            raise

    def _configure_export(
        self,
        page,
        export_format,
    ):
        print()
        print("=" * 60)
        print(f"[+] Configuring {export_format}")
        print("=" * 60)

        self._select_export_format(
            page,
            export_format,
        )

        self._select_default_view(page)
        self._enable_subpages(page)

        self._wait(page, 2000)

        print("[+] Export configuration complete")

    def _download_export(
        self,
        page,
        download_dir: Path,
        export_format,
    ):
        dialog = page.locator(
            '[role="dialog"][aria-label="Export"]'
        )

        export_buttons = (
            dialog.locator('[role="button"]')
            .filter(has_text="Export")
        )

        print("[+] Starting export")

        with page.expect_download(
            timeout=EXPORT_TIMEOUT_MS
        ) as dl:
            export_buttons.last.click()

        print("[+] Export requested")

        download = dl.value

        print("[+] Download detected")

        download_dir = Path(download_dir)

        download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        if export_format == "Markdown & CSV":
            filename = "markdown_export.zip"
        elif export_format == "HTML":
            filename = "html_export.zip"
        else:
            filename = download.suggested_filename

        print(f"[+] Filename: {filename}")

        target = download_dir / filename

        download.save_as(str(target))

        print(f"[+] Saved: {target}")

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

            self._open_export_dialog(page)

            self._configure_export(
                page,
                export_format,
            )

            return self._download_export(
                page,
                download_dir,
                export_format,
            )

        finally:
            try:
                if context:
                    context.close()
            except Exception:
                pass

            try:
                if playwright:
                    playwright.stop()
            except Exception:
                pass

    def export_markdown_csv(
        self,
        download_dir,
    ):
        return self._run_export(
            "Markdown & CSV",
            download_dir,
        )

    def export_html(
        self,
        download_dir,
    ):
        return self._run_export(
            "HTML",
            download_dir,
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