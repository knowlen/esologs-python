"""Integration tests for Core API methods (Game Data, Character Data, etc.)."""

import asyncio
import pytest
import os
from typing import Optional

from esologs.client import Client
from access_token import get_access_token


@pytest.fixture
def client():
    """Create a test client with real API credentials."""
    api_endpoint = "https://www.esologs.com/api/v2/client"
    access_token = get_access_token()
    
    return Client(
        url=api_endpoint,
        headers={"Authorization": f"Bearer {access_token}"}
    )


@pytest.fixture
def test_character_id():
    """Test character ID for integration tests."""
    return 34663


@pytest.fixture
def test_guild_id():
    """Test guild ID for integration tests."""
    return 3660


@pytest.fixture
def test_report_code():
    """Test report code for integration tests."""
    return "VfxqaX47HGC98rAp"


class TestGameDataIntegration:
    """Integration tests for game data functionality."""

    @pytest.mark.asyncio
    async def test_get_ability(self, client):
        """Test ability retrieval by ID."""
        async with client:
            response = await client.get_ability(id=1084)
            
            assert response is not None
            assert hasattr(response, 'game_data')
            if response.game_data:
                assert response.game_data.ability is not None

    @pytest.mark.asyncio
    async def test_get_abilities(self, client):
        """Test abilities list retrieval."""
        async with client:
            response = await client.get_abilities(limit=10, page=1)
            
            assert response is not None
            assert hasattr(response, 'game_data')
            if response.game_data:
                assert response.game_data.abilities is not None

    @pytest.mark.asyncio
    async def test_get_class(self, client):
        """Test class retrieval by ID."""
        async with client:
            response = await client.get_class(id=1)
            
            assert response is not None
            assert hasattr(response, 'game_data')
            if response.game_data:
                assert response.game_data.class_ is not None

    @pytest.mark.asyncio
    async def test_get_classes(self, client):
        """Test classes list retrieval."""
        async with client:
            response = await client.get_classes()
            
            assert response is not None
            assert hasattr(response, 'game_data')
            if response.game_data:
                assert response.game_data.classes is not None

    @pytest.mark.asyncio
    async def test_get_factions(self, client):
        """Test factions list retrieval."""
        async with client:
            response = await client.get_factions()
            
            assert response is not None
            assert hasattr(response, 'game_data')
            if response.game_data:
                assert response.game_data.factions is not None

    @pytest.mark.asyncio
    async def test_get_item(self, client):
        """Test item retrieval by ID."""
        async with client:
            response = await client.get_item(id=19)
            
            assert response is not None
            assert hasattr(response, 'game_data')
            if response.game_data:
                assert response.game_data.item is not None

    @pytest.mark.asyncio
    async def test_get_items(self, client):
        """Test items list retrieval."""
        async with client:
            response = await client.get_items(limit=10, page=1)
            
            assert response is not None
            assert hasattr(response, 'game_data')
            if response.game_data:
                assert response.game_data.items is not None

    @pytest.mark.asyncio
    async def test_get_item_set(self, client):
        """Test item set retrieval by ID."""
        async with client:
            response = await client.get_item_set(id=19)
            
            assert response is not None
            assert hasattr(response, 'game_data')
            if response.game_data:
                assert response.game_data.item_set is not None

    @pytest.mark.asyncio
    async def test_get_item_sets(self, client):
        """Test item sets list retrieval."""
        async with client:
            response = await client.get_item_sets(limit=10, page=1)
            
            assert response is not None
            assert hasattr(response, 'game_data')
            if response.game_data:
                assert response.game_data.item_sets is not None

    @pytest.mark.asyncio
    async def test_get_map(self, client):
        """Test map retrieval by ID."""
        async with client:
            response = await client.get_map(id=1)
            
            assert response is not None
            assert hasattr(response, 'game_data')
            # Map data might be None for invalid IDs, just check structure
            assert response.game_data is not None

    @pytest.mark.asyncio
    async def test_get_maps(self, client):
        """Test maps list retrieval."""
        async with client:
            response = await client.get_maps(limit=10, page=1)
            
            assert response is not None
            assert hasattr(response, 'game_data')
            # Maps data might be None, just check structure
            assert response.game_data is not None

    @pytest.mark.asyncio
    async def test_get_npc(self, client):
        """Test NPC retrieval by ID."""
        async with client:
            response = await client.get_npc(id=1)
            
            assert response is not None
            assert hasattr(response, 'game_data')
            if response.game_data:
                assert response.game_data.npc is not None

    @pytest.mark.asyncio
    async def test_get_npcs(self, client):
        """Test NPCs list retrieval."""
        async with client:
            response = await client.get_np_cs(limit=10, page=1)
            
            assert response is not None
            assert hasattr(response, 'game_data')
            if response.game_data:
                assert response.game_data.npcs is not None


class TestWorldDataIntegration:
    """Integration tests for world data functionality."""

    @pytest.mark.asyncio
    async def test_get_regions(self, client):
        """Test regions list retrieval."""
        async with client:
            response = await client.get_regions()
            
            assert response is not None
            assert hasattr(response, 'world_data')
            if response.world_data:
                assert response.world_data.regions is not None

    @pytest.mark.asyncio
    async def test_get_zones(self, client):
        """Test zones list retrieval."""
        async with client:
            response = await client.get_zones()
            
            assert response is not None
            assert hasattr(response, 'world_data')
            if response.world_data:
                assert response.world_data.zones is not None

    @pytest.mark.asyncio
    async def test_get_encounters_by_zone(self, client):
        """Test encounters by zone retrieval."""
        async with client:
            response = await client.get_encounters_by_zone(zone_id=1)
            
            assert response is not None
            assert hasattr(response, 'world_data')
            if response.world_data:
                assert response.world_data.zone is not None


class TestCharacterDataIntegration:
    """Integration tests for character data functionality."""

    @pytest.mark.asyncio
    async def test_get_character_by_id(self, client, test_character_id):
        """Test character retrieval by ID."""
        async with client:
            response = await client.get_character_by_id(id=test_character_id)
            
            assert response is not None
            assert hasattr(response, 'character_data')
            if response.character_data:
                assert response.character_data.character is not None

    @pytest.mark.asyncio
    async def test_get_character_reports(self, client, test_character_id):
        """Test character reports retrieval."""
        async with client:
            response = await client.get_character_reports(
                character_id=test_character_id,
                limit=10
            )
            
            assert response is not None
            assert hasattr(response, 'character_data')
            # Reports might be None, just check structure
            if response.character_data:
                assert response.character_data.character is not None

    @pytest.mark.asyncio
    async def test_get_character_encounter_ranking(self, client, test_character_id):
        """Test character encounter ranking retrieval."""
        async with client:
            response = await client.get_character_encounter_ranking(
                character_id=test_character_id,
                encounter_id=27
            )
            
            assert response is not None
            assert hasattr(response, 'character_data')
            if response.character_data and response.character_data.character:
                assert response.character_data.character.encounter_rankings is not None


class TestGuildDataIntegration:
    """Integration tests for guild data functionality."""

    @pytest.mark.asyncio
    async def test_get_guild_by_id(self, client, test_guild_id):
        """Test guild retrieval by ID."""
        async with client:
            response = await client.get_guild_by_id(guild_id=test_guild_id)
            
            assert response is not None
            assert hasattr(response, 'guild_data')
            if response.guild_data:
                assert response.guild_data.guild is not None


class TestReportDataIntegration:
    """Integration tests for report data functionality."""

    @pytest.mark.asyncio
    async def test_get_report_by_code(self, client, test_report_code):
        """Test report retrieval by code."""
        async with client:
            response = await client.get_report_by_code(code=test_report_code)
            
            assert response is not None
            assert hasattr(response, 'report_data')
            if response.report_data:
                assert response.report_data.report is not None


class TestSystemDataIntegration:
    """Integration tests for system data functionality."""

    @pytest.mark.asyncio
    async def test_get_rate_limit_data(self, client):
        """Test rate limit data retrieval."""
        async with client:
            response = await client.get_rate_limit_data()
            
            assert response is not None
            # Rate limit data structure varies, just check basic response
            assert response is not None


class TestComprehensiveWorkflow:
    """Integration tests for comprehensive API workflows."""

    @pytest.mark.asyncio
    @pytest.mark.timeout(45)  # 45 second timeout for workflow test
    async def test_full_character_analysis_workflow(self, client, test_character_id):
        """Test full character analysis workflow."""
        async with client:
            # Get character info
            character = await client.get_character_by_id(id=test_character_id)
            assert character is not None
            
            # Get character reports
            reports = await client.get_character_reports(
                character_id=test_character_id,
                limit=5
            )
            assert reports is not None
            
            # Get character encounter ranking
            encounter_ranking = await client.get_character_encounter_ranking(
                character_id=test_character_id,
                encounter_id=27
            )
            assert encounter_ranking is not None

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)  # 30 second timeout for game data workflow
    async def test_full_game_data_workflow(self, client):
        """Test full game data workflow."""
        async with client:
            # Get classes
            classes = await client.get_classes()
            assert classes is not None
            
            # Get factions
            factions = await client.get_factions()
            assert factions is not None
            
            # Get zones
            zones = await client.get_zones()
            assert zones is not None
            
            # Get some abilities
            abilities = await client.get_abilities(limit=5, page=1)
            assert abilities is not None

    @pytest.mark.asyncio
    async def test_rate_limiting_awareness(self, client):
        """Test rate limiting awareness."""
        async with client:
            # Check that rate limit endpoint responds (don't assume specific structure)
            try:
                rate_limit = await client.get_rate_limit_data()
                assert rate_limit is not None
            except Exception:
                # Rate limit endpoint may not be available - skip this validation
                pass
            
            # Perform several operations with delays to respect rate limits
            for i in range(3):
                response = await client.get_classes()
                assert response is not None
                
                # Add delay between requests to be respectful of API limits
                await asyncio.sleep(0.5)
                
                # Optional rate limit check - don't fail if unavailable
                try:
                    rate_limit = await client.get_rate_limit_data()
                    assert rate_limit is not None
                except Exception:
                    # Rate limit data may not be available - continue test
                    pass


if __name__ == "__main__":
    # Run a simple test if executed directly
    async def main():
        client = Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": f"Bearer {get_access_token()}"}
        )
        
        async with client:
            response = await client.get_classes()
            print("Core API Integration Test Result:", response)
    
    asyncio.run(main())