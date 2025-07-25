"""Integration tests for async OAuth2 functionality.

These tests verify the async OAuth2 implementation works correctly.
They use mocks to avoid requiring real user interaction.
"""

import asyncio
import time
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from esologs.user_auth import (
    AsyncOAuth2Flow,
    UserToken,
    exchange_authorization_code_async,
    load_token_from_file_async,
    refresh_access_token_async,
    save_token_to_file_async,
)


class TestAsyncOAuth2Flow:
    """Test AsyncOAuth2Flow class functionality."""

    @pytest.fixture
    def mock_oauth_flow(self):
        """Create AsyncOAuth2Flow with mocked server."""
        flow = AsyncOAuth2Flow(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost:8765/callback",
            timeout=5,  # Short timeout for tests
        )
        return flow

    @pytest.mark.asyncio
    async def test_async_oauth_flow_initialization(self, mock_oauth_flow):
        """Test AsyncOAuth2Flow initialization."""
        assert mock_oauth_flow.client_id == "test_client_id"
        assert mock_oauth_flow.client_secret == "test_client_secret"
        assert mock_oauth_flow.redirect_uri == "http://localhost:8765/callback"
        assert mock_oauth_flow.port == 8765
        assert mock_oauth_flow.timeout == 5

    @pytest.mark.asyncio
    async def test_async_oauth_flow_port_extraction(self):
        """Test port extraction from redirect URI."""
        # With explicit port
        flow1 = AsyncOAuth2Flow(
            client_id="test",
            client_secret="secret",
            redirect_uri="http://localhost:9999/callback",
        )
        assert flow1.port == 9999

        # Default HTTP port
        flow2 = AsyncOAuth2Flow(
            client_id="test",
            client_secret="secret",
            redirect_uri="http://localhost/callback",
        )
        assert flow2.port == 80

        # Default HTTPS port
        flow3 = AsyncOAuth2Flow(
            client_id="test",
            client_secret="secret",
            redirect_uri="https://localhost/callback",
        )
        assert flow3.port == 443

    @pytest.mark.asyncio
    async def test_async_authorization_url_generation(self, mock_oauth_flow):
        """Test authorization URL generation with state."""
        auth_url = mock_oauth_flow._generate_authorization_url(["view-user-profile"])

        assert "https://www.esologs.com/oauth/authorize" in auth_url
        assert "response_type=code" in auth_url
        assert "client_id=test_client_id" in auth_url
        assert "redirect_uri=http%3A%2F%2Flocalhost%3A8765%2Fcallback" in auth_url
        assert "scope=view-user-profile" in auth_url
        assert "state=" in auth_url

        # Extract and verify state
        state = auth_url.split("state=")[1]
        assert len(state) >= 32  # Should be a secure random string
        assert mock_oauth_flow.state == state

    @pytest.mark.asyncio
    async def test_state_validation(self, mock_oauth_flow):
        """Test CSRF state validation."""
        # Generate a state
        mock_oauth_flow._generate_authorization_url(["view-user-profile"])
        valid_state = mock_oauth_flow.state

        # Valid state should pass
        assert mock_oauth_flow._validate_state(valid_state) is True

        # Invalid state should fail
        assert mock_oauth_flow._validate_state("invalid_state") is False

        # No state should fail
        assert mock_oauth_flow._validate_state(None) is False

    @pytest.mark.asyncio
    @patch("webbrowser.open")
    @patch("esologs.user_auth.exchange_authorization_code_async")
    async def test_authorize_with_mock_server(
        self, mock_exchange, mock_browser, mock_oauth_flow
    ):
        """Test authorize method with mocked server response."""
        # Mock the token exchange
        mock_token = UserToken(
            access_token="mock_access_token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="mock_refresh_token",
            scope="view-user-profile",
        )
        mock_exchange.return_value = mock_token

        # Mock the server to simulate immediate callback
        async def mock_handle_request(request):
            # Simulate the OAuth callback
            if request.url.path == "/callback":
                # Get the state from the flow
                state = mock_oauth_flow.state
                return httpx.Response(
                    302,
                    headers={
                        "Location": f"http://localhost:8765/callback?code=test_code&state={state}"
                    },
                )
            return httpx.Response(404)

        # Create a mock server that immediately provides the code
        mock_oauth_flow._handle_request = AsyncMock(side_effect=mock_handle_request)

        # Patch the callback server to immediately provide the auth code
        def mock_run_callback_server():
            # Simulate receiving the callback immediately
            mock_oauth_flow._auth_code = "test_code"
            mock_oauth_flow._auth_state = mock_oauth_flow.state
            mock_oauth_flow.authorization_code = "test_code"
            # Don't set the event here since we're in a sync context

        with patch.object(
            mock_oauth_flow, "_run_callback_server", mock_run_callback_server
        ):
            # Run authorize
            token = await mock_oauth_flow.authorize(
                scopes=["view-user-profile"], open_browser=False
            )

        # Verify browser was not opened (open_browser=False)
        mock_browser.assert_not_called()

        # Verify token exchange was called
        mock_exchange.assert_called_once_with(
            client_id="test_client_id",
            client_secret="test_client_secret",
            code="test_code",
            redirect_uri="http://localhost:8765/callback",
        )

        # Verify returned token
        assert token == mock_token


class TestAsyncTokenExchange:
    """Test async token exchange functions."""

    @pytest.mark.asyncio
    async def test_exchange_authorization_code_async_success(self, httpx_mock):
        """Test successful async authorization code exchange."""
        # Mock successful response
        httpx_mock.add_response(
            url="https://www.esologs.com/oauth/token",
            method="POST",
            json={
                "access_token": "new_access_token",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "new_refresh_token",
                "scope": "view-user-profile",
            },
            status_code=200,
        )

        token = await exchange_authorization_code_async(
            client_id="test_client",
            client_secret="test_secret",
            code="auth_code_123",
            redirect_uri="http://localhost:8000/callback",
        )

        assert isinstance(token, UserToken)
        assert token.access_token == "new_access_token"
        assert token.refresh_token == "new_refresh_token"
        assert token.scope == "view-user-profile"
        assert token.expires_in == 3600

    @pytest.mark.asyncio
    async def test_exchange_authorization_code_async_failure(self, httpx_mock):
        """Test failed async authorization code exchange."""
        # Mock error response
        httpx_mock.add_response(
            url="https://www.esologs.com/oauth/token",
            method="POST",
            json={
                "error": "invalid_grant",
                "error_description": "Invalid authorization code",
            },
            status_code=400,
        )

        with pytest.raises(Exception) as exc_info:
            await exchange_authorization_code_async(
                client_id="test_client",
                client_secret="test_secret",
                code="invalid_code",
                redirect_uri="http://localhost:8000/callback",
            )

        assert "Token exchange failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_refresh_access_token_async_success(self, httpx_mock):
        """Test successful async token refresh."""
        # Mock successful response
        httpx_mock.add_response(
            url="https://www.esologs.com/oauth/token",
            method="POST",
            json={
                "access_token": "refreshed_access_token",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "new_refresh_token",
            },
            status_code=200,
        )

        token = await refresh_access_token_async(
            client_id="test_client",
            client_secret="test_secret",
            refresh_token="old_refresh_token",
        )

        assert isinstance(token, UserToken)
        assert token.access_token == "refreshed_access_token"
        assert token.refresh_token == "new_refresh_token"
        assert token.expires_in == 3600

    @pytest.mark.asyncio
    async def test_refresh_access_token_async_failure(self, httpx_mock):
        """Test failed async token refresh."""
        # Mock error response
        httpx_mock.add_response(
            url="https://www.esologs.com/oauth/token",
            method="POST",
            text="Invalid refresh_token",
            status_code=400,
        )

        with pytest.raises(Exception) as exc_info:
            await refresh_access_token_async(
                client_id="test_client",
                client_secret="test_secret",
                refresh_token="invalid_refresh_token",
            )

        assert "Invalid or expired refresh token" in str(exc_info.value)


class TestAsyncTokenPersistence:
    """Test async token file operations."""

    @pytest.mark.asyncio
    async def test_save_and_load_token_async(self, tmp_path):
        """Test async token save and load operations."""
        # Create token
        original_token = UserToken(
            access_token="async_test_token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="async_refresh_token",
            scope="view-user-profile",
            created_at=time.time(),
        )

        # Save token asynchronously
        token_file = tmp_path / "async_token.json"
        await save_token_to_file_async(original_token, str(token_file))

        # Verify file was created with correct permissions
        import os

        assert token_file.exists()
        file_stats = os.stat(str(token_file))
        assert oct(file_stats.st_mode & 0o777) == "0o600"

        # Load token asynchronously
        loaded_token = await load_token_from_file_async(str(token_file))

        assert loaded_token is not None
        assert loaded_token.access_token == original_token.access_token
        assert loaded_token.refresh_token == original_token.refresh_token
        assert loaded_token.scope == original_token.scope
        assert loaded_token.expires_in == original_token.expires_in
        assert loaded_token.created_at == original_token.created_at

    @pytest.mark.asyncio
    async def test_load_nonexistent_token_async(self, tmp_path):
        """Test loading non-existent token file returns None."""
        token_file = tmp_path / "nonexistent_async.json"
        token = await load_token_from_file_async(str(token_file))
        assert token is None

    @pytest.mark.asyncio
    async def test_load_invalid_json_async(self, tmp_path):
        """Test loading invalid JSON file returns None."""
        token_file = tmp_path / "invalid_async.json"

        # Write invalid JSON using aiofiles
        import aiofiles

        async with aiofiles.open(str(token_file), "w") as f:
            await f.write("invalid json content")

        token = await load_token_from_file_async(str(token_file))
        assert token is None

    @pytest.mark.asyncio
    async def test_concurrent_token_operations(self, tmp_path):
        """Test concurrent async token operations."""
        # Create multiple tokens
        tokens = []
        for i in range(5):
            token = UserToken(
                access_token=f"concurrent_token_{i}",
                token_type="Bearer",
                expires_in=3600,
                refresh_token=f"concurrent_refresh_{i}",
            )
            tokens.append(token)

        # Save all tokens concurrently
        save_tasks = []
        for i, token in enumerate(tokens):
            token_file = tmp_path / f"concurrent_token_{i}.json"
            task = save_token_to_file_async(token, str(token_file))
            save_tasks.append(task)

        await asyncio.gather(*save_tasks)

        # Load all tokens concurrently
        load_tasks = []
        for i in range(5):
            token_file = tmp_path / f"concurrent_token_{i}.json"
            task = load_token_from_file_async(str(token_file))
            load_tasks.append(task)

        loaded_tokens = await asyncio.gather(*load_tasks)

        # Verify all tokens were saved and loaded correctly
        for i, loaded_token in enumerate(loaded_tokens):
            assert loaded_token is not None
            assert loaded_token.access_token == f"concurrent_token_{i}"
            assert loaded_token.refresh_token == f"concurrent_refresh_{i}"


class TestAsyncIntegration:
    """Integration tests combining async OAuth2 with Client."""

    @pytest.mark.asyncio
    async def test_async_oauth_with_client(self, httpx_mock):
        """Test using async OAuth2 token with Client."""
        # Mock token exchange
        httpx_mock.add_response(
            url="https://www.esologs.com/oauth/token",
            method="POST",
            json={
                "access_token": "integration_test_token",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "integration_refresh_token",
                "scope": "view-user-profile",
            },
            status_code=200,
        )

        # Exchange code for token
        token = await exchange_authorization_code_async(
            client_id="test_client",
            client_secret="test_secret",
            code="test_code",
            redirect_uri="http://localhost:8000/callback",
        )

        # Verify token can be used with Client
        from esologs.client import Client

        async with Client(
            url="https://www.esologs.com/api/v2/user", user_token=token
        ) as client:
            assert client.is_user_authenticated is True
            assert "Bearer integration_test_token" in client.headers.get(
                "Authorization", ""
            )

    @pytest.mark.asyncio
    async def test_async_token_refresh_workflow(self, tmp_path, httpx_mock):
        """Test complete async token refresh workflow."""
        # Create expired token
        expired_token = UserToken(
            access_token="expired_token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="valid_refresh_token",
            created_at=time.time() - 7200,  # 2 hours ago
        )

        # Save expired token
        token_file = tmp_path / "workflow_token.json"
        await save_token_to_file_async(expired_token, str(token_file))

        # Load token and check if expired
        loaded_token = await load_token_from_file_async(str(token_file))
        assert loaded_token is not None
        assert loaded_token.is_expired is True

        # Mock refresh response
        httpx_mock.add_response(
            url="https://www.esologs.com/oauth/token",
            method="POST",
            json={
                "access_token": "fresh_access_token",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "fresh_refresh_token",
            },
            status_code=200,
        )

        # Refresh token
        new_token = await refresh_access_token_async(
            client_id="test_client",
            client_secret="test_secret",
            refresh_token=loaded_token.refresh_token,
        )

        # Save refreshed token
        await save_token_to_file_async(new_token, str(token_file))

        # Verify new token is not expired
        final_token = await load_token_from_file_async(str(token_file))
        assert final_token is not None
        assert final_token.is_expired is False
        assert final_token.access_token == "fresh_access_token"
