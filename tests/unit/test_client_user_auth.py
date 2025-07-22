"""Unit tests for Client user authentication support."""

from unittest.mock import patch

import pytest

from esologs.client import Client
from esologs.user_auth import UserToken


class TestClientUserAuth:
    """Test Client's user authentication features."""

    def test_client_with_string_token(self):
        """Test creating client with string access token."""
        token = "test_access_token_123"

        client = Client(url="https://www.esologs.com/api/v2/user", user_token=token)

        assert client.headers["Authorization"] == "Bearer test_access_token_123"
        assert client.is_user_authenticated is True

    def test_client_with_user_token_object(self):
        """Test creating client with UserToken object."""
        user_token = UserToken(
            access_token="token_from_object",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="refresh_123",
        )

        client = Client(
            url="https://www.esologs.com/api/v2/user", user_token=user_token
        )

        assert client.headers["Authorization"] == "Bearer token_from_object"
        assert client.is_user_authenticated is True

    def test_client_with_expired_token_warning(self):
        """Test that expired token triggers warning."""
        # Create expired token
        expired_token = UserToken(
            access_token="expired_token",
            token_type="Bearer",
            expires_in=3600,
            created_at=0,  # Very old timestamp
        )

        with pytest.warns(UserWarning, match="UserToken appears to be expired"):
            client = Client(
                url="https://www.esologs.com/api/v2/user", user_token=expired_token
            )

        # Token is still set despite being expired
        assert client.headers["Authorization"] == "Bearer expired_token"

    def test_client_user_endpoint_without_token_warning(self):
        """Test warning when using user endpoint without auth."""
        with pytest.warns(
            UserWarning, match="Using /api/v2/user endpoint without user authentication"
        ):
            client = Client(
                url="https://www.esologs.com/api/v2/user",
                headers={"Authorization": "Bearer client_token"},
            )

        assert client.is_user_authenticated is True

    def test_client_endpoint_detection(self):
        """Test endpoint type detection."""
        # Client endpoint
        client1 = Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": "Bearer token"},
        )
        assert client1.is_user_authenticated is False

        # User endpoint
        client2 = Client(
            url="https://www.esologs.com/api/v2/user", user_token="user_token"
        )
        assert client2.is_user_authenticated is True

    def test_client_preserves_existing_headers(self):
        """Test that user token doesn't override other headers."""
        headers = {"X-Custom-Header": "custom_value", "User-Agent": "Test/1.0"}

        client = Client(
            url="https://www.esologs.com/api/v2/user",
            headers=headers,
            user_token="test_token",
        )

        assert client.headers["Authorization"] == "Bearer test_token"
        assert client.headers["X-Custom-Header"] == "custom_value"
        assert client.headers["User-Agent"] == "Test/1.0"

    def test_client_token_precedence(self):
        """Test that user_token takes precedence over headers auth."""
        client = Client(
            url="https://www.esologs.com/api/v2/user",
            headers={"Authorization": "Bearer old_token"},
            user_token="new_token",
        )

        assert client.headers["Authorization"] == "Bearer new_token"

    @patch("esologs.client.warnings")
    def test_no_warnings_for_client_endpoint(self, mock_warnings):
        """Test no warnings for normal client endpoint usage."""
        client = Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": "Bearer client_token"},
        )

        # Should not have any warnings
        mock_warnings.warn.assert_not_called()
        assert client.is_user_authenticated is False
