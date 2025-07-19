"""
Game data related methods for ESO Logs API client.
"""

from typing import TYPE_CHECKING

from .._generated.get_abilities import GetAbilities
from .._generated.get_ability import GetAbility
from .._generated.get_class import GetClass
from .._generated.get_classes import GetClasses
from .._generated.get_factions import GetFactions
from .._generated.get_item import GetItem
from .._generated.get_item_set import GetItemSet
from .._generated.get_item_sets import GetItemSets
from .._generated.get_items import GetItems
from .._generated.get_map import GetMap
from .._generated.get_maps import GetMaps
from .._generated.get_np_cs import GetNPCs
from .._generated.get_npc import GetNPC
from ..method_factory import (
    NO_PARAM_GETTER_CONFIGS,
    PAGINATED_GETTER_CONFIGS,
    SIMPLE_GETTER_CONFIGS,
    create_no_params_getter,
    create_paginated_getter,
    create_simple_getter,
)

if TYPE_CHECKING:
    pass


class GameDataMixin:
    """Mixin providing game data related API methods."""

    def __init_subclass__(cls, **kwargs):
        """Initialize game data methods when subclass is created."""
        super().__init_subclass__(**kwargs)
        cls._register_game_data_methods()

    @classmethod
    def _register_game_data_methods(cls):
        """Register all game data methods on the class."""
        # Simple getters (single ID parameter)
        game_data_simple_getters = {
            "get_ability": (GetAbility, "getAbility"),
            "get_class": (GetClass, "getClass"),
            "get_item": (GetItem, "getItem"),
            "get_item_set": (GetItemSet, "getItemSet"),
            "get_map": (GetMap, "getMap"),
            "get_npc": (GetNPC, "getNPC"),
        }

        for method_name, (
            return_type,
            operation_name,
        ) in game_data_simple_getters.items():
            config = SIMPLE_GETTER_CONFIGS.get(
                method_name, {"operation_name": operation_name, "id_param_name": "id"}
            )
            method = create_simple_getter(
                operation_name=config["operation_name"],
                return_type=return_type,
                id_param_name=config.get("id_param_name", "id"),
            )
            setattr(cls, method_name, method)

        # No parameter getters
        if "get_factions" in NO_PARAM_GETTER_CONFIGS:
            method = create_no_params_getter(
                operation_name=NO_PARAM_GETTER_CONFIGS["get_factions"],
                return_type=GetFactions,
            )
            cls.get_factions = method

        # Paginated getters
        paginated_getters = {
            "get_abilities": GetAbilities,
            "get_items": GetItems,
            "get_item_sets": GetItemSets,
            "get_maps": GetMaps,
            "get_npcs": GetNPCs,
        }

        for method_name, return_type in paginated_getters.items():
            config = PAGINATED_GETTER_CONFIGS.get(
                method_name,
                {
                    "operation_name": method_name.replace("get_", "get")
                    .title()
                    .replace("_", "")
                },
            )
            method = create_paginated_getter(
                operation_name=config["operation_name"],
                return_type=return_type,
                extra_params=config.get("extra_params"),
            )
            setattr(cls, method_name, method)

        # Special case: get_classes with extra parameters
        if "get_classes" in PAGINATED_GETTER_CONFIGS:
            config = PAGINATED_GETTER_CONFIGS["get_classes"]
            method = create_paginated_getter(
                operation_name=config["operation_name"],
                return_type=GetClasses,
                extra_params=config.get("extra_params"),
            )
            cls.get_classes = method
