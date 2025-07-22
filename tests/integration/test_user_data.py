"""Integration tests for UserData API methods.

Note: These tests mock the OAuth2 user authentication since we cannot
perform real user authentication in automated tests.
"""

from unittest.mock import AsyncMock

import pytest

from esologs._generated.exceptions import GraphQLClientGraphQLMultiError
from esologs.client import Client


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
        mock_client = Client(
            url="https://www.esologs.com/api/v2/user",
            headers={"Authorization": "Bearer mock_user_token"},
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


# Note: In a real application, you would need to:
# 1. Implement a web server to handle OAuth2 callbacks
# 2. Use generate_authorization_url() to create the auth URL
# 3. Handle the callback and extract the authorization code
# 4. Use exchange_authorization_code() to get the access token
# 5. Use the access token with the /api/v2/user endpoint
#
# Example flow (not runnable in tests):
#
# from esologs.user_auth import generate_authorization_url, exchange_authorization_code
#
# # Step 1: Generate auth URL
# auth_url = generate_authorization_url(
#     client_id="your_client_id",
#     redirect_uri="http://localhost:8000/callback",
#     scopes=["view-user-profile"]
# )
# Visit: {auth_url}
#
# # Step 2: User authorizes and is redirected to callback
# # Extract 'code' from callback URL parameters
#
# # Step 3: Exchange code for token
# user_token = exchange_authorization_code(
#     client_id="your_client_id",
#     client_secret="your_client_secret",
#     code="authorization_code_from_callback",
#     redirect_uri="http://localhost:8000/callback"
# )
#
# # Step 4: Use token with client
# async with Client(
#     url="https://www.esologs.com/api/v2/user",
#     user_token=user_token
# ) as client:
#     current_user = await client.get_current_user()
#     Logged in as: {current_user.user_data.current_user.name}
