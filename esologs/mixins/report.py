"""
Report related methods for ESO Logs API client.
"""

from typing import TYPE_CHECKING, Any, Optional, Union

from .._generated.base_model import UNSET, UnsetType
from .._generated.get_rate_limit_data import GetRateLimitData
from .._generated.get_report_by_code import GetReportByCode
from .._generated.get_report_events import GetReportEvents
from .._generated.get_report_graph import GetReportGraph
from .._generated.get_report_player_details import GetReportPlayerDetails
from .._generated.get_report_rankings import GetReportRankings
from .._generated.get_report_table import GetReportTable
from .._generated.get_reports import GetReports
from ..method_factory import create_method_with_builder, create_no_params_getter
from ..param_builders import (
    build_report_event_params,
    build_report_graph_params,
    build_report_player_details_params,
    build_report_rankings_params,
    build_report_search_params,
    build_report_table_params,
)
from ..validators import (
    validate_limit_parameter,
    validate_positive_integer,
    validate_report_search_params,
)

if TYPE_CHECKING:
    pass


class ReportMixin:
    """Mixin providing report related API methods."""

    def __init_subclass__(cls, **kwargs):
        """Initialize report methods when subclass is created."""
        super().__init_subclass__(**kwargs)
        cls._register_report_methods()

    @classmethod
    def _register_report_methods(cls):
        """Register all report methods on the class."""

        # Simple getter: get_report_by_code (uses 'code' instead of 'id')
        async def get_report_by_code(self, code: str, **kwargs: Any) -> GetReportByCode:
            from ..queries import QUERIES

            query = QUERIES["getReportByCode"]
            variables = {"code": code}
            response = await self.execute(
                query=query,
                operation_name="getReportByCode",
                variables=variables,
            )
            data = self.get_data(response)
            return GetReportByCode.model_validate(data)

        setattr(cls, "get_report_by_code", get_report_by_code)

        # No params getter: get_rate_limit_data
        method = create_no_params_getter(
            operation_name="getRateLimitData", return_type=GetRateLimitData
        )
        setattr(cls, "get_rate_limit_data", method)

        # Complex report methods using builders
        report_methods = {
            "get_report_events": (GetReportEvents, build_report_event_params),
            "get_report_graph": (GetReportGraph, build_report_graph_params),
            "get_report_table": (GetReportTable, build_report_table_params),
            "get_report_rankings": (GetReportRankings, build_report_rankings_params),
            "get_report_player_details": (
                GetReportPlayerDetails,
                build_report_player_details_params,
            ),
            "get_reports": (GetReports, build_report_search_params),
        }

        for method_name, (return_type, builder) in report_methods.items():
            # Convert snake_case to camelCase for operation names
            parts = method_name.split("_")
            operation_name = parts[0] + "".join(word.capitalize() for word in parts[1:])
            # Special case mappings if needed
            operation_name_map = {
                "getReports": "getReports",  # Already correct
            }
            operation_name = operation_name_map.get(operation_name, operation_name)

            method = create_method_with_builder(
                operation_name=operation_name,
                return_type=return_type,
                param_builder=builder,
            )
            setattr(cls, method_name, method)

        # Convenience methods that wrap get_reports
        cls._register_report_convenience_methods()

    @classmethod
    def _register_report_convenience_methods(cls):
        """Register convenience methods for report searching."""

        async def search_reports(
            self,
            guild_id: Union[Optional[int], UnsetType] = UNSET,
            guild_name: Union[Optional[str], UnsetType] = UNSET,
            guild_server_slug: Union[Optional[str], UnsetType] = UNSET,
            guild_server_region: Union[Optional[str], UnsetType] = UNSET,
            guild_tag_id: Union[Optional[int], UnsetType] = UNSET,
            user_id: Union[Optional[int], UnsetType] = UNSET,
            zone_id: Union[Optional[int], UnsetType] = UNSET,
            game_zone_id: Union[Optional[int], UnsetType] = UNSET,
            start_time: Union[Optional[float], UnsetType] = UNSET,
            end_time: Union[Optional[float], UnsetType] = UNSET,
            limit: Union[Optional[int], UnsetType] = UNSET,
            page: Union[Optional[int], UnsetType] = UNSET,
            **kwargs: Any,
        ) -> GetReports:
            """Search for reports with flexible filtering options."""
            # Validate parameters before making API call
            validate_report_search_params(
                guild_name=guild_name,
                guild_server_slug=guild_server_slug,
                guild_server_region=guild_server_region,
                limit=limit,
                page=page,
                start_time=start_time,
                end_time=end_time,
                **kwargs,
            )

            return await self.get_reports(
                end_time=end_time,
                guild_id=guild_id,
                guild_name=guild_name,
                guild_server_slug=guild_server_slug,
                guild_server_region=guild_server_region,
                guild_tag_id=guild_tag_id,
                user_id=user_id,
                limit=limit,
                page=page,
                start_time=start_time,
                zone_id=zone_id,
                game_zone_id=game_zone_id,
                **kwargs,
            )

        async def get_guild_reports(
            self,
            guild_id: int,
            limit: Union[Optional[int], UnsetType] = UNSET,
            page: Union[Optional[int], UnsetType] = UNSET,
            start_time: Union[Optional[float], UnsetType] = UNSET,
            end_time: Union[Optional[float], UnsetType] = UNSET,
            zone_id: Union[Optional[int], UnsetType] = UNSET,
            **kwargs: Any,
        ) -> GetReports:
            """Convenience method to get reports for a specific guild."""
            # Validate guild-specific parameters
            validate_positive_integer(guild_id, "guild_id")
            if limit is not UNSET and limit is not None and isinstance(limit, int):
                validate_limit_parameter(limit)
            if page is not UNSET and page is not None and isinstance(page, int):
                validate_positive_integer(page, "page")

            return await self.search_reports(
                guild_id=guild_id,
                limit=limit,
                page=page,
                start_time=start_time,
                end_time=end_time,
                zone_id=zone_id,
                **kwargs,
            )

        async def get_user_reports(
            self,
            user_id: int,
            limit: Union[Optional[int], UnsetType] = UNSET,
            page: Union[Optional[int], UnsetType] = UNSET,
            start_time: Union[Optional[float], UnsetType] = UNSET,
            end_time: Union[Optional[float], UnsetType] = UNSET,
            zone_id: Union[Optional[int], UnsetType] = UNSET,
            **kwargs: Any,
        ) -> GetReports:
            """Convenience method to get reports for a specific user."""
            # Validate user-specific parameters
            validate_positive_integer(user_id, "user_id")
            if limit is not UNSET and limit is not None and isinstance(limit, int):
                validate_limit_parameter(limit)
            if page is not UNSET and page is not None and isinstance(page, int):
                validate_positive_integer(page, "page")

            return await self.search_reports(
                user_id=user_id,
                limit=limit,
                page=page,
                start_time=start_time,
                end_time=end_time,
                zone_id=zone_id,
                **kwargs,
            )

        # Add docstrings
        search_reports.__doc__ = """
        Search for reports with flexible filtering options.

        Args:
            guild_id: Filter by specific guild ID
            guild_name: Filter by guild name (requires guild_server_slug and guild_server_region)
            guild_server_slug: Guild server slug (required with guild_name)
            guild_server_region: Guild server region (required with guild_name)
            guild_tag_id: Filter by guild tag/team ID
            user_id: Filter by specific user ID
            zone_id: Filter by zone ID
            game_zone_id: Filter by game zone ID
            start_time: Start time filter (UNIX timestamp with milliseconds)
            end_time: End time filter (UNIX timestamp with milliseconds)
            limit: Number of reports per page (1-25, default 16)
            page: Page number (default 1)

        Returns:
            GetReports: Paginated list of reports matching the criteria
        """

        get_guild_reports.__doc__ = """
        Convenience method to get reports for a specific guild.

        Args:
            guild_id: The guild ID to search for
            limit: Number of reports per page (1-25, default 16)
            page: Page number (default 1)
            start_time: Start time filter (UNIX timestamp with milliseconds)
            end_time: End time filter (UNIX timestamp with milliseconds)
            zone_id: Filter by specific zone

        Returns:
            GetReports: Paginated list of guild reports
        """

        get_user_reports.__doc__ = """
        Convenience method to get reports for a specific user.

        Args:
            user_id: The user ID to search for
            limit: Number of reports per page (1-25, default 16)
            page: Page number (default 1)
            start_time: Start time filter (UNIX timestamp with milliseconds)
            end_time: End time filter (UNIX timestamp with milliseconds)
            zone_id: Filter by specific zone

        Returns:
            GetReports: Paginated list of user reports
        """

        setattr(cls, "search_reports", search_reports)
        setattr(cls, "get_guild_reports", get_guild_reports)
        setattr(cls, "get_user_reports", get_user_reports)
