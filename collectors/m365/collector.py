from pathlib import Path

from . import config
from .graph import get_token

from .audit import collect_audit
from .snapshots import collect_snapshots
from .security import collect_security


def collect(workspace, logger):

    config.WORKSPACE = Path(workspace)

    stats = {

        "status": "success",

        "items": {},

        "warnings": [],

        "errors": []

    }


    try:

        token = get_token()


        headers = {

            "Authorization":
            f"Bearer {token}"

        }


        logger.success(
            "Token acquired"
        )


        audit = collect_audit(
            headers,
            logger
        )

        stats["items"].update(
            audit
        )


        snapshots = collect_snapshots(
            headers,
            logger
        )

        stats["items"].update(
            snapshots
        )


        security = collect_security(
            headers,
            logger
        )


        stats["items"].update(
            security.get(
                "items",
                {}
            )
        )


        stats["warnings"].extend(
            security.get(
                "warnings",
                []
            )
        )


        logger.success(
            "M365 collection complete"
        )


    except Exception as e:


        stats["status"] = "failed"


        stats["errors"].append(
            str(e)
        )


        raise


    return stats



if __name__ == "__main__":

    raise SystemExit(
        "Use orchestrator.run to execute collectors"
    )