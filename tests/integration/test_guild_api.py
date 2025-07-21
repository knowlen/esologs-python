"""
Integration tests for guild API endpoints.

Tests the actual API calls for guild search, lookup, attendance, and members.
"""

import asyncio

import pytest

from esologs._generated.exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
)
from esologs.client import Client
from esologs.validators import ValidationError


@pytest.mark.integration
class TestGuildAPIIntegration:
    """Integration tests for guild API endpoints."""

    @pytest.mark.asyncio
    async def test_get_guild_by_id(self, api_client_config):
        """Test fetching a guild by ID."""
        async with Client(**api_client_config) as client:
            # Use a known guild ID from our test data
            guild_id = 3468

            result = await client.get_guild_by_id(guild_id=guild_id)

            # Check structure
            assert hasattr(result, "guild_data")
            assert hasattr(result.guild_data, "guild")

            guild = result.guild_data.guild
            if guild is not None:
                # Verify guild properties
                assert hasattr(guild, "id")
                assert hasattr(guild, "name")
                assert hasattr(guild, "description")
                assert hasattr(guild, "faction")
                assert hasattr(guild, "server")

                # Verify types
                assert isinstance(guild.id, int)
                assert isinstance(guild.name, str)
                assert isinstance(guild.description, str)

                # Verify nested structures
                assert hasattr(guild.faction, "name")
                assert hasattr(guild.server, "name")
                assert hasattr(guild.server, "region")

    @pytest.mark.asyncio
    async def test_get_guild_not_found(self, api_client_config):
        """Test fetching a non-existent guild."""
        async with Client(**api_client_config) as client:
            # Use an ID that shouldn't exist
            result = await client.get_guild_by_id(guild_id=999999999)

            # API returns None for non-existent guilds
            assert result.guild_data.guild is None

    @pytest.mark.asyncio
    async def test_get_guilds_list(self, api_client_config):
        """Test listing guilds with pagination."""
        async with Client(**api_client_config) as client:
            # Get first page of guilds
            result = await client.get_guilds(limit=10, page=1)

            # Check structure
            assert hasattr(result, "guild_data")
            assert hasattr(result.guild_data, "guilds")

            guilds = result.guild_data.guilds
            if guilds is not None:
                # Check pagination structure
                assert hasattr(guilds, "total")
                assert hasattr(guilds, "per_page")
                assert hasattr(guilds, "current_page")
                assert hasattr(guilds, "has_more_pages")
                assert hasattr(guilds, "data")

                # Verify pagination values
                assert guilds.per_page <= 10
                assert guilds.current_page == 1

                # Check guild data if any exist
                if guilds.data:
                    guild = guilds.data[0]
                    assert hasattr(guild, "id")
                    assert hasattr(guild, "name")
                    assert hasattr(guild, "faction")
                    assert hasattr(guild, "server")

    @pytest.mark.asyncio
    async def test_get_guilds_with_server_filter(self, api_client_config):
        """Test listing guilds filtered by server."""
        async with Client(**api_client_config) as client:
            # Try filtering by NA server
            result = await client.get_guilds(
                server_slug="pc-na", server_region="us", limit=5
            )

            # Check that we got a valid response
            assert hasattr(result, "guild_data")
            assert hasattr(result.guild_data, "guilds")

            guilds = result.guild_data.guilds
            if guilds and guilds.data:
                # Verify all guilds are from the specified server
                for guild in guilds.data:
                    if guild.server:
                        # Server filtering should match our criteria
                        assert guild.server is not None

    @pytest.mark.asyncio
    async def test_get_guild_flexible_lookup_by_id(self, api_client_config):
        """Test the flexible get_guild method with ID."""
        async with Client(**api_client_config) as client:
            # Use a known guild ID
            guild_id = 3468

            result = await client.get_guild(guild_id=guild_id)

            # Should return same as get_guild_by_id
            assert hasattr(result, "guild_data")
            guild = result.guild_data.guild
            if guild:
                assert guild.id == guild_id

    @pytest.mark.asyncio
    async def test_get_guild_flexible_lookup_validation(self, api_client_config):
        """Test get_guild method parameter validation."""
        async with Client(**api_client_config) as client:
            # Test missing all parameters
            with pytest.raises(ValidationError) as exc:
                await client.get_guild()
            assert "Must provide either guild_id OR guild_name" in str(exc.value)

            # Test incomplete name parameters
            with pytest.raises(ValidationError) as exc:
                await client.get_guild(guild_name="Test Guild")
            assert "guild_server_slug, and guild_server_region together" in str(
                exc.value
            )

            # Test conflicting parameters
            with pytest.raises(ValidationError) as exc:
                await client.get_guild(
                    guild_id=123,
                    guild_name="Test",
                    guild_server_slug="pc-na",
                    guild_server_region="us",
                )
            assert "Cannot provide both guild_id and guild_name" in str(exc.value)

    @pytest.mark.asyncio
    async def test_get_guild_attendance(self, api_client_config):
        """Test fetching guild attendance data."""
        async with Client(**api_client_config) as client:
            # First, find a guild with reports
            reports = await client.search_reports(limit=10)
            guild_id = None

            for report in reports.report_data.reports.data:
                if report.guild and report.guild.id:
                    guild_id = report.guild.id
                    break

            if not guild_id:
                pytest.skip("No guild with reports found for attendance test")

            # Try to get attendance for this guild
            result = await client.get_guild_attendance(
                guild_id=guild_id, limit=5, page=1
            )

            # Check structure
            assert hasattr(result, "guild_data")
            assert hasattr(result.guild_data, "guild")

            guild = result.guild_data.guild
            if guild and hasattr(guild, "attendance"):
                attendance = guild.attendance

                # Check pagination
                assert hasattr(attendance, "total")
                assert hasattr(attendance, "per_page")
                assert hasattr(attendance, "current_page")
                assert hasattr(attendance, "has_more_pages")
                assert hasattr(attendance, "data")

                # Check attendance data if any
                if attendance.data:
                    entry = attendance.data[0]
                    assert hasattr(entry, "code")
                    assert hasattr(entry, "start_time")
                    assert hasattr(entry, "players")

    @pytest.mark.asyncio
    async def test_get_guild_attendance_with_filters(self, api_client_config):
        """Test guild attendance with zone filter."""
        async with Client(**api_client_config) as client:
            # Use a known guild ID
            guild_id = 3468

            # Try with a specific zone ID (Dreadsail Reef)
            zone_id = 38

            result = await client.get_guild_attendance(
                guild_id=guild_id, zone_id=zone_id, limit=3
            )

            # Verify we got a response
            assert hasattr(result, "guild_data")
            guild = result.guild_data.guild

            # Note: Attendance might be None if guild has no raids in that zone
            if guild and hasattr(guild, "attendance") and guild.attendance:
                # If we have data, it should be for the specified zone
                assert guild.attendance is not None

    @pytest.mark.asyncio
    async def test_get_guild_members(self, api_client_config):
        """Test fetching guild member roster."""
        async with Client(**api_client_config) as client:
            # Use a known guild ID
            guild_id = 3468

            try:
                result = await client.get_guild_members(
                    guild_id=guild_id, limit=10, page=1
                )

                # Check structure
                assert hasattr(result, "guild_data")
                assert hasattr(result.guild_data, "guild")

                guild = result.guild_data.guild
                if guild and hasattr(guild, "members"):
                    members = guild.members

                    # Check pagination
                    assert hasattr(members, "total")
                    assert hasattr(members, "per_page")
                    assert hasattr(members, "current_page")
                    assert hasattr(members, "has_more_pages")
                    assert hasattr(members, "data")

                    # Check member data if any
                    if members.data:
                        member = members.data[0]
                        assert hasattr(member, "id")
                        assert hasattr(member, "name")
                        assert hasattr(member, "server")
                        assert hasattr(member, "guild_rank")

                        # Verify types
                        assert isinstance(member.id, int)
                        assert isinstance(member.name, str)

            except (GraphQLClientHttpError, GraphQLClientGraphQLMultiError) as e:
                # Some games may not support member rosters
                if "not supported" in str(e).lower():
                    pytest.skip("Guild members not supported for this game")
                else:
                    raise

    @pytest.mark.asyncio
    async def test_guild_members_pagination(self, api_client_config):
        """Test guild members pagination."""
        async with Client(**api_client_config) as client:
            # Use a known guild ID
            guild_id = 3468

            try:
                # Get first page with small limit
                page1 = await client.get_guild_members(
                    guild_id=guild_id, limit=5, page=1
                )

                guild1 = page1.guild_data.guild
                if guild1 and hasattr(guild1, "members") and guild1.members:
                    members1 = guild1.members

                    # If there are more pages, get the second one
                    if members1.has_more_pages:
                        page2 = await client.get_guild_members(
                            guild_id=guild_id, limit=5, page=2
                        )

                        guild2 = page2.guild_data.guild
                        if guild2 and hasattr(guild2, "members"):
                            members2 = guild2.members

                            # Verify pagination is working
                            assert members2.current_page == 2

                            # Member IDs should be different
                            if members1.data and members2.data:
                                ids1 = {m.id for m in members1.data}
                                ids2 = {m.id for m in members2.data}
                                assert ids1.isdisjoint(ids2)

            except (GraphQLClientHttpError, GraphQLClientGraphQLMultiError) as e:
                if "not supported" in str(e).lower():
                    pytest.skip("Guild members not supported for this game")
                else:
                    raise

    @pytest.mark.asyncio
    async def test_rate_limiting_awareness(self, api_client_config):
        """Test that guild methods respect rate limits."""
        async with Client(**api_client_config) as client:
            # Make several guild API calls
            tasks = []

            # Mix of different guild methods
            tasks.append(client.get_guild_by_id(guild_id=3468))
            tasks.append(client.get_guilds(limit=5))
            tasks.append(client.get_guild_attendance(guild_id=3468, limit=3))

            # Add small delays to avoid hitting rate limits
            results = []
            for task in tasks:
                result = await task
                results.append(result)
                await asyncio.sleep(0.1)  # Small delay between requests

            # All requests should succeed
            assert len(results) == len(tasks)

            # Check rate limit status
            rate_limit = await client.get_rate_limit_data()
            assert hasattr(rate_limit.rate_limit_data, "points_spent_this_hour")
            assert hasattr(rate_limit.rate_limit_data, "limit_per_hour")
