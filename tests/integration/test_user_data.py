"""Integration tests for UserData API methods.

Note: These tests mock the OAuth2 user authentication since we cannot
perform real user authentication in automated tests.
"""

import logging
import os
from unittest.mock import AsyncMock

import pytest

from esologs._generated.exceptions import GraphQLClientGraphQLMultiError
from esologs.client import Client
from esologs.user_auth import OAuth2Flow, UserToken


class TestOAuth2Configuration:
    """Test OAuth2 configuration detection.

    These tests help users identify if their OAuth2 client is properly
    configured with redirect URLs.
    """

    @pytest.fixture
    def oauth2_credentials(self):
        """Get OAuth2 credentials from environment."""
        client_id = os.environ.get("ESOLOGS_ID")
        client_secret = os.environ.get("ESOLOGS_SECRET")
        redirect_uri = os.environ.get(
            "ESOLOGS_REDIRECT_URI", "http://localhost:8765/callback"
        )

        return {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "has_credentials": bool(client_id and client_secret),
        }

    @pytest.mark.oauth2
    def test_oauth2_configuration_check(self, oauth2_credentials):
        """Check if OAuth2 is properly configured for testing."""
        if not oauth2_credentials["has_credentials"]:
            pytest.skip(
                "OAuth2 credentials not found. To run UserData tests:\n"
                "1. Set ESOLOGS_ID and ESOLOGS_SECRET environment variables\n"
                "2. Configure redirect URL in your ESO Logs app settings\n"
                "3. Optionally set ESOLOGS_REDIRECT_URI (default: http://localhost:8765/callback)"
            )

        # Inform about configuration
        logging.info("\n" + "=" * 60)
        logging.info("OAuth2 Configuration Detected:")
        logging.info(f"  Client ID: {oauth2_credentials['client_id'][:10]}...")
        logging.info(f"  Redirect URI: {oauth2_credentials['redirect_uri']}")
        logging.info("\nMake sure your ESO Logs app has this redirect URI configured!")
        logging.info("=" * 60)

    @pytest.mark.oauth2
    @pytest.mark.skipif(
        not os.environ.get("ESOLOGS_MANUAL_TEST"),
        reason="Set ESOLOGS_MANUAL_TEST=1 to run manual OAuth2 flow test",
    )
    def test_oauth2_flow_manual(self, oauth2_credentials):
        """Manual test for OAuth2 flow (requires user interaction).

        This test is skipped by default. To run it:
        1. Set ESOLOGS_MANUAL_TEST=1
        2. Ensure OAuth2 credentials are configured
        3. Be ready to authorize in your browser
        """
        if not oauth2_credentials["has_credentials"]:
            pytest.skip("OAuth2 credentials required for manual test")

        oauth_flow = OAuth2Flow(
            client_id=oauth2_credentials["client_id"],
            client_secret=oauth2_credentials["client_secret"],
            redirect_uri=oauth2_credentials["redirect_uri"],
            timeout=30,  # 30 second timeout for manual test
        )

        logging.info("\n" + "=" * 60)
        logging.info("Manual OAuth2 Flow Test")
        logging.info("A browser window will open for authorization...")
        logging.info("=" * 60)

        try:
            # This will open the browser and wait for authorization
            user_token = oauth_flow.authorize(
                scopes=["view-user-profile"], open_browser=True
            )

            assert isinstance(user_token, UserToken)
            assert user_token.access_token
            assert not user_token.is_expired

            logging.info("\n✅ OAuth2 flow successful!")
            logging.info(f"Token type: {user_token.token_type}")
            logging.info(f"Expires in: {user_token.expires_in} seconds")

        except Exception as e:
            pytest.fail(f"OAuth2 flow failed: {e}")


class TestUserDataIntegration:
    """Test UserData API integration.

    These tests demonstrate how the UserData methods would work with
    proper OAuth2 user authentication. In production, you would need
    to obtain a user access token through the OAuth2 flow.
    """

    @pytest.fixture
    async def mock_user_client(self):
        """Create a mock client configured for user authentication."""
        # In production, you would use a real user token obtained via OAuth2
        # Pass user_token to avoid warning about missing authentication
        mock_client = Client(
            url="https://www.esologs.com/api/v2/user",
            user_token="mock_user_token",  # This will set the Authorization header
        )

        # Mock the execute method to return fake user data
        mock_client.execute = AsyncMock()
        mock_client.get_data = lambda response: response

        yield mock_client

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self, mock_user_client):
        """Test successful user retrieval by ID."""
        # Mock response data
        mock_response = {
            "userData": {
                "user": {
                    "id": 12345,
                    "name": "MockUser",
                    "guilds": [
                        {
                            "id": 100,
                            "name": "Mock Guild",
                            "server": {
                                "name": "NA Megaserver",
                                "region": {"name": "North America"},
                            },
                        }
                    ],
                    "characters": [
                        {
                            "id": 200,
                            "name": "MockCharacter",
                            "server": {
                                "name": "NA Megaserver",
                                "region": {"name": "North America"},
                            },
                            "gameData": None,
                            "classID": 1,
                            "raceID": 1,
                            "hidden": False,
                        }
                    ],
                    "naDisplayName": "@MockUser",
                    "euDisplayName": None,
                }
            }
        }

        mock_user_client.execute.return_value = mock_response

        # Make the API call
        result = await mock_user_client.get_user_by_id(user_id=12345)

        # Verify the result
        assert result.user_data.user.id == 12345
        assert result.user_data.user.name == "MockUser"
        assert len(result.user_data.user.guilds) == 1
        assert result.user_data.user.guilds[0].name == "Mock Guild"
        assert len(result.user_data.user.characters) == 1
        assert result.user_data.user.characters[0].name == "MockCharacter"
        assert result.user_data.user.na_display_name == "@MockUser"

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, mock_user_client):
        """Test user not found scenario."""
        # Mock response with null user
        mock_response = {"userData": {"user": None}}

        mock_user_client.execute.return_value = mock_response

        # Make the API call
        result = await mock_user_client.get_user_by_id(user_id=99999)

        # Verify the result
        assert result.user_data.user is None

    @pytest.mark.asyncio
    async def test_get_current_user_success(self, mock_user_client):
        """Test successful current user retrieval."""
        # Mock response data
        mock_response = {
            "userData": {
                "currentUser": {
                    "id": 54321,
                    "name": "CurrentMockUser",
                    "guilds": [
                        {
                            "id": 101,
                            "name": "Guild One",
                            "server": {
                                "name": "NA Megaserver",
                                "region": {"name": "North America"},
                            },
                        },
                        {
                            "id": 102,
                            "name": "Guild Two",
                            "server": {
                                "name": "EU Megaserver",
                                "region": {"name": "Europe"},
                            },
                        },
                    ],
                    "characters": [],
                    "naDisplayName": "@CurrentMockUser",
                    "euDisplayName": "@CurrentMockUserEU",
                }
            }
        }

        mock_user_client.execute.return_value = mock_response

        # Make the API call
        result = await mock_user_client.get_current_user()

        # Verify the result
        assert result.user_data.current_user.id == 54321
        assert result.user_data.current_user.name == "CurrentMockUser"
        assert len(result.user_data.current_user.guilds) == 2
        assert result.user_data.current_user.guilds[0].name == "Guild One"
        assert result.user_data.current_user.guilds[1].name == "Guild Two"
        assert result.user_data.current_user.na_display_name == "@CurrentMockUser"
        assert result.user_data.current_user.eu_display_name == "@CurrentMockUserEU"

    @pytest.mark.asyncio
    async def test_get_current_user_no_auth(self, mock_user_client):
        """Test current user query without proper authentication."""
        # Mock an authentication error
        mock_user_client.execute.side_effect = GraphQLClientGraphQLMultiError(
            errors=[{"message": "Unauthorized: Invalid token"}], data=None
        )

        # Attempt to get current user
        with pytest.raises(GraphQLClientGraphQLMultiError) as exc_info:
            await mock_user_client.get_current_user()

        assert "Unauthorized" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_user_data_basic(self, mock_user_client):
        """Test basic userData query."""
        # Mock response data
        mock_response = {"userData": {"user": {"id": 1}}}

        mock_user_client.execute.return_value = mock_response

        # Make the API call
        result = await mock_user_client.get_user_data()

        # Verify the result
        assert result.user_data.user.id == 1

    @pytest.mark.asyncio
    async def test_user_without_guilds_or_characters(self, mock_user_client):
        """Test user with no guilds or characters."""
        # Mock response data
        mock_response = {
            "userData": {
                "user": {
                    "id": 77777,
                    "name": "NewUser",
                    "guilds": [],
                    "characters": [],
                    "naDisplayName": "@NewUser",
                    "euDisplayName": None,
                }
            }
        }

        mock_user_client.execute.return_value = mock_response

        # Make the API call
        result = await mock_user_client.get_user_by_id(user_id=77777)

        # Verify the result
        assert result.user_data.user.id == 77777
        assert result.user_data.user.name == "NewUser"
        assert len(result.user_data.user.guilds) == 0
        assert len(result.user_data.user.characters) == 0

    @pytest.mark.asyncio
    async def test_scope_restricted_fields(self, mock_user_client):
        """Test that scope-restricted fields may be None without proper scope."""
        # Mock response with restricted fields as None
        mock_response = {
            "userData": {
                "user": {
                    "id": 88888,
                    "name": "RestrictedUser",
                    "guilds": None,  # Requires view-user-profile scope
                    "characters": None,  # Requires view-user-profile scope
                    "naDisplayName": "@RestrictedUser",
                    "euDisplayName": None,
                }
            }
        }

        mock_user_client.execute.return_value = mock_response

        # Make the API call
        result = await mock_user_client.get_user_by_id(user_id=88888)

        # Verify the result
        assert result.user_data.user.id == 88888
        assert result.user_data.user.name == "RestrictedUser"
        assert result.user_data.user.guilds is None
        assert result.user_data.user.characters is None
        assert result.user_data.user.na_display_name == "@RestrictedUser"

    def test_client_endpoint_detection(self):
        """Test that client correctly identifies user endpoint."""
        # User endpoint
        user_client = Client(
            url="https://www.esologs.com/api/v2/user", user_token="user_token"
        )
        assert user_client.is_user_authenticated is True

        # Client endpoint
        client_client = Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": "Bearer client_token"},
        )
        assert client_client.is_user_authenticated is False


# Note: In a real application, you can now use the simplified OAuth2Flow class:
#
# from esologs import OAuth2Flow, Client
#
# # Create OAuth2 flow handler
# oauth_flow = OAuth2Flow(
#     client_id="your_client_id",
#     client_secret="your_client_secret",
#     redirect_uri="http://localhost:8765/callback"  # Must be registered in your ESO Logs app
# )
#
# # Authorize (opens browser automatically)
# user_token = oauth_flow.authorize(scopes=["view-user-profile"])
#
# # Use token with client
# async with Client(
#     url="https://www.esologs.com/api/v2/user",
#     user_token=user_token
# ) as client:
#     current_user = await client.get_current_user()
#     logging.info(f"Logged in as: {current_user.user_data.current_user.name}")
#
# For manual flow or custom implementations, you can still use:
# - generate_authorization_url()
# - exchange_authorization_code()
# - refresh_access_token()
