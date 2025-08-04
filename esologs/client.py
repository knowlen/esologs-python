"""ESO Logs API Client - the primary interface for interacting with the ESO Logs GraphQL API.

This client provides comprehensive access to ESO Logs data including game data,
character information, guild data, reports, rankings, and more.
"""

import re
import warnings
from typing import Any, Optional, Union

from esologs._generated.async_base_client import AsyncBaseClient
from esologs.mixins.character import CharacterMixin
from esologs.mixins.game_data import GameDataMixin
from esologs.mixins.guild import GuildMixin
from esologs.mixins.progress_race import ProgressRaceMixin
from esologs.mixins.report import ReportMixin
from esologs.mixins.user import UserMixin
from esologs.mixins.world_data import WorldDataMixin
from esologs.user_auth import UserToken

# Bearer token validation pattern
BEARER_TOKEN_PATTERN = re.compile(r"^Bearer\s+[\w\-\.~\+\/]+=*$")


def validate_bearer_token_format(auth_header: str) -> None:
    """Validate Bearer token format.

    Args:
        auth_header: Authorization header value

    Raises:
        ValueError: If the Bearer token format is invalid
    """
    if not auth_header:
        return

    if not BEARER_TOKEN_PATTERN.match(auth_header):
        if not auth_header.startswith("Bearer "):
            raise ValueError(
                "Authorization header must start with 'Bearer '. "
                f"Got: {auth_header[:20]}..."
            )
        raise ValueError(
            "Invalid Bearer token format. Token should contain only "
            "alphanumeric characters, hyphens, underscores, dots, tildes, "
            "plus signs, forward slashes, and may end with equals signs."
        )


class Client(
    AsyncBaseClient,
    GameDataMixin,
    CharacterMixin,
    WorldDataMixin,
    GuildMixin,
    ReportMixin,
    ProgressRaceMixin,
    UserMixin,
):
    """ESO Logs API Client with all available methods.

    This client supports both client credentials (for most API methods) and
    user authentication (for user-specific data).

    For user authentication, you can either:
    1. Pass a UserToken to the constructor
    2. Use the /api/v2/user endpoint for currentUser queries

    Example:
        # Client credentials (default)
        async with Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": f"Bearer {client_token}"}
        ) as client:
            character = await client.get_character_by_id(id=12345)

        # User authentication
        async with Client(
            url="https://www.esologs.com/api/v2/user",  # Note: /user endpoint
            headers={"Authorization": f"Bearer {user_token}"}
        ) as client:
            current_user = await client.get_current_user()
    """

    def __init__(
        self,
        url: str,
        headers: Optional[dict] = None,
        user_token: Optional[Union[str, UserToken]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the ESO Logs client.

        Args:
            url: GraphQL endpoint URL. Use /api/v2/client for client credentials
                 or /api/v2/user for user authentication
            headers: HTTP headers including Authorization
            user_token: Optional UserToken object or access token string for user auth
            **kwargs: Additional arguments passed to AsyncBaseClient
        """
        # Handle user token if provided
        if user_token:
            if isinstance(user_token, str):
                # If string, assume it's an access token
                headers = headers or {}
                auth_header = f"Bearer {user_token}"
                validate_bearer_token_format(auth_header)
                headers["Authorization"] = auth_header
            elif isinstance(user_token, UserToken):
                # If UserToken object, use its access token
                headers = headers or {}
                auth_header = f"Bearer {user_token.access_token}"
                validate_bearer_token_format(auth_header)
                headers["Authorization"] = auth_header

                # Check if token is expired
                if user_token.is_expired:
                    warnings.warn(
                        "UserToken appears to be expired. Consider refreshing it.",
                        UserWarning,
                        stacklevel=2,
                    )

        # Validate existing Authorization header if provided
        if headers and "Authorization" in headers:
            validate_bearer_token_format(headers["Authorization"])

        # Detect if using user endpoint and warn if no user token
        if "/api/v2/user" in url and not user_token:
            warnings.warn(
                "Using /api/v2/user endpoint without user authentication. "
                "Most queries will fail. Use /api/v2/client for client credentials.",
                UserWarning,
                stacklevel=2,
            )

        super().__init__(url=url, headers=headers, **kwargs)

    @property
    def is_user_authenticated(self) -> bool:
        """Check if the client is configured for user authentication."""
        return "/api/v2/user" in self.url
