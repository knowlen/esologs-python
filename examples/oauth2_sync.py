#!/usr/bin/env python3
"""
ESO Logs OAuth2 Synchronous Example

This example demonstrates how to use OAuth2 authentication with ESO Logs API
using the synchronous OAuth2Flow class.

Prerequisites:
1. Set ESOLOGS_ID and ESOLOGS_SECRET environment variables
2. Add http://localhost:8765/callback to your ESO Logs app's redirect URLs
3. Install required packages: pip install esologs-python

Usage:
    python oauth2_sync.py
"""

import asyncio
import os
import sys

from esologs import Client, OAuth2Flow
from esologs.user_auth import UserToken


def main() -> None:
    # Get credentials from environment
    client_id_opt = os.environ.get("ESOLOGS_ID")
    client_secret_opt = os.environ.get("ESOLOGS_SECRET")

    if not client_id_opt or not client_secret_opt:
        print("Error: Please set ESOLOGS_ID and ESOLOGS_SECRET environment variables")
        print("You can get these from https://www.esologs.com/api/clients/")
        sys.exit(1)

    # Type-safe assignments after validation
    client_id: str = client_id_opt
    client_secret: str = client_secret_opt

    # Create OAuth2 flow handler
    oauth_flow = OAuth2Flow(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8765/callback",
    )

    print("Starting OAuth2 authentication flow...")
    print("A browser window will open for you to authorize the application.")
    print("If the browser doesn't open automatically, visit the URL shown below.\n")

    try:
        # Authorize - this will open the browser and wait for callback
        user_token = oauth_flow.authorize(
            scopes=["view-user-profile"],
            open_browser=True,  # Set to False to manually open the URL
        )

        print("\n✅ Authentication successful!")
        print(f"Token type: {user_token.token_type}")
        print(f"Access token: {user_token.access_token[:20]}...")
        print(f"Expires in: {user_token.expires_in} seconds")

        # Save token for future use
        from esologs.user_auth import save_token_to_file

        save_token_to_file(user_token, ".esologs_token.json")
        print("\nToken saved to .esologs_token.json")

        # Use the token to make API calls
        asyncio.run(test_api_access(user_token))

    except KeyboardInterrupt:
        print("\n\nAuthentication cancelled by user")
    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        sys.exit(1)


async def test_api_access(user_token: UserToken) -> None:
    """Test API access with the user token."""
    print("\nTesting API access...")

    async with Client(
        url="https://www.esologs.com/api/v2/user", user_token=user_token
    ) as client:
        # Get current user info
        current_user = await client.get_current_user()  # type: ignore[attr-defined]
        user = current_user.user_data.current_user

        print(f"\n👤 Logged in as: {user.name}")
        print(f"User ID: {user.id}")

        if user.na_display_name:
            print(f"NA Display Name: {user.na_display_name}")
        if user.eu_display_name:
            print(f"EU Display Name: {user.eu_display_name}")

        # Show guilds
        if user.guilds:
            print(f"\n🏰 Guilds ({len(user.guilds)}):")
            for guild in user.guilds[:5]:  # Show first 5
                print(f"  - {guild.name} on {guild.server.name}")
            if len(user.guilds) > 5:
                print(f"  ... and {len(user.guilds) - 5} more")

        # Show characters
        if user.characters:
            print(f"\n⚔️ Characters ({len(user.characters)}):")
            for char in user.characters[:5]:  # Show first 5
                print(f"  - {char.name}")
            if len(user.characters) > 5:
                print(f"  ... and {len(user.characters) - 5} more")


if __name__ == "__main__":
    main()
