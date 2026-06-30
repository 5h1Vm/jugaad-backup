import subprocess


class Rclone:

    @staticmethod
    def copy(source: str, destination: str):

        subprocess.run(
            [
                "rclone",
                "copy",
                source,
                destination,
                "--create-empty-src-dirs",
            ],
            check=True,
        )

    @staticmethod
    def sync(source: str, destination: str):

        subprocess.run(
            [
                "rclone",
                "sync",
                source,
                destination,
                "--create-empty-src-dirs",
            ],
            check=True,
        )

    @staticmethod
    def check(source: str, destination: str):

        subprocess.run(
            [
                "rclone",
                "check",
                source,
                destination,
            ],
            check=True,
        )

    @staticmethod
    def ls(remote: str):

        subprocess.run(
            [
                "rclone",
                "ls",
                remote,
            ],
            check=True,
        )
