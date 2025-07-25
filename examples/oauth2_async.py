#!/usr/bin/env python3
"""
ESO Logs OAuth2 Asynchronous Example

This example demonstrates how to use OAuth2 authentication with ESO Logs API
using the asynchronous AsyncOAuth2Flow class for better performance.

Prerequisites:
1. Set ESOLOGS_ID and ESOLOGS_SECRET environment variables
2. Add http://localhost:8765/callback to your ESO Logs app's redirect URLs
3. Install required packages: pip install esologs-python aiofiles

Usage:
    python oauth2_async.py
"""

import asyncio
import os
import sys

from esologs import Client
from esologs.user_auth import (
    AsyncOAuth2Flow,
    UserToken,
    load_token_from_file_async,
    refresh_access_token_async,
    save_token_to_file_async,
)


async def main() -> None:
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

    # Try to load existing token first
    existing_token = await load_token_from_file_async(".esologs_token.json")

    if existing_token and not existing_token.is_expired:
        print("✅ Found valid saved token")
        user_token = existing_token
    elif existing_token and existing_token.is_expired:
        print("🔄 Found expired token, refreshing...")
        if existing_token.refresh_token:
            try:
                user_token = await refresh_access_token_async(
                    client_id=client_id,
                    client_secret=client_secret,
                    refresh_token=existing_token.refresh_token,
                )
                await save_token_to_file_async(user_token, ".esologs_token.json")
                print("✅ Token refreshed successfully")
            except Exception as e:
                print(f"❌ Token refresh failed: {e}")
                print("Starting new authentication flow...")
                user_token = await authenticate(client_id, client_secret)
        else:
            print("❌ No refresh token available")
            print("Starting new authentication flow...")
            user_token = await authenticate(client_id, client_secret)
    else:
        print("No saved token found, starting authentication...")
        user_token = await authenticate(client_id, client_secret)

    # Use the token to make API calls
    await test_api_access(user_token)

    # Demonstrate async file operations
    print("\n📁 Testing async file operations...")
    await demonstrate_async_file_ops(user_token)


async def authenticate(client_id: str, client_secret: str) -> UserToken:
    """Perform OAuth2 authentication flow."""
    # Create async OAuth2 flow handler
    oauth_flow = AsyncOAuth2Flow(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8765/callback",
    )

    print("\nStarting OAuth2 authentication flow...")
    print("A browser window will open for you to authorize the application.")
    print("If the browser doesn't open automatically, visit the URL shown below.\n")

    try:
        # Authorize asynchronously
        user_token = await oauth_flow.authorize(
            scopes=["view-user-profile"], open_browser=True
        )

        print("\n✅ Authentication successful!")
        print(f"Token type: {user_token.token_type}")
        print(f"Access token: {user_token.access_token[:20]}...")
        print(f"Expires in: {user_token.expires_in} seconds")

        # Save token asynchronously
        await save_token_to_file_async(user_token, ".esologs_token.json")
        print("Token saved to .esologs_token.json")

        return user_token

    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        sys.exit(1)


async def test_api_access(user_token: UserToken) -> None:
    """Test API access with the user token."""
    print("\n🔍 Testing API access...")

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


async def demonstrate_async_file_ops(user_token: UserToken) -> None:
    """Demonstrate async file operations with tokens."""
    import os
    import tempfile

    # Create temporary file
    temp_file = tempfile.mktemp(suffix=".json")

    try:
        # Save token asynchronously
        await save_token_to_file_async(user_token, temp_file)
        print("✅ Token saved asynchronously to temporary file")

        # Check file permissions
        file_stats = os.stat(temp_file)
        permissions = oct(file_stats.st_mode & 0o777)
        print(f"📝 File permissions: {permissions} (should be 0o600 for security)")

        # Load token asynchronously
        loaded_token = await load_token_from_file_async(temp_file)
        if loaded_token:
            print("✅ Token loaded asynchronously")
            print(
                f"🔐 Token matches: {loaded_token.access_token == user_token.access_token}"
            )

    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)
            print("🗑️ Temporary file cleaned up")


async def demonstrate_concurrent_operations() -> None:
    """Demonstrate concurrent async operations."""
    print("\n⚡ Demonstrating concurrent operations...")

    # Example of running multiple async operations concurrently
    tasks = []

    # Simulate multiple token loads
    for i in range(3):
        task = load_token_from_file_async(f".esologs_token_{i}.json")
        tasks.append(task)

    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Token {i}: Failed - {result}")
        elif result is None:
            print(f"Token {i}: Not found")
        else:
            print(f"Token {i}: Loaded successfully")


if __name__ == "__main__":
    # Run the async main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
