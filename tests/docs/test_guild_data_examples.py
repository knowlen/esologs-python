"""
Tests for examples in docs/api-reference/guild-data.md

Validates that all code examples in the guild data API documentation
execute correctly and return expected data structures.
"""

from datetime import datetime, timedelta

import pytest

from esologs._generated.exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
)
from esologs._generated.get_guild_attendance import GetGuildAttendance
from esologs._generated.get_guild_by_id import GetGuildById
from esologs._generated.get_guild_by_name import GetGuildByName
from esologs._generated.get_guild_members import GetGuildMembers
from esologs._generated.get_guilds import GetGuilds
from esologs.client import Client
from esologs.validators import ValidationError


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

    @pytest.mark.asyncio
    async def test_get_guild_reports_example(self, api_client_config):
        """Test the get_guild_reports() basic example"""
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
            guild_reports = await client.get_guild_reports(guild_id=guild_id, limit=5)

            # Validate response structure
            assert hasattr(guild_reports, "report_data")
            assert hasattr(guild_reports.report_data, "reports")
            assert hasattr(guild_reports.report_data.reports, "data")

            # Validate reports structure
            reports_obj = guild_reports.report_data.reports
            assert hasattr(reports_obj, "total")
            assert hasattr(reports_obj, "per_page")
            assert hasattr(reports_obj, "current_page")
            assert hasattr(reports_obj, "has_more_pages")

            # Validate report data if any exists
            if len(reports_obj.data) > 0:
                report = reports_obj.data[0]
                assert hasattr(report, "code")
                assert hasattr(report, "title")
                assert isinstance(report.code, str)
                assert isinstance(report.title, str)

                # Validate guild info in report
                if hasattr(report, "guild") and report.guild:
                    assert hasattr(report.guild, "name")
                    assert isinstance(report.guild.name, str)

    @pytest.mark.asyncio
    async def test_get_guild_reports_error_handling_example(self, api_client_config):
        """Test error handling for get_guild_reports() with validation"""
        async with Client(**api_client_config) as client:
            # Test with invalid parameters
            with pytest.raises(
                (
                    ValidationError,
                    GraphQLClientHttpError,
                    GraphQLClientGraphQLMultiError,
                )
            ):
                await client.get_guild_reports(
                    guild_id=-1, limit=100
                )  # Invalid guild_id and limit too high

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
            end_time = datetime.now().timestamp() * 1000
            start_time = (datetime.now() - timedelta(days=30)).timestamp() * 1000

            time_filtered_reports = await client.get_guild_reports(
                guild_id=guild_id, start_time=start_time, end_time=end_time, limit=10
            )

            # Validate response
            assert hasattr(time_filtered_reports, "report_data")
            assert hasattr(time_filtered_reports.report_data, "reports")

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

            # Test getting guild reports (simplified version of the pattern)
            guild_reports = await client.get_guild_reports(guild_id=guild_id, limit=3)

            # Validate we can get reports
            assert hasattr(guild_reports, "report_data")
            assert hasattr(guild_reports.report_data, "reports")

            # Test that we can iterate through reports
            for report in guild_reports.report_data.reports.data:
                assert hasattr(report, "title")
                assert hasattr(report, "code")
                assert isinstance(report.code, str)

                # Note: We don't test actual report detail fetching to avoid rate limiting
                # await asyncio.sleep(0.1)  # Would be needed for real implementation

    @pytest.mark.asyncio
    async def test_get_guild_flexible_example(self, api_client_config):
        """Test the get_guild() flexible lookup example"""
        async with Client(**api_client_config) as client:
            # Test lookup by ID
            guild1 = await client.get_guild(guild_id=3468)
            assert isinstance(guild1, GetGuildById)
            if guild1.guild_data.guild:
                assert guild1.guild_data.guild.name == "The Shadow Court"

            # Test lookup by name and server
            guild2 = await client.get_guild(
                guild_name="The Shadow Court",
                guild_server_slug="megaserver",
                guild_server_region="NA",
            )
            assert isinstance(guild2, GetGuildByName)
            if guild2.guild_data.guild:
                assert guild2.guild_data.guild.name == "The Shadow Court"

    @pytest.mark.asyncio
    async def test_get_guilds_example(self, api_client_config):
        """Test the get_guilds() list example"""
        async with Client(**api_client_config) as client:
            # Get all guilds
            all_guilds = await client.get_guilds(limit=20, page=1)
            assert isinstance(all_guilds, GetGuilds)
            assert hasattr(all_guilds.guild_data.guilds, "total")
            assert all_guilds.guild_data.guilds.total > 0

            # Filter by server
            na_guilds = await client.get_guilds(
                server_slug="megaserver", server_region="NA", limit=10
            )
            assert isinstance(na_guilds, GetGuilds)
            assert hasattr(na_guilds.guild_data.guilds, "data")

            # Check that we got guilds
            if na_guilds.guild_data.guilds.data:
                for guild in na_guilds.guild_data.guilds.data:
                    assert hasattr(guild, "name")
                    assert hasattr(guild, "faction")
                    assert hasattr(guild.faction, "name")

    @pytest.mark.asyncio
    async def test_get_guild_attendance_example(self, api_client_config):
        """Test the get_guild_attendance() example"""
        async with Client(**api_client_config) as client:
            # Get attendance for a guild
            attendance = await client.get_guild_attendance(
                guild_id=3468, zone_id=38, limit=10  # Dreadsail Reef
            )
            assert isinstance(attendance, GetGuildAttendance)

            guild = attendance.guild_data.guild
            if guild and guild.attendance and guild.attendance.data:
                for raid in guild.attendance.data[:2]:  # Check first 2 raids
                    assert hasattr(raid, "code")
                    assert hasattr(raid, "start_time")
                    assert hasattr(raid, "players")
                    assert isinstance(raid.code, str)
                    assert isinstance(raid.start_time, float)

                    # Check player data
                    if raid.players:
                        for player in raid.players[:3]:
                            assert hasattr(player, "name")
                            assert hasattr(player, "presence")
                            assert isinstance(player.name, str)
                            assert 0.0 <= player.presence <= 1.0

    @pytest.mark.asyncio
    async def test_get_guild_members_example(self, api_client_config):
        """Test the get_guild_members() example"""
        async with Client(**api_client_config) as client:
            members = await client.get_guild_members(guild_id=3468, limit=50, page=1)
            assert isinstance(members, GetGuildMembers)

            guild = members.guild_data.guild
            if guild and guild.members:
                assert hasattr(guild.members, "total")
                # Guild might have 0 members, which is valid
                assert isinstance(guild.members.total, int)
                assert guild.members.total >= 0

                if guild.members.data and guild.members.total > 0:
                    for member in guild.members.data[:5]:  # Check first 5 members
                        assert hasattr(member, "name")
                        assert hasattr(member, "guild_rank")
                        assert hasattr(member, "server")
                        assert hasattr(member.server, "name")
                        assert isinstance(member.name, str)
                        assert isinstance(member.guild_rank, int)

    @pytest.mark.asyncio
    async def test_handle_missing_guild_example(self, api_client_config):
        """Test the error handling example for non-existent guilds"""
        async with Client(**api_client_config) as client:
            guild = await client.get_guild_by_id(guild_id=999999)  # Non-existent guild

            # Check if guild exists
            assert (
                guild.guild_data.guild is None
            )  # Should be None for non-existent guild

    @pytest.mark.asyncio
    async def test_get_guild_validation_errors(self, api_client_config):
        """Test validation errors for get_guild method"""
        async with Client(**api_client_config) as client:
            # Test missing all parameters
            with pytest.raises(ValidationError) as exc_info:
                await client.get_guild()
            assert "Must provide either guild_id OR guild_name" in str(exc_info.value)

            # Test incomplete name parameters
            with pytest.raises(ValidationError) as exc_info:
                await client.get_guild(guild_name="Test")
            assert "guild_server_slug, and guild_server_region together" in str(
                exc_info.value
            )

            # Test both ID and name parameters
            with pytest.raises(ValidationError) as exc_info:
                await client.get_guild(
                    guild_id=123,
                    guild_name="Test",
                    guild_server_slug="megaserver",
                    guild_server_region="NA",
                )
            assert "Cannot provide both guild_id and guild_name" in str(exc_info.value)
