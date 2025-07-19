"""
World data related methods for ESO Logs API client.
"""

from typing import TYPE_CHECKING

from .._generated.get_encounters_by_zone import GetEncountersByZone
from .._generated.get_regions import GetRegions
from .._generated.get_world_data import GetWorldData
from .._generated.get_zones import GetZones
from ..method_factory import (
    NO_PARAM_GETTER_CONFIGS,
    SIMPLE_GETTER_CONFIGS,
    create_no_params_getter,
    create_simple_getter,
)

if TYPE_CHECKING:
    pass


class WorldDataMixin:
    """Mixin providing world data related API methods."""

    def __init_subclass__(cls, **kwargs):
        """Initialize world data methods when subclass is created."""
        super().__init_subclass__(**kwargs)
        cls._register_world_data_methods()

    @classmethod
    def _register_world_data_methods(cls):
        """Register all world data methods on the class."""
        # No parameter getters
        no_param_methods = {
            "get_world_data": GetWorldData,
            "get_zones": GetZones,
            "get_regions": GetRegions,
        }

        for method_name, return_type in no_param_methods.items():
            if method_name in NO_PARAM_GETTER_CONFIGS:
                operation_name = NO_PARAM_GETTER_CONFIGS[method_name]
                method = create_no_params_getter(
                    operation_name=operation_name, return_type=return_type
                )
                setattr(cls, method_name, method)

        # Simple getter: get_encounters_by_zone
        if "get_encounters_by_zone" in SIMPLE_GETTER_CONFIGS:
            config = SIMPLE_GETTER_CONFIGS["get_encounters_by_zone"]
            method = create_simple_getter(
                operation_name=config["operation_name"],
                return_type=GetEncountersByZone,
                id_param_name=config["id_param_name"],
            )
            cls.get_encounters_by_zone = method
