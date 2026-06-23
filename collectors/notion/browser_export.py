from pathlib import Path
from datetime import datetime
from .config import PROFILE_DIR


EXPORT_GLOB = '*ExportBlock*.zip'


def get_download_dir():
    return Path.home() / 'Downloads'


def detect_existing_exports():
    download_dir = get_download_dir()
    return sorted(download_dir.glob(EXPORT_GLOB))


def newest_export():
    exports = detect_existing_exports()
    if not exports:
        return None
    return max(exports, key=lambda p: p.stat().st_mtime)


def profile_path():
    return Path(PROFILE_DIR)


def export_status_snapshot():
    latest = newest_export()
    return {
        'timestamp': datetime.utcnow().isoformat(),
        'profile_dir': str(profile_path()),
        'download_dir': str(get_download_dir()),
        'latest_export': str(latest) if latest else None,
        'known_export_count': len(detect_existing_exports())
    }
