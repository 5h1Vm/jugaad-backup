from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / 'config' / 'backup.conf'


def load_config():
    cfg = {}
    with open(CONFIG_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            k, v = line.split('=', 1)
            cfg[k] = v
    return cfg


CFG = load_config()

BACKUP_TARGET = Path(CFG['BACKUP_TARGET'])
WORKSPACE = Path(CFG['WORKSPACE'])
LOG_DIR = Path(CFG['LOG_DIR'])
ARCHIVE_PUBLIC_KEY = Path(CFG['ARCHIVE_PUBLIC_KEY'])
WORKSPACE_RETENTION_DAYS = int(CFG.get('WORKSPACE_RETENTION_DAYS', '7'))
ARCHIVE_RETENTION_DAYS = int(CFG.get('ARCHIVE_RETENTION_DAYS', '30'))
