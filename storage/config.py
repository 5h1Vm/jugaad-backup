from pathlib import Path


CONFIG_FILE = Path("config/backup.conf")


def load_config():

    config = {}

    if not CONFIG_FILE.exists():
        return config

    with open(CONFIG_FILE) as f:

        for line in f:

            line = line.strip()

            if (
                not line
                or line.startswith("#")
                or "=" not in line
            ):
                continue

            key, value = line.split("=", 1)

            config[key.strip()] = value.strip()

    return config


CFG = load_config()


def enabled(name: str) -> bool:

    return CFG.get(
        name,
        "false",
    ).lower() == "true"


#
# Repository
#

REPOSITORY_ENABLED = enabled(
    "REPOSITORY_ENABLED"
)

REPOSITORY_PATH = Path(
    CFG.get(
        "REPOSITORY_PATH",
        "backupvault",
    )
)


#
# USB
#

USB_ENABLED = enabled(
    "USB_ENABLED"
)

USB_UUID = CFG.get(
    "USB_UUID",
    ""
)

USB_LABEL = CFG.get(
    "USB_LABEL",
    ""
)

USB_BACKUP_PATH = CFG.get(
    "USB_BACKUP_PATH",
    "Backup",
)


#
# Backblaze
#

BACKBLAZE_ENABLED = enabled(
    "BACKBLAZE_ENABLED"
)

BACKBLAZE_BUCKET = CFG.get(
    "BACKBLAZE_BUCKET",
    ""
)

BACKBLAZE_REMOTE = CFG.get(
    "BACKBLAZE_REMOTE",
)


#
# Amazon S3
#

S3_ENABLED = enabled(
    "S3_ENABLED"
)

S3_BUCKET = CFG.get(
    "S3_BUCKET",
    ""
)

S3_REGION = CFG.get(
    "S3_REGION",
    ""
)

S3_ACCESS_KEY = CFG.get(
    "S3_ACCESS_KEY",
    ""
)

S3_SECRET_KEY = CFG.get(
    "S3_SECRET_KEY",
    ""
)