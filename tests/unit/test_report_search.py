"""Unit tests for report search functionality."""

from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from esologs.client import Client
from esologs.validators import (
    ValidationError,
    parse_date_to_timestamp,
    validate_guild_search_params,
    validate_report_search_params,
)


class TestReportSearchValidation:
    """Test parameter validation for report search."""

    def test_validate_report_search_params_valid(self):
        """Test validation passes for valid parameters."""
        # Should not raise any exceptions
        validate_report_search_params(
            guild_name="Test Guild",
            guild_server_slug="test-server",
            guild_server_region="NA",
            limit=10,
            page=1,
        )

    def test_validate_report_search_params_guild_name_missing_server(self):
        """Test guild name requires server info."""
        with pytest.raises(ValidationError, match="guild_name requires both"):
            validate_report_search_params(guild_name="Test Guild")

        with pytest.raises(ValidationError, match="guild_name requires both"):
            validate_report_search_params(
                guild_name="Test Guild", guild_server_slug="test-server"
            )

    def test_validate_report_search_params_limit_validation(self):
        """Test limit parameter validation."""
        with pytest.raises(ValidationError, match="Limit must be an integer"):
            validate_report_search_params(limit="10")

        with pytest.raises(ValidationError, match="Limit must be between 1 and 25"):
            validate_report_search_params(limit=0)

        with pytest.raises(ValidationError, match="Limit must be between 1 and 25"):
            validate_report_search_params(limit=26)

    def test_validate_report_search_params_page_validation(self):
        """Test page parameter validation."""
        with pytest.raises(ValidationError, match="page must be an integer"):
            validate_report_search_params(page="1")

        with pytest.raises(ValidationError, match="page must be positive"):
            validate_report_search_params(page=0)

    def test_validate_guild_search_params_valid(self):
        """Test guild search parameter validation."""
        # Guild ID only
        validate_guild_search_params(guild_id=123)

        # Guild name with server info only
        validate_guild_search_params(
            guild_name="Test Guild",
            guild_server_slug="test-server",
            guild_server_region="NA",
        )

        # No guild filtering (should be fine)
        validate_guild_search_params()

    def test_validate_guild_search_params_conflicting(self):
        """Test conflicting guild parameters."""
        with pytest.raises(
            ValidationError, match="Provide either guild_id OR guild_name"
        ):
            validate_guild_search_params(
                guild_id=123,
                guild_name="Test Guild",
                guild_server_slug="test-server",
                guild_server_region="NA",
            )

    def test_validate_guild_search_params_invalid_guild_id(self):
        """Test invalid guild ID validation."""
        with pytest.raises(ValidationError, match="guild_id must be an integer"):
            validate_guild_search_params(guild_id="123")

        with pytest.raises(ValidationError, match="guild_id must be positive"):
            validate_guild_search_params(guild_id=-1)


class TestDateTimestampParsing:
    """Test date to timestamp conversion utilities."""

    def test_parse_timestamp_seconds(self):
        """Test parsing timestamp in seconds."""
        # Unix epoch start (Jan 1, 1970)
        result = parse_date_to_timestamp(0)
        assert result == 0.0

        # Small timestamp (assume seconds, convert to milliseconds)
        result = parse_date_to_timestamp(1672531200)  # Jan 1, 2023 in seconds
        assert result == 1672531200000.0  # Should convert to milliseconds

    def test_parse_timestamp_milliseconds(self):
        """Test parsing timestamp in milliseconds."""
        # Large timestamp (assume already in milliseconds)
        timestamp_ms = 1672531200000  # Jan 1, 2023 in milliseconds
        result = parse_date_to_timestamp(timestamp_ms)
        assert result == timestamp_ms

    def test_parse_datetime_object(self):
        """Test parsing datetime object."""
        dt = datetime(2023, 1, 1, 12, 0, 0)
        result = parse_date_to_timestamp(dt)
        expected = dt.timestamp() * 1000
        assert result == expected

    def test_parse_string_dates(self):
        """Test parsing various string date formats."""
        # Date only
        result = parse_date_to_timestamp("2023-01-01")
        expected = datetime(2023, 1, 1).timestamp() * 1000
        assert result == expected

        # Date with time
        result = parse_date_to_timestamp("2023-01-01T12:00:00")
        expected = datetime(2023, 1, 1, 12, 0, 0).timestamp() * 1000
        assert result == expected

        # Date with time and Z
        result = parse_date_to_timestamp("2023-01-01T12:00:00Z")
        expected = datetime(2023, 1, 1, 12, 0, 0).timestamp() * 1000
        assert result == expected

    def test_parse_string_timestamp(self):
        """Test parsing timestamp as string."""
        result = parse_date_to_timestamp("1672531200")
        assert result == 1672531200000.0

    def test_parse_invalid_date_format(self):
        """Test parsing invalid date formats."""
        with pytest.raises(ValidationError, match="Invalid date format"):
            parse_date_to_timestamp("not-a-date")

        with pytest.raises(ValidationError, match="Invalid date format"):
            parse_date_to_timestamp("2023/01/01")  # Wrong format

    def test_parse_unsupported_type(self):
        """Test parsing unsupported data types."""
        with pytest.raises(ValidationError, match="Unsupported date type"):
            parse_date_to_timestamp(["2023-01-01"])  # List is not supported


class TestReportSearchMethods:
    """Test report search methods on Client."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = Client(url="http://test.com", headers={})
        # Mock the underlying get_reports method
        client.get_reports = AsyncMock()
        return client

    @pytest.mark.asyncio
    async def test_search_reports_basic(self, mock_client):
        """Test basic search_reports functionality."""
        await mock_client.search_reports(guild_id=123)

        # Verify get_reports was called with correct parameters
        mock_client.get_reports.assert_called_once()
        call_kwargs = mock_client.get_reports.call_args.kwargs
        assert call_kwargs["guild_id"] == 123

    @pytest.mark.asyncio
    async def test_search_reports_with_all_params(self, mock_client):
        """Test search_reports with all parameters."""
        await mock_client.search_reports(
            guild_id=123,
            guild_name="Test Guild",
            guild_server_slug="test-server",
            guild_server_region="NA",
            guild_tag_id=456,
            user_id=789,
            zone_id=101,
            game_zone_id=102,
            start_time=1640995200000,
            end_time=1672531200000,
            limit=20,
            page=2,
        )

        # Verify all parameters were passed through
        call_kwargs = mock_client.get_reports.call_args.kwargs
        assert call_kwargs["guild_id"] == 123
        assert call_kwargs["guild_name"] == "Test Guild"
        assert call_kwargs["guild_server_slug"] == "test-server"
        assert call_kwargs["guild_server_region"] == "NA"
        assert call_kwargs["guild_tag_id"] == 456
        assert call_kwargs["user_id"] == 789
        assert call_kwargs["zone_id"] == 101
        assert call_kwargs["game_zone_id"] == 102
        assert call_kwargs["start_time"] == 1640995200000
        assert call_kwargs["end_time"] == 1672531200000
        assert call_kwargs["limit"] == 20
        assert call_kwargs["page"] == 2

    @pytest.mark.asyncio
    async def test_get_guild_reports(self, mock_client):
        """Test get_guild_reports convenience method."""
        await mock_client.get_guild_reports(
            guild_id=123, limit=25, page=1, start_time=1640995200000
        )

        # Verify search_reports was called internally
        mock_client.get_reports.assert_called_once()
        call_kwargs = mock_client.get_reports.call_args.kwargs
        assert call_kwargs["guild_id"] == 123
        assert call_kwargs["limit"] == 25
        assert call_kwargs["page"] == 1
        assert call_kwargs["start_time"] == 1640995200000

    @pytest.mark.asyncio
    async def test_get_user_reports(self, mock_client):
        """Test get_user_reports convenience method."""
        await mock_client.get_user_reports(
            user_id=456, limit=10, zone_id=789, end_time=1672531200000
        )

        # Verify search_reports was called internally
        mock_client.get_reports.assert_called_once()
        call_kwargs = mock_client.get_reports.call_args.kwargs
        assert call_kwargs["user_id"] == 456
        assert call_kwargs["limit"] == 10
        assert call_kwargs["zone_id"] == 789
        assert call_kwargs["end_time"] == 1672531200000

    @pytest.mark.asyncio
    async def test_convenience_methods_kwargs_not_passed(self, mock_client):
        """Test that extra kwargs are NOT passed through in convenience methods."""
        custom_kwarg = {"custom_param": "test_value"}

        # This should work without error, but kwargs won't be passed through
        await mock_client.get_guild_reports(guild_id=123, **custom_kwarg)

        # Verify only the expected parameters were passed through
        call_kwargs = mock_client.get_reports.call_args.kwargs
        # Only standard parameters should be present
        assert "guild_id" in call_kwargs
        assert call_kwargs["guild_id"] == 123
        # Custom kwargs should NOT be passed through
        assert "custom_param" not in call_kwargs


class TestReportSearchIntegration:
    """Integration tests for report search parameter handling."""

    def test_search_methods_exist_on_client(self):
        """Test that search methods exist on Client class."""
        client = Client(url="http://test.com", headers={})

        # Verify methods exist
        assert hasattr(client, "search_reports")
        assert hasattr(client, "get_guild_reports")
        assert hasattr(client, "get_user_reports")

        # Verify methods are callable
        assert callable(client.search_reports)
        assert callable(client.get_guild_reports)
        assert callable(client.get_user_reports)

    def test_search_method_signatures(self):
        """Test that search methods have correct signatures."""
        client = Client(url="http://test.com", headers={})

        # Get method signatures
        import inspect

        search_sig = inspect.signature(client.search_reports)
        guild_sig = inspect.signature(client.get_guild_reports)
        user_sig = inspect.signature(client.get_user_reports)

        # Verify search_reports has all expected parameters (excluding 'self')
        search_params = list(search_sig.parameters.keys())
        expected_search_params = [
            "guild_id",
            "guild_name",
            "guild_server_slug",
            "guild_server_region",
            "guild_tag_id",
            "user_id",
            "zone_id",
            "game_zone_id",
            "start_time",
            "end_time",
            "limit",
            "page",
            "kwargs",
        ]
        assert search_params == expected_search_params

        # Verify convenience methods have required parameters
        assert "guild_id" in guild_sig.parameters
        assert "user_id" in user_sig.parameters
