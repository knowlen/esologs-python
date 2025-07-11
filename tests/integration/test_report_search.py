"""Integration tests for report search functionality."""

import pytest
from datetime import datetime, timedelta

from esologs.exceptions import ValidationError


@pytest.mark.integration
class TestReportSearchIntegration:
    """Integration tests for report search methods."""

    @pytest.mark.asyncio
    async def test_search_reports_by_guild_id(self, client, test_data):
        """Test searching reports by guild ID."""
        result = await client.search_reports(guild_id=test_data["guild_id"], limit=5)

        assert result is not None
        assert hasattr(result, "report_data")
        assert hasattr(result.report_data, "reports")
        assert hasattr(result.report_data.reports, "data")

        # Should return some reports
        reports = result.report_data.reports
        assert reports.total >= 0
        assert len(reports.data) <= 5  # Respects limit

        # Each report should have expected structure
        for report in reports.data:
            assert hasattr(report, "code")
            assert hasattr(report, "title")
            assert hasattr(report, "start_time")
            assert hasattr(report, "end_time")
            assert hasattr(report, "guild")
            assert report.guild.id == test_data["guild_id"]

    @pytest.mark.asyncio
    async def test_search_reports_with_pagination(self, client, test_data):
        """Test report search with pagination."""
        # Get first page
        page1 = await client.search_reports(
            guild_id=test_data["guild_id"], limit=3, page=1
        )

        # Get second page
        page2 = await client.search_reports(
            guild_id=test_data["guild_id"], limit=3, page=2
        )

        assert page1 is not None
        assert page2 is not None

        # Both should be valid responses
        assert page1.report_data.reports.current_page == 1
        assert page2.report_data.reports.current_page == 2

        # Pages should have different data (if enough reports exist)
        if len(page1.report_data.reports.data) > 0 and len(page2.report_data.reports.data) > 0:
            page1_codes = {r.code for r in page1.report_data.reports.data}
            page2_codes = {r.code for r in page2.report_data.reports.data}
            assert page1_codes != page2_codes

    @pytest.mark.asyncio
    async def test_search_reports_with_date_range(self, client, test_data):
        """Test report search with date range filtering."""
        # Search for recent reports (last 30 days)
        now = datetime.now()
        thirty_days_ago = now - timedelta(days=30)
        
        start_time = thirty_days_ago.timestamp() * 1000
        end_time = now.timestamp() * 1000

        result = await client.search_reports(
            guild_id=test_data["guild_id"],
            start_time=start_time,
            end_time=end_time,
            limit=5
        )

        assert result is not None
        reports = result.report_data.reports

        # All reports should be within the date range
        for report in reports.data:
            assert start_time <= report.start_time <= end_time

    @pytest.mark.asyncio
    async def test_search_reports_with_zone_filter(self, client, test_data):
        """Test report search with zone filtering."""
        result = await client.search_reports(
            guild_id=test_data["guild_id"],
            zone_id=test_data["zone_id"],
            limit=5
        )

        assert result is not None
        reports = result.report_data.reports

        # All reports should be from the specified zone
        for report in reports.data:
            if report.zone:  # Some reports might not have zone info
                assert report.zone.id == test_data["zone_id"]

    @pytest.mark.asyncio
    async def test_search_reports_no_results(self, client, test_data):
        """Test search with parameters that return no results."""
        # Use a very specific date range unlikely to have results with valid guild
        specific_date = datetime(2020, 1, 1)
        start_time = specific_date.timestamp() * 1000
        end_time = (specific_date + timedelta(hours=1)).timestamp() * 1000

        result = await client.search_reports(
            guild_id=test_data["guild_id"],  # Use valid guild ID
            start_time=start_time,  # But very old date range
            end_time=end_time
        )

        assert result is not None
        reports = result.report_data.reports
        assert reports.total == 0
        assert len(reports.data) == 0

    @pytest.mark.asyncio
    async def test_get_guild_reports_convenience(self, client, test_data):
        """Test get_guild_reports convenience method."""
        result = await client.get_guild_reports(
            guild_id=test_data["guild_id"], limit=3
        )

        assert result is not None
        reports = result.report_data.reports
        assert len(reports.data) <= 3

        # Should only contain reports from the specified guild
        for report in reports.data:
            assert report.guild.id == test_data["guild_id"]

    @pytest.mark.asyncio
    async def test_get_user_reports_convenience(self, client):
        """Test get_user_reports convenience method."""
        # Note: This test might not find results for every user
        # We'll test the structure even if no results are found
        result = await client.get_user_reports(user_id=1, limit=3)

        assert result is not None
        assert hasattr(result, "report_data")
        assert hasattr(result.report_data, "reports")
        reports = result.report_data.reports
        assert reports.total >= 0

    @pytest.mark.asyncio
    async def test_search_reports_limit_boundaries(self, client, test_data):
        """Test search with limit boundary values."""
        # Test minimum limit
        result = await client.search_reports(
            guild_id=test_data["guild_id"], limit=1
        )
        assert result is not None
        reports = result.report_data.reports
        assert len(reports.data) <= 1

        # Test maximum limit
        result = await client.search_reports(
            guild_id=test_data["guild_id"], limit=25
        )
        assert result is not None
        reports = result.report_data.reports
        assert len(reports.data) <= 25

    @pytest.mark.asyncio
    async def test_search_reports_response_structure(self, client, test_data):
        """Test that search response has expected structure."""
        result = await client.search_reports(guild_id=test_data["guild_id"], limit=1)

        assert result is not None
        assert hasattr(result, "report_data")

        reports = result.report_data.reports
        assert hasattr(reports, "data")
        assert hasattr(reports, "total")
        assert hasattr(reports, "per_page")
        assert hasattr(reports, "current_page")
        assert hasattr(reports, "from_")  # Note: from is a reserved word
        assert hasattr(reports, "to")
        assert hasattr(reports, "last_page")
        assert hasattr(reports, "has_more_pages")

        if len(reports.data) > 0:
            report = reports.data[0]
            assert hasattr(report, "code")
            assert hasattr(report, "title")
            assert hasattr(report, "start_time")
            assert hasattr(report, "end_time")
            assert hasattr(report, "zone")
            assert hasattr(report, "guild")
            assert hasattr(report, "owner")

            # Guild structure
            if report.guild:
                assert hasattr(report.guild, "id")
                assert hasattr(report.guild, "name")
                assert hasattr(report.guild, "server")

                if report.guild.server:
                    assert hasattr(report.guild.server, "name")
                    assert hasattr(report.guild.server, "slug")
                    assert hasattr(report.guild.server, "region")

            # Zone structure
            if report.zone:
                assert hasattr(report.zone, "id")
                assert hasattr(report.zone, "name")

            # Owner structure
            if report.owner:
                assert hasattr(report.owner, "id")
                assert hasattr(report.owner, "name")


@pytest.mark.integration
class TestReportSearchErrorHandling:
    """Integration tests for error handling in report search."""

    @pytest.mark.asyncio
    async def test_search_reports_invalid_guild_id(self, client):
        """Test search with invalid guild ID."""
        from esologs.exceptions import GraphQLClientGraphQLMultiError
        
        # Very large guild ID that likely doesn't exist
        with pytest.raises(GraphQLClientGraphQLMultiError) as exc_info:
            await client.search_reports(guild_id=999999999)
        
        # Should raise an error about guild not existing
        assert "No guild exists for this id" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_search_reports_rate_limiting_awareness(self, client, test_data):
        """Test that multiple concurrent searches don't cause issues."""
        import asyncio

        # Make multiple concurrent requests
        tasks = [
            client.search_reports(guild_id=test_data["guild_id"], limit=1)
            for _ in range(3)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # All should succeed or handle rate limiting gracefully
        for result in results:
            assert not isinstance(result, Exception) or "rate limit" in str(result).lower()

    @pytest.mark.asyncio
    async def test_search_reports_with_invalid_dates(self, client, test_data):
        """Test search with invalid date ranges."""
        # Future date that's too far ahead
        future_time = (datetime.now() + timedelta(days=3650)).timestamp() * 1000

        result = await client.search_reports(
            guild_id=test_data["guild_id"],
            start_time=future_time,
            limit=1
        )

        # Should handle gracefully and return no results
        assert result is not None
        reports = result.report_data.reports
        assert reports.total == 0


@pytest.mark.integration 
class TestReportSearchPerformance:
    """Integration tests for performance aspects of report search."""

    @pytest.mark.asyncio
    async def test_search_large_result_set(self, client, test_data):
        """Test search that returns maximum allowed results."""
        result = await client.search_reports(
            guild_id=test_data["guild_id"], limit=25
        )

        assert result is not None
        reports = result.report_data.reports

        # Response should be structured even with max results
        assert len(reports.data) <= 25
        assert reports.per_page == 25

    @pytest.mark.asyncio
    async def test_search_response_time(self, client, test_data):
        """Test that search responds within reasonable time."""
        import time

        start_time = time.time()
        result = await client.search_reports(guild_id=test_data["guild_id"], limit=5)
        end_time = time.time()

        response_time = end_time - start_time

        # Should respond within 10 seconds (reasonable for API call)
        assert response_time < 10.0
        assert result is not None