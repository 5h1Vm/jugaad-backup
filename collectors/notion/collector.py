from pathlib import Path
from datetime import datetime

from .browser_export import export_status_snapshot
from .state import save_state
from .api_inventory import build_inventory


def collect(workspace):
    workspace = Path(workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    export_dir = workspace / 'export'
    export_dir.mkdir(parents=True, exist_ok=True)

    inventory_dir = workspace / 'inventory'
    inventory_dir.mkdir(parents=True, exist_ok=True)

    print('[+] Notion collector')
    print(f'[+] Export directory: {export_dir}')
    print(f'[+] Inventory directory: {inventory_dir}')

    snapshot = export_status_snapshot()

    inventory_file = build_inventory(
        export_dir,
        inventory_dir
    )

    state = {
        'last_run': datetime.utcnow().isoformat(),
        'status': 'ready-for-browser-export',
        'export_dir': str(export_dir),
        'inventory_dir': str(inventory_dir),
        'inventory_file': str(inventory_file),
        'browser': snapshot
    }

    save_state(state)

    print(f"[+] Existing exports detected: {snapshot['known_export_count']}")

    if snapshot['latest_export']:
        print(f"[+] Latest export: {snapshot['latest_export']}")

    print(f'[+] Inventory written: {inventory_file}')

    return True
