import json

from . import config

from .graph import graph_paginated_get

SECURITY_ENDPOINTS = {

    "riskyUsers":
    "identityProtection/riskyUsers",

    "riskDetections":
    "identityProtection/riskDetections",

    "secureScore":
    "security/secureScores",

    "alerts":
    "security/alerts_v2"
}


def collect_security(headers):

    security_dir = (
    config.WORKSPACE /
    "security"
    )
    security_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    for name, endpoint in SECURITY_ENDPOINTS.items():

        print(
            f"[+] Security {name}"
        )

        url = (
            f"{config.GRAPH_ROOT}/"
            f"{endpoint}"
        )

        try:

            data = graph_paginated_get(
                url,
                headers
            )

        except Exception as e:

            print(
                f"[-] {name}: {e}"
            )

            continue

        outfile = (
            security_dir /
            f"{name}.json"
        )

        with open(
            outfile,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )

        print(
            f"Collected {len(data)}"
        )
