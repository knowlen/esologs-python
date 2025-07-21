"""
Unit tests for guild-related API methods.

Tests the guild search, lookup, attendance, and member methods.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from esologs._generated.get_guild_attendance import GetGuildAttendance
from esologs._generated.get_guild_by_id import GetGuildById
from esologs._generated.get_guild_by_name import GetGuildByName
from esologs._generated.get_guild_members import GetGuildMembers
from esologs._generated.get_guilds import GetGuilds
from esologs.client import Client
from esologs.validators import ValidationError


class TestGuildMethods:
    """Test guild API method implementations."""

    def test_guild_methods_exist(self):
        """Test that all guild methods are registered on the client."""
        client = Client(url="http://test.com", headers={})

        # Check that all guild methods exist
        assert hasattr(client, "get_guild_by_id")
        assert hasattr(client, "get_guilds")
        assert hasattr(client, "get_guild")
        assert hasattr(client, "get_guild_attendance")
        assert hasattr(client, "get_guild_members")

    @pytest.mark.asyncio
    async def test_get_guild_by_id(self):
        """Test get_guild_by_id method."""
        client = Client(url="http://test.com", headers={})

        # Mock the execute method
        mock_response = {
            "guildData": {
                "guild": {
                    "id": 123,
                    "name": "Test Guild",
                    "description": "A test guild",
                    "faction": {"name": "Aldmeri Dominion"},
                    "server": {
                        "name": "NA Megaserver",
                        "region": {"name": "North America"},
                    },
                    "tags": [],
                }
            }
        }

        with patch.object(client, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = mock_response

            result = await client.get_guild_by_id(guild_id=123)

            # Verify the method was called correctly
            mock_execute.assert_called_once()
            call_args = mock_execute.call_args
            assert "getGuildById" in call_args.kwargs["operation_name"]
            assert call_args.kwargs["variables"]["guildId"] == 123

            # Verify result type
            assert isinstance(result, GetGuildById)

    @pytest.mark.asyncio
    async def test_get_guilds_pagination(self):
        """Test get_guilds method with pagination."""
        client = Client(url="http://test.com", headers={})

        mock_response = {
            "guildData": {
                "guilds": {
                    "total": 100,
                    "per_page": 10,
                    "current_page": 1,
                    "from": 1,
                    "to": 10,
                    "last_page": 10,
                    "has_more_pages": True,
                    "data": [
                        {
                            "id": 1,
                            "name": "Guild 1",
                            "faction": {"name": "Ebonheart Pact"},
                            "server": {
                                "name": "EU Megaserver",
                                "region": {"name": "Europe"},
                            },
                        }
                    ],
                }
            }
        }

        with patch.object(client, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = mock_response

            result = await client.get_guilds(limit=10, page=1)

            # Verify the method was called correctly
            mock_execute.assert_called_once()
            call_args = mock_execute.call_args
            assert "getGuilds" in call_args.kwargs["operation_name"]
            assert call_args.kwargs["variables"]["limit"] == 10
            assert call_args.kwargs["variables"]["page"] == 1

            # Verify result type
            assert isinstance(result, GetGuilds)

    @pytest.mark.asyncio
    async def test_get_guilds_with_server_filter(self):
        """Test get_guilds method with server filters."""
        client = Client(url="http://test.com", headers={})

        mock_response = {
            "guildData": {
                "guilds": {
                    "total": 10,
                    "per_page": 100,
                    "current_page": 1,
                    "from": 1,
                    "to": 10,
                    "last_page": 1,
                    "has_more_pages": False,
                    "data": [],
                }
            }
        }

        with patch.object(client, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = mock_response

            await client.get_guilds(
                server_id=1, server_slug="na", server_region="north-america"
            )

            # Verify the method was called with server filters
            call_args = mock_execute.call_args
            variables = call_args.kwargs["variables"]
            assert variables["serverID"] == 1
            assert variables["serverSlug"] == "na"
            assert variables["serverRegion"] == "north-america"

    @pytest.mark.asyncio
    async def test_get_guild_by_id_path(self):
        """Test get_guild method using ID lookup path."""
        client = Client(url="http://test.com", headers={})

        with patch.object(
            client, "get_guild_by_id", new_callable=AsyncMock
        ) as mock_method:
            mock_method.return_value = Mock(spec=GetGuildById)

            await client.get_guild(guild_id=456)

            # Verify it called get_guild_by_id
            mock_method.assert_called_once_with(guild_id=456)

    @pytest.mark.asyncio
    async def test_get_guild_by_name_path(self):
        """Test get_guild method using name/server lookup path."""
        client = Client(url="http://test.com", headers={})

        mock_response = {
            "guildData": {
                "guild": {
                    "id": 789,
                    "name": "Named Guild",
                    "description": "Found by name",
                    "faction": {"name": "Aldmeri Dominion"},
                    "server": {"name": "EU Megaserver", "region": {"name": "Europe"}},
                    "tags": [],
                }
            }
        }

        with patch.object(client, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = mock_response

            result = await client.get_guild(
                guild_name="Named Guild",
                guild_server_slug="eu",
                guild_server_region="europe",
            )

            # Verify it used the name-based query
            mock_execute.assert_called_once()
            call_args = mock_execute.call_args
            assert "getGuildByName" in call_args.kwargs["operation_name"]
            assert call_args.kwargs["variables"]["name"] == "Named Guild"
            assert call_args.kwargs["variables"]["serverSlug"] == "eu"
            assert call_args.kwargs["variables"]["serverRegion"] == "europe"

            # Verify result type
            assert isinstance(result, GetGuildByName)

    @pytest.mark.asyncio
    async def test_get_guild_validation_error(self):
        """Test get_guild method validation errors."""
        client = Client(url="http://test.com", headers={})

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
                guild_server_slug="na",
                guild_server_region="north-america",
            )
        assert "Cannot provide both guild_id and guild_name" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_guild_attendance(self):
        """Test get_guild_attendance method."""
        client = Client(url="http://test.com", headers={})

        mock_response = {
            "guildData": {
                "guild": {
                    "attendance": {
                        "total": 50,
                        "per_page": 16,
                        "current_page": 1,
                        "has_more_pages": True,
                        "data": [
                            {
                                "code": "abc123",
                                "startTime": 1234567890.0,
                                "players": [
                                    {
                                        "name": "Player1",
                                        "type": "Member",
                                        "presence": 1.0,
                                    }
                                ],
                            }
                        ],
                    }
                }
            }
        }

        with patch.object(client, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = mock_response

            result = await client.get_guild_attendance(
                guild_id=123, zone_id=456, limit=10, page=2
            )

            # Verify the method was called correctly
            mock_execute.assert_called_once()
            call_args = mock_execute.call_args
            assert "getGuildAttendance" in call_args.kwargs["operation_name"]

            variables = call_args.kwargs["variables"]
            assert variables["guildId"] == 123
            assert variables["zoneID"] == 456
            assert variables["limit"] == 10
            assert variables["page"] == 2

            # Verify result type
            assert isinstance(result, GetGuildAttendance)

    @pytest.mark.asyncio
    async def test_get_guild_attendance_defaults(self):
        """Test get_guild_attendance method with default pagination."""
        client = Client(url="http://test.com", headers={})

        mock_response = {
            "guildData": {
                "guild": {
                    "attendance": {
                        "total": 10,
                        "per_page": 16,
                        "current_page": 1,
                        "has_more_pages": False,
                        "data": [],
                    }
                }
            }
        }

        with patch.object(client, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = mock_response

            # Call without limit/page to test defaults
            await client.get_guild_attendance(guild_id=999)

            # Verify defaults were applied
            call_args = mock_execute.call_args
            variables = call_args.kwargs["variables"]
            assert variables["limit"] == 16  # Default from param builder
            assert variables["page"] == 1  # Default from param builder

    @pytest.mark.asyncio
    async def test_get_guild_members(self):
        """Test get_guild_members method."""
        client = Client(url="http://test.com", headers={})

        mock_response = {
            "guildData": {
                "guild": {
                    "members": {
                        "total": 200,
                        "per_page": 100,
                        "current_page": 1,
                        "has_more_pages": True,
                        "data": [
                            {
                                "id": 1001,
                                "name": "Member1",
                                "server": {
                                    "name": "NA Megaserver",
                                    "region": {"name": "North America"},
                                },
                                "guildRank": 5,
                            }
                        ],
                    }
                }
            }
        }

        with patch.object(client, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = mock_response

            result = await client.get_guild_members(guild_id=789, limit=50, page=2)

            # Verify the method was called correctly
            mock_execute.assert_called_once()
            call_args = mock_execute.call_args
            assert "getGuildMembers" in call_args.kwargs["operation_name"]

            variables = call_args.kwargs["variables"]
            assert variables["guildId"] == 789
            assert variables["limit"] == 50
            assert variables["page"] == 2

            # Verify result type
            assert isinstance(result, GetGuildMembers)

    def test_parameter_builder_import(self):
        """Test that the guild attendance parameter builder is available."""
        from esologs.param_builders import build_guild_attendance_params

        # Test the builder
        params = build_guild_attendance_params(
            guild_id=123, guild_tag_id=456, zone_id=789, limit=20, page=3
        )

        # Verify parameter mapping
        assert params["guildId"] == 123
        assert params["guildTagID"] == 456
        assert params["zoneID"] == 789
        assert params["limit"] == 20
        assert params["page"] == 3

    def test_parameter_builder_defaults(self):
        """Test guild attendance parameter builder defaults."""
        from esologs.param_builders import build_guild_attendance_params

        # Test with minimal parameters
        params = build_guild_attendance_params(guild_id=999)

        # Verify defaults are applied
        assert params["guildId"] == 999
        assert params["limit"] == 16  # Default
        assert params["page"] == 1  # Default
        assert "guildTagID" not in params  # Optional, not provided
        assert "zoneID" not in params  # Optional, not provided
