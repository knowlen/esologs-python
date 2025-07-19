"""
Guild related methods for ESO Logs API client.
"""

from typing import TYPE_CHECKING

from .._generated.get_guild_by_id import GetGuildById
from ..method_factory import SIMPLE_GETTER_CONFIGS, create_simple_getter

if TYPE_CHECKING:
    pass


class GuildMixin:
    """Mixin providing guild related API methods."""

    def __init_subclass__(cls, **kwargs):
        """Initialize guild methods when subclass is created."""
        super().__init_subclass__(**kwargs)
        cls._register_guild_methods()

    @classmethod
    def _register_guild_methods(cls):
        """Register all guild methods on the class."""
        # Simple getter: get_guild_by_id
        if "get_guild_by_id" in SIMPLE_GETTER_CONFIGS:
            config = SIMPLE_GETTER_CONFIGS["get_guild_by_id"]
            method = create_simple_getter(
                operation_name=config["operation_name"],
                return_type=GetGuildById,
                id_param_name=config["id_param_name"],
            )
            setattr(cls, "get_guild_by_id", method)
