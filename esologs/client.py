"""
ESO Logs API client with mixin-based architecture.

This module provides the main Client class that combines functionality
from all API mixins.
"""

from typing import Any, Optional

from ._generated.generated_client import Client as GeneratedClient
from .mixins import (
    CharacterMixin,
    GameDataMixin,
    GuildMixin,
    ReportMixin,
    WorldDataMixin,
)


class Client(
    GeneratedClient,
    CharacterMixin,
    GameDataMixin,
    GuildMixin,
    ReportMixin,
    WorldDataMixin,
):
    """
    ESO Logs API client.

    This client provides access to all ESO Logs API functionality through
    a mixin-based architecture. Methods are organized by functional area:

    - Character methods: Character data and rankings
    - Game data methods: Abilities, classes, items, NPCs, etc.
    - Guild methods: Guild search, members, attendance
    - Report methods: Report data, events, rankings, tables
    - World data methods: Zones, regions, encounters

    Example:
        >>> from esologs import Client
        >>> client = Client(
        ...     client_id="your_client_id",
        ...     client_secret="your_client_secret"
        ... )
        >>> guilds = client.get_guilds(server_slug="pc-na", limit=10)
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        """
        Initialize the ESO Logs client.

        Args:
            client_id: OAuth client ID (can also be set via ESOLOGS_ID env var)
            client_secret: OAuth client secret (can also be set via ESOLOGS_SECRET env var)
            *args: Additional positional arguments for the base client
            **kwargs: Additional keyword arguments for the base client
        """
        # The auth handling should be done by the generated client or auth module
        # For now, just pass through to the generated client
        super().__init__(*args, **kwargs)
