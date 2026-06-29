from .artifact import BackupArtifact


class StorageManager:

    def __init__(self):

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

                    healthy.append(
                        provider
                    )

                else:

                    print(
                        f"[Storage] {provider.name} unavailable"
                    )

            except Exception as e:

                print(
                    f"[Storage] {provider.name} healthcheck failed: {e}"
                )

        return healthy

    def upload(
        self,
        artifact: BackupArtifact,
    ):

        uploaded = []

        for provider in self.healthy_providers():

            print(
                f"[Storage] Upload -> {provider.name}"
            )

            try:

                ok = provider.upload(
                    artifact
                )

                if ok:

                    uploaded.append(
                        provider.name
                    )

                else:

                    print(
                        f"[Storage] {provider.name} upload failed"
                    )

            except Exception as e:

                print(
                    f"[Storage] {provider.name}: {e}"
                )

        return uploaded