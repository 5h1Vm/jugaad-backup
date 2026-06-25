import json
from pathlib import Path

from .config import ZONE_ID, ACCOUNT_ID
from . import config as cf_config
from .api import get


DISPLAY = {

    "zone": "Zone",
    "dns-records": "DNS Records",
    "zone-settings": "Zone Settings",
    "dnssec": "DNSSEC",
    "rulesets": "Rulesets",

    "firewall-rules": "Firewall Rules",
    "filters": "Filters",
    "rate-limits": "Rate Limits",
    "waf-packages": "WAF Packages",

    "access-apps": "Access Applications",
    "access-groups": "Access Groups",
    "access-users": "Access Users",
    "service-tokens": "Service Tokens",
    "identity-providers": "Identity Providers",
    "device-posture": "Device Posture",
    "devices": "Devices",
    "gateway-rules": "Gateway Rules",
    "tunnels": "Tunnels"
}


def count(obj):

    if isinstance(obj, list):

        return len(obj)


    if isinstance(obj, dict):

        if "result" in obj:

            if isinstance(obj["result"], list):

                return len(obj["result"])


    return None



def save_json(path, data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "w") as f:

        json.dump(
            data,
            f,
            indent=2
        )



def collect(workspace, logger):

    cf_config.WORKSPACE = Path(workspace)



    zone_dir = (
        cf_config.WORKSPACE /
        "zone"
    )

    zone_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    zone_endpoints = {

        "zone":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}",

        "dns-records":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records",

        "zone-settings":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/settings",

        "dnssec":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dnssec",

        "rulesets":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/rulesets"

    }



    for name, url in zone_endpoints.items():

        try:

            logger.info(
                DISPLAY[name]
            )


            data = get(url)


            save_json(
                zone_dir / f"{name}.json",
                data
            )


            total = count(data)


            if total is None:

                logger.success(
                    "Collected"
                )

            else:

                logger.success(
                    f"Collected {total}"
                )


        except Exception as e:

            logger.error(
                f"{DISPLAY[name]}: {e}"
            )




    security_dir = (
        cf_config.WORKSPACE /
        "security"
    )

    security_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    security_endpoints = {

        "firewall-rules":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/firewall/rules",

        "filters":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/filters",

        "rate-limits":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/rate_limits",

        "waf-packages":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/firewall/waf/packages"

    }



    for name, url in security_endpoints.items():

        try:

            logger.info(
                DISPLAY[name]
            )


            data = get(url)


            save_json(
                security_dir / f"{name}.json",
                data
            )


            total = count(data)


            if total is None:

                logger.success(
                    "Collected"
                )

            else:

                logger.success(
                    f"Collected {total}"
                )


        except Exception as e:

            logger.error(
                f"{DISPLAY[name]}: {e}"
            )




    zt_dir = (
        cf_config.WORKSPACE /
        "zerotrust"
    )

    zt_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    zt_endpoints = {

        "access-apps":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/apps",

        "access-groups":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/groups",

        "access-users":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/users",

        "service-tokens":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/service_tokens",

        "identity-providers":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/identity_providers",

        "device-posture":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/devices/posture",

        "devices":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/devices",

        "gateway-rules":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/gateway/rules",

        "tunnels":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/cfd_tunnel"

    }



    for name, url in zt_endpoints.items():

        try:

            logger.info(
                DISPLAY[name]
            )


            data = get(url)


            save_json(
                zt_dir / f"{name}.json",
                data
            )


            total = count(data)


            if total is None:

                logger.success(
                    "Collected"
                )

            else:

                logger.success(
                    f"Collected {total}"
                )


        except Exception as e:

            logger.error(
                f"{DISPLAY[name]}: {e}"
            )




    try:

        logger.info(
            "Access Policies"
        )


        policy_dump = []


        apps = get(
            f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/apps"
        )


        for app in apps.get("result", []):

            app_id = app["id"]


            policies = get(
                f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/apps/{app_id}/policies"
            )


            policy_dump.append(
                {
                    "application": app.get("name"),
                    "application_id": app_id,
                    "policies": policies.get("result", [])
                }
            )


        save_json(
            zt_dir / "access-policies.json",
            policy_dump
        )


        logger.success(
            f"Collected {len(policy_dump)}"
        )


    except Exception as e:

        logger.error(
            f"Access Policies: {e}"
        )




    audit_dir = (
        cf_config.WORKSPACE /
        "audit"
    )


    audit_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    try:

        logger.info(
            "Audit Logs"
        )


        data = get(
            f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/audit_logs"
        )


        save_json(
            audit_dir / "audit-logs.json",
            data
        )


        total = count(data)


        if total is None:

            logger.success(
                "Collected"
            )

        else:

            logger.success(
                f"Collected {total}"
            )


    except Exception as e:

        logger.error(
            f"Audit Logs: {e}"
        )