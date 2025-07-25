#!/usr/bin/env python3
"""
Update API Status in Documentation

This script checks the ESO Logs API status and updates the JavaScript
status indicator in the documentation.
"""

import os
import re
import sys
from datetime import datetime
from typing import Dict, Tuple

import requests


def check_api_status() -> Tuple[bool, Dict[str, bool]]:
    """Check if ESO Logs API is responding."""
    endpoints = [
        ("OAuth", "https://www.esologs.com/oauth/token", "POST"),
        ("GraphQL", "https://www.esologs.com/api/v2/client", "POST"),
    ]

    statuses = {}

    for name, url, method in endpoints:
        try:
            if method == "POST":
                response = requests.post(url, timeout=5, json={})
            else:
                response = requests.get(url, timeout=5)

            # 502 = Down, 400/401 = Up but needs auth
            if response.status_code == 502:
                statuses[name] = False
            else:
                statuses[name] = True

        except Exception as e:
            print(f"Error checking {name}: {e}")
            statuses[name] = False

    # API is considered down if any critical endpoint is down
    return all(statuses.values()), statuses


def update_status_js(is_online: bool, details: Dict[str, bool]) -> bool:
    """Update the JavaScript status file."""
    js_file = "docs/javascripts/api-status-simple.js"

    if not os.path.exists(js_file):
        print(f"Error: {js_file} not found")
        return False

    with open(js_file) as f:
        content = f.read()

    # Update API_IS_DOWN
    content = re.sub(
        r"const API_IS_DOWN = \w+;",
        f"const API_IS_DOWN = {str(not is_online).lower()};",
        content,
    )

    # Update LAST_CHECKED
    today = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(
        r"const LAST_CHECKED = \'[\d-]+\';", f"const LAST_CHECKED = '{today}';", content
    )

    with open(js_file, "w") as f:
        f.write(content)

    print(f"Updated {js_file}:")
    print(f"  API_IS_DOWN = {not is_online}")
    print(f"  LAST_CHECKED = {today}")

    return True


def create_status_badge() -> None:
    """Create a status badge for the README."""
    badge_file = "docs/assets/api-status-badge.json"

    is_online, _ = check_api_status()

    badge_data = {
        "schemaVersion": 1,
        "label": "ESO Logs API",
        "message": "online" if is_online else "offline",
        "color": "brightgreen" if is_online else "red",
    }

    os.makedirs(os.path.dirname(badge_file), exist_ok=True)

    import json

    with open(badge_file, "w") as f:
        json.dump(badge_data, f, indent=2)

    print(f"Created status badge: {badge_file}")


def main() -> None:
    """Check API status and update documentation."""
    print("Checking ESO Logs API status...")

    is_online, details = check_api_status()

    print("\nStatus check results:")
    for endpoint, status in details.items():
        print(f"  {endpoint}: {'✅ Online' if status else '❌ Offline'}")

    print(f"\nOverall status: {'✅ ONLINE' if is_online else '❌ OFFLINE'}")

    # Update JavaScript file
    if update_status_js(is_online, details):
        print("\n✅ Successfully updated status indicator")
    else:
        print("\n❌ Failed to update status indicator")
        sys.exit(1)

    # Create status badge
    create_status_badge()

    # Exit with appropriate code for CI
    sys.exit(0 if is_online else 2)


if __name__ == "__main__":
    main()
