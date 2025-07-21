"""
Tests for examples in docs/api-reference/game-data.md

Validates that all code examples in the game data API documentation
execute correctly and return expected data structures.
"""


import pytest

from esologs._generated.exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
)
from esologs.client import Client
from esologs.validators import ValidationError


class TestGameDataExamples:
    """Test all examples from game-data.md documentation"""

    @pytest.mark.asyncio
    async def test_get_all_abilities_example(self, api_client_config):
        """Test the get_abilities() basic example"""
        async with Client(**api_client_config) as client:
            # Get first page of abilities
            abilities = await client.get_abilities(limit=50)

            # Validate response structure
            assert hasattr(abilities, "game_data")
            assert hasattr(abilities.game_data, "abilities")
            assert len(abilities.game_data.abilities.data) > 0

            # Validate ability structure
            ability = abilities.game_data.abilities.data[0]
            assert hasattr(ability, "name")
            assert hasattr(ability, "id")
            assert isinstance(ability.id, int)
            assert isinstance(ability.name, str)

    @pytest.mark.asyncio
    async def test_get_abilities_error_handling_example(self, api_client_config):
        """Test error handling for get_abilities() with invalid parameters"""
        async with Client(**api_client_config) as client:
            # Test GraphQL error with limit too high (server-side validation)
            with pytest.raises(
                (
                    ValidationError,
                    GraphQLClientHttpError,
                    GraphQLClientGraphQLMultiError,
                )
            ):
                await client.get_abilities(limit=2000)  # Should exceed max limit

    @pytest.mark.asyncio
    async def test_get_ability_details_example(self, api_client_config):
        """Test the get_ability() example with specific ability ID"""
        async with Client(**api_client_config) as client:
            # First get a valid ability ID from the abilities list
            abilities = await client.get_abilities(limit=10)
            valid_ability_id = abilities.game_data.abilities.data[0].id

            # Get specific ability details
            ability = await client.get_ability(id=valid_ability_id)

            # Validate response structure
            assert hasattr(ability, "game_data")
            assert hasattr(ability.game_data, "ability")
            if ability.game_data.ability:  # Some abilities might be None
                assert hasattr(ability.game_data.ability, "name")
                assert ability.game_data.ability.id == valid_ability_id

    @pytest.mark.asyncio
    async def test_list_character_classes_example(self, api_client_config):
        """Test the get_classes() example"""
        async with Client(**api_client_config) as client:
            # Get all character classes
            classes = await client.get_classes()

            # Validate response structure
            assert hasattr(classes, "game_data")
            assert hasattr(classes.game_data, "classes")
            assert len(classes.game_data.classes) > 0

            # Validate class structure
            char_class = classes.game_data.classes[0]
            assert hasattr(char_class, "name")
            assert hasattr(char_class, "id")
            assert isinstance(char_class.id, int)
            assert isinstance(char_class.name, str)

    @pytest.mark.asyncio
    async def test_get_class_details_example(self, api_client_config):
        """Test the get_class() example with Sorcerer"""
        async with Client(**api_client_config) as client:
            # Get Sorcerer class details
            sorcerer = await client.get_class(id=1)

            # Validate response structure
            assert hasattr(sorcerer, "game_data")
            assert hasattr(sorcerer.game_data, "class_")
            assert hasattr(sorcerer.game_data.class_, "name")
            assert sorcerer.game_data.class_.id == 1

    @pytest.mark.asyncio
    async def test_browse_items_example(self, api_client_config):
        """Test the get_items() example"""
        async with Client(**api_client_config) as client:
            # Get first page of items
            items = await client.get_items(limit=25)

            # Validate response structure
            assert hasattr(items, "game_data")
            assert hasattr(items.game_data, "items")
            assert len(items.game_data.items.data) > 0

            # Validate item structure
            item = items.game_data.items.data[0]
            assert hasattr(item, "name")
            assert hasattr(item, "id")
            assert isinstance(item.id, int)
            # Note: item.name can be None for some items
            assert item.name is None or isinstance(item.name, str)

    @pytest.mark.asyncio
    async def test_get_item_details_example(self, api_client_config):
        """Test the get_item() example with specific item ID"""
        async with Client(**api_client_config) as client:
            # Get specific item details
            item = await client.get_item(id=71063)  # Kjalnar's Nightmare set piece

            # Validate response structure
            assert hasattr(item, "game_data")
            assert hasattr(item.game_data, "item")
            assert hasattr(item.game_data.item, "name")
            assert item.game_data.item.id == 71063

    @pytest.mark.asyncio
    async def test_list_npcs_example(self, api_client_config):
        """Test the get_npcs() example"""
        async with Client(**api_client_config) as client:
            # Get NPCs
            npcs = await client.get_npcs(limit=20)

            # Validate response structure
            assert hasattr(npcs, "game_data")
            assert hasattr(npcs.game_data, "npcs")
            assert len(npcs.game_data.npcs.data) > 0

            # Validate NPC structure
            npc = npcs.game_data.npcs.data[0]
            assert hasattr(npc, "name")
            assert hasattr(npc, "id")
            assert isinstance(npc.id, int)
            assert isinstance(npc.name, str)

    @pytest.mark.asyncio
    async def test_get_npc_details_example(self, api_client_config):
        """Test the get_npc() example with specific NPC ID"""
        async with Client(**api_client_config) as client:
            # Get specific NPC details
            npc = await client.get_npc(id=45166)  # A trial boss

            # Validate response structure
            assert hasattr(npc, "game_data")
            assert hasattr(npc.game_data, "npc")
            assert hasattr(npc.game_data.npc, "name")
            assert npc.game_data.npc.id == 45166

    @pytest.mark.asyncio
    async def test_list_maps_example(self, api_client_config):
        """Test the get_maps() example"""
        async with Client(**api_client_config) as client:
            # Get all maps
            maps = await client.get_maps()

            # Validate response structure
            assert hasattr(maps, "game_data")
            assert hasattr(maps.game_data, "maps")
            assert len(maps.game_data.maps.data) > 0

            # Validate map structure
            game_map = maps.game_data.maps.data[0]
            assert hasattr(game_map, "name")
            assert hasattr(game_map, "id")
            assert isinstance(game_map.id, int)
            assert isinstance(game_map.name, str)

    @pytest.mark.asyncio
    async def test_get_map_details_example(self, api_client_config):
        """Test the get_map() example with valid map ID"""
        async with Client(**api_client_config) as client:
            # First get a valid map ID from the maps list
            maps = await client.get_maps()
            valid_map_id = maps.game_data.maps.data[0].id

            # Get specific map details
            game_map = await client.get_map(id=valid_map_id)

            # Validate response structure
            assert hasattr(game_map, "game_data")
            assert hasattr(game_map.game_data, "map")
            assert hasattr(game_map.game_data.map, "name")
            assert game_map.game_data.map.id == valid_map_id

    @pytest.mark.asyncio
    async def test_list_factions_example(self, api_client_config):
        """Test the get_factions() example"""
        async with Client(**api_client_config) as client:
            # Get all factions
            factions = await client.get_factions()

            # Validate response structure
            assert hasattr(factions, "game_data")
            assert hasattr(factions.game_data, "factions")
            assert len(factions.game_data.factions) > 0

            # Validate faction structure
            faction = factions.game_data.factions[0]
            assert hasattr(faction, "name")
            assert hasattr(faction, "id")
            assert isinstance(faction.id, int)
            assert isinstance(faction.name, str)

    @pytest.mark.asyncio
    async def test_build_item_database_pattern(self, api_client_config):
        """Test the build_item_database() common pattern example (limited)"""
        async with Client(**api_client_config) as client:
            items_database = []

            # Test just first page to avoid rate limits in testing
            items_response = await client.get_items(limit=10, page=1)
            items = items_response.game_data.items.data

            # Process each item
            for item in items:
                items_database.append(
                    {
                        "id": item.id,
                        "name": item.name or f"Item_{item.id}",  # Handle None names
                    }
                )

            # Validate the pattern works
            assert len(items_database) > 0
            assert all("id" in item and "name" in item for item in items_database)
            assert all(isinstance(item["id"], int) for item in items_database)
            assert all(isinstance(item["name"], str) for item in items_database)
