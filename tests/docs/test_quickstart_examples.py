"""Tests for quickstart.md code examples.

This module tests all code blocks from docs/quickstart.md to ensure they
execute without errors and produce expected results.
"""

import asyncio
import pytest
from esologs.client import Client
from esologs.exceptions import GraphQLClientHttpError, GraphQLClientGraphQLError, ValidationError
from access_token import get_access_token


class TestQuickstartExamples:
    """Test all code examples from quickstart.md."""

    @pytest.mark.asyncio
    async def test_first_api_call(self, api_client_config):
        """Test: Your First API Call example."""
        # This tests the hello_esologs() function from quickstart
        async with Client(**api_client_config) as client:
            # Check rate limits
            rate_limit = await client.get_rate_limit_data()
            
            # Verify we get expected structure
            assert hasattr(rate_limit, 'rate_limit_data')
            assert hasattr(rate_limit.rate_limit_data, 'limit_per_hour')
            assert hasattr(rate_limit.rate_limit_data, 'points_spent_this_hour')
            
            # Verify reasonable values
            assert rate_limit.rate_limit_data.limit_per_hour > 0
            assert rate_limit.rate_limit_data.points_spent_this_hour >= 0

    @pytest.mark.asyncio
    async def test_async_await_pattern(self, api_client_config):
        """Test: Async/Await Pattern example."""
        async with Client(**api_client_config) as client:
            result = await client.get_abilities()
            
            # Verify structure matches documentation example
            assert hasattr(result, 'game_data')
            assert hasattr(result.game_data, 'abilities')
            assert hasattr(result.game_data.abilities, 'data')
            assert len(result.game_data.abilities.data) > 0

    @pytest.mark.asyncio
    async def test_client_context_manager(self, api_client_config, test_character_id):
        """Test: Client Context Manager example."""
        async with Client(**api_client_config) as client:
            # Client automatically closes connections when done
            result = await client.get_character_by_id(test_character_id)
            
            # Verify we get character data
            assert hasattr(result, 'character_data')
            assert hasattr(result.character_data, 'character')
            assert hasattr(result.character_data.character, 'name')

    @pytest.mark.asyncio
    async def test_error_handling(self, api_client_config, test_character_id):
        """Test: Error Handling example."""
        # Test that the error handling structure works
        async with Client(**api_client_config) as client:
            try:
                character = await client.get_character_by_id(test_character_id)
                # If successful, verify structure
                assert hasattr(character.character_data.character, 'name')
                
            except GraphQLClientHttpError as e:
                # Verify we can access status code
                assert hasattr(e, 'status_code')
                assert isinstance(e.status_code, int)
                
            except GraphQLClientGraphQLError as e:
                # Verify we can access message
                assert hasattr(e, 'message')
                
            except ValidationError as e:
                # Verify it's a proper validation error
                assert str(e)

    @pytest.mark.asyncio
    async def test_game_data_exploration(self, api_client_config):
        """Test: Game Data Exploration example."""
        async with Client(**api_client_config) as client:
            # Get abilities with pagination
            abilities = await client.get_abilities(limit=10, page=1)
            assert len(abilities.game_data.abilities.data) <= 10
            assert len(abilities.game_data.abilities.data) > 0
            
            # Verify each ability has expected attributes
            for ability in abilities.game_data.abilities.data:
                assert hasattr(ability, 'name')
                
            # Get character classes - verify it's a direct list
            classes = await client.get_classes()
            assert isinstance(classes.game_data.classes, list)
            assert len(classes.game_data.classes) > 0
            
            # Verify each class has expected attributes
            for cls in classes.game_data.classes:
                assert hasattr(cls, 'name')
            
            # Get zones - verify it's a direct list
            zones = await client.get_zones()
            assert isinstance(zones.world_data.zones, list)
            assert len(zones.world_data.zones) > 0
            
            # Verify each zone has expected attributes
            for zone in zones.world_data.zones[:5]:  # Test first 5
                assert hasattr(zone, 'name')

    @pytest.mark.asyncio
    async def test_character_analysis(self, api_client_config, test_character_id):
        """Test: Character Analysis example."""
        async with Client(**api_client_config) as client:
            # Get character profile
            character = await client.get_character_by_id(id=test_character_id)
            char_data = character.character_data.character
            
            # Verify available attributes match documentation
            assert hasattr(char_data, 'name')
            assert hasattr(char_data, 'server')
            assert hasattr(char_data.server, 'name')
            assert hasattr(char_data, 'class_id')
            assert hasattr(char_data, 'race_id')
            
            # Verify types
            assert isinstance(char_data.name, str)
            assert isinstance(char_data.class_id, int)
            assert isinstance(char_data.race_id, int)
            
            # Get recent reports
            reports = await client.get_character_reports(
                character_id=test_character_id, 
                limit=5
            )
            
            # Verify reports structure
            assert hasattr(reports, 'character_data')
            assert hasattr(reports.character_data, 'character')
            assert hasattr(reports.character_data.character, 'recent_reports')
            assert hasattr(reports.character_data.character.recent_reports, 'data')
            
            # Verify each report has expected attributes for duration calculation
            for report in reports.character_data.character.recent_reports.data:
                assert hasattr(report, 'end_time')
                assert hasattr(report, 'start_time')
                assert hasattr(report, 'code')
                assert hasattr(report, 'zone')
                assert hasattr(report.zone, 'name')

    @pytest.mark.asyncio
    async def test_report_search(self, api_client_config, test_guild_id, test_zone_id):
        """Test: Report Search example."""
        async with Client(**api_client_config) as client:
            # Search reports with filtering
            reports = await client.search_reports(
                guild_id=test_guild_id,
                zone_id=test_zone_id,
                limit=10
            )
            
            # Verify structure (results may be empty with test IDs)
            assert hasattr(reports, 'report_data')
            
            # If we have reports, verify structure
            if reports.report_data and reports.report_data.reports:
                assert hasattr(reports.report_data.reports, 'data')
                
                for report in reports.report_data.reports.data:
                    assert hasattr(report, 'end_time')
                    assert hasattr(report, 'start_time')
                    assert hasattr(report, 'code')
                    assert hasattr(report, 'zone')
                    assert hasattr(report.zone, 'name')

    @pytest.mark.asyncio
    async def test_type_safety_example(self, api_client_config):
        """Test: Type Safety example."""
        async with Client(**api_client_config) as client:
            # Response is fully typed
            abilities = await client.get_abilities(limit=5)
            
            # Verify structure for type safety demonstration
            assert hasattr(abilities, 'game_data')
            assert hasattr(abilities.game_data, 'abilities')
            assert hasattr(abilities.game_data.abilities, 'data')
            assert len(abilities.game_data.abilities.data) <= 5
            
            # IDE will provide autocomplete and type checking
            for ability in abilities.game_data.abilities.data:
                assert hasattr(ability, 'name')
                assert hasattr(ability, 'icon')
                assert isinstance(ability.name, str)
                assert isinstance(ability.icon, str)

    @pytest.mark.asyncio
    async def test_data_validation_example(self, api_client_config):
        """Test: Data Validation example."""
        async with Client(**api_client_config) as client:
            # This should pass validation
            reports = await client.search_reports(
                limit=25,        # Valid: 1-25
                page=1,          # Valid: >= 1
                start_time=1640995200000  # Valid timestamp
            )
            
            # Verify we get a response structure
            assert hasattr(reports, 'report_data')
            
            # Test that invalid parameters raise ValidationError
            with pytest.raises(ValidationError):
                await client.search_reports(limit=100)  # Invalid: > 25

    @pytest.mark.asyncio
    async def test_character_dashboard(self, api_client_config, test_character_id):
        """Test: Character Dashboard example."""
        async with Client(**api_client_config) as client:
            # Get character info
            character = await client.get_character_by_id(id=test_character_id)
            char_data = character.character_data.character
            
            # Verify dashboard data is available
            assert isinstance(char_data.name, str)
            assert isinstance(char_data.server.name, str)
            assert isinstance(char_data.class_id, int)
            assert isinstance(char_data.race_id, int)
            
            # Get recent activity
            reports = await client.get_character_reports(character_id=test_character_id, limit=3)
            
            # Verify recent activity structure
            assert hasattr(reports.character_data.character.recent_reports, 'data')
            
            # Verify duration calculation works
            for report in reports.character_data.character.recent_reports.data:
                duration = (report.end_time - report.start_time) / 1000
                assert isinstance(duration, (int, float))
                assert duration >= 0

    @pytest.mark.asyncio
    async def test_guild_monitor(self, api_client_config, test_guild_id):
        """Test: Guild Monitor example."""
        async with Client(**api_client_config) as client:
            # Get guild info
            guild = await client.get_guild_by_id(guild_id=test_guild_id)
            guild_data = guild.guild_data.guild
            
            # Verify guild data structure
            assert hasattr(guild_data, 'name')
            assert hasattr(guild_data, 'server')
            assert hasattr(guild_data.server, 'name')
            assert isinstance(guild_data.name, str)
            assert isinstance(guild_data.server.name, str)
            
            # Get recent guild reports
            reports = await client.get_guild_reports(guild_id=test_guild_id, limit=5)
            
            # Verify reports structure
            assert hasattr(reports, 'report_data')
            
            # If we have reports, verify duration calculation
            if reports.report_data and reports.report_data.reports:
                for report in reports.report_data.reports.data:
                    duration = (report.end_time - report.start_time) / 1000
                    assert isinstance(duration, (int, float))
                    assert duration >= 0


class TestDocumentationIntegrity:
    """Additional tests for documentation integrity."""
    
    def test_access_token_import(self):
        """Test that access_token module is importable."""
        # This validates the documentation assumption
        from access_token import get_access_token
        assert callable(get_access_token)
    
    def test_required_exceptions_importable(self):
        """Test that all exceptions used in docs are importable."""
        from esologs.exceptions import (
            GraphQLClientHttpError, 
            GraphQLClientGraphQLError, 
            ValidationError
        )
        
        # Verify they're proper exception classes
        assert issubclass(GraphQLClientHttpError, Exception)
        assert issubclass(GraphQLClientGraphQLError, Exception)
        assert issubclass(ValidationError, Exception)
    
    def test_client_importable(self):
        """Test that Client class is importable."""
        from esologs.client import Client
        assert Client is not None
