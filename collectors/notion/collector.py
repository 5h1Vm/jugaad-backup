from pathlib import Path


def collect(workspace):

    workspace = Path(workspace)

    workspace.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        "[+] Notion collector"
    )

    print(
        "[+] Notion export not implemented yet"
    )