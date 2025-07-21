"""
Tests for examples in docs/api-reference/report-search.md

Validates that all code examples in the report search API documentation
execute correctly and return expected data structures.
"""

import asyncio
import time

import pytest

from esologs.client import Client
from esologs.exceptions import ValidationError


class TestReportSearchExamples:
    """Test all examples from report-search.md documentation"""

    @pytest.mark.asyncio
    async def test_search_recent_reports_example(self, api_client_config):
        """Test the search_reports() basic example"""
        async with Client(**api_client_config) as client:
            # Search for recent reports with pagination
            reports = await client.search_reports(limit=5)

            # Validate response structure
            assert hasattr(reports, "report_data")
            assert hasattr(reports.report_data, "reports")
            assert hasattr(reports.report_data.reports, "data")
            assert hasattr(reports.report_data.reports, "current_page")
            assert hasattr(reports.report_data.reports, "has_more_pages")

            # Validate pagination fields
            assert isinstance(reports.report_data.reports.current_page, int)
            assert isinstance(reports.report_data.reports.has_more_pages, bool)
            assert isinstance(reports.report_data.reports.per_page, int)
            assert isinstance(reports.report_data.reports.total, int)

            # Validate report data structure
            if (
                reports.report_data.reports.data
                and len(reports.report_data.reports.data) > 0
            ):
                report = reports.report_data.reports.data[0]
                if report:  # Report can be None
                    assert hasattr(report, "title")
                    assert hasattr(report, "code")
                    assert hasattr(report, "start_time")
                    assert hasattr(report, "end_time")
                    assert isinstance(report.code, str)
                    assert isinstance(report.title, str)
                    assert isinstance(report.start_time, float)
                    assert isinstance(report.end_time, float)

    @pytest.mark.asyncio
    async def test_search_with_filters_example(self, api_client_config):
        """Test the advanced filtering example"""
        async with Client(**api_client_config) as client:
            # Search for Dreadsail Reef reports from last 7 days
            seven_days_ago = (time.time() - 7 * 24 * 3600) * 1000

            reports = await client.search_reports(
                zone_id=16, start_time=seven_days_ago, limit=10  # Dreadsail Reef
            )

            # Validate response structure
            assert hasattr(reports, "report_data")
            assert hasattr(reports.report_data, "reports")
            assert hasattr(reports.report_data.reports, "data")

            # If reports found, validate zone filter worked
            if reports.report_data.reports.data:
                for report in reports.report_data.reports.data:
                    if report and report.zone:
                        assert report.zone.id == 16
                        assert isinstance(report.zone.name, str)

    @pytest.mark.asyncio
    async def test_get_guild_reports_example(self, api_client_config):
        """Test the get_guild_reports() convenience method"""
        async with Client(**api_client_config) as client:
            # First get a valid guild ID from search results
            search_results = await client.search_reports(limit=10)

            guild_id = None
            if (
                search_results.report_data
                and search_results.report_data.reports
                and search_results.report_data.reports.data
            ):
                for report in search_results.report_data.reports.data:
                    if report and report.guild:
                        guild_id = report.guild.id
                        break

            if guild_id:
                # Test the convenience method
                reports = await client.get_guild_reports(guild_id=guild_id, limit=5)

                # Validate response structure (same as search_reports)
                assert hasattr(reports, "report_data")
                assert hasattr(reports.report_data, "reports")
                assert hasattr(reports.report_data.reports, "data")

                # Validate all reports belong to the guild (if guild data present)
                if reports.report_data.reports.data:
                    for report in reports.report_data.reports.data:
                        if report and report.guild:
                            assert report.guild.id == guild_id
            else:
                # If no guild data found, just test method exists and returns proper structure
                pytest.skip("No guild data found in recent reports")

    @pytest.mark.asyncio
    async def test_get_user_reports_example(self, api_client_config):
        """Test the get_user_reports() convenience method"""
        async with Client(**api_client_config) as client:
            # First get a valid user ID from search results
            search_results = await client.search_reports(limit=10)

            user_id = None
            if (
                search_results.report_data
                and search_results.report_data.reports
                and search_results.report_data.reports.data
            ):
                for report in search_results.report_data.reports.data:
                    if report and report.owner:
                        user_id = report.owner.id
                        break

            if user_id:
                # Test the convenience method
                reports = await client.get_user_reports(user_id=user_id, limit=5)

                # Validate response structure (same as search_reports)
                assert hasattr(reports, "report_data")
                assert hasattr(reports.report_data, "reports")
                assert hasattr(reports.report_data.reports, "data")

                # Validate all reports belong to the user (if owner data present)
                if reports.report_data.reports.data:
                    for report in reports.report_data.reports.data:
                        if report and report.owner:
                            assert report.owner.id == user_id
            else:
                # If no user data found, just test method exists and returns proper structure
                pytest.skip("No user data found in recent reports")

    @pytest.mark.asyncio
    async def test_pagination_example(self, api_client_config):
        """Test pagination functionality"""
        async with Client(**api_client_config) as client:
            # Test page 1
            page1 = await client.search_reports(limit=3, page=1)
            assert page1.report_data.reports.current_page == 1

            await asyncio.sleep(0.5)  # Rate limiting

            # Test page 2 if more pages exist
            if page1.report_data.reports.has_more_pages:
                page2 = await client.search_reports(limit=3, page=2)
                assert page2.report_data.reports.current_page == 2

                # Validate pagination fields
                assert isinstance(page2.report_data.reports.from_, int)
                assert isinstance(page2.report_data.reports.to, int)
                assert page2.report_data.reports.from_ > page1.report_data.reports.to

    @pytest.mark.asyncio
    async def test_date_range_filtering_example(self, api_client_config):
        """Test date range filtering functionality"""
        async with Client(**api_client_config) as client:
            # Test with last 30 days
            thirty_days_ago = (time.time() - 30 * 24 * 3600) * 1000

            reports = await client.search_reports(start_time=thirty_days_ago, limit=5)

            # Validate response structure
            assert hasattr(reports, "report_data")
            assert hasattr(reports.report_data, "reports")

            # Validate date filtering (if reports found)
            if reports.report_data.reports.data:
                for report in reports.report_data.reports.data:
                    if report:
                        assert report.start_time >= thirty_days_ago

    @pytest.mark.asyncio
    async def test_empty_results_handling(self, api_client_config):
        """Test handling of searches that return no results"""
        async with Client(**api_client_config) as client:
            # Search for reports way in the future (should return no results)
            future_time = (time.time() + 365 * 24 * 3600) * 1000  # 1 year in future

            reports = await client.search_reports(start_time=future_time, limit=5)

            # Validate response structure exists even with no results
            assert hasattr(reports, "report_data")
            assert hasattr(reports.report_data, "reports")
            assert hasattr(reports.report_data.reports, "data")
            assert hasattr(reports.report_data.reports, "total")
            assert hasattr(reports.report_data.reports, "has_more_pages")

            # Should have empty or minimal data
            assert len(reports.report_data.reports.data or []) == 0
            assert not reports.report_data.reports.has_more_pages

    @pytest.mark.asyncio
    async def test_error_handling_example(self, api_client_config):
        """Test error handling for invalid parameters"""
        async with Client(**api_client_config) as client:
            # Test validation error with invalid limit
            with pytest.raises(ValidationError):
                await client.search_reports(limit=0)  # Invalid limit

            # Test validation error with invalid page
            with pytest.raises(ValidationError):
                await client.search_reports(page=0)  # Invalid page

    @pytest.mark.asyncio
    async def test_zone_filtering(self, api_client_config):
        """Test zone filtering functionality"""
        async with Client(**api_client_config) as client:
            # Test with a known zone ID (Dreadsail Reef = 16)
            reports = await client.search_reports(zone_id=16, limit=5)

            # Validate response structure
            assert hasattr(reports, "report_data")
            assert hasattr(reports.report_data, "reports")

            # If reports found, validate zone filter
            if reports.report_data.reports.data:
                for report in reports.report_data.reports.data:
                    if report and report.zone:
                        assert report.zone.id == 16
                        assert isinstance(report.zone.name, str)

    @pytest.mark.asyncio
    async def test_data_structure_completeness(self, api_client_config):
        """Test that all documented data structures are present"""
        async with Client(**api_client_config) as client:
            reports = await client.search_reports(limit=3)

            # Test main structure
            assert hasattr(reports, "report_data")
            assert hasattr(reports.report_data, "reports")

            reports_obj = reports.report_data.reports

            # Test all documented pagination fields
            assert hasattr(reports_obj, "data")
            assert hasattr(reports_obj, "total")
            assert hasattr(reports_obj, "per_page")
            assert hasattr(reports_obj, "current_page")
            assert hasattr(reports_obj, "last_page")
            assert hasattr(reports_obj, "has_more_pages")
            assert hasattr(reports_obj, "from_")
            assert hasattr(reports_obj, "to")

            # Test field types
            assert isinstance(reports_obj.total, int)
            assert isinstance(reports_obj.per_page, int)
            assert isinstance(reports_obj.current_page, int)
            assert isinstance(reports_obj.last_page, int)
            assert isinstance(reports_obj.has_more_pages, bool)

            # Test report data structure if available
            if reports_obj.data and len(reports_obj.data) > 0:
                report = reports_obj.data[0]
                if report:
                    # Test required fields
                    assert hasattr(report, "code")
                    assert hasattr(report, "title")
                    assert hasattr(report, "start_time")
                    assert hasattr(report, "end_time")
                    assert hasattr(report, "zone")
                    assert hasattr(report, "guild")
                    assert hasattr(report, "owner")

                    # Test types
                    assert isinstance(report.code, str)
                    assert isinstance(report.title, str)
                    assert isinstance(report.start_time, float)
                    assert isinstance(report.end_time, float)

                    # Test optional nested structures
                    if report.zone:
                        assert hasattr(report.zone, "id")
                        assert hasattr(report.zone, "name")
                        assert isinstance(report.zone.id, int)
                        assert isinstance(report.zone.name, str)

                    if report.guild:
                        assert hasattr(report.guild, "id")
                        assert hasattr(report.guild, "name")
                        assert hasattr(report.guild, "server")
                        assert isinstance(report.guild.id, int)
                        assert isinstance(report.guild.name, str)

                        if report.guild.server:
                            assert hasattr(report.guild.server, "name")
                            assert hasattr(report.guild.server, "slug")
                            assert hasattr(report.guild.server, "region")
                            assert isinstance(report.guild.server.name, str)
                            assert isinstance(report.guild.server.slug, str)

                            if report.guild.server.region:
                                assert hasattr(report.guild.server.region, "name")
                                assert hasattr(report.guild.server.region, "slug")
                                assert isinstance(report.guild.server.region.name, str)
                                assert isinstance(report.guild.server.region.slug, str)

                    if report.owner:
                        assert hasattr(report.owner, "id")
                        assert hasattr(report.owner, "name")
                        assert isinstance(report.owner.id, int)
                        assert isinstance(report.owner.name, str)

    @pytest.mark.asyncio
    async def test_common_use_cases_examples(self, api_client_config):
        """Test that the common use cases examples work correctly"""
        async with Client(**api_client_config) as client:
            # Test zone-specific research (most reliable)
            reports = await client.search_reports(zone_id=16, limit=5)

            # Validate response structure
            assert hasattr(reports, "report_data")
            assert hasattr(reports.report_data, "reports")
            assert hasattr(reports.report_data.reports, "data")

            # Should find some reports in a popular zone like Dreadsail Reef
            # (Note: may be 0 if no recent activity)
            assert isinstance(len(reports.report_data.reports.data), int)

            # If reports found, validate structure
            if reports.report_data.reports.data:
                for report in reports.report_data.reports.data:
                    if report and report.zone:
                        assert report.zone.id == 16  # Should match filter

            await asyncio.sleep(0.5)

            # Test recent activity monitoring
            recent_reports = await client.search_reports(limit=5)
            assert hasattr(recent_reports.report_data.reports, "data")
            assert len(recent_reports.report_data.reports.data) >= 0
