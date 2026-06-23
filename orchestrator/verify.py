import hashlib

from pathlib import Path

from config import BACKUP_TARGET


def sha256_file(path):

    h = hashlib.sha256()

    with open(path, "rb") as f:

        while True:

            chunk = f.read(8192)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def verify_archive(day):

    archive = (
        BACKUP_TARGET /
        "archives" /
        f"{day}.tar.zst.age"
    )

    hash_file = (
        BACKUP_TARGET /
        "hashes" /
        f"{day}.sha256"
    )

    if not archive.exists():

        raise Exception(
            f"Missing archive: {archive}"
        )

    if not hash_file.exists():

        raise Exception(
            f"Missing hash: {hash_file}"
        )

    expected = (
        hash_file
        .read_text()
        .strip()
    )

    actual = sha256_file(
        archive
    )

    if actual != expected:

        raise Exception(
            "Hash mismatch"
        )

    return True
