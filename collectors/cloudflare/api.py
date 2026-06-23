import requests

from . import config as cf_config

ENV = cf_config.ENV


def headers():
    return {
        "Authorization": f"Bearer {ENV['CLOUDFLARE_API_TOKEN']}",
        "Content-Type": "application/json"
    }


def get(url):
    r = requests.get(url, headers=headers())
    r.raise_for_status()
    return r.json()