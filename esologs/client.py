"""
Refactored ESO Logs API client using mixins and factory methods.

This is a cleaner, more maintainable implementation of the client.
"""

from typing import Any

from ._generated.async_base_client import AsyncBaseClient
from ._generated.base_model import UNSET, UnsetType
from .mixins import (
    CharacterMixin,
    GameDataMixin,
    GuildMixin,
    ReportMixin,
    WorldDataMixin,
)

# Re-export UNSET for backward compatibility
__all__ = ["Client", "UNSET", "UnsetType"]


def gql(q: str) -> str:
    """Helper function for GraphQL queries."""
    return q


class Client(
    AsyncBaseClient,
    GameDataMixin,
    CharacterMixin,
    WorldDataMixin,
    GuildMixin,
    ReportMixin,
):
    """
    ESO Logs API client with comprehensive validation and security features.

    This refactored client uses mixins to organize methods by functional area:
    - GameDataMixin: Abilities, items, NPCs, classes, factions, maps
    - CharacterMixin: Character info, reports, rankings
    - WorldDataMixin: World data, zones, regions, encounters
    - GuildMixin: Guild information
    - ReportMixin: Combat reports, events, graphs, rankings, analysis

    Security Features:
    - Input validation with length limits to prevent DoS attacks
    - API key sanitization in error messages
    - Parameter validation before API calls

    Rate Limiting:
    - ESO Logs API has rate limits (typically 300 requests/minute)
    - Users should implement rate limiting in production applications
    - Consider using exponential backoff for failed requests

    Example:
        ```python
        from esologs import Client

        async with Client(
            client_id="your-client-id",
            client_secret="your-client-secret"
        ) as client:
            # Get ability information
            ability = await client.get_ability(id=12345)

            # Search for reports
            reports = await client.search_reports(
                guild_id=123,
                limit=25
            )

            # Get character rankings
            rankings = await client.get_character_zone_rankings(
                character_id=456,
                metric=CharacterRankingMetricType.dps
            )
        ```
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the client and register all methods from mixins."""
        super().__init__(*args, **kwargs)
        # Methods are automatically registered by mixin __init_subclass__ hooks

    def __repr__(self) -> str:
        """Return a string representation of the client."""
        return "<ESO Logs Client (Refactored)>"
