from pathlib import Path
import json
from datetime import datetime


def collect(workspace):

    workspace = Path(workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    export_dir = workspace / 'export'
    export_dir.mkdir(parents=True, exist_ok=True)

    inventory_dir = workspace / 'inventory'
    inventory_dir.mkdir(parents=True, exist_ok=True)

    state_dir = Path('state/notion')
    state_dir.mkdir(parents=True, exist_ok=True)

    state_file = state_dir / 'state.json'

    print('[+] Notion collector')
    print(f'[+] Export directory: {export_dir}')
    print(f'[+] Inventory directory: {inventory_dir}')
    print('[+] Browser export implementation pending')
    print('[+] API inventory implementation pending')

    state = {
        'last_run': datetime.utcnow().isoformat(),
        'status': 'placeholder',
        'export_dir': str(export_dir),
        'inventory_dir': str(inventory_dir)
    }

    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

    return True
