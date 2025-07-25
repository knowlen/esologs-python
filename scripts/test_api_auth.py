#!/usr/bin/env python3
"""
Test ESO Logs API Authentication

This script tests if we can authenticate with the ESO Logs API.
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Optional

try:
    from esologs.auth import get_access_token
    from esologs.client import Client
except ImportError:
    print("Error: Please install esologs-python or run from the project directory")
    sys.exit(1)


def test_oauth_authentication() -> Optional[str]:
    """Test OAuth authentication."""
    print("Testing OAuth Authentication...")
    print("-" * 40)

    client_id = os.environ.get("ESOLOGS_ID")
    client_secret = os.environ.get("ESOLOGS_SECRET")

    if not client_id or not client_secret:
        print(
            "❌ Missing credentials: Set ESOLOGS_ID and ESOLOGS_SECRET environment variables"
        )
        return None

    print(f"Client ID: {client_id[:10]}...")

    try:
        token = get_access_token(client_id, client_secret)
        print(f"✅ Successfully obtained access token: {token[:20]}...")
        return token
    except Exception as e:
        print(f"❌ Authentication failed: {type(e).__name__}: {e}")
        return None


async def test_api_call(token: Optional[str]) -> bool:
    """Test making an API call with the token."""
    print("\nTesting API Call...")
    print("-" * 40)

    if not token:
        print("❌ No token available, skipping API test")
        return False

    try:
        async with Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": f"Bearer {token}"},
        ) as client:
            # Try the simplest possible query
            rate_limit = await client.get_rate_limit_data()  # type: ignore[attr-defined]
            print("✅ API call successful!")
            print(f"   Rate limit: {rate_limit.rate_limit_data.limit_per_hour}/hour")
            print(
                f"   Points used: {rate_limit.rate_limit_data.points_spent_this_hour}"
            )
            return True

    except Exception as e:
        print(f"❌ API call failed: {type(e).__name__}: {e}")
        return False


async def test_user_endpoint() -> bool:
    """Test the user endpoint without authentication."""
    print("\nTesting User Endpoint...")
    print("-" * 40)

    try:
        async with Client(
            url="https://www.esologs.com/api/v2/user",
            headers={"Authorization": "Bearer dummy_token"},
        ) as client:
            # This should fail with auth error, not 502
            await client.get_user_data()  # type: ignore[attr-defined]
            print("⚠️  Unexpected success with dummy token")
            return True

    except Exception as e:
        error_msg = str(e)
        if "502" in error_msg:
            print("❌ User endpoint is DOWN (502 Bad Gateway)")
            return False
        elif "401" in error_msg or "Unauthorized" in error_msg:
            print("✅ User endpoint is UP (got expected auth error)")
            return True
        else:
            print(f"⚠️  User endpoint error: {type(e).__name__}: {e}")
            return False


async def main() -> bool:
    """Run all tests."""
    print(
        f"ESO Logs API Authentication Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print("=" * 60)

    # Test OAuth
    token = test_oauth_authentication()

    # Test API call
    api_success = await test_api_call(token)

    # Test user endpoint
    user_endpoint_up = await test_user_endpoint()

    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  OAuth Authentication: {'✅ Success' if token else '❌ Failed'}")
    print(f"  API Call:            {'✅ Success' if api_success else '❌ Failed'}")
    print(f"  User Endpoint:       {'✅ UP' if user_endpoint_up else '❌ DOWN'}")

    if token and not api_success:
        print("\n⚠️  Authentication works but API calls are failing")
        print("    The GraphQL endpoint may be experiencing issues")

    return token is not None and api_success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
