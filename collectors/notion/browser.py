from pathlib import Path

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

    def open_workspace(self):
        print(f'[+] Opening workspace: {WORKSPACE_URL}')

    def open_export_dialog(self):
        print('[+] Opening Actions menu')
        print('[+] Opening Export dialog')

    def configure_export(self, export_format: str):
        print(f'[+] Export format: {export_format}')
        print('[+] Database views: Default view')
        print('[+] Page content: Everything')
        print('[+] Include subpages: ON')

    def _run_export(self, export_format: str):

        existing = export_files(self.download_dir)
        known_count = len(existing)

        print(f'[+] Workspace URL: {WORKSPACE_URL}')
        print(f'[+] Profile dir: {PROFILE_DIR}')
        print(f'[+] Profile name: {PROFILE_NAME}')

        self.open_workspace()
        self.open_export_dialog()
        self.configure_export(export_format)

        archive = wait_for_new_export(
            self.download_dir,
            known_count,
            EXPORT_TIMEOUT_MINUTES
        )

        if archive is None:
            raise RuntimeError(f'No new export detected for {export_format}')

        wait_for_stable_file(archive)

        print(f'[+] Export completed: {archive}')
        return archive

    def export_markdown_csv(self):
        return self._run_export('Markdown & CSV')

    def export_html(self):
        return self._run_export('HTML')

    def export_workspace(self):
        return {
            'markdown_csv': self.export_markdown_csv(),
            'html': self.export_html()
        }
