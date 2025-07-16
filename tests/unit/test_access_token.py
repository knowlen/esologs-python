"""Unit tests for access token functionality."""

import os
from unittest.mock import Mock, patch

import pytest
from requests import Response

from esologs.auth import get_access_token


class TestGetAccessToken:
    """Test the get_access_token function."""

    def test_get_access_token_with_parameters(self):
        """Test getting access token with explicit parameters."""
        with patch("esologs.auth.requests.post") as mock_post:
            mock_response = Mock(spec=Response)
            mock_response.status_code = 200
            mock_response.json.return_value = {"access_token": "test_token"}
            mock_post.return_value = mock_response

            token = get_access_token("test_id", "test_secret")

            assert token == "test_token"
            mock_post.assert_called_once()

    def test_get_access_token_with_env_vars(self):
        """Test getting access token using environment variables."""
        with patch.dict(
            os.environ, {"ESOLOGS_ID": "env_id", "ESOLOGS_SECRET": "env_secret"}
        ):
            with patch("esologs.auth.requests.post") as mock_post:
                mock_response = Mock(spec=Response)
                mock_response.status_code = 200
                mock_response.json.return_value = {"access_token": "env_token"}
                mock_post.return_value = mock_response

                token = get_access_token()

                assert token == "env_token"

    def test_get_access_token_missing_client_id(self):
        """Test error when client ID is missing."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Client ID not provided"):
                get_access_token(None, "secret")

    def test_get_access_token_missing_client_secret(self):
        """Test error when client secret is missing."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Client secret not provided"):
                get_access_token("id", None)

    def test_get_access_token_http_error(self):
        """Test error handling for HTTP errors."""
        with patch("esologs.auth.requests.post") as mock_post:
            mock_response = Mock(spec=Response)
            mock_response.status_code = 401
            mock_response.text = "Unauthorized"
            mock_post.return_value = mock_response

            with pytest.raises(Exception, match="OAuth request failed with status 401"):
                get_access_token("test_id", "test_secret")

    def test_get_access_token_missing_token_in_response(self):
        """Test error when access token is missing from response."""
        with patch("esologs.auth.requests.post") as mock_post:
            mock_response = Mock(spec=Response)
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_post.return_value = mock_response

            with pytest.raises(Exception, match="Access token not found in response"):
                get_access_token("test_id", "test_secret")
