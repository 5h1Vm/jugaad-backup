from .artifact import BackupArtifact
from .local import LocalStorage


class StorageManager:

    def __init__(self):

        self.providers = [

            LocalStorage(),

            #
            # Future providers
            #
            # USBStorage(),
            # S3Storage(),
            # BackblazeStorage(),
            # GoogleDriveStorage(),
            # OneDriveStorage(),
            #

        ]

    def enabled_providers(self):

        return [

            provider

            for provider in self.providers

            if provider.enabled()

        ]

    def healthy_providers(self):

        return [

            provider

            for provider in self.enabled_providers()

            if provider.healthcheck()

        ]

    def upload(
        self,
        artifact: BackupArtifact,
    ):

        uploaded = []

        for provider in self.healthy_providers():

            print(
                f"[Storage] Upload -> {provider.name}"
            )

            provider.upload(
                artifact
            )

            uploaded.append(
                provider.name
            )

        return uploaded