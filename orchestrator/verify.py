import hashlib

from pathlib import Path

from .config import WORKSPACE


def sha256_file(path: Path) -> str:

    h = hashlib.sha256()

    with open(path, "rb") as f:

        while True:

            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def verify_archive(day):

    archive = (
        WORKSPACE
        / "archive"
        / f"{day}.tar.zst.age"
    )

    hash_file = (
        WORKSPACE
        / "archive"
        / f"{day}.sha256"
    )

    if not archive.exists():

        raise FileNotFoundError(archive)

    if not hash_file.exists():

        raise FileNotFoundError(hash_file)

    expected = hash_file.read_text().strip()

    actual = sha256_file(archive)

    if expected != actual:

        raise RuntimeError(
            "Archive checksum mismatch."
        )

    return True