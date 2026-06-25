import json

from . import config
from .graph import graph_paginated_get


SNAPSHOT_KEYS = {

    "users":
    "users",

    "groups":
    "groups",

    "applications":
    "applications",

    "servicePrincipals":
    "service_principals",

    "roles":
    "roles",

    "domains":
    "domains",

    "organization":
    "organization",

    "conditionalAccessPolicies":
    "conditional_access_policies",

    "namedLocations":
    "named_locations"
}

def collect_snapshots(headers, logger):

    counts = {}

    snapshot_dir = (
        config.WORKSPACE /
        "snapshots"
    )

    snapshot_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    for name, endpoint in SNAPSHOTS.items():

        logger.info(
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

        count = len(data)

        counts[
            SNAPSHOT_KEYS[name]
        ] = count

        logger.info(
            f"Collected {count}"
        )

    return counts