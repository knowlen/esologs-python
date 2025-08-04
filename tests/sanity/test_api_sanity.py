"""
Sanity tests for comprehensive API coverage.

These tests exercise all major API endpoints to ensure basic functionality
and serve as living documentation of the API surface area.
"""

from datetime import datetime, timedelta

import pytest

from esologs._generated.enums import (
    CharacterRankingMetricType,
    EventDataType,
    ReportRankingMetricType,
    TableDataType,
)


@pytest.mark.integration
class TestGameDataAPISanity:
    """Sanity tests for Game Data API endpoints."""

    @pytest.mark.asyncio
    async def test_abilities_api(self, client, test_data):
        """Test abilities API endpoints."""
        # Test single ability
        ability = await client.get_ability(id=test_data["ability_id"])
        assert ability.game_data.ability is not None
        assert ability.game_data.ability.id == test_data["ability_id"]

        # Test abilities list
        abilities = await client.get_abilities(limit=10, page=1)
        assert abilities.game_data.abilities is not None
        assert len(abilities.game_data.abilities.data) <= 10

    @pytest.mark.asyncio
    async def test_classes_api(self, client, test_data):
        """Test classes API endpoints."""
        # Test single class
        class_response = await client.get_class(id=test_data["class_id"])
        assert class_response.game_data.class_ is not None
        assert class_response.game_data.class_.id == test_data["class_id"]

        # Test classes list
        classes = await client.get_classes()
        assert classes.game_data.classes is not None
        assert len(classes.game_data.classes) > 0

    @pytest.mark.asyncio
    async def test_factions_api(self, client):
        """Test factions API endpoint."""
        factions = await client.get_factions()
        assert factions.game_data.factions is not None
        assert len(factions.game_data.factions) > 0

    @pytest.mark.asyncio
    async def test_items_api(self, client, test_data):
        """Test items API endpoints."""
        # Test single item
        item = await client.get_item(id=test_data["item_id"])
        assert item.game_data.item is not None
        assert item.game_data.item.id == test_data["item_id"]

        # Test items list
        items = await client.get_items(limit=10, page=1)
        assert items.game_data.items is not None
        assert len(items.game_data.items.data) <= 10

    @pytest.mark.asyncio
    async def test_item_sets_api(self, client, test_data):
        """Test item sets API endpoints."""
        # Test single item set
        item_set = await client.get_item_set(id=test_data["item_set_id"])
        assert item_set.game_data.item_set is not None
        assert item_set.game_data.item_set.id == test_data["item_set_id"]

        # Test item sets list
        item_sets = await client.get_item_sets(limit=10, page=1)
        assert item_sets.game_data.item_sets is not None
        assert len(item_sets.game_data.item_sets.data) <= 10

    @pytest.mark.asyncio
    async def test_maps_api(self, client, test_data):
        """Test maps API endpoints."""
        # Test single map
        map_response = await client.get_map(id=test_data["map_id"])
        assert map_response.game_data.map is not None
        assert map_response.game_data.map.id == test_data["map_id"]

        # Test maps list
        maps = await client.get_maps(limit=10, page=1)
        assert maps.game_data.maps is not None
        assert len(maps.game_data.maps.data) <= 10

    @pytest.mark.asyncio
    async def test_npcs_api(self, client, test_data):
        """Test NPCs API endpoints."""
        # Test single NPC
        npc = await client.get_npc(id=test_data["npc_id"])
        assert npc.game_data.npc is not None
        assert npc.game_data.npc.id == test_data["npc_id"]

        # Test NPCs list
        npcs = await client.get_npcs(limit=10, page=1)
        assert npcs.game_data.npcs is not None
        assert len(npcs.game_data.npcs.data) <= 10


@pytest.mark.integration
class TestWorldDataAPISanity:
    """Sanity tests for World Data API endpoints."""

    @pytest.mark.asyncio
    async def test_zones_api(self, client):
        """Test zones API endpoint."""
        zones = await client.get_zones()
        assert zones.world_data.zones is not None
        assert len(zones.world_data.zones) > 0

    @pytest.mark.asyncio
    async def test_regions_api(self, client):
        """Test regions API endpoint."""
        regions = await client.get_regions()
        assert regions.world_data.regions is not None
        assert len(regions.world_data.regions) > 0

    @pytest.mark.asyncio
    async def test_encounters_by_zone_api(self, client, test_data):
        """Test encounters by zone API endpoint."""
        encounters = await client.get_encounters_by_zone(zone_id=test_data["zone_id"])
        assert encounters.world_data.zone is not None
        assert encounters.world_data.zone.id == test_data["zone_id"]


@pytest.mark.integration
class TestCharacterDataAPISanity:
    """Sanity tests for Character Data API endpoints."""

    @pytest.mark.asyncio
    async def test_character_basic_api(self, client, test_data):
        """Test basic character API endpoints."""
        # Test character by ID
        character = await client.get_character_by_id(id=test_data["character_id"])
        assert character.character_data.character is not None
        assert character.character_data.character.id == test_data["character_id"]

        # Test character reports
        reports = await client.get_character_reports(
            character_id=test_data["character_id"], limit=5
        )
        assert reports.character_data.character is not None
        assert reports.character_data.character.recent_reports is not None

    @pytest.mark.asyncio
    async def test_character_rankings_api(self, client, test_data):
        """Test character rankings API endpoints."""
        # Test encounter ranking (basic)
        encounter_ranking = await client.get_character_encounter_ranking(
            character_id=test_data["character_id"],
            encounter_id=test_data["encounter_id"],
        )
        assert encounter_ranking.character_data.character is not None

        # Test encounter rankings (detailed)
        encounter_rankings = await client.get_character_encounter_rankings(
            character_id=test_data["character_id"],
            encounter_id=test_data["encounter_id"],
            metric=CharacterRankingMetricType.dps,
        )
        assert encounter_rankings.character_data.character is not None

        # Test zone rankings
        zone_rankings = await client.get_character_zone_rankings(
            character_id=test_data["character_id"],
            zone_id=test_data["zone_id"],
            metric=CharacterRankingMetricType.playerscore,
        )
        assert zone_rankings.character_data.character is not None


@pytest.mark.integration
class TestGuildDataAPISanity:
    """Sanity tests for Guild Data API endpoints."""

    @pytest.mark.asyncio
    async def test_guild_basic_api(self, client, test_data):
        """Test basic guild API endpoints."""
        guild = await client.get_guild_by_id(guild_id=test_data["guild_id"])
        assert guild.guild_data.guild is not None
        assert guild.guild_data.guild.id == test_data["guild_id"]


@pytest.mark.integration
class TestReportDataAPISanity:
    """Sanity tests for Report Data API endpoints."""

    @pytest.mark.asyncio
    async def test_report_basic_api(self, client, test_data):
        """Test basic report API endpoints."""
        report = await client.get_report_by_code(code=test_data["report_code"])
        assert report.report_data.report is not None
        assert report.report_data.report.code == test_data["report_code"]

    @pytest.mark.asyncio
    async def test_report_analysis_api(self, client, test_data):
        """Test comprehensive report analysis API endpoints."""
        report_code = test_data["report_code"]

        # Test report events
        events = await client.get_report_events(
            code=report_code,
            data_type=EventDataType.DamageDone,
            start_time=0.0,
            end_time=60000.0,
            limit=10,
        )
        assert events.report_data.report is not None
        assert events.report_data.report.events is not None

        # Test report table
        table = await client.get_report_table(
            code=report_code,
            data_type=TableDataType.DamageDone,
            start_time=0.0,
            end_time=60000.0,
        )
        assert table.report_data.report is not None

        # Test report rankings
        rankings = await client.get_report_rankings(
            code=report_code, player_metric=ReportRankingMetricType.dps
        )
        assert rankings.report_data.report is not None

        # Test report player details
        player_details = await client.get_report_player_details(
            code=report_code, start_time=0.0, end_time=60000.0
        )
        assert player_details.report_data.report is not None

    @pytest.mark.asyncio
    async def test_report_search_api(self, client, test_data):
        """Test advanced report search API endpoints."""
        guild_id = test_data["guild_id"]

        # Test basic search
        search_results = await client.search_reports(guild_id=guild_id, limit=5)
        assert search_results.report_data.reports is not None
        assert len(search_results.report_data.reports.data) <= 5

        # Test guild reports convenience method
        guild_reports = await client.get_guild_reports(guild_id=guild_id, limit=3)
        assert guild_reports.report_data.reports is not None
        assert len(guild_reports.report_data.reports.data) <= 3

        # Test user reports convenience method
        user_reports = await client.get_user_reports(user_id=1, limit=3)
        assert user_reports.report_data.reports is not None

        # Test search with date filtering
        end_time = datetime.now().timestamp() * 1000
        start_time = (datetime.now() - timedelta(days=30)).timestamp() * 1000

        date_filtered = await client.search_reports(
            guild_id=guild_id, start_time=start_time, end_time=end_time, limit=3
        )
        assert date_filtered.report_data.reports is not None


@pytest.mark.integration
class TestSystemAPISanity:
    """Sanity tests for System API endpoints."""

    @pytest.mark.asyncio
    async def test_rate_limit_api(self, client):
        """Test rate limit API endpoint."""
        rate_limit = await client.get_rate_limit_data()
        assert rate_limit.rate_limit_data is not None
        assert hasattr(rate_limit.rate_limit_data, "limit_per_hour")
        assert hasattr(rate_limit.rate_limit_data, "points_spent_this_hour")


@pytest.mark.integration
class TestAPICoverageReport:
    """Generate a coverage report of API functionality."""

    @pytest.mark.asyncio
    async def test_api_coverage_summary(self, client, test_data):
        """Comprehensive test that exercises major API areas for coverage reporting."""
        coverage_report = {
            "game_data": [],
            "world_data": [],
            "character_data": [],
            "guild_data": [],
            "report_data": [],
            "system_data": [],
        }

        # Game Data API
        try:
            await client.get_abilities(limit=1)
            coverage_report["game_data"].append("abilities")
        except Exception:
            pass

        try:
            await client.get_classes()
            coverage_report["game_data"].append("classes")
        except Exception:
            pass

        try:
            await client.get_factions()
            coverage_report["game_data"].append("factions")
        except Exception:
            pass

        try:
            await client.get_items(limit=1)
            coverage_report["game_data"].append("items")
        except Exception:
            pass

        try:
            await client.get_npcs(limit=1)
            coverage_report["game_data"].append("npcs")
        except Exception:
            pass

        # World Data API
        try:
            await client.get_zones()
            coverage_report["world_data"].append("zones")
        except Exception:
            pass

        try:
            await client.get_regions()
            coverage_report["world_data"].append("regions")
        except Exception:
            pass

        # Character Data API
        try:
            await client.get_character_by_id(id=test_data["character_id"])
            coverage_report["character_data"].append("character_profiles")
        except Exception:
            pass

        try:
            await client.get_character_encounter_rankings(
                character_id=test_data["character_id"],
                encounter_id=test_data["encounter_id"],
            )
            coverage_report["character_data"].append("character_rankings")
        except Exception:
            pass

        # Guild Data API
        try:
            await client.get_guild_by_id(guild_id=test_data["guild_id"])
            coverage_report["guild_data"].append("guild_basic_info")
        except Exception:
            pass

        # Report Data API
        try:
            await client.get_report_by_code(code=test_data["report_code"])
            coverage_report["report_data"].append("individual_reports")
        except Exception:
            pass

        try:
            await client.get_report_events(code=test_data["report_code"], limit=1)
            coverage_report["report_data"].append("report_analysis")
        except Exception:
            pass

        try:
            await client.search_reports(guild_id=test_data["guild_id"], limit=1)
            coverage_report["report_data"].append("report_search")
        except Exception:
            pass

        # System Data API
        try:
            await client.get_rate_limit_data()
            coverage_report["system_data"].append("rate_limiting")
        except Exception:
            pass

        # Calculate coverage metrics
        total_features = sum(len(features) for features in coverage_report.values())

        # Assert we have good coverage
        assert total_features >= 10, f"API coverage too low: {coverage_report}"

        # Coverage report logged via pytest output capture
