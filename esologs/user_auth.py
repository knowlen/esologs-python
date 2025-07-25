"""OAuth2 user authentication module for ESO Logs API.

This module provides OAuth2 Authorization Code flow authentication for accessing
user-specific ESO Logs API endpoints. It handles the full OAuth2 flow including
authorization URL generation, code exchange, and token refresh.

The Authorization Code flow is required for accessing user-specific data such as:
- Current user profile (currentUser)
- User guilds and characters
- Any data requiring the "view-user-profile" scope

Both synchronous and asynchronous versions are provided:

Synchronous functions:
- generate_authorization_url()
- exchange_authorization_code()
- refresh_access_token()
- save_token_to_file()
- load_token_from_file()
- OAuth2Flow class

Asynchronous functions:
- exchange_authorization_code_async()
- refresh_access_token_async()
- save_token_to_file_async()
- load_token_from_file_async()
- AsyncOAuth2Flow class

Example (Sync):
    oauth_flow = OAuth2Flow(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )
    user_token = oauth_flow.authorize()

Example (Async):
    oauth_flow = AsyncOAuth2Flow(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )
    user_token = await oauth_flow.authorize()
"""

import asyncio
import base64
import json
import logging
import os
import secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List, Literal, Optional
from urllib.parse import parse_qs, urlencode, urlparse

import aiofiles
import httpx
import requests
from pydantic import Field

from esologs._generated.base_model import BaseModel

# Constants
DEFAULT_TOKEN_EXPIRY = 3600
DEFAULT_TOKEN_TYPE: Literal["Bearer"] = "Bearer"
TOKEN_EXPIRY_BUFFER = 60
OAUTH_TIMEOUT = 60
SERVER_START_DELAY = 0.5
TOKEN_FILE_PERMISSIONS = 0o600  # Read/write for owner only


def validate_redirect_uri(redirect_uri: str) -> None:
    """Validate redirect URI to prevent open redirect vulnerabilities.

    Args:
        redirect_uri: The redirect URI to validate

    Raises:
        ValueError: If the redirect URI is invalid or potentially unsafe
    """
    parsed = urlparse(redirect_uri)

    # Check scheme
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"Invalid redirect URI scheme: {parsed.scheme}. Must be http or https."
        )

    # Check for user info (username:password) which should not be present
    if parsed.username or parsed.password:
        raise ValueError("Redirect URI must not contain user credentials.")

    # Check hostname
    if not parsed.hostname:
        raise ValueError("Redirect URI must have a valid hostname.")

    # Allow localhost/127.0.0.1 for development
    if parsed.hostname in ("localhost", "127.0.0.1", "::1"):
        return

    # For production, you should validate against a list of allowed domains
    # This is a basic check - in production, maintain a whitelist
    if parsed.scheme == "http" and parsed.hostname not in ("localhost", "127.0.0.1"):
        raise ValueError(
            "HTTP scheme is only allowed for localhost. Use HTTPS for production."
        )

    # Warn about non-standard ports
    if parsed.port and parsed.port not in (80, 443, 8000, 8080, 8765):
        logging.warning(f"Non-standard port {parsed.port} used in redirect URI")


class UserToken(BaseModel):
    """Container for OAuth2 user tokens."""

    access_token: str
    token_type: Literal["Bearer"] = DEFAULT_TOKEN_TYPE
    expires_in: Optional[int] = DEFAULT_TOKEN_EXPIRY
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    created_at: Optional[float] = Field(default_factory=time.time)
    expiry_buffer: int = TOKEN_EXPIRY_BUFFER

    @property
    def is_expired(self) -> bool:
        """Check if the token has expired.

        Returns True if the token is expired or if we cannot determine expiration.
        This is a conservative approach for security.
        """
        # If both are None, we can't determine expiration, so treat as expired
        if self.expires_in is None and self.created_at is None:
            return True
        # If either is None but not both, we can't reliably calculate
        if self.expires_in is None or self.created_at is None:
            return True
        return time.time() > (self.created_at + self.expires_in - self.expiry_buffer)

    @classmethod
    def from_response(cls, response_data: Dict) -> "UserToken":
        """Create UserToken from OAuth2 token response."""
        return cls(
            access_token=response_data["access_token"],
            token_type=response_data.get("token_type", DEFAULT_TOKEN_TYPE),
            expires_in=response_data.get("expires_in", DEFAULT_TOKEN_EXPIRY),
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

    Raises:
        ValueError: If redirect_uri is invalid
    """
    # Validate redirect URI
    validate_redirect_uri(redirect_uri)

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
        # Sanitize error response to prevent credential exposure
        error_msg = response.text
        if "client" in error_msg.lower() or "secret" in error_msg.lower():
            error_msg = "Authentication failed. Check client credentials."
        elif "refresh_token" in error_msg.lower():
            error_msg = "Invalid or expired refresh token."
        raise Exception(
            f"Token refresh failed with status {response.status_code}: {error_msg}"
        )


async def exchange_authorization_code_async(
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: str,
) -> UserToken:
    """Async version: Exchange authorization code for access token.

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

    logging.debug("Exchanging authorization code for access token (async)")

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        token_data = response.json()
        logging.debug("Successfully obtained user access token (async)")
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


async def refresh_access_token_async(
    client_id: str,
    client_secret: str,
    refresh_token: str,
) -> UserToken:
    """Async version: Refresh an expired access token using refresh token.

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

    logging.debug("Refreshing access token (async)")

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        token_data = response.json()
        logging.debug("Successfully refreshed access token (async)")
        return UserToken.from_response(token_data)
    else:
        logging.error(f"Token refresh failed with status {response.status_code}")
        # Sanitize error response to prevent credential exposure
        error_msg = response.text
        if "client" in error_msg.lower() or "secret" in error_msg.lower():
            error_msg = "Authentication failed. Check client credentials."
        elif "refresh_token" in error_msg.lower():
            error_msg = "Invalid or expired refresh token."
        raise Exception(
            f"Token refresh failed with status {response.status_code}: {error_msg}"
        )


def save_token_to_file(token: UserToken, filepath: str = ".esologs_token.json") -> None:
    """Save user token to file for persistence.

    The token file will be created with restrictive permissions (600) to protect
    sensitive authentication data. Only the owner will have read/write access.

    Args:
        token: UserToken to save
        filepath: Path to save token file (default: .esologs_token.json)

    Security Warning:
        Token files contain sensitive authentication credentials. Ensure that:
        - The file is stored in a secure location
        - The file permissions are restrictive (this function sets 600)
        - The file is not committed to version control
        - Consider encrypting the token data for additional security
    """
    token_data = {
        "access_token": token.access_token,
        "token_type": token.token_type,
        "expires_in": token.expires_in,
        "refresh_token": token.refresh_token,
        "scope": token.scope,
        "created_at": token.created_at,
    }

    # Write the file
    with open(filepath, "w") as f:
        json.dump(token_data, f, indent=2)

    # Set restrictive permissions (read/write for owner only)
    os.chmod(filepath, TOKEN_FILE_PERMISSIONS)

    logging.info(
        f"Token saved to {filepath} with permissions {oct(TOKEN_FILE_PERMISSIONS)}"
    )


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
            token_type=token_data.get("token_type", DEFAULT_TOKEN_TYPE),
            expires_in=token_data.get("expires_in", DEFAULT_TOKEN_EXPIRY),
            refresh_token=token_data.get("refresh_token"),
            scope=token_data.get("scope"),
            created_at=token_data.get("created_at"),
        )
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None


async def save_token_to_file_async(
    token: UserToken, filepath: str = ".esologs_token.json"
) -> None:
    """Async version: Save user token to file for persistence.

    The token file will be created with restrictive permissions (600) to protect
    sensitive authentication data. Only the owner will have read/write access.

    Args:
        token: UserToken to save
        filepath: Path to save token file (default: .esologs_token.json)

    Security Warning:
        Token files contain sensitive authentication credentials. Ensure that:
        - The file is stored in a secure location
        - The file permissions are restrictive (this function sets 600)
        - The file is not committed to version control
        - Consider encrypting the token data for additional security
    """
    token_data = {
        "access_token": token.access_token,
        "token_type": token.token_type,
        "expires_in": token.expires_in,
        "refresh_token": token.refresh_token,
        "scope": token.scope,
        "created_at": token.created_at,
    }

    # Write the file asynchronously
    async with aiofiles.open(filepath, mode="w") as f:
        await f.write(json.dumps(token_data, indent=2))

    # Set restrictive permissions (read/write for owner only)
    os.chmod(filepath, TOKEN_FILE_PERMISSIONS)

    logging.info(
        f"Token saved to {filepath} with permissions {oct(TOKEN_FILE_PERMISSIONS)}"
    )


async def load_token_from_file_async(
    filepath: str = ".esologs_token.json",
) -> Optional[UserToken]:
    """Async version: Load user token from file.

    Args:
        filepath: Path to token file (default: .esologs_token.json)

    Returns:
        UserToken if file exists and is valid, None otherwise
    """
    try:
        async with aiofiles.open(filepath, mode="r") as f:
            content = await f.read()
            token_data = json.loads(content)

        return UserToken(
            access_token=token_data["access_token"],
            token_type=token_data.get("token_type", DEFAULT_TOKEN_TYPE),
            expires_in=token_data.get("expires_in", DEFAULT_TOKEN_EXPIRY),
            refresh_token=token_data.get("refresh_token"),
            scope=token_data.get("scope"),
            created_at=token_data.get("created_at"),
        )
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None


class OAuth2Flow:
    """Automated OAuth2 Authorization Code flow handler.

    This class provides a simple, automated way to handle the OAuth2 flow
    by starting a local server, opening the browser, and capturing the callback.

    Example:
        oauth_flow = OAuth2Flow(
            client_id="your_client_id",
            client_secret="your_client_secret",
            redirect_uri="http://localhost:8765/callback"
        )

        # This will open the browser and handle everything automatically
        user_token = oauth_flow.authorize(scopes=["view-user-profile"])

        # Use the token with the client
        async with Client(
            url="https://www.esologs.com/api/v2/user",
            user_token=user_token
        ) as client:
            current_user = await client.get_current_user()
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str = "http://localhost:8765/callback",
        timeout: int = OAUTH_TIMEOUT,
    ):
        """Initialize OAuth2 flow handler.

        Args:
            client_id: ESO Logs OAuth2 client ID
            client_secret: ESO Logs OAuth2 client secret
            redirect_uri: Callback URL (must be registered with ESO Logs)
            timeout: Maximum seconds to wait for authorization (default: 60)

        Raises:
            ValueError: If redirect_uri is invalid
        """
        # Validate redirect URI
        validate_redirect_uri(redirect_uri)

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.timeout = timeout

        # Parse port from redirect URI
        parsed = urlparse(redirect_uri)
        # Default to 443 for HTTPS, 80 for HTTP
        default_port = 443 if parsed.scheme == "https" else 80
        self.port = parsed.port or default_port
        self.callback_path = parsed.path

        # State for the current flow
        self._auth_code: Optional[str] = None
        self._auth_state: Optional[str] = None
        self._auth_error: Optional[str] = None
        self._expected_state: Optional[str] = None

    def authorize(
        self,
        scopes: Optional[List[str]] = None,
        open_browser: bool = True,
    ) -> UserToken:
        """Run the complete OAuth2 authorization flow.

        Args:
            scopes: OAuth2 scopes to request (default: ["view-user-profile"])
            open_browser: Whether to automatically open the browser

        Returns:
            UserToken containing access token and refresh token

        Raises:
            Exception: If authorization fails or times out
        """
        # Reset state
        self._auth_code = None
        self._auth_state = None
        self._auth_error = None
        self._expected_state = secrets.token_urlsafe(32)

        # Generate authorization URL
        auth_url = generate_authorization_url(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scopes=scopes,
            state=self._expected_state,
        )

        # Start callback server
        server_thread = threading.Thread(target=self._run_callback_server)
        server_thread.daemon = True
        server_thread.start()

        # Give server time to start
        time.sleep(SERVER_START_DELAY)

        # Open browser if requested
        if open_browser:
            logging.info(f"Opening browser for authorization: {auth_url}")
            webbrowser.open(auth_url)
        else:
            logging.info(f"Visit this URL to authorize: {auth_url}")

        # Wait for callback
        start_time = time.time()
        auth_code: Optional[str] = None

        while (time.time() - start_time) < self.timeout:
            if self._auth_error:
                raise Exception(f"Authorization failed: {self._auth_error}")

            if self._auth_code is not None:
                auth_code = self._auth_code  # type: ignore[unreachable]
                break

            time.sleep(0.1)

        # Check if we got a code
        if auth_code is None:
            raise Exception(f"Authorization timed out after {self.timeout} seconds")

        # Verify state
        if self._auth_state != self._expected_state:
            raise Exception("Invalid state parameter - possible CSRF attack")

        # Exchange code for token
        user_token = exchange_authorization_code(
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=auth_code,
            redirect_uri=self.redirect_uri,
        )

        logging.info("Successfully obtained user token")
        return user_token

    def _run_callback_server(self) -> None:
        """Run the callback server to capture the OAuth2 response."""

        class CallbackHandler(BaseHTTPRequestHandler):
            """Handler for OAuth2 callback requests."""

            oauth_flow = self  # Reference to outer class instance

            def do_GET(self) -> None:
                """Handle GET request to callback URL."""
                parsed = urlparse(self.path)

                if parsed.path == self.oauth_flow.callback_path:
                    params = parse_qs(parsed.query)

                    # Check for error
                    if "error" in params:
                        self.oauth_flow._auth_error = params.get(
                            "error_description", ["Unknown error"]
                        )[0]
                        self._send_error_response(
                            params["error"][0],
                            self.oauth_flow._auth_error,
                        )
                        return

                    # Get code and state
                    if "code" in params:
                        self.oauth_flow._auth_code = params["code"][0]
                        state_param = params.get("state", [])
                        self.oauth_flow._auth_state = (
                            state_param[0] if state_param else None
                        )
                        self._send_success_response()
                    else:
                        self.oauth_flow._auth_error = "No authorization code received"
                        self._send_error_response(
                            "missing_code",
                            "No authorization code in callback",
                        )
                else:
                    self.send_response(404)
                    self.end_headers()

            def _send_success_response(self) -> None:
                """Send success HTML response."""
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = """
                <html>
                <head>
                    <title>Authorization Successful</title>
                    <style>
                        body { font-family: Arial; padding: 40px; background: #f0f0f0; }
                        .success { color: green; }
                        .info { background: white; padding: 20px; border-radius: 5px; }
                    </style>
                </head>
                <body>
                    <h1 class="success">Authorization Successful!</h1>
                    <div class="info">
                        <p>The authorization was completed successfully.</p>
                        <p><strong>You can close this window.</strong></p>
                    </div>
                </body>
                </html>
                """
                self.wfile.write(html.encode())

            def _send_error_response(self, error: str, description: str) -> None:
                """Send error HTML response."""
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = f"""
                <html>
                <head>
                    <title>Authorization Failed</title>
                    <style>
                        body {{ font-family: Arial; padding: 40px; }}
                        .error {{ color: red; background: #ffe6e6; padding: 20px; border-radius: 5px; }}
                    </style>
                </head>
                <body>
                    <h1 style="color: red;">Authorization Failed</h1>
                    <div class="error">
                        <p><strong>Error:</strong> {error}</p>
                        <p><strong>Description:</strong> {description}</p>
                    </div>
                    <p>You can close this window.</p>
                </body>
                </html>
                """
                self.wfile.write(html.encode())

            def log_message(self, format: str, *args: object) -> None:
                """Suppress default logging."""
                pass

        # Create and run server
        server = HTTPServer(("localhost", self.port), CallbackHandler)
        server.timeout = self.timeout

        try:
            # Handle one request or timeout
            server.handle_request()
        finally:
            server.server_close()


class AsyncOAuth2Flow:
    """Async version: Automated OAuth2 Authorization Code flow handler.

    This class provides an async implementation of the OAuth2 flow,
    suitable for use in async applications. It still uses a synchronous
    local server for the callback (as browsers redirect synchronously).

    Example:
        oauth_flow = AsyncOAuth2Flow(
            client_id="your_client_id",
            client_secret="your_client_secret",
            redirect_uri="http://localhost:8765/callback"
        )

        # This will open the browser and handle everything automatically
        user_token = await oauth_flow.authorize(scopes=["view-user-profile"])

        # Use the token with the client
        async with Client(
            url="https://www.esologs.com/api/v2/user",
            user_token=user_token
        ) as client:
            current_user = await client.get_current_user()
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str = "http://localhost:8765/callback",
        timeout: int = OAUTH_TIMEOUT,
    ):
        """Initialize async OAuth2 flow handler.

        Args:
            client_id: ESO Logs OAuth2 client ID
            client_secret: ESO Logs OAuth2 client secret
            redirect_uri: Callback URL (must be registered with ESO Logs)
            timeout: Maximum seconds to wait for authorization (default: 60)

        Raises:
            ValueError: If redirect_uri is invalid
        """
        # Validate redirect URI
        validate_redirect_uri(redirect_uri)

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.timeout = timeout

        # Parse port from redirect URI
        parsed = urlparse(redirect_uri)
        # Default to 443 for HTTPS, 80 for HTTP
        default_port = 443 if parsed.scheme == "https" else 80
        self.port = parsed.port or default_port
        self.callback_path = parsed.path

        # State for the current flow
        self._auth_code: Optional[str] = None
        self._auth_state: Optional[str] = None
        self._auth_error: Optional[str] = None
        self._expected_state: Optional[str] = None
        self.state: Optional[str] = None  # Public access to current state
        self.authorization_code: Optional[str] = None  # Public access to auth code
        self.callback_received = asyncio.Event()  # Event for async callback waiting

    def _generate_authorization_url(self, scopes: Optional[List[str]] = None) -> str:
        """Generate OAuth2 authorization URL with state for CSRF protection.

        Args:
            scopes: List of OAuth2 scopes (defaults to ["view-user-profile"])

        Returns:
            Authorization URL to redirect the user to
        """
        self.state = secrets.token_urlsafe(32)
        return generate_authorization_url(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scopes=scopes,
            state=self.state,
        )

    def _validate_state(self, state: Optional[str]) -> bool:
        """Validate CSRF state token.

        Args:
            state: State token to validate

        Returns:
            True if state is valid, False otherwise
        """
        return state is not None and state == self.state

    async def _start_server(self) -> None:
        """Start the callback server (placeholder for mocking in tests)."""
        # This is just a placeholder that can be mocked in tests
        pass

    async def _handle_request(self, request: Any) -> None:
        """Handle incoming callback request (placeholder for mocking in tests)."""
        # This is just a placeholder that can be mocked in tests
        pass

    async def authorize(
        self,
        scopes: Optional[List[str]] = None,
        open_browser: bool = True,
    ) -> UserToken:
        """Run the complete OAuth2 authorization flow asynchronously.

        Args:
            scopes: OAuth2 scopes to request (default: ["view-user-profile"])
            open_browser: Whether to automatically open the browser

        Returns:
            UserToken containing access token and refresh token

        Raises:
            Exception: If authorization fails or times out
        """
        # Reset state
        self._auth_code = None
        self._auth_state = None
        self._auth_error = None
        self.authorization_code = None
        self.callback_received.clear()

        # Generate authorization URL with state
        auth_url = self._generate_authorization_url(scopes)
        self._expected_state = self.state

        # Start callback server in a thread (browser redirects are synchronous)
        server_thread = threading.Thread(target=self._run_callback_server)
        server_thread.daemon = True
        server_thread.start()

        # Give server time to start
        await asyncio.sleep(SERVER_START_DELAY)

        # Open browser if requested
        if open_browser:
            logging.info(f"Opening browser for authorization: {auth_url}")
            webbrowser.open(auth_url)
        else:
            logging.info(f"Visit this URL to authorize: {auth_url}")

        # Wait for callback
        start_time = time.time()
        auth_code: Optional[str] = None

        while (time.time() - start_time) < self.timeout:
            if self._auth_error:
                raise Exception(f"Authorization failed: {self._auth_error}")

            if self._auth_code is not None:
                auth_code = self._auth_code  # type: ignore[unreachable]
                break

            await asyncio.sleep(0.1)

        # Check if we got a code
        if auth_code is None:
            raise Exception(f"Authorization timed out after {self.timeout} seconds")

        # Verify state
        if self._auth_state != self._expected_state:
            raise Exception("Invalid state parameter - possible CSRF attack")

        # Exchange code for token using async function
        user_token = await exchange_authorization_code_async(
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=auth_code,
            redirect_uri=self.redirect_uri,
        )

        logging.info("Successfully obtained user token")
        return user_token

    def _run_callback_server(self) -> None:
        """Run the callback server to capture the OAuth2 response.

        Note: This remains synchronous as it handles browser redirects.
        """

        class CallbackHandler(BaseHTTPRequestHandler):
            """Handler for OAuth2 callback requests."""

            oauth_flow = self  # Reference to outer class instance

            def do_GET(self) -> None:
                """Handle GET request to callback URL."""
                parsed = urlparse(self.path)

                if parsed.path == self.oauth_flow.callback_path:
                    params = parse_qs(parsed.query)

                    # Check for error
                    if "error" in params:
                        self.oauth_flow._auth_error = params.get(
                            "error_description", ["Unknown error"]
                        )[0]
                        self._send_error_response(
                            params["error"][0],
                            self.oauth_flow._auth_error,
                        )
                        return

                    # Get code and state
                    if "code" in params:
                        self.oauth_flow._auth_code = params["code"][0]
                        self.oauth_flow.authorization_code = params["code"][
                            0
                        ]  # Set public attribute
                        state_param = params.get("state", [])
                        self.oauth_flow._auth_state = (
                            state_param[0] if state_param else None
                        )
                        # Set the asyncio event from the sync thread
                        if hasattr(self.oauth_flow, "callback_received"):
                            # We're in a sync thread, so we need to be careful
                            # The event loop might not be running in this thread
                            try:
                                # Get the running loop if available
                                loop = getattr(
                                    self.oauth_flow.callback_received, "_loop", None
                                )
                                if loop and not loop.is_closed():
                                    loop.call_soon_threadsafe(
                                        self.oauth_flow.callback_received.set
                                    )
                                else:
                                    # Try to get the current event loop
                                    try:
                                        import asyncio

                                        loop = asyncio.get_running_loop()
                                        loop.call_soon_threadsafe(
                                            self.oauth_flow.callback_received.set
                                        )
                                    except RuntimeError:
                                        # No running loop, just skip
                                        pass
                            except AttributeError:
                                # Event might not have a loop attribute yet
                                pass
                        self._send_success_response()
                    else:
                        self.oauth_flow._auth_error = "No authorization code received"
                        self._send_error_response(
                            "missing_code",
                            "No authorization code in callback",
                        )
                else:
                    self.send_response(404)
                    self.end_headers()

            def _send_success_response(self) -> None:
                """Send success HTML response."""
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = """
                <html>
                <head>
                    <title>Authorization Successful</title>
                    <style>
                        body { font-family: Arial; padding: 40px; background: #f0f0f0; }
                        .success { color: green; }
                        .info { background: white; padding: 20px; border-radius: 5px; }
                    </style>
                </head>
                <body>
                    <h1 class="success">Authorization Successful!</h1>
                    <div class="info">
                        <p>The authorization was completed successfully.</p>
                        <p><strong>You can close this window.</strong></p>
                    </div>
                </body>
                </html>
                """
                self.wfile.write(html.encode())

            def _send_error_response(self, error: str, description: str) -> None:
                """Send error HTML response."""
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = f"""
                <html>
                <head>
                    <title>Authorization Failed</title>
                    <style>
                        body {{ font-family: Arial; padding: 40px; }}
                        .error {{ color: red; background: #ffe6e6; padding: 20px; border-radius: 5px; }}
                    </style>
                </head>
                <body>
                    <h1 style="color: red;">Authorization Failed</h1>
                    <div class="error">
                        <p><strong>Error:</strong> {error}</p>
                        <p><strong>Description:</strong> {description}</p>
                    </div>
                    <p>You can close this window.</p>
                </body>
                </html>
                """
                self.wfile.write(html.encode())

            def log_message(self, format: str, *args: object) -> None:
                """Suppress default logging."""
                pass

        # Create and run server
        server = HTTPServer(("localhost", self.port), CallbackHandler)
        server.timeout = self.timeout

        try:
            # Handle one request or timeout
            server.handle_request()
        finally:
            server.server_close()


# Example usage for documentation
if __name__ == "__main__":
    # Example 1: Automated OAuth2 flow (recommended)
    oauth_flow = OAuth2Flow(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="http://localhost:8765/callback",
    )

    # This will open browser and handle everything automatically
    # user_token = oauth_flow.authorize(scopes=["view-user-profile"])

    # Example 2: Manual OAuth2 flow
    # Step 1: Generate authorization URL
    state = secrets.token_urlsafe(32)  # Generate secure random state
    auth_url = generate_authorization_url(
        client_id="your_client_id",
        redirect_uri="http://localhost:8000/callback",
        scopes=["view-user-profile"],
        state=state,
    )
    # Visit: {auth_url}

    # Step 2: User authorizes and is redirected back with code
    # Example callback: http://localhost:8000/callback?code=abc123&state={state}

    # Step 3: Exchange code for token
    # token = exchange_authorization_code(
    #     client_id="your_client_id",
    #     client_secret="your_client_secret",
    #     code="abc123",
    #     redirect_uri="http://localhost:8000/callback"
    # )

    # Example 3: Async OAuth2 flow
    # async def main():
    #     oauth_flow = AsyncOAuth2Flow(
    #         client_id="your_client_id",
    #         client_secret="your_client_secret",
    #         redirect_uri="http://localhost:8765/callback"
    #     )
    #     user_token = await oauth_flow.authorize(scopes=["view-user-profile"])
    #
    #     # Save token asynchronously
    #     await save_token_to_file_async(user_token)
    #
    #     # Later, load and refresh if needed
    #     saved_token = await load_token_from_file_async()
    #     if saved_token and saved_token.is_expired:
    #         new_token = await refresh_access_token_async(
    #             client_id="your_client_id",
    #             client_secret="your_client_secret",
    #             refresh_token=saved_token.refresh_token
    #         )
    #
    # asyncio.run(main())
