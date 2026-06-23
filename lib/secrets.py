import subprocess

def get_config():

    cfg = {}

    with open("/opt/backup/config/backup.conf") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            key, value = line.split(
                "=",
                1
            )

            cfg[key] = value

    return cfg


def load_env():

    cfg = get_config()

    env = {}

    output = subprocess.check_output([
        "age",
        "-d",
        "-i",
        cfg["RUNTIME_KEY"],
        cfg["SECRETS_FILE"]
    ])

    for line in output.decode().splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        key, value = line.split(
            "=",
            1
        )

        env[key] = value

    return env
