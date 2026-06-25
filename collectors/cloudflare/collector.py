import json
from pathlib import Path

from .config import ZONE_ID, ACCOUNT_ID
from . import config as cf_config
from .api import get


DISPLAY = {

    "zone": "Zone",
    "dns_records": "DNS Records",
    "zone_settings": "Zone Settings",
    "dnssec": "DNSSEC",
    "rulesets": "Rulesets",

    "firewall_rules": "Firewall Rules",
    "filters": "Filters",
    "rate_limits": "Rate Limits",
    "waf_packages": "WAF Packages",

    "access_applications": "Access Applications",
    "access_groups": "Access Groups",
    "access_users": "Access Users",
    "service_tokens": "Service Tokens",
    "identity_providers": "Identity Providers",
    "device_posture": "Device Posture",
    "devices": "Devices",
    "gateway_rules": "Gateway Rules",
    "tunnels": "Tunnels",

    "access_policies": "Access Policies",
    "audit_logs": "Audit Logs"
}


def count(obj):

    if isinstance(obj, list):
        return len(obj)

    if isinstance(obj, dict):

        result = obj.get("result")

        if isinstance(result, list):
            return len(result)

        if isinstance(result, dict):
            return 1

    return 0



def save_json(path, data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )



def collect(workspace, logger):

    cf_config.WORKSPACE = Path(workspace)


    stats = {

        "status": "success",

        "items": {

        },

        "warnings": [],

        "errors": []

    }


    zone_dir = (
        cf_config.WORKSPACE /
        "zone"
    )

    zone_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    endpoints = {


        "zone":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}",


        "dns_records":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records",


        "zone_settings":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/settings",


        "dnssec":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dnssec",


        "rulesets":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/rulesets",


        "firewall_rules":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/firewall/rules",


        "filters":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/filters",


        "rate_limits":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/rate_limits",


        "waf_packages":
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/firewall/waf/packages",


        "access_applications":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/apps",


        "access_groups":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/groups",


        "access_users":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/users",


        "service_tokens":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/service_tokens",


        "identity_providers":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/identity_providers",


        "device_posture":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/devices/posture",


        "devices":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/devices",


        "gateway_rules":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/gateway/rules",


        "tunnels":
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/cfd_tunnel"

    }


    for name, url in endpoints.items():

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


            stats["items"][name] = total


            logger.success(
                f"Collected {total}"
            )


        except Exception as e:


            message = (
                f"{DISPLAY[name]} failed: {e}"
            )


            logger.error(
                message
            )


            stats["warnings"].append(
                message
            )



    #
    # Access policies
    #

    try:


        logger.info(
            "Access Policies"
        )


        policies = []


        apps = get(
            f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/apps"
        )


        for app in apps.get(
            "result",
            []
        ):


            app_id = app["id"]


            data = get(
                f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/access/apps/{app_id}/policies"
            )


            policies.append(
                {
                    "application": app.get("name"),
                    "application_id": app_id,
                    "policies": data.get(
                        "result",
                        []
                    )
                }
            )


        save_json(
            cf_config.WORKSPACE /
            "access-policies.json",
            policies
        )


        stats["items"]["access_policies"] = len(
            policies
        )


    except Exception as e:


        stats["warnings"].append(
            f"Access Policies failed: {e}"
        )



    #
    # Audit logs
    #

    try:


        logger.info(
            "Audit Logs"
        )


        data = get(
            f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/audit_logs"
        )


        save_json(
            cf_config.WORKSPACE /
            "audit_logs.json",
            data
        )


        stats["items"]["audit_logs"] = count(
            data
        )


    except Exception as e:


        stats["warnings"].append(
            f"Audit Logs failed: {e}"
        )



    logger.success(
        "Cloudflare collection complete"
    )


    return stats