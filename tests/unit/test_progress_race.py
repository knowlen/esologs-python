"""
Unit tests for progress race API methods.

Tests the progress race tracking method.
"""

from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from esologs._generated.get_progress_race import GetProgressRace
from esologs.client import Client


class TestProgressRaceMethods:
    """Test progress race API method implementations."""

    def test_progress_race_method_exists(self):
        """Test that the progress race method is registered on the client."""
        client = Client(url="http://test.com", headers={})

        # Check that the progress race method exists
        assert hasattr(client, "get_progress_race")

    @pytest.mark.asyncio
    async def test_get_progress_race_all_params(self):
        """Test get_progress_race method with all parameters."""
        client = Client(url="http://test.com", headers={})

        # Mock the response data
        mock_response_data = {
            "progressRaceData": {
                "progressRace": {
                    "rankings": [
                        {
                            "guild": {
                                "id": 123,
                                "name": "Test Guild",
                                "faction": "Aldmeri Dominion",
                            },
                            "duration": 3600000,
                            "completionTime": 1640000000000,
                        }
                    ]
                }
            }
        }

        # Create mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"data": mock_response_data}
        mock_response.is_error = False

        # Mock the execute method
        client.execute = AsyncMock(return_value=mock_response)
        client.get_data = Mock(return_value=mock_response_data)

        # Call the method with all parameters
        result = await client.get_progress_race(
            guild_id=123,
            zone_id=38,
            competition_id=1,
            difficulty=1,
            size=12,
            server_region="NA",
            server_subregion="US",
            server_slug="megaserver",
            guild_name="Test Guild",
        )

        # Verify the result
        assert isinstance(result, GetProgressRace)
        assert result.progress_race_data is not None
        assert result.progress_race_data.progress_race is not None
        assert (
            result.progress_race_data.progress_race
            == mock_response_data["progressRaceData"]["progressRace"]
        )

        # Verify the GraphQL query was called with correct parameters
        client.execute.assert_called_once()
        args, kwargs = client.execute.call_args
        assert kwargs["operation_name"] == "getProgressRace"
        assert kwargs["variables"]["guildID"] == 123
        assert kwargs["variables"]["zoneID"] == 38
        assert kwargs["variables"]["competitionID"] == 1
        assert kwargs["variables"]["difficulty"] == 1
        assert kwargs["variables"]["size"] == 12
        assert kwargs["variables"]["serverRegion"] == "NA"
        assert kwargs["variables"]["serverSubregion"] == "US"
        assert kwargs["variables"]["serverSlug"] == "megaserver"
        assert kwargs["variables"]["guildName"] == "Test Guild"

    @pytest.mark.asyncio
    async def test_get_progress_race_minimal_params(self):
        """Test get_progress_race method with minimal parameters."""
        client = Client(url="http://test.com", headers={})

        # Mock the response data - no active race
        mock_response_data = {"progressRaceData": {"progressRace": None}}

        # Create mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"data": mock_response_data}
        mock_response.is_error = False

        # Mock the execute method
        client.execute = AsyncMock(return_value=mock_response)
        client.get_data = Mock(return_value=mock_response_data)

        # Call the method with no parameters
        result = await client.get_progress_race()

        # Verify the result
        assert isinstance(result, GetProgressRace)
        assert result.progress_race_data is not None
        assert result.progress_race_data.progress_race is None

        # Verify the GraphQL query was called
        client.execute.assert_called_once()
        args, kwargs = client.execute.call_args
        assert kwargs["operation_name"] == "getProgressRace"

    @pytest.mark.asyncio
    async def test_get_progress_race_guild_filter(self):
        """Test get_progress_race method with guild-specific filters."""
        client = Client(url="http://test.com", headers={})

        # Mock the response data
        mock_response_data = {
            "progressRaceData": {
                "progressRace": {
                    "guild": {
                        "id": 456,
                        "name": "Specific Guild",
                        "rank": 5,
                        "duration": 7200000,
                    }
                }
            }
        }

        # Create mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"data": mock_response_data}
        mock_response.is_error = False

        # Mock the execute method
        client.execute = AsyncMock(return_value=mock_response)
        client.get_data = Mock(return_value=mock_response_data)

        # Call the method with guild filters
        result = await client.get_progress_race(
            guild_id=456, zone_id=40  # Lucent Citadel
        )

        # Verify the result
        assert isinstance(result, GetProgressRace)
        assert result.progress_race_data is not None
        assert result.progress_race_data.progress_race is not None
        assert "guild" in result.progress_race_data.progress_race

        # Verify only specified parameters were sent
        client.execute.assert_called_once()
        args, kwargs = client.execute.call_args
        variables = kwargs["variables"]
        assert variables["guildID"] == 456
        assert variables["zoneID"] == 40

    @pytest.mark.asyncio
    async def test_get_progress_race_competition_filter(self):
        """Test get_progress_race method with competition and difficulty filters."""
        client = Client(url="http://test.com", headers={})

        # Mock the response data - JSON can be any structure
        mock_response_data = {
            "progressRaceData": {
                "progressRace": [
                    {"rank": 1, "guild": "Top Guild", "time": "2:30:45"},
                    {"rank": 2, "guild": "Second Guild", "time": "2:45:30"},
                ]
            }
        }

        # Create mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"data": mock_response_data}
        mock_response.is_error = False

        # Mock the execute method
        client.execute = AsyncMock(return_value=mock_response)
        client.get_data = Mock(return_value=mock_response_data)

        # Call the method with competition filters
        result = await client.get_progress_race(
            competition_id=2, difficulty=2, size=8  # Hard mode 8-person
        )

        # Verify the result
        assert isinstance(result, GetProgressRace)
        assert result.progress_race_data is not None
        assert result.progress_race_data.progress_race is not None
        assert isinstance(result.progress_race_data.progress_race, list)
        assert len(result.progress_race_data.progress_race) == 2

        # Verify parameters
        client.execute.assert_called_once()
        args, kwargs = client.execute.call_args
        variables = kwargs["variables"]
        assert variables["competitionID"] == 2
        assert variables["difficulty"] == 2
        assert variables["size"] == 8
