"""
Integration tests for progress race API endpoints.

These tests make real API calls to verify progress race functionality.
Note: Progress race data is only available during active progression races.
"""

import pytest

from esologs import Client
from esologs._generated.get_progress_race import GetProgressRace


class TestProgressRaceAPI:
    """Test progress race API endpoints with real API calls."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_progress_race_no_params(self, api_client_config):
        """Test fetching progress race data with no parameters."""
        async with Client(**api_client_config) as client:
            result = await client.get_progress_race()

            # Verify response structure
            assert isinstance(result, GetProgressRace)
            assert hasattr(result, "progress_race_data")
            assert result.progress_race_data is not None

            # The progressRace field can be None if no race is active
            # or can contain JSON data (any structure)
            if result.progress_race_data.progress_race is not None:
                # If data exists, it should be a dict or list
                assert isinstance(result.progress_race_data.progress_race, (dict, list))

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_progress_race_with_zone(self, api_client_config):
        """Test fetching progress race data for a specific zone."""
        async with Client(**api_client_config) as client:
            # Test with Dreadsail Reef (zone 38)
            result = await client.get_progress_race(zone_id=38)

            # Verify response structure
            assert isinstance(result, GetProgressRace)
            assert hasattr(result, "progress_race_data")
            assert result.progress_race_data is not None

            # Progress race data may be None if no race is active for this zone
            # This is expected behavior

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_progress_race_with_guild(self, api_client_config):
        """Test fetching progress race data for a specific guild."""
        async with Client(**api_client_config) as client:
            # Test with a known guild ID
            result = await client.get_progress_race(guild_id=3468, zone_id=38)

            # Verify response structure
            assert isinstance(result, GetProgressRace)
            assert hasattr(result, "progress_race_data")
            assert result.progress_race_data is not None

            # Data might be None if guild hasn't participated or no active race
            # This is normal behavior

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_progress_race_with_difficulty(self, api_client_config):
        """Test fetching progress race data with difficulty and size filters."""
        async with Client(**api_client_config) as client:
            # Test with veteran difficulty (2) and 12-person size
            result = await client.get_progress_race(
                zone_id=40,  # Lucent Citadel
                difficulty=2,  # Veteran
                size=12,  # 12-person
            )

            # Verify response structure
            assert isinstance(result, GetProgressRace)
            assert hasattr(result, "progress_race_data")
            assert result.progress_race_data is not None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_progress_race_with_server_filters(self, api_client_config):
        """Test fetching progress race data with server filters."""
        async with Client(**api_client_config) as client:
            # Test with NA server filters
            result = await client.get_progress_race(
                server_region="NA", server_slug="megaserver", zone_id=38
            )

            # Verify response structure
            assert isinstance(result, GetProgressRace)
            assert hasattr(result, "progress_race_data")
            assert result.progress_race_data is not None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_progress_race_all_params(self, api_client_config):
        """Test fetching progress race data with all parameters."""
        async with Client(**api_client_config) as client:
            # Test with all available parameters
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

            # Even with all filters, data might be None if no matching race
            # This is expected behavior

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_progress_race_invalid_zone(self, api_client_config):
        """Test fetching progress race data with invalid zone ID."""
        async with Client(**api_client_config) as client:
            # Test with invalid zone ID - should not raise error
            result = await client.get_progress_race(zone_id=99999)

            # API should still return a valid response structure
            assert isinstance(result, GetProgressRace)
            assert hasattr(result, "progress_race_data")
            assert result.progress_race_data is not None

            # Progress race data should be None for invalid zone
            assert result.progress_race_data.progress_race is None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_progress_race_response_flexibility(self, api_client_config):
        """Test that progress race can handle various JSON response formats."""
        async with Client(**api_client_config) as client:
            # Multiple calls to test different response structures
            zones_to_test = [38, 40, 41]  # Different raid zones

            for zone_id in zones_to_test:
                result = await client.get_progress_race(zone_id=zone_id)

                # Basic structure validation
                assert isinstance(result, GetProgressRace)
                assert hasattr(result, "progress_race_data")
                assert result.progress_race_data is not None

                # If data exists, it should be JSON-serializable
                if result.progress_race_data.progress_race is not None:
                    import json

                    # Should be able to serialize the data
                    json_str = json.dumps(result.progress_race_data.progress_race)
                    assert isinstance(json_str, str)
