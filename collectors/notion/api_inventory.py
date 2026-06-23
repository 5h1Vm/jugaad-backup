from pathlib import Path
import json


def build_inventory(export_dir, inventory_dir):
    export_dir = Path(export_dir)
    inventory_dir = Path(inventory_dir)
    inventory_dir.mkdir(parents=True, exist_ok=True)

    inventory = {
        'markdown_files': 0,
        'html_files': 0,
        'csv_files': 0,
        'directories': 0
    }

    for path in export_dir.rglob('*'):
        if path.is_dir():
            inventory['directories'] += 1
        elif path.suffix.lower() == '.md':
            inventory['markdown_files'] += 1
        elif path.suffix.lower() == '.html':
            inventory['html_files'] += 1
        elif path.suffix.lower() == '.csv':
            inventory['csv_files'] += 1

    output = inventory_dir / 'inventory.json'

    with open(output, 'w') as f:
        json.dump(inventory, f, indent=2)

    return output
