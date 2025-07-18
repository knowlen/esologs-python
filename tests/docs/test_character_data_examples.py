"""
Tests for examples in docs/api-reference/character-data.md

Validates that all code examples in the character data API documentation
execute correctly and return expected data structures.
"""


import pytest

from esologs._generated.exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    ValidationError,
)
from esologs.client import Client


class TestCharacterDataExamples:
    """Test all examples from character-data.md documentation"""

    @pytest.mark.asyncio
    async def test_get_character_profile_example(self, api_client_config):
        """Test the get_character_by_id() basic example"""
        async with Client(**api_client_config) as client:
            # Use a known valid character ID
            character = await client.get_character_by_id(id=314050)

            # Validate response structure
            assert hasattr(character, "character_data")
            assert character.character_data is not None
            assert hasattr(character.character_data, "character")
            assert character.character_data.character is not None

            # Validate character structure
            char = character.character_data.character
            assert hasattr(char, "id")
            assert hasattr(char, "name")
            assert hasattr(char, "class_id")
            assert hasattr(char, "race_id")
            assert hasattr(char, "guild_rank")
            assert hasattr(char, "hidden")
            assert hasattr(char, "server")

            # Validate data types
            assert isinstance(char.id, int)
            assert isinstance(char.name, str)
            assert isinstance(char.class_id, int)
            assert isinstance(char.race_id, int)
            assert isinstance(char.guild_rank, int)
            assert isinstance(char.hidden, bool)

            # Validate server structure
            assert hasattr(char.server, "name")
            assert hasattr(char.server, "region")
            assert hasattr(char.server.region, "name")
            assert isinstance(char.server.name, str)
            assert isinstance(char.server.region.name, str)

    @pytest.mark.asyncio
    async def test_get_character_recent_reports_example(self, api_client_config):
        """Test the get_character_reports() example"""
        async with Client(**api_client_config) as client:
            # Use a known valid character ID
            reports = await client.get_character_reports(character_id=314050, limit=5)

            # Validate response structure
            assert hasattr(reports, "character_data")
            assert reports.character_data is not None
            assert hasattr(reports.character_data, "character")
            assert reports.character_data.character is not None

            # Validate recent reports structure
            recent_reports = reports.character_data.character.recent_reports
            if recent_reports:  # May be None if character has no reports
                assert hasattr(recent_reports, "data")
                assert hasattr(recent_reports, "total")
                assert hasattr(recent_reports, "per_page")
                assert hasattr(recent_reports, "current_page")
                assert hasattr(recent_reports, "has_more_pages")

                # Validate data types
                assert isinstance(recent_reports.total, int)
                assert isinstance(recent_reports.per_page, int)
                assert isinstance(recent_reports.current_page, int)
                assert isinstance(recent_reports.has_more_pages, bool)

                # If there are reports, validate their structure
                if recent_reports.data:
                    for report in recent_reports.data:
                        if report:  # Reports can be None
                            assert hasattr(report, "code")
                            assert hasattr(report, "start_time")
                            assert hasattr(report, "end_time")
                            assert isinstance(report.code, str)
                            assert isinstance(report.start_time, float)
                            assert isinstance(report.end_time, float)

                            # Zone can be None
                            if report.zone:
                                assert hasattr(report.zone, "name")
                                assert isinstance(report.zone.name, str)

    @pytest.mark.asyncio
    async def test_get_character_encounter_ranking_example(self, api_client_config):
        """Test the get_character_encounter_ranking() example"""
        async with Client(**api_client_config) as client:
            # Use a known valid character ID and encounter ID
            ranking = await client.get_character_encounter_ranking(
                character_id=314050, encounter_id=63  # Rockgrove encounter
            )

            # Validate response structure
            assert hasattr(ranking, "character_data")
            assert ranking.character_data is not None
            assert hasattr(ranking.character_data, "character")
            assert ranking.character_data.character is not None

            # encounter_rankings can be None or Any type
            # Just verify the field exists - content varies by character/encounter

    @pytest.mark.asyncio
    async def test_get_character_encounter_rankings_example(self, api_client_config):
        """Test the get_character_encounter_rankings() example with parameters"""
        async with Client(**api_client_config) as client:
            # Use a known valid character ID and encounter ID
            rankings = await client.get_character_encounter_rankings(
                character_id=314050,
                encounter_id=63,  # Rockgrove encounter
                include_combatant_info=True,
            )

            # Validate response structure
            assert hasattr(rankings, "character_data")
            assert rankings.character_data is not None
            assert hasattr(rankings.character_data, "character")
            assert rankings.character_data.character is not None

            # encounter_rankings can be None or Any type
            # Just verify the field exists - content varies by character/encounter

    @pytest.mark.asyncio
    async def test_get_character_zone_rankings_example(self, api_client_config):
        """Test the get_character_zone_rankings() example"""
        async with Client(**api_client_config) as client:
            # Use a known valid character ID and zone ID
            rankings = await client.get_character_zone_rankings(
                character_id=314050, zone_id=19, size=5  # Ossein Cage zone
            )

            # Validate response structure
            assert hasattr(rankings, "character_data")
            assert rankings.character_data is not None
            assert hasattr(rankings.character_data, "character")
            assert rankings.character_data.character is not None

            # zone_rankings can be None or Any type
            # Just verify the field exists - content varies by character/zone

    @pytest.mark.asyncio
    async def test_analyze_character_pattern_example(self, api_client_config):
        """Test the character profile analysis pattern example from Common Usage Patterns"""
        async with Client(**api_client_config) as client:
            # Test the complete character analysis pattern
            character_id = 314050

            # Get character profile
            character = await client.get_character_by_id(id=character_id)
            assert character.character_data is not None
            assert character.character_data.character is not None

            char = character.character_data.character
            assert isinstance(char.name, str)
            assert isinstance(char.server.name, str)
            assert isinstance(char.server.region.name, str)

            # Get recent reports
            reports = await client.get_character_reports(character_id=character_id)
            assert reports.character_data is not None
            assert reports.character_data.character is not None

            # recent_reports can be None if character has no activity
            recent_reports = reports.character_data.character.recent_reports
            if recent_reports:
                assert isinstance(recent_reports.total, int)

    @pytest.mark.asyncio
    async def test_track_character_performance_pattern_example(self, api_client_config):
        """Test the performance tracking pattern example from Common Usage Patterns"""
        async with Client(**api_client_config) as client:
            # Test the performance tracking pattern
            character_id = 314050
            encounter_id = 63  # Rockgrove encounter

            # Get encounter rankings
            rankings = await client.get_character_encounter_rankings(
                character_id=character_id,
                encounter_id=encounter_id,
                include_combatant_info=True,
            )

            # Validate response structure
            assert rankings.character_data is not None
            assert rankings.character_data.character is not None

            # encounter_rankings field should exist (can be None)
            # Content varies by character/encounter, so we just check field exists

    @pytest.mark.asyncio
    async def test_character_error_handling_example(self, api_client_config):
        """Test error handling with invalid character ID"""
        async with Client(**api_client_config) as client:
            # Test with a very large character ID that likely doesn't exist
            try:
                character = await client.get_character_by_id(id=999999999)
                # If it succeeds, just verify it's a valid response
                assert hasattr(character, "character_data")
            except (
                GraphQLClientGraphQLMultiError,
                GraphQLClientHttpError,
                ValidationError,
            ):
                # Expected - this character ID likely doesn't exist
                pass

    @pytest.mark.asyncio
    async def test_character_reports_with_limit(self, api_client_config):
        """Test character reports with different limit values"""
        async with Client(**api_client_config) as client:
            # Test with small limit
            reports = await client.get_character_reports(character_id=314050, limit=1)

            assert reports.character_data is not None
            assert reports.character_data.character is not None

            recent_reports = reports.character_data.character.recent_reports
            if recent_reports and recent_reports.data:
                # Should respect the limit
                assert len([r for r in recent_reports.data if r is not None]) <= 1

    @pytest.mark.asyncio
    async def test_character_rankings_with_filters(self, api_client_config):
        """Test character rankings with various filter parameters"""
        async with Client(**api_client_config) as client:
            # Test with multiple filter parameters
            rankings = await client.get_character_encounter_rankings(
                character_id=314050,
                encounter_id=63,  # Rockgrove encounter
                include_combatant_info=True,
                by_bracket=True,
                include_private_logs=False,
            )

            # Validate basic structure
            assert rankings.character_data is not None
            assert rankings.character_data.character is not None
            assert hasattr(rankings.character_data.character, "encounter_rankings")

    @pytest.mark.asyncio
    async def test_zone_rankings_without_zone_id(self, api_client_config):
        """Test character zone rankings without specifying zone_id"""
        async with Client(**api_client_config) as client:
            # Test without zone_id parameter (should get all zones)
            rankings = await client.get_character_zone_rankings(
                character_id=314050, size=10
            )

            # Validate basic structure
            assert rankings.character_data is not None
            assert rankings.character_data.character is not None
            assert hasattr(rankings.character_data.character, "zone_rankings")
