"""
Test all code examples from the progress race documentation.

This ensures our documentation examples actually work.
"""

import json

import pytest

from esologs import Client
from esologs._generated.exceptions import GraphQLClientGraphQLMultiError
from esologs._generated.get_progress_race import GetProgressRace


class TestProgressRaceExamples:
    """Test examples from the progress race documentation."""

    @pytest.mark.asyncio
    async def test_basic_progress_race_example(self, api_client_config):
        """Test the basic progress race tracking example."""
        async with Client(**api_client_config) as client:
            try:
                # Get current progress race standings
                race_data = await client.get_progress_race(
                    zone_id=40,  # Lucent Citadel
                    difficulty=2,  # Veteran
                    size=12,  # 12-person
                )

                # Verify response structure
                assert isinstance(race_data, GetProgressRace)
                assert hasattr(race_data, "progress_race_data")
                assert race_data.progress_race_data is not None

                if race_data.progress_race_data.progress_race:
                    # If data exists, verify it's JSON-serializable
                    data = race_data.progress_race_data.progress_race
                    json_str = json.dumps(data)
                    assert isinstance(json_str, str)
                else:
                    # No active race is also valid
                    assert race_data.progress_race_data.progress_race is None
            except GraphQLClientGraphQLMultiError as e:
                # Expected when no race is active for the game
                assert "No race supported for this game currently" in str(e)

    @pytest.mark.asyncio
    async def test_track_guild_progress_example(self, api_client_config):
        """Test the guild progress tracking example."""
        guild_id = 3468  # Test guild ID

        async with Client(**api_client_config) as client:
            try:
                # Check guild's standing
                result = await client.get_progress_race(
                    guild_id=guild_id, zone_id=40  # Current progression zone
                )

                # Verify response structure
                assert isinstance(result, GetProgressRace)
                assert hasattr(result, "progress_race_data")
                assert result.progress_race_data is not None

                if result.progress_race_data.progress_race:
                    data = result.progress_race_data.progress_race
                    # Data should be dict or list
                    assert isinstance(data, (dict, list))
                else:
                    # No data is valid (guild hasn't completed or no active race)
                    assert result.progress_race_data.progress_race is None
            except GraphQLClientGraphQLMultiError as e:
                # Expected when no race is active for the game
                assert "No race supported for this game currently" in str(e)

    @pytest.mark.asyncio
    async def test_monitor_server_race_example(self, api_client_config):
        """Test the server competition monitoring example."""
        region = "NA"

        async with Client(**api_client_config) as client:
            try:
                # Get server-specific standings
                result = await client.get_progress_race(
                    server_region=region,
                    server_slug="megaserver",
                    zone_id=40,
                    difficulty=2,
                    size=12,
                )

                # Verify response structure
                assert isinstance(result, GetProgressRace)
                assert hasattr(result, "progress_race_data")
                assert result.progress_race_data is not None

                if result.progress_race_data.progress_race:
                    standings = result.progress_race_data.progress_race
                    # Should be JSON data
                    assert isinstance(standings, (dict, list))
            except GraphQLClientGraphQLMultiError as e:
                # Expected when no race is active for the game
                assert "No race supported for this game currently" in str(e)

    @pytest.mark.asyncio
    async def test_compare_difficulties_example(self, api_client_config):
        """Test the difficulty comparison example."""
        zone_id = 40  # Lucent Citadel

        async with Client(**api_client_config) as client:
            difficulties = {1: "Normal", 2: "Veteran"}

            results = {}
            for diff_id, diff_name in difficulties.items():
                try:
                    result = await client.get_progress_race(
                        zone_id=zone_id, difficulty=diff_id, size=12
                    )

                    # Verify response structure
                    assert isinstance(result, GetProgressRace)
                    assert hasattr(result, "progress_race_data")
                    assert result.progress_race_data is not None

                    if result.progress_race_data.progress_race:
                        results[diff_name] = result.progress_race_data.progress_race
                    else:
                        results[diff_name] = None
                except GraphQLClientGraphQLMultiError as e:
                    # Expected when no race is active for the game
                    assert "No race supported for this game currently" in str(e)
                    results[diff_name] = "no_race"

            # Should have results for both difficulties
            assert "Normal" in results
            assert "Veteran" in results

    @pytest.mark.asyncio
    async def test_safe_progress_check_example(self, api_client_config):
        """Test the error handling example."""
        async with Client(**api_client_config) as client:
            try:
                # Use an invalid zone ID
                result = await client.get_progress_race(zone_id=999)

                # Should still get a valid response
                assert isinstance(result, GetProgressRace)
                assert hasattr(result, "progress_race_data")
                assert result.progress_race_data is not None

                # Check if race data exists
                if result.progress_race_data.progress_race is None:
                    # This is expected for invalid zone
                    assert True
                else:
                    # If data exists, it should be valid JSON
                    race_data = result.progress_race_data.progress_race
                    json.dumps(race_data)

            except GraphQLClientGraphQLMultiError as e:
                # This is now the expected behavior when no race is active
                assert "No race supported for this game currently" in str(e)
            except Exception as e:
                # Other exceptions should fail the test
                pytest.fail(f"Unexpected error: {e}")

    @pytest.mark.asyncio
    async def test_progress_race_all_params_example(self, api_client_config):
        """Test using all available parameters."""
        async with Client(**api_client_config) as client:
            try:
                # Test with all parameters
                result = await client.get_progress_race(
                    guild_id=3468,
                    zone_id=38,
                    competition_id=1,
                    difficulty=2,
                    size=12,
                    server_region="NA",
                    server_slug="megaserver",
                    guild_name="The Shadow Court",
                )

                # Verify response structure
                assert isinstance(result, GetProgressRace)
                assert hasattr(result, "progress_race_data")
                assert result.progress_race_data is not None

                # Any response (including None) is valid
            except GraphQLClientGraphQLMultiError as e:
                # Expected when no race is active for the game
                assert "No race supported for this game currently" in str(e)

    @pytest.mark.asyncio
    async def test_progress_race_minimal_example(self, api_client_config):
        """Test with no parameters (uses defaults)."""
        async with Client(**api_client_config) as client:
            try:
                # Call with no parameters
                result = await client.get_progress_race()

                # Should still get valid response
                assert isinstance(result, GetProgressRace)
                assert hasattr(result, "progress_race_data")
                assert result.progress_race_data is not None
            except GraphQLClientGraphQLMultiError as e:
                # Expected when no race is active for the game
                assert "No race supported for this game currently" in str(e)

    @pytest.mark.asyncio
    async def test_progress_race_json_flexibility(self, api_client_config):
        """Test that various JSON response formats are handled."""
        async with Client(**api_client_config) as client:
            # Test multiple scenarios
            test_cases = [
                {},  # No params
                {"zone_id": 38},  # Just zone
                {"guild_id": 3468, "zone_id": 40},  # Guild + zone
                {"difficulty": 2, "size": 8},  # Difficulty + size
            ]

            for params in test_cases:
                try:
                    result = await client.get_progress_race(**params)

                    # All should return valid structure
                    assert isinstance(result, GetProgressRace)
                    assert hasattr(result, "progress_race_data")
                    assert result.progress_race_data is not None

                    # If data exists, should be JSON-compatible
                    if result.progress_race_data.progress_race is not None:
                        json.dumps(result.progress_race_data.progress_race)
                except GraphQLClientGraphQLMultiError as e:
                    # Expected when no race is active for the game
                    assert "No race supported for this game currently" in str(e)
