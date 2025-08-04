"""
Unit tests for parameter builder utilities.
"""


import pytest

from esologs._generated.base_model import UNSET
from esologs._generated.enums import (
    CharacterRankingMetricType,
    EventDataType,
    HostilityType,
    KillType,
    RankingCompareType,
    RankingTimeframeType,
    RoleType,
)
from esologs.param_builders import (
    ParameterBuilder,
    RankingParameterBuilder,
    ReportFilterBuilder,
    build_character_ranking_params,
    build_report_event_params,
    build_report_player_details_params,
    build_report_rankings_params,
    build_report_search_params,
    clean_unset_params,
    validate_param_combination,
)


class TestParameterBuilder:
    """Test base ParameterBuilder class."""

    def test_add_param(self):
        """Test adding parameters."""
        builder = ParameterBuilder()
        builder.add_param("key1", "value1")
        builder.add_param("key2", 123)

        result = builder.build()
        assert result == {"key1": "value1", "key2": 123}

    def test_add_param_ignores_unset(self):
        """Test that UNSET values are ignored."""
        builder = ParameterBuilder()
        builder.add_param("key1", "value1")
        builder.add_param("key2", UNSET)
        builder.add_param("key3", None)  # None is kept

        result = builder.build()
        assert result == {"key1": "value1", "key3": None}
        assert "key2" not in result

    def test_chaining(self):
        """Test method chaining."""
        builder = ParameterBuilder()
        result = builder.add_param("a", 1).add_param("b", 2).add_param("c", 3).build()
        assert result == {"a": 1, "b": 2, "c": 3}


class TestReportFilterBuilder:
    """Test ReportFilterBuilder class."""

    def test_add_time_range(self):
        """Test adding time range parameters."""
        builder = ReportFilterBuilder()
        builder.add_time_range(start_time=1000.0, end_time=2000.0)

        result = builder.build()
        assert result == {"startTime": 1000.0, "endTime": 2000.0}

    def test_add_time_range_partial(self):
        """Test adding partial time range."""
        builder = ReportFilterBuilder()
        builder.add_time_range(start_time=1000.0, end_time=UNSET)

        result = builder.build()
        assert result == {"startTime": 1000.0}
        assert "endTime" not in result

    def test_add_combat_filters(self):
        """Test adding combat filters."""
        builder = ReportFilterBuilder()
        builder.add_combat_filters(
            ability_id=12345.0,
            source_id=1,
            target_id=2,
            source_class="Dragonknight",
            target_class=UNSET,
        )

        result = builder.build()
        assert result == {
            "abilityID": 12345.0,
            "sourceID": 1,
            "targetID": 2,
            "sourceClass": "Dragonknight",
        }

    def test_add_aura_filters(self):
        """Test adding aura filters."""
        builder = ReportFilterBuilder()
        builder.add_aura_filters(
            source_auras_present="buff1,buff2",
            source_auras_absent="debuff1",
            target_auras_present=UNSET,
            target_auras_absent="debuff2",
        )

        result = builder.build()
        assert result == {
            "sourceAurasPresent": "buff1,buff2",
            "sourceAurasAbsent": "debuff1",
            "targetAurasAbsent": "debuff2",
        }

    def test_build_from_kwargs(self):
        """Test building from kwargs with parameter mapping."""
        builder = ReportFilterBuilder()
        params = builder.build_from_kwargs(
            code="ABC123",
            fight_i_ds=[1, 2, 3],
            encounter_id=27,
            start_time=1000.0,
            end_time=2000.0,
            data_type=EventDataType.DamageDone,
            hostility_type=HostilityType.Enemies,
            kill_type=KillType.Kills,
            limit=100,
            use_ability_i_ds=True,
            use_actor_i_ds=False,
            translate=True,
        )

        assert params == {
            "code": "ABC123",
            "fightIDs": [1, 2, 3],
            "encounterID": 27,
            "startTime": 1000.0,
            "endTime": 2000.0,
            "dataType": EventDataType.DamageDone,
            "hostilityType": HostilityType.Enemies,
            "killType": KillType.Kills,
            "limit": 100,
            "useAbilityIDs": True,
            "useActorIDs": False,
            "translate": True,
        }

    def test_build_from_kwargs_with_unset(self):
        """Test that UNSET values are filtered out."""
        builder = ReportFilterBuilder()
        params = builder.build_from_kwargs(
            code="ABC123",
            start_time=1000.0,
            end_time=UNSET,
            limit=UNSET,
            difficulty=125,
        )

        assert params == {"code": "ABC123", "startTime": 1000.0, "difficulty": 125}
        assert "endTime" not in params
        assert "limit" not in params


class TestRankingParameterBuilder:
    """Test RankingParameterBuilder class."""

    def test_add_ranking_filters(self):
        """Test adding ranking filters."""
        builder = RankingParameterBuilder()
        builder.add_ranking_filters(
            metric=CharacterRankingMetricType.dps,
            partition=25,
            timeframe=RankingTimeframeType.Historical,
            compare=RankingCompareType.Rankings,
        )

        result = builder.build()
        assert result == {
            "metric": CharacterRankingMetricType.dps,
            "partition": 25,
            "timeframe": RankingTimeframeType.Historical,
            "compare": RankingCompareType.Rankings,
        }

    def test_add_class_filters(self):
        """Test adding class/spec/role filters."""
        builder = RankingParameterBuilder()
        builder.add_class_filters(
            class_name="Nightblade", spec_name="Nightblade", role=RoleType.DPS
        )

        result = builder.build()
        assert result == {
            "className": "Nightblade",
            "specName": "Nightblade",
            "role": RoleType.DPS,
        }

    def test_build_from_kwargs(self):
        """Test building from kwargs with parameter mapping."""
        builder = RankingParameterBuilder()
        params = builder.build_from_kwargs(
            character_id=12345,
            encounter_id=27,
            zone_id=1,
            by_bracket=True,
            class_name="Dragonknight",
            spec_name="Dragonknight",
            include_combatant_info=True,
            include_private_logs=False,
            metric=CharacterRankingMetricType.hps,
            partition=25,
            difficulty=125,
            size=12,
            role=RoleType.Healer,
        )

        assert params == {
            "characterId": 12345,
            "encounterId": 27,
            "zoneId": 1,
            "byBracket": True,
            "className": "Dragonknight",
            "specName": "Dragonknight",
            "includeCombatantInfo": True,
            "includePrivateLogs": False,
            "metric": CharacterRankingMetricType.hps,
            "partition": 25,
            "difficulty": 125,
            "size": 12,
            "role": RoleType.Healer,
        }


class TestConvenienceFunctions:
    """Test convenience builder functions."""

    def test_build_report_event_params(self):
        """Test build_report_event_params function."""
        params = build_report_event_params(
            code="ABC123",
            fight_i_ds=[1, 2],
            start_time=1000.0,
            data_type=EventDataType.Healing,
        )

        assert params == {
            "code": "ABC123",
            "fightIDs": [1, 2],
            "startTime": 1000.0,
            "dataType": EventDataType.Healing,
        }

    def test_build_character_ranking_params(self):
        """Test build_character_ranking_params function."""
        params = build_character_ranking_params(
            character_id=12345,
            encounter_id=27,
            metric=CharacterRankingMetricType.playerscore,
            by_bracket=False,
        )

        assert params == {
            "characterId": 12345,
            "encounterId": 27,
            "metric": CharacterRankingMetricType.playerscore,
            "byBracket": False,
        }

    def test_build_report_search_params(self):
        """Test build_report_search_params function."""
        params = build_report_search_params(
            guild_id=123,
            guild_name="Test Guild",
            guild_server_slug="test-server",
            guild_server_region="NA",
            start_time=1000000.0,
            end_time=2000000.0,
            limit=25,
            page=1,
        )

        assert params == {
            "guildID": 123,
            "guildName": "Test Guild",
            "guildServerSlug": "test-server",
            "guildServerRegion": "NA",
            "startTime": 1000000.0,
            "endTime": 2000000.0,
            "limit": 25,
            "page": 1,
        }

    def test_build_report_player_details_params(self):
        """Test build_report_player_details_params function."""
        params = build_report_player_details_params(
            code="ABC123",
            encounter_id=27,
            fight_i_ds=[1, 2, 3],
            kill_type=KillType.Kills,
            start_time=1000.0,
            end_time=2000.0,
            difficulty=125,
            translate=True,
            include_combatant_info=True,
        )

        assert params == {
            "code": "ABC123",
            "encounterID": 27,
            "fightIDs": [1, 2, 3],
            "killType": KillType.Kills,
            "startTime": 1000.0,
            "endTime": 2000.0,
            "difficulty": 125,
            "translate": True,
            "includeCombatantInfo": True,
        }

    def test_build_report_rankings_params(self):
        """Test build_report_rankings_params function."""
        params = build_report_rankings_params(
            code="ABC123",
            encounter_id=27,
            fight_i_ds=[1],
            player_metric="dps",
            compare="Rankings",
            difficulty=125,
            timeframe="Historical",
        )

        assert params == {
            "code": "ABC123",
            "encounterID": 27,
            "fightIDs": [1],
            "playerMetric": "dps",
            "compare": "Rankings",
            "difficulty": 125,
            "timeframe": "Historical",
        }


class TestValidationHelpers:
    """Test validation helper functions."""

    def test_validate_param_combination_valid(self):
        """Test validate_param_combination with valid params."""
        params = {
            "guild_name": "Test Guild",
            "guild_server_slug": "test-server",
            "guild_server_region": "NA",
        }

        # Should not raise
        validate_param_combination(
            params, [["guild_name", "guild_server_slug", "guild_server_region"]]
        )

    def test_validate_param_combination_invalid(self):
        """Test validate_param_combination with invalid params."""
        params = {
            "guild_name": "Test Guild",
            "guild_server_slug": "test-server"
            # Missing guild_server_region
        }

        with pytest.raises(ValueError, match="must be provided together"):
            validate_param_combination(
                params, [["guild_name", "guild_server_slug", "guild_server_region"]]
            )

    def test_validate_param_combination_none_provided(self):
        """Test validate_param_combination when none are provided."""
        params = {"other_param": "value"}

        # Should not raise when none of the group is provided
        validate_param_combination(
            params, [["guild_name", "guild_server_slug", "guild_server_region"]]
        )

    def test_clean_unset_params(self):
        """Test clean_unset_params function."""
        params = {
            "key1": "value1",
            "key2": UNSET,
            "key3": None,
            "key4": 0,
            "key5": "",
            "key6": UNSET,
        }

        cleaned = clean_unset_params(params)
        assert cleaned == {
            "key1": "value1",
            "key3": None,  # None is kept
            "key4": 0,  # 0 is kept
            "key5": "",  # Empty string is kept
        }
        assert "key2" not in cleaned
        assert "key6" not in cleaned
