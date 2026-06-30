from .artifact import BackupArtifact
from .repository import Repository


class StorageManager:

    def __init__(self):

        self.repository = Repository()

        from .registry import PROVIDERS

        self.providers = [

            provider()

            for provider in PROVIDERS

        ]

    def enabled_providers(self):

        return [

            provider

            for provider in self.providers

            if provider.enabled()

        ]

    def healthy_providers(self):

        healthy = []

        for provider in self.enabled_providers():

            try:

                if provider.healthcheck():

                    healthy.append(provider)

                else:

                    print(
                        f"[Storage] {provider.name} unavailable"
                    )

            except Exception as e:

                print(
                    f"[Storage] {provider.name}: {e}"
                )

        return healthy

    def upload(
        self,
        artifact: BackupArtifact,
    ):

        #
        # Repository is mandatory.
        #

        print(
            "[Repository] Storing backup"
        )

        self.repository.upload(
            artifact
        )

        uploaded = [

            "Repository"

        ]

        #
        # Replicate.
        #

        for provider in self.healthy_providers():

            print(
                f"[Storage] Replicate -> {provider.name}"
            )

            try:

                if provider.upload(
                    artifact
                ):

                    uploaded.append(
                        provider.name
                    )

            except Exception as e:

                print(
                    f"[Storage] {provider.name}: {e}"
                )

        return uploaded