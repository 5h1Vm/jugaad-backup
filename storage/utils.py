from pathlib import Path
import hashlib


def sha256(path: Path) -> str:

    h = hashlib.sha256()

    with open(path, "rb") as f:

        while True:

            block = f.read(1024 * 1024)

            if not block:
                break

            h.update(block)

    return h.hexdigest()