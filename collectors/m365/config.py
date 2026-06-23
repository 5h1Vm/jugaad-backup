from pathlib import Path

WORKSPACE = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_FILE = PROJECT_ROOT / 'state' / 'm365' / 'state.json'

GRAPH_ROOT = 'https://graph.microsoft.com/v1.0'
