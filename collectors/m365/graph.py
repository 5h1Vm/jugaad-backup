import requests

from msal import ConfidentialClientApplication

from .secrets import load_env


def get_token():

    env = load_env()

    app = ConfidentialClientApplication(
        env["CLIENT_ID"],
        authority=f"https://login.microsoftonline.com/{env['TENANT_ID']}",
        client_credential=env["CLIENT_SECRET"]
    )

    token = app.acquire_token_for_client(
        scopes=[
            "https://graph.microsoft.com/.default"
        ]
    )

    if "access_token" not in token:

        raise Exception(token)

    return token["access_token"]


def graph_paginated_get(
    url,
    headers
):

    results = []

    while url:

        r = requests.get(
            url,
            headers=headers,
            timeout=60
        )

        r.raise_for_status()

        data = r.json()

        results.extend(
            data.get(
                "value",
                []
            )
        )

        url = data.get(
            "@odata.nextLink"
        )

    return results
