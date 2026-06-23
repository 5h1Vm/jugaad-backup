from orchestrator.config import CFG

PROFILE_DIR = CFG.get(
    "NOTION_PROFILE_DIR",
    "state/notion/profile"
)

DOWNLOAD_DIR = CFG.get(
    "NOTION_DOWNLOAD_DIR",
    "/home/hc/Downloads"
)

EXPORT_TIMEOUT_MINUTES = int(
    CFG.get(
        "NOTION_EXPORT_TIMEOUT_MINUTES",
        "240"
    )
)
