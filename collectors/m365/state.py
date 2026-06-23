import json

from .config import STATE_FILE


def load_state():

    try:

        with open(STATE_FILE) as f:

            return json.load(f)

    except:

        return {
            "audit": {}
        }


def save_state(state):

    with open(
        STATE_FILE,
        "w"
    ) as f:

        json.dump(
            state,
            f,
            indent=4
        )
