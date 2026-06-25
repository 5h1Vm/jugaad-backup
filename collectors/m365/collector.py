from pathlib import Path

from . import config
from .graph import get_token
from .audit import collect_audit
from .snapshots import collect_snapshots
from .security import collect_security


def collect(workspace, logger):

    config.WORKSPACE = Path(workspace)

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    logger.success(
        "Token acquired"
    )

    collect_audit(
        headers,
        logger
    )

    collect_snapshots(
        headers,
        logger
    )

    collect_security(
        headers,
        logger
    )

    logger.success(
        "M365 collection complete"
    )


if __name__ == "__main__":
    raise SystemExit(
        "Use orchestrator.run to execute collectors"
    )