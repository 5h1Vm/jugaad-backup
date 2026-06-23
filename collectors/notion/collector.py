from pathlib import Path
from datetime import datetime

from .browser_export import detect_existing_exports
from .state import save_state


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

    exports = detect_existing_exports()

    state = {
        'last_run': datetime.utcnow().isoformat(),
        'status': 'ready-for-browser-export',
        'export_dir': str(export_dir),
        'inventory_dir': str(inventory_dir),
        'known_export_count': len(exports)
    }

    save_state(state)

    print(f'[+] Existing exports detected: {len(exports)}')
    print('[+] Browser export engine next step')

    return True
