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

    def export_workspace(self):

        existing = export_files(self.download_dir)
        known_count = len(existing)

        print('[+] Notion browser automation initialized')
        print(f'[+] Workspace URL: {WORKSPACE_URL}')
        print(f'[+] Profile dir: {PROFILE_DIR}')
        print(f'[+] Profile name: {PROFILE_NAME}')
        print(f'[+] Download path: {self.download_dir}')
        print(f'[+] Known exports: {known_count}')

        print('[+] Include subpages policy: ENABLED')
        print('[+] Browser click automation pending implementation')
        print('[+] Waiting for export ZIP')

        archive = wait_for_new_export(
            self.download_dir,
            known_count,
            EXPORT_TIMEOUT_MINUTES
        )

        if archive is None:
            raise RuntimeError('No new Notion export detected')

        wait_for_stable_file(archive)

        print(f'[+] Export completed: {archive}')

        return archive
