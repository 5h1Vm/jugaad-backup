import importlib.util

spec = importlib.util.spec_from_file_location(
    "backup_lib_secrets",
    "/opt/backup/lib/secrets.py"
)

backup_secrets = importlib.util.module_from_spec(spec)

spec.loader.exec_module(
    backup_secrets
)

ENV = backup_secrets.load_env()

ZONE_ID = ENV["ZONE_ID"]

ACCOUNT_ID = ENV["CLOUDFLARE_ACCOUNT_ID"]

WORKSPACE = None
