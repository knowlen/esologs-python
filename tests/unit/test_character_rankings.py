"""Unit tests for character rankings functionality."""

from unittest.mock import AsyncMock, Mock

import pytest

from esologs.client import Client
from esologs.enums import CharacterRankingMetricType, RankingTimeframeType, RoleType
from esologs.get_character_encounter_rankings import GetCharacterEncounterRankings
from esologs.get_character_zone_rankings import GetCharacterZoneRankings


class TestCharacterRankings:
    """Test class for character rankings methods."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = Mock(spec=Client)
        client.execute = AsyncMock()
        client.get_data = Mock()
        return client

    @pytest.fixture
    def mock_encounter_rankings_response(self):
        """Mock response for encounter rankings."""
        return {
            "characterData": {
                "character": {
                    "encounterRankings": {
                        "bestAmount": 12345,
                        "medianPerformance": 85.5,
                        "averagePerformance": 82.1,
                        "totalKills": 15,
                        "fastestKill": 120000,
                        "difficulty": 125,
                        "metric": "dps",
                        "partition": 25,
                        "zone": 8,
                        "ranks": [
                            {
                                "rankPercent": 95.5,
                                "medianPercent": 85.2,
                                "lockedIn": True,
                                "regionName": "North America",
                                "serverName": "PC-NA",
                            }
                        ],
                    }
                }
            }
        }

    @pytest.fixture
    def mock_zone_rankings_response(self):
        """Mock response for zone rankings."""
        return {
            "characterData": {
                "character": {
                    "zoneRankings": {
                        "bestPerformanceAverage": 90.5,
                        "medianPerformanceAverage": 85.2,
                        "difficulty": 122,
                        "metric": "playerscore",
                        "partition": 25,
                        "zone": 1,
                        "allStars": [],
                        "rankings": [
                            {
                                "encounter": {
                                    "id": 1,
                                    "name": "Lightning Storm Atronach",
                                },
                                "rankPercent": 95.5,
                                "medianPercent": 85.2,
                                "allStars": None,
                                "lockedIn": True,
                                "totalKills": 5,
                                "fastestKill": 98000,
                                "bestAmount": 67890,
                                "spec": "Dragonknight",
                            }
                        ],
                    }
                }
            }
        }

    @pytest.mark.asyncio
    async def test_get_character_encounter_rankings_basic(
        self, mock_client, mock_encounter_rankings_response
    ):
        """Test basic encounter rankings functionality."""
        # Setup
        mock_client.get_data.return_value = mock_encounter_rankings_response

        # Create a real client instance and replace the necessary methods
        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test
        result = await client.get_character_encounter_rankings(
            character_id=12345, encounter_id=27
        )

        # Assertions
        assert isinstance(result, GetCharacterEncounterRankings)
        assert result.character_data is not None
        assert result.character_data.character is not None
        assert result.character_data.character.encounter_rankings is not None

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        assert call_args[1]["operation_name"] == "getCharacterEncounterRankings"
        assert call_args[1]["variables"]["characterId"] == 12345
        assert call_args[1]["variables"]["encounterId"] == 27

    @pytest.mark.asyncio
    async def test_get_character_encounter_rankings_with_params(
        self, mock_client, mock_encounter_rankings_response
    ):
        """Test encounter rankings with all parameters."""
        # Setup
        mock_client.get_data.return_value = mock_encounter_rankings_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test with all parameters
        result = await client.get_character_encounter_rankings(
            character_id=12345,
            encounter_id=27,
            by_bracket=True,
            class_name="Dragonknight",
            difficulty=125,
            include_combatant_info=True,
            metric=CharacterRankingMetricType.dps,
            partition=25,
            role=RoleType.DPS,
            size=12,
            spec_name="Dragonknight",
            timeframe=RankingTimeframeType.Today,
        )

        # Assertions
        assert isinstance(result, GetCharacterEncounterRankings)

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        variables = call_args[1]["variables"]

        assert variables["characterId"] == 12345
        assert variables["encounterId"] == 27
        assert variables["byBracket"] is True
        assert variables["className"] == "Dragonknight"
        assert variables["difficulty"] == 125
        assert variables["includeCombatantInfo"] is True
        assert variables["metric"] == CharacterRankingMetricType.dps
        assert variables["partition"] == 25
        assert variables["role"] == RoleType.DPS
        assert variables["size"] == 12
        assert variables["specName"] == "Dragonknight"
        assert variables["timeframe"] == RankingTimeframeType.Today

    @pytest.mark.asyncio
    async def test_get_character_zone_rankings_basic(
        self, mock_client, mock_zone_rankings_response
    ):
        """Test basic zone rankings functionality."""
        # Setup
        mock_client.get_data.return_value = mock_zone_rankings_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test
        result = await client.get_character_zone_rankings(character_id=12345, zone_id=1)

        # Assertions
        assert isinstance(result, GetCharacterZoneRankings)
        assert result.character_data is not None
        assert result.character_data.character is not None
        assert result.character_data.character.zone_rankings is not None

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        assert call_args[1]["operation_name"] == "getCharacterZoneRankings"
        assert call_args[1]["variables"]["characterId"] == 12345
        assert call_args[1]["variables"]["zoneId"] == 1

    @pytest.mark.asyncio
    async def test_get_character_zone_rankings_latest_zone(
        self, mock_client, mock_zone_rankings_response
    ):
        """Test zone rankings without specifying zone ID (should use latest)."""
        # Setup
        mock_client.get_data.return_value = mock_zone_rankings_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test without zone_id (should use latest zone)
        result = await client.get_character_zone_rankings(
            character_id=12345, metric=CharacterRankingMetricType.playerscore
        )

        # Assertions
        assert isinstance(result, GetCharacterZoneRankings)

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        variables = call_args[1]["variables"]

        assert variables["characterId"] == 12345
        assert variables["metric"] == CharacterRankingMetricType.playerscore
        # zoneId should be UNSET, not None
        from esologs.client import UNSET

        assert variables["zoneId"] == UNSET

    @pytest.mark.asyncio
    async def test_get_character_zone_rankings_with_all_params(
        self, mock_client, mock_zone_rankings_response
    ):
        """Test zone rankings with all parameters."""
        # Setup
        mock_client.get_data.return_value = mock_zone_rankings_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test with all parameters
        result = await client.get_character_zone_rankings(
            character_id=12345,
            zone_id=1,
            by_bracket=False,
            class_name="Nightblade",
            difficulty=122,
            include_private_logs=True,
            metric=CharacterRankingMetricType.hps,
            partition=25,
            role=RoleType.Healer,
            size=12,
            spec_name="Nightblade",
            timeframe=RankingTimeframeType.Historical,
        )

        # Assertions
        assert isinstance(result, GetCharacterZoneRankings)

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        variables = call_args[1]["variables"]

        assert variables["characterId"] == 12345
        assert variables["zoneId"] == 1
        assert variables["byBracket"] is False
        assert variables["className"] == "Nightblade"
        assert variables["difficulty"] == 122
        assert variables["includePrivateLogs"] is True
        assert variables["metric"] == CharacterRankingMetricType.hps
        assert variables["partition"] == 25
        assert variables["role"] == RoleType.Healer
        assert variables["size"] == 12
        assert variables["specName"] == "Nightblade"
        assert variables["timeframe"] == RankingTimeframeType.Historical

    def test_enum_values(self):
        """Test that enum values are properly defined."""
        # Test CharacterRankingMetricType enum
        assert CharacterRankingMetricType.dps == "dps"
        assert CharacterRankingMetricType.hps == "hps"
        assert CharacterRankingMetricType.playerscore == "playerscore"
        assert CharacterRankingMetricType.default == "default"

        # Test RoleType enum
        assert RoleType.DPS == "DPS"
        assert RoleType.Healer == "Healer"
        assert RoleType.Tank == "Tank"
        assert RoleType.Any == "Any"

        # Test RankingTimeframeType enum
        assert RankingTimeframeType.Today == "Today"
        assert RankingTimeframeType.Historical == "Historical"
