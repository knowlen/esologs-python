"""OAuth2 user authentication module for ESO Logs API.

This module provides OAuth2 Authorization Code flow authentication for accessing
user-specific ESO Logs API endpoints. It handles the full OAuth2 flow including
authorization URL generation, code exchange, and token refresh.

The Authorization Code flow is required for accessing user-specific data such as:
- Current user profile (currentUser)
- User guilds and characters
- Any data requiring the "view-user-profile" scope
"""

import base64
import json
import logging
import time
from dataclasses import dataclass
from typing import Dict, List, Optional
from urllib.parse import urlencode

import requests


@dataclass
class UserToken:
    """Container for OAuth2 user tokens."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    created_at: Optional[float] = None

    def __post_init__(self) -> None:
        """Set creation time if not provided."""
        if self.created_at is None:
            self.created_at = time.time()

    @property
    def is_expired(self) -> bool:
        """Check if the token has expired."""
        if self.expires_in is None or self.created_at is None:
            return False
        return time.time() > (
            self.created_at + self.expires_in - 60
        )  # 60 second buffer

    @classmethod
    def from_response(cls, response_data: Dict) -> "UserToken":
        """Create UserToken from OAuth2 token response."""
        return cls(
            access_token=response_data["access_token"],
            token_type=response_data.get("token_type", "Bearer"),
            expires_in=response_data.get("expires_in", 3600),
            refresh_token=response_data.get("refresh_token"),
            scope=response_data.get("scope"),
        )


def generate_authorization_url(
    client_id: str,
    redirect_uri: str,
    scopes: Optional[List[str]] = None,
    state: Optional[str] = None,
) -> str:
    """Generate OAuth2 authorization URL for user authentication.

    Args:
        client_id: ESO Logs OAuth2 client ID
        redirect_uri: Callback URL registered with your ESO Logs application
        scopes: List of OAuth2 scopes (defaults to ["view-user-profile"])
        state: Optional state parameter for CSRF protection

    Returns:
        Authorization URL to redirect the user to
    """
    base_url = "https://www.esologs.com/oauth/authorize"

    if scopes is None:
        scopes = ["view-user-profile"]

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes),
    }

    if state:
        params["state"] = state

    return f"{base_url}?{urlencode(params)}"


def exchange_authorization_code(
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: str,
) -> UserToken:
    """Exchange authorization code for access token.

    Args:
        client_id: ESO Logs OAuth2 client ID
        client_secret: ESO Logs OAuth2 client secret
        code: Authorization code from callback
        redirect_uri: Same redirect URI used in authorization request

    Returns:
        UserToken containing access token and refresh token

    Raises:
        Exception: If token exchange fails
    """
    token_url = "https://www.esologs.com/oauth/token"

    # Prepare Basic auth header
    auth_str = f"{client_id}:{client_secret}"
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }

    logging.debug("Exchanging authorization code for access token")

    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        token_data = response.json()
        logging.debug("Successfully obtained user access token")
        return UserToken.from_response(token_data)
    else:
        logging.error(f"Token exchange failed with status {response.status_code}")
        # Sanitize error response to prevent credential exposure
        error_msg = response.text
        if "client" in error_msg.lower():
            error_msg = "Authentication failed. Check client credentials."
        raise Exception(
            f"Token exchange failed with status {response.status_code}: {error_msg}"
        )


def refresh_access_token(
    client_id: str,
    client_secret: str,
    refresh_token: str,
) -> UserToken:
    """Refresh an expired access token using refresh token.

    Args:
        client_id: ESO Logs OAuth2 client ID
        client_secret: ESO Logs OAuth2 client secret
        refresh_token: Refresh token from previous token response

    Returns:
        New UserToken with refreshed access token

    Raises:
        Exception: If token refresh fails
    """
    token_url = "https://www.esologs.com/oauth/token"

    # Prepare Basic auth header
    auth_str = f"{client_id}:{client_secret}"
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    logging.debug("Refreshing access token")

    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        token_data = response.json()
        logging.debug("Successfully refreshed access token")
        return UserToken.from_response(token_data)
    else:
        logging.error(f"Token refresh failed with status {response.status_code}")
        raise Exception(
            f"Token refresh failed with status {response.status_code}: {response.text}"
        )


def save_token_to_file(token: UserToken, filepath: str = ".esologs_token.json") -> None:
    """Save user token to file for persistence.

    Args:
        token: UserToken to save
        filepath: Path to save token file (default: .esologs_token.json)
    """
    token_data = {
        "access_token": token.access_token,
        "token_type": token.token_type,
        "expires_in": token.expires_in,
        "refresh_token": token.refresh_token,
        "scope": token.scope,
        "created_at": token.created_at,
    }

    with open(filepath, "w") as f:
        json.dump(token_data, f, indent=2)

    logging.info(f"Token saved to {filepath}")


def load_token_from_file(filepath: str = ".esologs_token.json") -> Optional[UserToken]:
    """Load user token from file.

    Args:
        filepath: Path to token file (default: .esologs_token.json)

    Returns:
        UserToken if file exists and is valid, None otherwise
    """
    try:
        with open(filepath) as f:
            token_data = json.load(f)

        return UserToken(
            access_token=token_data["access_token"],
            token_type=token_data.get("token_type", "Bearer"),
            expires_in=token_data.get("expires_in", 3600),
            refresh_token=token_data.get("refresh_token"),
            scope=token_data.get("scope"),
            created_at=token_data.get("created_at", time.time()),
        )
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None


# Example usage for documentation
if __name__ == "__main__":
    # This example shows the OAuth2 flow

    # Step 1: Generate authorization URL
    auth_url = generate_authorization_url(
        client_id="your_client_id",
        redirect_uri="http://localhost:8000/callback",
        scopes=["view-user-profile"],
        state="random_state_string",
    )

    # Step 2: User authorizes and is redirected back with code
    # Example callback: http://localhost:8000/callback?code=abc123&state=random_state_string

    # Step 3: Exchange code for token
    # token = exchange_authorization_code(
    #     client_id="your_client_id",
    #     client_secret="your_client_secret",
    #     code="abc123",
    #     redirect_uri="http://localhost:8000/callback"
    # )

    # Step 4: Use token for API requests
    # Client will automatically handle user tokens
