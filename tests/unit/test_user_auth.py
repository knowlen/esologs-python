"""Unit tests for OAuth2 user authentication module."""

import json
import time

import pytest
import responses

from esologs.user_auth import (
    UserToken,
    exchange_authorization_code,
    generate_authorization_url,
    load_token_from_file,
    refresh_access_token,
    save_token_to_file,
)


class TestUserToken:
    """Test UserToken class functionality."""

    def test_user_token_creation(self):
        """Test creating a UserToken with all fields."""
        token = UserToken(
            access_token="test_access_token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="test_refresh_token",
            scope="view-user-profile",
        )

        assert token.access_token == "test_access_token"
        assert token.token_type == "Bearer"
        assert token.expires_in == 3600
        assert token.refresh_token == "test_refresh_token"
        assert token.scope == "view-user-profile"
        assert token.created_at is not None

    def test_user_token_from_response(self):
        """Test creating UserToken from OAuth2 response."""
        response_data = {
            "access_token": "response_token",
            "token_type": "Bearer",
            "expires_in": 7200,
            "refresh_token": "response_refresh",
            "scope": "view-user-profile",
        }

        token = UserToken.from_response(response_data)

        assert token.access_token == "response_token"
        assert token.token_type == "Bearer"
        assert token.expires_in == 7200
        assert token.refresh_token == "response_refresh"
        assert token.scope == "view-user-profile"

    def test_token_expiration_check(self):
        """Test token expiration checking."""
        # Create expired token
        expired_token = UserToken(
            access_token="expired",
            token_type="Bearer",
            expires_in=3600,
            created_at=time.time() - 4000,  # Created over an hour ago
        )
        assert expired_token.is_expired is True

        # Create valid token
        valid_token = UserToken(
            access_token="valid",
            token_type="Bearer",
            expires_in=3600,
            created_at=time.time() - 1000,  # Created less than an hour ago
        )
        assert valid_token.is_expired is False

        # Token without expires_in
        no_expiry_token = UserToken(
            access_token="no_expiry",
            token_type="Bearer",
            expires_in=None,
        )
        assert no_expiry_token.is_expired is False


class TestAuthorizationUrl:
    """Test OAuth2 authorization URL generation."""

    def test_basic_authorization_url(self):
        """Test generating basic authorization URL."""
        url = generate_authorization_url(
            client_id="test_client_id",
            redirect_uri="http://localhost:8000/callback",
        )

        assert "https://www.esologs.com/oauth/authorize" in url
        assert "response_type=code" in url
        assert "client_id=test_client_id" in url
        assert "redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcallback" in url
        assert "scope=view-user-profile" in url

    def test_authorization_url_with_custom_scopes(self):
        """Test authorization URL with custom scopes."""
        url = generate_authorization_url(
            client_id="test_client_id",
            redirect_uri="http://localhost:8000/callback",
            scopes=["view-user-profile", "read-reports"],
        )

        assert "scope=view-user-profile+read-reports" in url

    def test_authorization_url_with_state(self):
        """Test authorization URL with state parameter."""
        url = generate_authorization_url(
            client_id="test_client_id",
            redirect_uri="http://localhost:8000/callback",
            state="random_state_123",
        )

        assert "state=random_state_123" in url


class TestTokenExchange:
    """Test OAuth2 token exchange functionality."""

    @responses.activate
    def test_successful_token_exchange(self):
        """Test successful authorization code exchange."""
        # Mock successful response
        responses.add(
            responses.POST,
            "https://www.esologs.com/oauth/token",
            json={
                "access_token": "new_access_token",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "new_refresh_token",
                "scope": "view-user-profile",
            },
            status=200,
        )

        token = exchange_authorization_code(
            client_id="test_client",
            client_secret="test_secret",
            code="auth_code_123",
            redirect_uri="http://localhost:8000/callback",
        )

        assert token.access_token == "new_access_token"
        assert token.refresh_token == "new_refresh_token"
        assert token.scope == "view-user-profile"

        # Verify request
        assert len(responses.calls) == 1
        request = responses.calls[0].request
        assert request.headers["Authorization"].startswith("Basic ")
        assert "grant_type=authorization_code" in request.body
        assert "code=auth_code_123" in request.body

    @responses.activate
    def test_failed_token_exchange(self):
        """Test failed authorization code exchange."""
        # Mock error response
        responses.add(
            responses.POST,
            "https://www.esologs.com/oauth/token",
            json={"error": "invalid_grant"},
            status=400,
        )

        with pytest.raises(Exception) as exc_info:
            exchange_authorization_code(
                client_id="test_client",
                client_secret="test_secret",
                code="invalid_code",
                redirect_uri="http://localhost:8000/callback",
            )

        assert "Token exchange failed" in str(exc_info.value)


class TestTokenRefresh:
    """Test OAuth2 token refresh functionality."""

    @responses.activate
    def test_successful_token_refresh(self):
        """Test successful token refresh."""
        # Mock successful response
        responses.add(
            responses.POST,
            "https://www.esologs.com/oauth/token",
            json={
                "access_token": "refreshed_access_token",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "new_refresh_token",
            },
            status=200,
        )

        token = refresh_access_token(
            client_id="test_client",
            client_secret="test_secret",
            refresh_token="old_refresh_token",
        )

        assert token.access_token == "refreshed_access_token"
        assert token.refresh_token == "new_refresh_token"

        # Verify request
        assert len(responses.calls) == 1
        request = responses.calls[0].request
        assert "grant_type=refresh_token" in request.body
        assert "refresh_token=old_refresh_token" in request.body

    @responses.activate
    def test_failed_token_refresh(self):
        """Test failed token refresh."""
        # Mock error response
        responses.add(
            responses.POST,
            "https://www.esologs.com/oauth/token",
            json={"error": "invalid_refresh_token"},
            status=400,
        )

        with pytest.raises(Exception) as exc_info:
            refresh_access_token(
                client_id="test_client",
                client_secret="test_secret",
                refresh_token="invalid_refresh_token",
            )

        assert "Token refresh failed" in str(exc_info.value)


class TestTokenPersistence:
    """Test token save/load functionality."""

    def test_save_and_load_token(self, tmp_path):
        """Test saving and loading token from file."""
        # Create token
        original_token = UserToken(
            access_token="persist_token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="persist_refresh",
            scope="view-user-profile",
        )

        # Save to file
        token_file = tmp_path / "test_token.json"
        save_token_to_file(original_token, str(token_file))

        # Load from file
        loaded_token = load_token_from_file(str(token_file))

        assert loaded_token is not None
        assert loaded_token.access_token == original_token.access_token
        assert loaded_token.refresh_token == original_token.refresh_token
        assert loaded_token.scope == original_token.scope
        assert loaded_token.expires_in == original_token.expires_in

    def test_load_nonexistent_token_file(self, tmp_path):
        """Test loading from non-existent file returns None."""
        token_file = tmp_path / "nonexistent.json"
        token = load_token_from_file(str(token_file))
        assert token is None

    def test_load_invalid_token_file(self, tmp_path):
        """Test loading from invalid JSON file returns None."""
        token_file = tmp_path / "invalid.json"
        token_file.write_text("invalid json content")

        token = load_token_from_file(str(token_file))
        assert token is None

    def test_load_incomplete_token_file(self, tmp_path):
        """Test loading from incomplete token file still works with defaults."""
        token_file = tmp_path / "incomplete.json"
        token_file.write_text(json.dumps({"access_token": "only_this"}))

        token = load_token_from_file(str(token_file))
        assert token is not None
        assert token.access_token == "only_this"
        assert token.token_type == "Bearer"  # default
        assert token.expires_in == 3600  # default
