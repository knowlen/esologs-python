"""
Method factory functions for dynamically creating API client methods.

This module provides factory functions that generate async methods
following common patterns in the ESO Logs API.
"""

import re
from functools import wraps
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union

from ._generated.base_model import UNSET, UnsetType
from .queries import QUERIES

T = TypeVar("T")


def create_simple_getter(
    operation_name: str,
    return_type: Type[T],
    id_param_name: str = "id",
) -> Callable:
    """
    Create a simple getter method that takes a single ID parameter.

    This factory handles methods like:
    - get_ability(id)
    - get_class(id)
    - get_item(id)
    - get_guild_by_id(guild_id)

    Args:
        operation_name: The GraphQL operation name
        return_type: The pydantic model class for the return type
        id_param_name: The name of the ID parameter (default: "id")

    Returns:
        An async method that executes the query
    """

    # Convert camelCase to snake_case properly
    snake_name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", operation_name).lower()
    
    async def method(self, id: int = None, **kwargs: Any) -> T:
        """Execute a simple ID-based query."""
        # Support both positional and keyword arguments
        if id is None:
            # Try to get from kwargs using various possible names
            if "id" in kwargs:
                id = kwargs.pop("id")
            elif id_param_name in kwargs:
                id = kwargs.pop(id_param_name)
            else:
                # Try snake_case version of id_param_name
                param_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', id_param_name).lower()
                if param_key in kwargs:
                    id = kwargs.pop(param_key)
                else:
                    raise TypeError(f"{snake_name}() missing required parameter: id")
        
        query = QUERIES[operation_name]
        variables: Dict[str, object] = {id_param_name: id}

        response = await self.execute(
            query=query, operation_name=operation_name, variables=variables, **kwargs
        )
        data = self.get_data(response)
        return return_type.model_validate(data)

    # Update method metadata
    method.__name__ = snake_name
    method.__doc__ = f"Get {return_type.__name__} by {id_param_name}."

    return method


def create_no_params_getter(
    operation_name: str,
    return_type: Type[T],
) -> Callable:
    """
    Create a getter method that takes no parameters.

    This factory handles methods like:
    - get_world_data()
    - get_regions()
    - get_factions()
    - get_rate_limit_data()

    Args:
        operation_name: The GraphQL operation name
        return_type: The pydantic model class for the return type

    Returns:
        An async method that executes the query
    """

    async def method(self, **kwargs: Any) -> T:
        """Execute a parameterless query."""
        query = QUERIES[operation_name]
        variables: Dict[str, object] = {}

        response = await self.execute(
            query=query, operation_name=operation_name, variables=variables, **kwargs
        )
        data = self.get_data(response)
        return return_type.model_validate(data)

    # Update method metadata
    # Convert camelCase to snake_case properly
    snake_name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", operation_name).lower()
    method.__name__ = snake_name
    method.__doc__ = f"Get {return_type.__name__}."

    return method


def create_paginated_getter(
    operation_name: str,
    return_type: Type[T],
    extra_params: Optional[Dict[str, Type]] = None,
) -> Callable:
    """
    Create a paginated getter method with limit and page parameters.

    This factory handles methods like:
    - get_abilities(limit, page)
    - get_items(limit, page)
    - get_classes(faction_id, zone_id) - with extra params

    Args:
        operation_name: The GraphQL operation name
        return_type: The pydantic model class for the return type
        extra_params: Additional parameters beyond limit/page

    Returns:
        An async method that executes the paginated query
    """
    extra_params = extra_params or {}

    async def method(
        self,
        limit: Union[Optional[int], UnsetType] = UNSET,
        page: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> T:
        """Execute a paginated query."""
        query = QUERIES[operation_name]
        variables: Dict[str, object] = {
            "limit": limit,
            "page": page,
        }

        # Add any extra parameters from kwargs
        for param_name in extra_params:
            if param_name in kwargs:
                variables[param_name] = kwargs.pop(param_name)
            else:
                variables[param_name] = UNSET

        response = await self.execute(
            query=query, operation_name=operation_name, variables=variables, **kwargs
        )
        data = self.get_data(response)
        return return_type.model_validate(data)

    # Update method metadata
    # Convert camelCase to snake_case properly
    snake_name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", operation_name).lower()
    method.__name__ = snake_name
    method.__doc__ = f"Get paginated {return_type.__name__}."

    return method


def create_complex_method(
    operation_name: str,
    return_type: Type[T],
    required_params: Dict[str, Type],
    optional_params: Optional[Dict[str, Type]] = None,
    param_mapping: Optional[Dict[str, str]] = None,
) -> Callable:
    """
    Create a method with complex parameter requirements.

    This factory handles methods with many parameters like:
    - get_report_events(code, many optional params...)
    - get_character_encounter_rankings(character_id, encounter_id, many optional params...)

    Args:
        operation_name: The GraphQL operation name
        return_type: The pydantic model class for the return type
        required_params: Dict of required parameter names to types
        optional_params: Dict of optional parameter names to types
        param_mapping: Dict to map Python param names to GraphQL names

    Returns:
        An async method that executes the complex query
    """
    optional_params = optional_params or {}
    param_mapping = param_mapping or {}

    # Build the full parameter list for the method signature

    async def method(self, **kwargs: Any) -> T:
        """Execute a complex query with many parameters."""
        query = QUERIES[operation_name]
        variables: Dict[str, object] = {}

        # Process required parameters
        for param_name, _param_type in required_params.items():
            if param_name not in kwargs:
                raise TypeError(f"Missing required parameter: {param_name}")
            variables[param_mapping.get(param_name, param_name)] = kwargs.pop(
                param_name
            )

        # Process optional parameters
        for param_name in optional_params:
            value = kwargs.pop(param_name, UNSET)
            variables[param_mapping.get(param_name, param_name)] = value

        response = await self.execute(
            query=query, operation_name=operation_name, variables=variables, **kwargs
        )
        data = self.get_data(response)
        return return_type.model_validate(data)

    # Update method metadata
    # Convert camelCase to snake_case properly
    snake_name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", operation_name).lower()
    method.__name__ = snake_name
    method.__doc__ = f"Execute {operation_name} with complex parameters."

    # This is a simplified version - in production, we'd want to preserve
    # the full signature with proper type hints
    return method


def create_method_with_builder(
    operation_name: str,
    return_type: Type[T],
    param_builder: Callable[[Dict[str, Any]], Dict[str, object]],
) -> Callable:
    """
    Create a method that uses a parameter builder function.

    This factory is useful for methods that need custom parameter processing
    or validation before execution.

    Args:
        operation_name: The GraphQL operation name
        return_type: The pydantic model class for the return type
        param_builder: Function that builds variables dict from kwargs

    Returns:
        An async method that executes the query
    """

    async def method(self, **kwargs: Any) -> T:
        """Execute a query with custom parameter building."""
        query = QUERIES[operation_name]
        variables = param_builder(**kwargs)

        response = await self.execute(
            query=query, operation_name=operation_name, variables=variables, **kwargs
        )
        data = self.get_data(response)
        return return_type.model_validate(data)

    # Update method metadata
    # Convert camelCase to snake_case properly
    snake_name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", operation_name).lower()
    method.__name__ = snake_name
    method.__doc__ = f"Execute {operation_name} with custom parameter building."

    return method


# Method configuration for simple getters
SIMPLE_GETTER_CONFIGS = {
    "get_ability": {
        "operation_name": "getAbility",
        "id_param_name": "id",
    },
    "get_class": {
        "operation_name": "getClass",
        "id_param_name": "id",
    },
    "get_item": {
        "operation_name": "getItem",
        "id_param_name": "id",
    },
    "get_item_set": {
        "operation_name": "getItemSet",
        "id_param_name": "id",
    },
    "get_map": {
        "operation_name": "getMap",
        "id_param_name": "id",
    },
    "get_npc": {
        "operation_name": "getNPC",
        "id_param_name": "id",
    },
    "get_character_by_id": {
        "operation_name": "getCharacterById",
        "id_param_name": "id",
    },
    "get_guild_by_id": {
        "operation_name": "getGuildById",
        "id_param_name": "guildId",
    },
    "get_encounters_by_zone": {
        "operation_name": "getEncountersByZone",
        "id_param_name": "zoneId",
    },
}

# Method configuration for no-param getters
NO_PARAM_GETTER_CONFIGS = {
    "get_world_data": "getWorldData",
    "get_regions": "getRegions",
    "get_zones": "getZones",
    "get_factions": "getFactions",
    "get_rate_limit_data": "getRateLimitData",
}

# Method configuration for paginated getters
PAGINATED_GETTER_CONFIGS = {
    "get_abilities": {
        "operation_name": "getAbilities",
    },
    "get_items": {
        "operation_name": "getItems",
    },
    "get_item_sets": {
        "operation_name": "getItemSets",
    },
    "get_maps": {
        "operation_name": "getMaps",
    },
    "get_npcs": {
        "operation_name": "getNPCs",
    },
    "get_classes": {
        "operation_name": "getClasses",
        "extra_params": {"faction_id": int, "zone_id": int},
    },
}
