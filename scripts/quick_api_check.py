#!/usr/bin/env python3
"""Quick API status check using curl-like requests."""

import requests

endpoints = [
    ("Main Website", "https://www.esologs.com/", "GET"),
    ("OAuth Token", "https://www.esologs.com/oauth/token", "POST"),
    ("GraphQL Client", "https://www.esologs.com/api/v2/client", "POST"),
    ("GraphQL User", "https://www.esologs.com/api/v2/user", "POST"),
    ("API Docs", "https://www.esologs.com/v2-api-docs/eso/", "GET"),
]

print("ESO Logs Endpoint Status Check")
print("=" * 50)

for name, url, method in endpoints:
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        else:
            response = requests.post(url, timeout=5, json={})

        status = response.status_code
        if status == 502:
            print(f"❌ {name:<20} {status} Bad Gateway")
        elif status in (200, 201):
            print(f"✅ {name:<20} {status} OK")
        elif status in (400, 401, 403):
            print(f"✅ {name:<20} {status} (Auth required - endpoint is up)")
        else:
            print(f"⚠️  {name:<20} {status}")

    except requests.exceptions.Timeout:
        print(f"⏱️  {name:<20} TIMEOUT")
    except Exception as e:
        print(f"❌ {name:<20} ERROR: {type(e).__name__}")

print("=" * 50)
print("\nIf you see 502 errors, the API is experiencing issues.")
print("Check https://twitter.com/LogsEso for updates.")
