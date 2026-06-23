import json

from . import config

from .graph import graph_paginated_get


SNAPSHOTS = {

    "users":
    "users",

    "groups":
    "groups",

    "applications":
    "applications",

    "servicePrincipals":
    "servicePrincipals",

    "roles":
    "directoryRoles",

    "domains":
    "domains",

    "organization":
    "organization",

    "conditionalAccessPolicies":
    "identity/conditionalAccess/policies",

    "namedLocations":
    "identity/conditionalAccess/namedLocations"
}


def collect_snapshots(headers):

    snapshot_dir = (
    config.WORKSPACE /
    "snapshots"
    )

    snapshot_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    for name, endpoint in SNAPSHOTS.items():

        print(
            f"[+] Snapshot {name}"
        )

        url = (
            f"{config.GRAPH_ROOT}/"
            f"{endpoint}"
        )

        data = graph_paginated_get(
            url,
            headers
        )

        outfile = (
            snapshot_dir /
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
