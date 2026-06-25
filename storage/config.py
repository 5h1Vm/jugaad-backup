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
