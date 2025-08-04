"""
Progress race related methods for ESO Logs API client.

This mixin provides access to progress race data for tracking world/realm first
achievement races in ESO.
"""

from typing import TYPE_CHECKING, Any, Dict, Optional, Protocol

from esologs._generated.get_progress_race import GetProgressRace
from esologs.method_factory import create_complex_method

if TYPE_CHECKING:
    import httpx


class ClientProtocol(Protocol):
    """Protocol for ESO Logs client methods needed by progress race operations."""

    async def execute(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> "httpx.Response":
        """Execute a GraphQL query."""
        ...

    def get_data(self, response: "httpx.Response") -> Dict[str, Any]:
        """Extract data from GraphQL response."""
        ...


class ProgressRaceMixin:
    """Mixin class for progress race-related operations."""

    def __init_subclass__(cls, **kwargs: Any):
        """Initialize the subclass with progress race methods."""
        super().__init_subclass__(**kwargs)
        cls._register_progress_race_methods()

    @classmethod
    def _register_progress_race_methods(cls) -> None:
        """Register all progress race-related methods on the class."""
        # get_progress_race with all optional parameters
        method = create_complex_method(
            operation_name="getProgressRace",
            return_type=GetProgressRace,
            required_params={},  # All parameters are optional
            optional_params={
                "guild_id": int,
                "zone_id": int,
                "competition_id": int,
                "difficulty": int,
                "size": int,
                "server_region": str,
                "server_subregion": str,
                "server_slug": str,
                "guild_name": str,
            },
            param_mapping={
                "guild_id": "guildID",
                "zone_id": "zoneID",
                "competition_id": "competitionID",
                "server_region": "serverRegion",
                "server_subregion": "serverSubregion",
                "server_slug": "serverSlug",
                "guild_name": "guildName",
            },
        )
        cls.get_progress_race = method  # type: ignore[attr-defined]
