import json
from pathlib import Path

from .config import ZONE_ID, ACCOUNT_ID
from . import config as cf_config
from .api import get


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def collect(workspace):
    cf_config.WORKSPACE = Path(workspace)

    zone_dir = cf_config.WORKSPACE / "zone"
    zone_dir.mkdir(parents=True, exist_ok=True)

    zone_endpoints = {
        "zone": f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}",
        "dns-records": f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records",
        "zone-settings": f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/settings",
        "dnssec": f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dnssec",
        "rulesets": f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/rulesets"
    }

    for name, url in zone_endpoints.items():
        try:
            save_json(zone_dir / f"{name}.json", get(url))
        except Exception as e:
            print(f"[-] {name}: {e}")

    security_dir = cf_config.WORKSPACE / "security"
    security_dir.mkdir(parents=True, exist_ok=True)

    security_endpoints = {
        "firewall-rules": f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/firewall/rules",
        "filters": f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/filters",
        "rate-limits": f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/rate_limits",
        "waf-packages": f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/firewall/waf/packages"
    }

    for name, url in security_endpoints.items():
        try:
            save_json(security_dir / f"{name}.json", get(url))
        except Exception as e:
            print(f"[-] {name}: {e}")

    zt_dir = cf_config.WORKSPACE / "zerotrust"
    zt_dir.mkdir(parents=True, exist_ok=True)

    zt_endpoints = {
        "access-apps": f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/apps",
        "access-groups": f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/groups",
        "access-users": f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/users",
        "service-tokens": f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/service_tokens",
        "identity-providers": f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/identity_providers",
        "device-posture": f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/devices/posture",
        "devices": f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/devices",
        "gateway-rules": f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/gateway/rules",
        "tunnels": f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/cfd_tunnel"
    }

    for name, url in zt_endpoints.items():
        try:
            save_json(zt_dir / f"{name}.json", get(url))
        except Exception as e:
            print(f"[-] {name}: {e}")

    try:
        apps = get(f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/apps")
        policy_dump = []
        for app in apps.get("result", []):
            app_id = app["id"]
            policies = get(f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/apps/{app_id}/policies")
            policy_dump.append({"application": app.get("name"), "application_id": app_id, "policies": policies.get("result", [])})
        save_json(zt_dir / "access-policies.json", policy_dump)
    except Exception as e:
        print(f"[-] access-policies: {e}")

    audit_dir = cf_config.WORKSPACE / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    try:
        save_json(audit_dir / "audit-logs.json", get(f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/audit_logs"))
    except Exception as e:
        print(f"[-] audit-logs: {e}")
