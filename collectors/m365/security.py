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


def collect_security(headers, logger):

    counts = {}

    warnings = []

    security_dir = (
        config.WORKSPACE /
        "security"
    )

    security_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    for name, endpoint in SECURITY_ENDPOINTS.items():

        logger.info(
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

            message = (
                f"{name} endpoint failed: {e}"
            )

            logger.info(
                f"[-] {message}"
            )

            warnings.append(
                message
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


        count = len(data)

        key_map = {
    "riskyUsers": "risky_users",
    "riskDetections": "risk_detections",
    "secureScore": "secure_score",
    "alerts": "alerts"
}

counts[key_map[name]] = count


        logger.info(
            f"Collected {count}"
        )


    return {
        "items": counts,
        "warnings": warnings,
            "errors": []
    }