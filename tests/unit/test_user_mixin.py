"""Unit tests for UserMixin functionality."""

from unittest.mock import AsyncMock, Mock

import pytest

from esologs._generated.get_current_user import GetCurrentUser
from esologs._generated.get_user_by_id import GetUserById
from esologs._generated.get_user_data import GetUserData
from esologs.mixins.user import UserMixin


class MockClient(UserMixin):
    """Mock client that includes UserMixin."""

    def __init__(self):
        self.execute = AsyncMock()
        self.get_data = Mock()


class TestUserMixin:
    """Test UserMixin methods."""

    @pytest.fixture
    def client(self):
        """Create test client with UserMixin."""
        return MockClient()

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, client):
        """Test get_user_by_id method."""
        # Mock response
        mock_response = Mock()
        mock_data = {
            "userData": {
                "user": {
                    "id": 12345,
                    "name": "TestUser",
                    "guilds": [
                        {
                            "id": 100,
                            "name": "Test Guild",
                            "server": {
                                "name": "NA Megaserver",
                                "region": {"name": "North America"},
                            },
                        }
                    ],
                    "characters": [
                        {
                            "id": 200,
                            "name": "TestCharacter",
                            "server": {
                                "name": "NA Megaserver",
                                "region": {"name": "North America"},
                            },
                            "gameData": {"some": "data"},
                            "classID": 1,
                            "raceID": 1,
                            "hidden": False,
                        }
                    ],
                    "naDisplayName": "@TestUser",
                    "euDisplayName": None,
                }
            }
        }

        client.execute.return_value = mock_response
        client.get_data.return_value = mock_data

        # Call method
        result = await client.get_user_by_id(user_id=12345)

        # Verify call
        client.execute.assert_called_once()
        call_args = client.execute.call_args
        assert "getUserById" in call_args.kwargs["operation_name"]
        assert call_args.kwargs["variables"]["userId"] == 12345

        # Verify result type
        assert isinstance(result, GetUserById)
        assert result.user_data.user.id == 12345
        assert result.user_data.user.name == "TestUser"
        assert len(result.user_data.user.guilds) == 1
        assert result.user_data.user.guilds[0].name == "Test Guild"

    @pytest.mark.asyncio
    async def test_get_current_user(self, client):
        """Test get_current_user method."""
        # Mock response
        mock_response = Mock()
        mock_data = {
            "userData": {
                "currentUser": {
                    "id": 54321,
                    "name": "CurrentUser",
                    "guilds": [],
                    "characters": [],
                    "naDisplayName": "@CurrentUser",
                    "euDisplayName": "@CurrentUserEU",
                }
            }
        }

        client.execute.return_value = mock_response
        client.get_data.return_value = mock_data

        # Call method
        result = await client.get_current_user()

        # Verify call
        client.execute.assert_called_once()
        call_args = client.execute.call_args
        assert "getCurrentUser" in call_args.kwargs["operation_name"]
        assert call_args.kwargs["variables"] == {}

        # Verify result type
        assert isinstance(result, GetCurrentUser)
        assert result.user_data.current_user.id == 54321
        assert result.user_data.current_user.name == "CurrentUser"
        assert result.user_data.current_user.na_display_name == "@CurrentUser"
        assert result.user_data.current_user.eu_display_name == "@CurrentUserEU"

    @pytest.mark.asyncio
    async def test_get_user_data(self, client):
        """Test get_user_data method."""
        # Mock response
        mock_response = Mock()
        mock_data = {"userData": {"user": {"id": 1}}}

        client.execute.return_value = mock_response
        client.get_data.return_value = mock_data

        # Call method
        result = await client.get_user_data()

        # Verify call
        client.execute.assert_called_once()
        call_args = client.execute.call_args
        assert "getUserData" in call_args.kwargs["operation_name"]
        assert call_args.kwargs["variables"] == {}

        # Verify result type
        assert isinstance(result, GetUserData)
        assert result.user_data.user.id == 1

    def test_method_registration(self):
        """Test that methods are properly registered on the class."""
        # Verify methods exist
        assert hasattr(MockClient, "get_user_by_id")
        assert hasattr(MockClient, "get_current_user")
        assert hasattr(MockClient, "get_user_data")

        # Verify they're callable
        client = MockClient()
        assert callable(client.get_user_by_id)
        assert callable(client.get_current_user)
        assert callable(client.get_user_data)

    def test_method_docstrings(self):
        """Test that methods have proper docstrings."""
        client = MockClient()

        # Check docstrings exist and contain key information
        assert client.get_user_by_id.__doc__ is not None
        assert "OAuth2 user authentication" in client.get_user_by_id.__doc__
        assert "view-user-profile" in client.get_user_by_id.__doc__

        assert client.get_current_user.__doc__ is not None
        assert "/api/v2/user endpoint" in client.get_current_user.__doc__
        assert "Authorization Code flow" in client.get_current_user.__doc__

        assert client.get_user_data.__doc__ is not None
        assert "testing" in client.get_user_data.__doc__
