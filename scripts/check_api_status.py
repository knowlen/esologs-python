#!/usr/bin/env python3
"""
Check ESO Logs API Status

This script checks if the ESO Logs API endpoints are responding.
"""

import asyncio
import sys
from datetime import datetime

import httpx
import requests


def check_oauth_endpoint() -> bool:
    """Check if the OAuth token endpoint is responding."""
    print("Checking OAuth endpoint...")
    url = "https://www.esologs.com/oauth/token"

    try:
        # Just check if the endpoint responds (we expect 401 without credentials)
        response = requests.post(url, timeout=10)
        if response.status_code == 401:
            print(
                "✅ OAuth endpoint is UP (401 Unauthorized - expected without credentials)"
            )
            return True
        elif response.status_code == 502:
            print("❌ OAuth endpoint is DOWN (502 Bad Gateway)")
            return False
        else:
            print(
                f"⚠️  OAuth endpoint returned unexpected status: {response.status_code}"
            )
            return True  # It's responding, just not as expected
    except requests.exceptions.Timeout:
        print("❌ OAuth endpoint TIMEOUT")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ OAuth endpoint CONNECTION ERROR: {e}")
        return False
    except Exception as e:
        print(f"❌ OAuth endpoint ERROR: {type(e).__name__}: {e}")
        return False


async def check_graphql_endpoint() -> bool:
    """Check if the GraphQL endpoint is responding."""
    print("\nChecking GraphQL endpoint...")
    url = "https://www.esologs.com/api/v2/client"

    # Simple introspection query
    query = """
    {
        __schema {
            queryType {
                name
            }
        }
    }
    """

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json={"query": query}, timeout=10.0)

            if response.status_code == 200:
                print("✅ GraphQL endpoint is UP (200 OK)")
                return True
            elif response.status_code == 401:
                print("✅ GraphQL endpoint is UP (401 Unauthorized - needs auth)")
                return True
            elif response.status_code == 502:
                print("❌ GraphQL endpoint is DOWN (502 Bad Gateway)")
                return False
            else:
                print(f"⚠️  GraphQL endpoint returned status: {response.status_code}")
                print(f"    Response: {response.text[:200]}...")
                return True

        except httpx.TimeoutException:
            print("❌ GraphQL endpoint TIMEOUT")
            return False
        except httpx.ConnectError as e:
            print(f"❌ GraphQL endpoint CONNECTION ERROR: {e}")
            return False
        except Exception as e:
            print(f"❌ GraphQL endpoint ERROR: {type(e).__name__}: {e}")
            return False


def check_website() -> bool:
    """Check if the main website is responding."""
    print("\nChecking main website...")
    url = "https://www.esologs.com/"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("✅ Main website is UP (200 OK)")
            return True
        elif response.status_code == 502:
            print("❌ Main website is DOWN (502 Bad Gateway)")
            return False
        else:
            print(f"⚠️  Main website returned status: {response.status_code}")
            return True
    except Exception as e:
        print(f"❌ Main website ERROR: {type(e).__name__}: {e}")
        return False


async def check_all_endpoints() -> bool:
    """Check all ESO Logs endpoints."""
    print(f"ESO Logs API Status Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Check OAuth
    oauth_status = check_oauth_endpoint()

    # Check GraphQL
    graphql_status = await check_graphql_endpoint()

    # Check website
    website_status = check_website()

    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  OAuth Endpoint:   {'✅ UP' if oauth_status else '❌ DOWN'}")
    print(f"  GraphQL Endpoint: {'✅ UP' if graphql_status else '❌ DOWN'}")
    print(f"  Main Website:     {'✅ UP' if website_status else '❌ DOWN'}")

    if not (oauth_status or graphql_status):
        print("\n⚠️  API appears to be down or experiencing issues")
        return False
    else:
        print("\n✅ API is operational")
        return True


async def monitor_api(interval: int = 60) -> None:
    """Monitor API status continuously."""
    print(f"Starting API monitor (checking every {interval} seconds)")
    print("Press Ctrl+C to stop\n")

    while True:
        try:
            await check_all_endpoints()
            print(f"\nNext check in {interval} seconds...\n")
            await asyncio.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped")
            break


def main() -> None:
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        # Monitor mode
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        asyncio.run(monitor_api(interval))
    else:
        # Single check
        is_up = asyncio.run(check_all_endpoints())
        sys.exit(0 if is_up else 1)


if __name__ == "__main__":
    main()
