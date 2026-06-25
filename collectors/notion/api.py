from notion_client import Client

from lib.secrets import load_env


class NotionAPI:

    def __init__(self):
        env = load_env()

        self.client = Client(
            auth=env["NOTION_TOKEN"]
        )

    def search(self, **kwargs):
        return self.client.search(**kwargs)

    def users(self):
        return self.client.users.list()

    def page(self, page_id):
        return self.client.pages.retrieve(page_id)

    def database(self, database_id):
        return self.client.databases.retrieve(database_id)

    def block_children(self, block_id, **kwargs):
        return self.client.blocks.children.list(
            block_id=block_id,
            **kwargs
        )
