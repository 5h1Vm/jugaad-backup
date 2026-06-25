from pathlib import Path
import json

from .api_client import NotionAPI


class NotionMetadataCollector:

    def __init__(self, output_dir: Path):

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.api = NotionAPI()

    def _write(self, filename, data):

        path = self.output_dir / filename

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )

        print(f"[+] Wrote {path}")

        return path

    def collect_pages(self):

        print()

        print("===================================")
        print("Collecting Pages")
        print("===================================")

        pages = []

        for obj in self.api.list_all_objects():

            if obj["object"] == "page":

                pages.append(obj)

        print(f"[+] Pages collected: {len(pages)}")

        return self._write(
            "pages.json",
            pages
        )

    def collect_data_sources(self):

        print()

        print("===================================")
        print("Collecting Data Sources")
        print("===================================")

        data_sources = []

        for obj in self.api.list_all_objects():

            if obj["object"] in (
                "database",
                "data_source"
            ):

                data_sources.append(obj)

        print(
            f"[+] Data Sources collected: {len(data_sources)}"
        )

        return self._write(
            "data_sources.json",
            data_sources
        )

    def collect_users(self):

        print()

        print("===================================")
        print("Collecting Users")
        print("===================================")

        users = []

        cursor = None

        while True:

            result = self.api.client.users.list(
                start_cursor=cursor
            )

            users.extend(
                result["results"]
            )

            if not result["has_more"]:
                break

            cursor = result["next_cursor"]

        print(f"[+] Users collected: {len(users)}")

        return self._write(
            "users.json",
            users
        )

    def collect_all(self):

        return {

            "pages":
                self.collect_pages(),

            "data_sources":
                self.collect_data_sources(),

            "users":
                self.collect_users()

        }
