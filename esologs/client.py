"""
ESO Logs API Client.

This is the main client class that combines all API functionality through mixins.
"""

from typing import Any

from esologs._generated.async_base_client import AsyncBaseClient
from esologs.mixins import (
    CharacterMixin,
    GameDataMixin,
    GuildMixin,
    ProgressRaceMixin,
    ReportMixin,
    WorldDataMixin,
)


class Client(
    AsyncBaseClient,
    GameDataMixin,
    CharacterMixin,
    WorldDataMixin,
    GuildMixin,
    ReportMixin,
    ProgressRaceMixin,
):
    """
    ESO Logs API Client.

    This client provides access to all ESO Logs API functionality through
    a modular mixin-based architecture.

    Example:
        >>> import asyncio
        >>> from esologs import Client
        >>>
        >>> async def main():
        ...     async with Client(
        ...         client_id="your_client_id",
        ...         client_secret="your_client_secret"
        ...     ) as client:
        ...         # Get ability information
        ...         ability = await client.get_ability(id=20301)
        ...         # Access ability name: ability.game_data.ability.name
        >>>
        >>> asyncio.run(main())
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the ESO Logs client."""
        super().__init__(**kwargs)

    async def __aenter__(self) -> "Client":
        """Async context manager entry."""
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        # Use parent's __aexit__ which closes the http_client
        await super().__aexit__(*args)
