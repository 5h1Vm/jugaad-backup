from pathlib import Path
import time

EXPORT_GLOB = "*ExportBlock*.zip"

def export_files(download_dir):
    return sorted(Path(download_dir).glob(EXPORT_GLOB))

def newest_export(download_dir):
    files = export_files(download_dir)
    return max(files, key=lambda p: p.stat().st_mtime) if files else None

def wait_for_new_export(download_dir, known_count, timeout_minutes=240):
    timeout = time.time() + timeout_minutes * 60

    while time.time() < timeout:
        files = export_files(download_dir)

        if len(files) > known_count:
            return newest_export(download_dir)

        time.sleep(60)

    return None

def wait_for_stable_file(path, checks=3):
    previous = -1
    stable = 0

    while stable < checks:
        size = path.stat().st_size

        if size == previous:
            stable += 1
        else:
            stable = 0

        previous = size
        time.sleep(60)

    return True