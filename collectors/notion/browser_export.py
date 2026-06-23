from pathlib import Path
from .config import PROFILE_DIR


def get_download_dir():
    return Path.home() / 'Downloads'


def detect_existing_exports():
    download_dir = get_download_dir()
    return sorted(download_dir.glob('*ExportBlock*.zip'))


def profile_path():
    return Path(PROFILE_DIR)
