"""
Parameter builder utilities for ESO Logs API client.

This module provides functions and classes for building and validating
complex parameter sets for API methods.
"""

from typing import Any, Dict, List, Optional, Union

from ._generated.base_model import UNSET, UnsetType
from ._generated.enums import (
    CharacterRankingMetricType,
    RankingCompareType,
    RankingTimeframeType,
    RoleType,
)


class ParameterBuilder:
    """Base class for parameter builders."""

    def __init__(self) -> None:
        self.params: Dict[str, Any] = {}

    def add_param(self, name: str, value: Any) -> "ParameterBuilder":
        """Add a parameter if it's not UNSET."""
        if value is not UNSET:
            self.params[name] = value
        return self

    def build(self) -> Dict[str, object]:
        """Build the final parameter dictionary."""
        return self.params


class ReportFilterBuilder(ParameterBuilder):
    """Builder for report filtering parameters used across multiple methods."""

    def __init__(self) -> None:
        super().__init__()
        self._param_mapping = {
            "fight_i_ds": "fightIDs",
            "encounter_id": "encounterID",
            "ability_id": "abilityID",
            "source_id": "sourceID",
            "target_id": "targetID",
            "source_instance_id": "sourceInstanceID",
            "target_instance_id": "targetInstanceID",
            "start_time": "startTime",
            "end_time": "endTime",
            "data_type": "dataType",
            "hostility_type": "hostilityType",
            "kill_type": "killType",
            "wipe_cutoff": "wipeCutoff",
            "filter_expression": "filterExpression",
            "source_class": "sourceClass",
            "target_class": "targetClass",
            "source_auras_present": "sourceAurasPresent",
            "source_auras_absent": "sourceAurasAbsent",
            "target_auras_present": "targetAurasPresent",
            "target_auras_absent": "targetAurasAbsent",
            "include_resources": "includeResources",
            "use_ability_i_ds": "useAbilityIDs",
            "use_actor_i_ds": "useActorIDs",
            "view_options": "viewOptions",
            "view_by": "viewBy",
        }

    def add_time_range(
        self,
        start_time: Union[Optional[float], UnsetType] = UNSET,
        end_time: Union[Optional[float], UnsetType] = UNSET,
    ) -> "ReportFilterBuilder":
        """Add time range parameters."""
        self.add_param("startTime", start_time).add_param("endTime", end_time)
        return self

    def add_combat_filters(
        self,
        ability_id: Union[Optional[float], UnsetType] = UNSET,
        source_id: Union[Optional[int], UnsetType] = UNSET,
        target_id: Union[Optional[int], UnsetType] = UNSET,
        source_class: Union[Optional[str], UnsetType] = UNSET,
        target_class: Union[Optional[str], UnsetType] = UNSET,
    ) -> "ReportFilterBuilder":
        """Add combat-related filters."""
        self.add_param("abilityID", ability_id)
        self.add_param("sourceID", source_id)
        self.add_param("targetID", target_id)
        self.add_param("sourceClass", source_class)
        self.add_param("targetClass", target_class)
        return self

    def add_aura_filters(
        self,
        source_auras_present: Union[Optional[str], UnsetType] = UNSET,
        source_auras_absent: Union[Optional[str], UnsetType] = UNSET,
        target_auras_present: Union[Optional[str], UnsetType] = UNSET,
        target_auras_absent: Union[Optional[str], UnsetType] = UNSET,
    ) -> "ReportFilterBuilder":
        """Add aura-based filters."""
        self.add_param("sourceAurasPresent", source_auras_present)
        self.add_param("sourceAurasAbsent", source_auras_absent)
        self.add_param("targetAurasPresent", target_auras_present)
        self.add_param("targetAurasAbsent", target_auras_absent)
        return self

    def build_from_kwargs(self, **kwargs: Any) -> Dict[str, object]:
        """Build parameters from kwargs with proper mapping."""
        result = {}

        for python_name, graphql_name in self._param_mapping.items():
            if python_name in kwargs:
                value = kwargs[python_name]
                if value is not UNSET:
                    result[graphql_name] = value

        # Handle parameters that don't need mapping
        for param in ["code", "death", "difficulty", "limit", "translate"]:
            if param in kwargs and kwargs[param] is not UNSET:
                result[param] = kwargs[param]

        return result


class RankingParameterBuilder(ParameterBuilder):
    """Builder for ranking-related parameters."""

    def __init__(self) -> None:
        super().__init__()
        self._param_mapping = {
            "character_id": "characterId",
            "encounter_id": "encounterId",
            "zone_id": "zoneId",
            "by_bracket": "byBracket",
            "class_name": "className",
            "spec_name": "specName",
            "include_combatant_info": "includeCombatantInfo",
            "include_private_logs": "includePrivateLogs",
        }

    def add_ranking_filters(
        self,
        metric: Union[Optional[CharacterRankingMetricType], UnsetType] = UNSET,
        partition: Union[Optional[int], UnsetType] = UNSET,
        timeframe: Union[Optional[RankingTimeframeType], UnsetType] = UNSET,
        compare: Union[Optional[RankingCompareType], UnsetType] = UNSET,
    ) -> "RankingParameterBuilder":
        """Add ranking-specific filters."""
        self.add_param("metric", metric)
        self.add_param("partition", partition)
        self.add_param("timeframe", timeframe)
        self.add_param("compare", compare)
        return self

    def add_class_filters(
        self,
        class_name: Union[Optional[str], UnsetType] = UNSET,
        spec_name: Union[Optional[str], UnsetType] = UNSET,
        role: Union[Optional[RoleType], UnsetType] = UNSET,
    ) -> "RankingParameterBuilder":
        """Add class/spec/role filters."""
        self.add_param("className", class_name)
        self.add_param("specName", spec_name)
        self.add_param("role", role)
        return self

    def build_from_kwargs(self, **kwargs: Any) -> Dict[str, object]:
        """Build parameters from kwargs with proper mapping."""
        result = {}

        for python_name, graphql_name in self._param_mapping.items():
            if python_name in kwargs:
                value = kwargs[python_name]
                if value is not UNSET:
                    result[graphql_name] = value

        # Handle parameters that don't need mapping
        direct_params = [
            "metric",
            "partition",
            "timeframe",
            "compare",
            "difficulty",
            "size",
            "role",
        ]
        for param in direct_params:
            if param in kwargs and kwargs[param] is not UNSET:
                result[param] = kwargs[param]

        return result


# Convenience functions for building specific parameter sets


def build_report_event_params(**kwargs: Any) -> Dict[str, object]:
    """Build parameters for get_report_events method."""
    builder = ReportFilterBuilder()
    return builder.build_from_kwargs(**kwargs)


def build_report_graph_params(**kwargs: Any) -> Dict[str, object]:
    """Build parameters for get_report_graph method."""
    builder = ReportFilterBuilder()
    return builder.build_from_kwargs(**kwargs)


def build_report_table_params(**kwargs: Any) -> Dict[str, object]:
    """Build parameters for get_report_table method."""
    builder = ReportFilterBuilder()
    return builder.build_from_kwargs(**kwargs)


def build_character_ranking_params(**kwargs: Any) -> Dict[str, object]:
    """Build parameters for character ranking methods."""
    builder = RankingParameterBuilder()
    return builder.build_from_kwargs(**kwargs)


def build_report_search_params(**kwargs: Any) -> Dict[str, object]:
    """Build parameters for report search methods."""
    param_mapping = {
        "guild_id": "guildID",
        "guild_name": "guildName",
        "guild_server_slug": "guildServerSlug",
        "guild_server_region": "guildServerRegion",
        "guild_tag_id": "guildTagID",
        "user_id": "userID",
        "zone_id": "zoneID",
        "game_zone_id": "gameZoneID",
        "start_time": "startTime",
        "end_time": "endTime",
    }

    result = {}
    for python_name, graphql_name in param_mapping.items():
        if python_name in kwargs:
            value = kwargs[python_name]
            if value is not UNSET:
                result[graphql_name] = value

    # Handle direct params
    for param in ["limit", "page"]:
        if param in kwargs and kwargs[param] is not UNSET:
            result[param] = kwargs[param]

    return result


def build_report_player_details_params(**kwargs: Any) -> Dict[str, object]:
    """Build parameters for get_report_player_details method."""
    param_mapping = {
        "encounter_id": "encounterID",
        "fight_i_ds": "fightIDs",
        "kill_type": "killType",
        "start_time": "startTime",
        "end_time": "endTime",
        "include_combatant_info": "includeCombatantInfo",
    }

    result = {"code": kwargs["code"]}

    for python_name, graphql_name in param_mapping.items():
        if python_name in kwargs:
            value = kwargs[python_name]
            if value is not UNSET:
                result[graphql_name] = value

    # Handle direct params
    for param in ["difficulty", "translate"]:
        if param in kwargs and kwargs[param] is not UNSET:
            result[param] = kwargs[param]

    return result


def build_report_rankings_params(**kwargs: Any) -> Dict[str, object]:
    """Build parameters for get_report_rankings method."""
    param_mapping = {
        "encounter_id": "encounterID",
        "fight_i_ds": "fightIDs",
        "player_metric": "playerMetric",
    }

    result = {"code": kwargs["code"]}

    for python_name, graphql_name in param_mapping.items():
        if python_name in kwargs:
            value = kwargs[python_name]
            if value is not UNSET:
                result[graphql_name] = value

    # Handle direct params
    for param in ["compare", "difficulty", "timeframe"]:
        if param in kwargs and kwargs[param] is not UNSET:
            result[param] = kwargs[param]

    return result


# Parameter validation helpers


def validate_param_combination(
    params: Dict[str, Any], required_together: List[List[str]]
) -> None:
    """
    Validate that certain parameters are provided together.

    Args:
        params: The parameter dictionary
        required_together: List of parameter groups that must be provided together

    Raises:
        ValueError: If required parameters are not provided together
    """
    for group in required_together:
        provided = [p for p in group if params.get(p) not in (None, UNSET)]
        if provided and len(provided) != len(group):
            raise ValueError(
                f"Parameters {group} must be provided together. "
                f"Only got: {provided}"
            )


def clean_unset_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Remove UNSET values from a parameter dictionary."""
    return {k: v for k, v in params.items() if v is not UNSET}
