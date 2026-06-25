import hashlib
import subprocess

from pathlib import Path

from .config import (
    WORKSPACE,
    ARCHIVE_PUBLIC_KEY,
)


def sha256_file(path: Path) -> str:

    h = hashlib.sha256()

    with open(path, "rb") as f:

        while True:

            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def build_archive(day):

    workspace = WORKSPACE / day

    archive_dir = WORKSPACE / "archive"

    archive_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    tar_file = archive_dir / f"{day}.tar"

    subprocess.run(
        [
            "tar",
            "-cf",
            str(tar_file),
            "-C",
            str(WORKSPACE),
            day,
        ],
        check=True,
    )

    subprocess.run(
        [
            "zstd",
            "-f",
            str(tar_file),
        ],
        check=True,
    )

    zst_file = Path(str(tar_file) + ".zst")

    public_key = ARCHIVE_PUBLIC_KEY.read_text().strip()

    encrypted = Path(str(zst_file) + ".age")

    subprocess.run(
        [
            "age",
            "-r",
            public_key,
            "-o",
            str(encrypted),
            str(zst_file),
        ],
        check=True,
    )

    digest = sha256_file(encrypted)

    hash_file = archive_dir / f"{day}.sha256"

    hash_file.write_text(digest)

    tar_file.unlink()

    zst_file.unlink()

    return {
        "archive": encrypted,
        "hash": hash_file,
    }