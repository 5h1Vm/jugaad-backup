import json

from . import config
from .graph import graph_paginated_get
from .state import load_state
from .state import save_state


AUDIT_ENDPOINTS = {

    "signins": {
        "endpoint": "auditLogs/signIns",
        "timestamp": "createdDateTime"
    },

    "directoryAudits": {
        "endpoint": "auditLogs/directoryAudits",
        "timestamp": "activityDateTime"
    },

    "provisioning": {
        "endpoint": "auditLogs/provisioning",
        "timestamp": "activityDateTime"
    }
}


def collect_audit(headers, logger):

    counts = {}

    state = load_state()

    if "audit" not in state:

        state["audit"] = {}

    audit_dir = (
        config.WORKSPACE /
        "audit"
    )

    audit_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    for dataset, cfg in AUDIT_ENDPOINTS.items():

        logger.info(
            f"[+] Audit {dataset}"
        )

        url = (
            f"{config.GRAPH_ROOT}/"
            f"{cfg['endpoint']}"
        )

        checkpoint = (
            state["audit"]
            .get(dataset)
        )

        if checkpoint:

            url += (
                f"?$filter="
                f"{cfg['timestamp']} "
                f"gt {checkpoint}"
            )

        data = graph_paginated_get(
            url,
            headers
        )

        outfile = (
            audit_dir /
            f"{dataset}.json"
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

        counts[dataset] = count

        logger.info(
            f"Collected {count}"
        )

        if data:

            timestamps = [
                item.get(cfg["timestamp"])
                for item in data
                if item.get(cfg["timestamp"])
            ]

            if timestamps:

                state["audit"][dataset] = max(
                    timestamps
                )

    save_state(state)

    return counts