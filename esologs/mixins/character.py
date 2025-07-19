"""
Character related methods for ESO Logs API client.
"""

from typing import TYPE_CHECKING, Any

from .._generated.enums import (
    CharacterRankingMetricType,
    RankingCompareType,
    RankingTimeframeType,
    RoleType,
)
from .._generated.get_character_by_id import GetCharacterById
from .._generated.get_character_encounter_ranking import GetCharacterEncounterRanking
from .._generated.get_character_encounter_rankings import GetCharacterEncounterRankings
from .._generated.get_character_reports import GetCharacterReports
from .._generated.get_character_zone_rankings import GetCharacterZoneRankings
from ..method_factory import (
    SIMPLE_GETTER_CONFIGS,
    create_complex_method,
    create_simple_getter,
)

if TYPE_CHECKING:
    pass


class CharacterMixin:
    """Mixin providing character related API methods."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Initialize character methods when subclass is created."""
        super().__init_subclass__(**kwargs)
        cls._register_character_methods()

    @classmethod
    def _register_character_methods(cls) -> None:
        """Register all character methods on the class."""
        # Simple getter: get_character_by_id
        if "get_character_by_id" in SIMPLE_GETTER_CONFIGS:
            config = SIMPLE_GETTER_CONFIGS["get_character_by_id"]
            method = create_simple_getter(
                operation_name=config["operation_name"],
                return_type=GetCharacterById,
                id_param_name=config["id_param_name"],
            )
            cls.get_character_by_id = method  # type: ignore[attr-defined]

        # get_character_reports (has limit parameter)
        method = create_complex_method(
            operation_name="getCharacterReports",
            return_type=GetCharacterReports,
            required_params={"character_id": int},
            optional_params={"limit": int},
            param_mapping={"character_id": "characterId"},
        )
        cls.get_character_reports = method  # type: ignore[attr-defined]

        # get_character_encounter_ranking (simple version)
        method = create_complex_method(
            operation_name="getCharacterEncounterRanking",
            return_type=GetCharacterEncounterRanking,
            required_params={"character_id": int, "encounter_id": int},
            param_mapping={
                "character_id": "characterId",
                "encounter_id": "encounterId",
            },
        )
        cls.get_character_encounter_ranking = method  # type: ignore[attr-defined]

        # get_character_encounter_rankings (complex version with many params)
        method = create_complex_method(
            operation_name="getCharacterEncounterRankings",
            return_type=GetCharacterEncounterRankings,
            required_params={"character_id": int, "encounter_id": int},
            optional_params={
                "by_bracket": bool,
                "class_name": str,
                "compare": RankingCompareType,
                "difficulty": int,
                "include_combatant_info": bool,
                "include_private_logs": bool,
                "metric": CharacterRankingMetricType,
                "partition": int,
                "role": RoleType,
                "size": int,
                "spec_name": str,
                "timeframe": RankingTimeframeType,
            },
            param_mapping={
                "character_id": "characterId",
                "encounter_id": "encounterId",
                "by_bracket": "byBracket",
                "class_name": "className",
                "spec_name": "specName",
                "include_combatant_info": "includeCombatantInfo",
                "include_private_logs": "includePrivateLogs",
            },
        )
        cls.get_character_encounter_rankings = method  # type: ignore[attr-defined]

        # get_character_zone_rankings
        method = create_complex_method(
            operation_name="getCharacterZoneRankings",
            return_type=GetCharacterZoneRankings,
            required_params={"character_id": int},
            optional_params={
                "zone_id": int,
                "by_bracket": bool,
                "class_name": str,
                "compare": RankingCompareType,
                "difficulty": int,
                "include_private_logs": bool,
                "metric": CharacterRankingMetricType,
                "partition": int,
                "role": RoleType,
                "size": int,
                "spec_name": str,
                "timeframe": RankingTimeframeType,
            },
            param_mapping={
                "character_id": "characterId",
                "zone_id": "zoneId",
                "by_bracket": "byBracket",
                "class_name": "className",
                "spec_name": "specName",
                "include_private_logs": "includePrivateLogs",
            },
        )
        cls.get_character_zone_rankings = method  # type: ignore[attr-defined]
