import requests
import importlib.util

spec = importlib.util.spec_from_file_location(
    "cloudflare_config",
    "/opt/backup/collectors/cloudflare/config.py"
)

cf_config = importlib.util.module_from_spec(spec)

spec.loader.exec_module(
    cf_config
)

ENV = cf_config.ENV


def headers():

    return {
        "Authorization":
        f"Bearer {ENV['CLOUDFLARE_API_TOKEN']}",
        "Content-Type":
        "application/json"
    }


def get(url):

    r = requests.get(
        url,
        headers=headers()
    )

    r.raise_for_status()

    return r.json()
