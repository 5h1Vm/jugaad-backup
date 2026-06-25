import json
from pathlib import Path

from .config import ZONE_ID, ACCOUNT_ID
from . import config as cf_config
from .api import get

DISPLAY_NAMES = {

    "dns_records": "DNS Records",

    "dnssec": "DNSSEC",

    "waf_packages": "WAF Packages",

    "access_applications": "Access Applications",

    "access_groups": "Access Groups",

    "service_tokens": "Service Tokens",

    "identity_providers": "Identity Providers",

    "device_posture": "Device Posture",

    "gateway_rules": "Gateway Rules",

}

BASE = "https://api.cloudflare.com/client/v4"



DATASETS = {


    #
    # Zone
    #

    "zone": (
        "zone",
        f"{BASE}/zones/{ZONE_ID}"
    ),


    "dns_records": (
        "zone",
        f"{BASE}/zones/{ZONE_ID}/dns_records"
    ),


    "zone_settings": (
        "zone",
        f"{BASE}/zones/{ZONE_ID}/settings"
    ),


    "dnssec": (
        "zone",
        f"{BASE}/zones/{ZONE_ID}/dnssec"
    ),


    "rulesets": (
        "zone",
        f"{BASE}/zones/{ZONE_ID}/rulesets"
    ),



    #
    # Security
    #

    "firewall_rules": (
        "security",
        f"{BASE}/zones/{ZONE_ID}/firewall/rules"
    ),


    "filters": (
        "security",
        f"{BASE}/zones/{ZONE_ID}/filters"
    ),


    "rate_limits": (
        "security",
        f"{BASE}/zones/{ZONE_ID}/rate_limits"
    ),


    "waf_packages": (
        "security",
        f"{BASE}/zones/{ZONE_ID}/firewall/waf/packages"
    ),




    #
    # Zero Trust
    #

    "access_applications": (
        "zerotrust",
        f"{BASE}/accounts/{ACCOUNT_ID}/access/apps"
    ),


    "access_groups": (
        "zerotrust",
        f"{BASE}/accounts/{ACCOUNT_ID}/access/groups"
    ),


    "access_users": (
        "zerotrust",
        f"{BASE}/accounts/{ACCOUNT_ID}/access/users"
    ),


    "service_tokens": (
        "zerotrust",
        f"{BASE}/accounts/{ACCOUNT_ID}/access/service_tokens"
    ),


    "identity_providers": (
        "zerotrust",
        f"{BASE}/accounts/{ACCOUNT_ID}/access/identity_providers"
    ),


    "device_posture": (
        "zerotrust",
        f"{BASE}/accounts/{ACCOUNT_ID}/devices/posture"
    ),


    "devices": (
        "zerotrust",
        f"{BASE}/accounts/{ACCOUNT_ID}/devices"
    ),


    "gateway_rules": (
        "zerotrust",
        f"{BASE}/accounts/{ACCOUNT_ID}/gateway/rules"
    ),


    "tunnels": (
        "zerotrust",
        f"{BASE}/accounts/{ACCOUNT_ID}/cfd_tunnel"
    )

}




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




def count(data):

    if isinstance(data, list):

        return len(data)


    if isinstance(data, dict):

        result = data.get(
            "result"
        )


        if isinstance(result, list):

            return len(result)


        if isinstance(result, dict):

            return 1


    return 0





def collect(workspace, logger):


    cf_config.WORKSPACE = Path(
        workspace
    )



    stats = {

        "status": "success",

        "items": {},

        "warnings": [],

        "errors": []

    }



    root = cf_config.WORKSPACE



    folders = {

        "zone":
            root / "zone",

        "security":
            root / "security",

        "zerotrust":
            root / "zerotrust",

        "audit":
            root / "audit"

    }



    for folder in folders.values():

        folder.mkdir(
            parents=True,
            exist_ok=True
        )





    for name, (category, url) in DATASETS.items():


        try:


            logger.info(
                name.replace(
                    "_",
                    " "
                ).title()
            )



            data = get(url)



            save_json(

                folders[category] /
                f"{name}.json",

                data

            )



            total = count(
                data
            )



            stats["items"][name] = total



            logger.success(
                f"Collected {total}"
            )



        except Exception as e:


            msg = (
                f"{name} failed: {e}"
            )


            logger.error(
                msg
            )


            stats["warnings"].append(
                msg
            )






    #
    # Access Policies
    #

    try:


        logger.info(
            "Access Policies"
        )


        policies = []


        apps = get(

            f"{BASE}/accounts/{ACCOUNT_ID}/access/apps"

        )


        for app in apps.get(
            "result",
            []
        ):


            app_id = app["id"]


            result = get(

                f"{BASE}/accounts/{ACCOUNT_ID}/"
                f"access/apps/{app_id}/policies"

            )


            policies.append({

                "application":
                    app.get("name"),


                "application_id":
                    app_id,


                "policies":
                    result.get(
                        "result",
                        []
                    )

            })



        save_json(

            folders["zerotrust"] /
            "access_policies.json",

            policies

        )


        stats["items"]["access_policies"] = len(
            policies
        )


        logger.success(
            f"Collected {len(policies)}"
        )



    except Exception as e:


        stats["warnings"].append(
            f"Access Policies failed: {e}"
        )






    #
    # Audit Logs
    #

    try:


        logger.info(
            "Audit Logs"
        )


        data = get(

            f"{BASE}/accounts/{ACCOUNT_ID}/audit_logs"

        )


        save_json(

            folders["audit"] /
            "audit_logs.json",

            data

        )


        total = count(
            data
        )


        stats["items"]["audit_logs"] = total



        logger.success(
            f"Collected {total}"
        )


    except Exception as e:


        stats["warnings"].append(
            f"Audit Logs failed: {e}"
        )




    logger.success(
        "Cloudflare collection complete"
    )


    return stats