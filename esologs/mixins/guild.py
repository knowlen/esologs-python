"""
Guild related methods for ESO Logs API client.

Validation Strategy:
- Methods that map directly to single GraphQL operations (get_guild_by_id, get_guilds,
  get_guild_attendance, get_guild_members) rely on GraphQL schema validation.
- The get_guild() convenience method has additional client-side validation because it
  routes to different GraphQL queries based on the parameters provided.
"""

from typing import TYPE_CHECKING, Any, Dict, Optional, Protocol, Union, cast

from esologs._generated.base_model import UNSET, UnsetType
from esologs._generated.get_guild_attendance import GetGuildAttendance
from esologs._generated.get_guild_by_id import GetGuildById
from esologs._generated.get_guild_by_name import GetGuildByName
from esologs._generated.get_guild_members import GetGuildMembers
from esologs._generated.get_guilds import GetGuilds
from esologs.method_factory import (
    SIMPLE_GETTER_CONFIGS,
    create_complex_method,
    create_method_with_builder,
    create_simple_getter,
)
from esologs.param_builders import build_guild_attendance_params
from esologs.queries import QUERIES
from esologs.validators import ValidationError

if TYPE_CHECKING:
    import httpx


class ClientProtocol(Protocol):
    """Protocol for ESO Logs client methods needed by guild operations."""

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

    async def get_guild_by_id(self, guild_id: int) -> GetGuildById:
        """Get guild by ID."""
        ...


class GuildMixin:
    """Mixin providing guild related API methods."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Initialize guild methods when subclass is created."""
        super().__init_subclass__(**kwargs)
        cls._register_guild_methods()

    @classmethod
    def _register_guild_methods(cls) -> None:
        """Register all guild methods on the class."""
        # Simple getter: get_guild_by_id
        if "get_guild_by_id" in SIMPLE_GETTER_CONFIGS:
            config = SIMPLE_GETTER_CONFIGS["get_guild_by_id"]
            method = create_simple_getter(
                operation_name=config["operation_name"],
                return_type=GetGuildById,
                id_param_name=config["id_param_name"],
            )
            cls.get_guild_by_id = method  # type: ignore[attr-defined]

        # Guild search with pagination
        # For getGuilds, we need to use create_complex_method because it has optional params with mapping
        guilds_method = create_complex_method(
            operation_name="getGuilds",
            return_type=GetGuilds,
            required_params={},  # No required params for getGuilds
            optional_params={
                "server_id": int,
                "server_slug": str,
                "server_region": str,
                "limit": int,
                "page": int,
            },
            param_mapping={
                "server_id": "serverID",
                "server_slug": "serverSlug",
                "server_region": "serverRegion",
            },
        )
        cls.get_guilds = guilds_method  # type: ignore[attr-defined]

        # Guild attendance
        attendance_method = create_method_with_builder(
            operation_name="getGuildAttendance",
            return_type=GetGuildAttendance,
            param_builder=build_guild_attendance_params,
        )
        cls.get_guild_attendance = attendance_method  # type: ignore[attr-defined]

        # Guild members
        members_method = create_complex_method(
            operation_name="getGuildMembers",
            return_type=GetGuildMembers,
            required_params={"guild_id": int},
            optional_params={
                "limit": int,
                "page": int,
            },
            param_mapping={"guild_id": "guildId"},
        )
        cls.get_guild_members = members_method  # type: ignore[attr-defined]

    async def get_guild(
        self: ClientProtocol,
        guild_id: Union[Optional[int], UnsetType] = UNSET,
        guild_name: Union[Optional[str], UnsetType] = UNSET,
        guild_server_slug: Union[Optional[str], UnsetType] = UNSET,
        guild_server_region: Union[Optional[str], UnsetType] = UNSET,
    ) -> Union[GetGuildById, GetGuildByName]:
        """Get guild by ID or name/server/region combination.

        Note: This method has comprehensive client-side validation because it's a
        convenience method that routes to different GraphQL queries based on the
        parameters provided. The other guild methods rely on GraphQL schema validation
        as they map directly to single GraphQL operations.

        Args:
            guild_id: The ID of the guild (optional)
            guild_name: The name of the guild (required with server info)
            guild_server_slug: The server slug (required with name)
            guild_server_region: The server region (required with name)

        Returns:
            Guild information

        Raises:
            ValidationError: If neither ID nor name/server combination provided
        """
        # Check if we have guild_id
        has_guild_id = guild_id is not UNSET and guild_id is not None

        # Check if we have complete name info
        has_guild_name = guild_name is not UNSET and guild_name is not None
        has_server_slug = (
            guild_server_slug is not UNSET and guild_server_slug is not None
        )
        has_server_region = (
            guild_server_region is not UNSET and guild_server_region is not None
        )
        has_complete_name_info = (
            has_guild_name and has_server_slug and has_server_region
        )

        # Validation logic for get_guild
        # First check if guild_name is provided but missing server info
        if has_guild_name and not (has_server_slug and has_server_region):
            raise ValidationError(
                "When using guild_name, must also provide "
                "guild_server_slug, and guild_server_region together"
            )

        # Then check if we have neither ID nor complete name info
        if not has_guild_id and not has_complete_name_info:
            raise ValidationError(
                "Must provide either guild_id OR guild_name with "
                "guild_server_slug and guild_server_region"
            )

        # Finally check if both are provided
        if has_guild_id and has_complete_name_info:
            raise ValidationError(
                "Cannot provide both guild_id and guild_name/server parameters. "
                "Use one or the other."
            )

        # Use appropriate query based on parameters
        if guild_id is not UNSET and guild_id is not None:
            return await self.get_guild_by_id(guild_id=cast(int, guild_id))
        else:
            # Use the name-based query
            response = await self.execute(
                query=QUERIES["getGuildByName"],
                operation_name="getGuildByName",
                variables={
                    "name": guild_name,
                    "serverSlug": guild_server_slug,
                    "serverRegion": guild_server_region,
                },
            )
            data = self.get_data(response)
            return GetGuildByName.model_validate(data)
