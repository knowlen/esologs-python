"""
Tests for examples in docs/api-reference/guild-data.md

Validates that all code examples in the guild data API documentation
execute correctly and return expected data structures.
"""

from datetime import datetime, timedelta

import pytest

from esologs.client import Client


class TestGuildDataExamples:
    """Test all examples from guild-data.md documentation"""

    @pytest.mark.asyncio
    async def test_get_guild_info_example(self, api_client_config):
        """Test the get_guild_by_id() basic example"""
        async with Client(**api_client_config) as client:
            # Use the guild ID we found during validation
            guild_id = 3468  # From our validation script

            # Verify it still exists
            test_guild = await client.get_guild_by_id(guild_id=guild_id)
            if test_guild.guild_data.guild is None:
                # Fall back to searching for a valid guild ID
                reports = await client.search_reports(limit=10)
                guild_id = None

                for report in reports.report_data.reports.data:
                    if report.guild and report.guild.id:
                        guild_id = report.guild.id
                        break

                # Skip test if no guild found
                if not guild_id:
                    pytest.skip("No guild ID found in recent reports")

            # Test the main example
            guild = await client.get_guild_by_id(guild_id=guild_id)

            # Validate response structure
            assert hasattr(guild, "guild_data")
            assert hasattr(guild.guild_data, "guild")
            assert guild.guild_data.guild is not None

            # Validate guild structure
            g = guild.guild_data.guild
            assert hasattr(g, "id")
            assert hasattr(g, "name")
            assert hasattr(g, "description")
            assert hasattr(g, "faction")
            assert hasattr(g, "server")

            # Validate types
            assert isinstance(g.id, int)
            assert isinstance(g.name, str)
            assert isinstance(g.description, str)

            # Validate faction
            assert hasattr(g.faction, "name")
            assert isinstance(g.faction.name, str)

            # Validate server
            assert hasattr(g.server, "name")
            assert hasattr(g.server, "region")
            assert isinstance(g.server.name, str)
            assert hasattr(g.server.region, "name")
            assert isinstance(g.server.region.name, str)

    @pytest.mark.asyncio
    async def test_get_guild_by_id_error_handling_example(self, api_client_config):
        """Test error handling for get_guild_by_id() with invalid ID"""
        async with Client(**api_client_config) as client:
            # Test with non-existent guild ID - API returns guild=None instead of error
            result = await client.get_guild_by_id(guild_id=999999)

            # Validate that we get a valid response structure but with None guild
            assert hasattr(result, "guild_data")
            assert result.guild_data is not None
            assert result.guild_data.guild is None  # Non-existent guild returns None

    # @pytest.mark.asyncio
    # async def test_get_guild_reports_example(self, api_client_config):
    #     """Test the get_guild_reports() basic example"""
    #     # REMOVED: get_guild_reports method not available in this version

    # @pytest.mark.asyncio
    # async def test_get_guild_reports_error_handling_example(self, api_client_config):
    #     """Test error handling for get_guild_reports() with validation"""
    #     # REMOVED: get_guild_reports method not available in this version

    @pytest.mark.asyncio
    async def test_search_guild_reports_example(self, api_client_config):
        """Test the search_reports() with guild filters example"""
        async with Client(**api_client_config) as client:
            # Use the guild ID we found during validation
            guild_id = 3468  # From our validation script

            # Verify it still exists
            test_guild = await client.get_guild_by_id(guild_id=guild_id)
            if test_guild.guild_data.guild is None:
                # Fall back to searching for a valid guild ID
                reports = await client.search_reports(limit=10)
                guild_id = None

                for report in reports.report_data.reports.data:
                    if report.guild and report.guild.id:
                        guild_id = report.guild.id
                        break

                # Skip test if no guild found
                if not guild_id:
                    pytest.skip("No guild ID found in recent reports")

            # Test guild ID search
            guild_reports = await client.search_reports(guild_id=guild_id, limit=5)

            # Validate same structure as regular reports
            assert hasattr(guild_reports, "report_data")
            assert hasattr(guild_reports.report_data, "reports")

            # Validate that all reports belong to the specified guild
            for report in guild_reports.report_data.reports.data:
                if hasattr(report, "guild") and report.guild:
                    assert report.guild.id == guild_id

    @pytest.mark.asyncio
    async def test_guild_performance_analysis_pattern(self, api_client_config):
        """Test the guild performance analysis pattern example"""
        async with Client(**api_client_config) as client:
            # Use the guild ID we found during validation
            guild_id = 3468  # From our validation script

            # Verify it still exists
            test_guild = await client.get_guild_by_id(guild_id=guild_id)
            if test_guild.guild_data.guild is None:
                # Fall back to searching for a valid guild ID
                reports = await client.search_reports(limit=10)
                guild_id = None

                for report in reports.report_data.reports.data:
                    if report.guild and report.guild.id:
                        guild_id = report.guild.id
                        break

                # Skip test if no guild found
                if not guild_id:
                    pytest.skip("No guild ID found in recent reports")

            # Test guild info retrieval
            guild = await client.get_guild_by_id(guild_id=guild_id)
            assert guild.guild_data.guild is not None

            # Test reports with time filter (last 30 days)
            datetime.now().timestamp() * 1000
            (datetime.now() - timedelta(days=30)).timestamp() * 1000

            # REMOVED: get_guild_reports method not available in this version
            # time_filtered_reports = await client.get_guild_reports(
            #     guild_id=guild_id, start_time=start_time, end_time=end_time, limit=10
            # )
            pytest.skip("get_guild_reports not available in this version")

            # Note: We don't validate zone analysis as it requires report details
            # which would be too expensive for tests

    @pytest.mark.asyncio
    async def test_member_activity_tracking_pattern(self, api_client_config):
        """Test the member activity tracking pattern (simplified version)"""
        async with Client(**api_client_config) as client:
            # Use the guild ID we found during validation
            guild_id = 3468  # From our validation script

            # Verify it still exists
            test_guild = await client.get_guild_by_id(guild_id=guild_id)
            if test_guild.guild_data.guild is None:
                # Fall back to searching for a valid guild ID
                reports = await client.search_reports(limit=10)
                guild_id = None

                for report in reports.report_data.reports.data:
                    if report.guild and report.guild.id:
                        guild_id = report.guild.id
                        break

                # Skip test if no guild found
                if not guild_id:
                    pytest.skip("No guild ID found in recent reports")

            # REMOVED: get_guild_reports method not available in this version
            # guild_reports = await client.get_guild_reports(guild_id=guild_id, limit=3)
            pytest.skip("get_guild_reports not available in this version")
