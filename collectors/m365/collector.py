from pathlib import Path

from . import config
from .graph import get_token
from .audit import collect_audit
from .snapshots import collect_snapshots
from .security import collect_security


def collect(workspace):

    config.WORKSPACE = Path(workspace)

    token = get_token()

    headers = {
        'Authorization': f'Bearer {token}'
    }

    print('[+] Token acquired')

    collect_audit(headers)
    collect_snapshots(headers)
    collect_security(headers)

    print('[+] M365 collection complete')


if __name__ == '__main__':
    raise SystemExit('Use orchestrator.run to execute collectors')
