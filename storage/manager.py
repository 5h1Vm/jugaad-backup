from .local import LocalStorage


class StorageManager:

    def __init__(self):

        self.providers = [

            LocalStorage(),

        ]

    def enabled_providers(self):

        return [

            provider

            for provider in self.providers

            if provider.enabled()

        ]

    def upload(
        self,
        archive,
        manifest,
    ):

        uploaded = []

        for provider in self.enabled_providers():

            if not provider.healthcheck():

                print(
                    f"[Storage] {provider.name} unavailable"
                )

                continue

            print(
                f"[Storage] Uploading to {provider.name}"
            )

            provider.upload(
                archive,
                manifest
            )

            uploaded.append(
                provider.name
            )

        return uploaded