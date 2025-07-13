"""
Tests for examples in docs/api-reference/world-data.md

Validates that all code examples in the world data API documentation 
execute correctly and return expected data structures.
"""

import pytest
import asyncio
from esologs.client import Client
from access_token import get_access_token
from collections import defaultdict


class TestWorldDataExamples:
    """Test all examples from world-data.md documentation"""

    @pytest.mark.asyncio
    async def test_list_zones_example(self, api_client_config):
        """Test the get_zones() basic example"""
        async with Client(**api_client_config) as client:
            zones = await client.get_zones()
            
            # Validate response structure
            assert hasattr(zones, 'world_data')
            assert hasattr(zones.world_data, 'zones')
            assert len(zones.world_data.zones) > 0
            
            # Validate zone structure
            zone = zones.world_data.zones[0]
            assert hasattr(zone, 'id')
            assert hasattr(zone, 'name')
            assert hasattr(zone, 'frozen')
            assert hasattr(zone, 'expansion')
            assert isinstance(zone.id, int)
            assert isinstance(zone.name, str)
            assert isinstance(zone.frozen, bool)
            
            # Validate expansion structure
            assert hasattr(zone.expansion, 'id')
            assert hasattr(zone.expansion, 'name')
            assert isinstance(zone.expansion.id, int)
            assert isinstance(zone.expansion.name, str)
            
            # Validate encounters if present
            if zone.encounters:
                encounter = zone.encounters[0]
                assert hasattr(encounter, 'id')
                assert hasattr(encounter, 'name')
                assert isinstance(encounter.id, int)
                assert isinstance(encounter.name, str)
            
            # Validate difficulties if present
            if zone.difficulties:
                difficulty = zone.difficulties[0]
                assert hasattr(difficulty, 'id')
                assert hasattr(difficulty, 'name')
                assert hasattr(difficulty, 'sizes')
                assert isinstance(difficulty.id, int)
                assert isinstance(difficulty.name, str)
                assert isinstance(difficulty.sizes, list)

    @pytest.mark.asyncio
    async def test_list_regions_example(self, api_client_config):
        """Test the get_regions() basic example"""
        async with Client(**api_client_config) as client:
            regions = await client.get_regions()
            
            # Validate response structure
            assert hasattr(regions, 'world_data')
            assert hasattr(regions.world_data, 'regions')
            assert len(regions.world_data.regions) > 0
            
            # Validate region structure
            region = regions.world_data.regions[0]
            assert hasattr(region, 'id')
            assert hasattr(region, 'name')
            assert isinstance(region.id, int)
            assert isinstance(region.name, str)
            
            # Validate subregions if present
            if region.subregions:
                subregion = region.subregions[0]
                assert hasattr(subregion, 'id')
                assert hasattr(subregion, 'name')
                assert isinstance(subregion.id, int)
                assert isinstance(subregion.name, str)

    @pytest.mark.asyncio
    async def test_get_dungeon_encounters_example(self, api_client_config):
        """Test the get_encounters_by_zone() example"""
        async with Client(**api_client_config) as client:
            # First, get all zones to find the Dungeons zone ID
            zones = await client.get_zones()
            dungeon_zone = next((z for z in zones.world_data.zones if z.name == "Dungeons"), None)
            
            # This test should work if Dungeons zone exists
            if dungeon_zone:
                # Get encounters for the Dungeons zone
                encounters_data = await client.get_encounters_by_zone(dungeon_zone.id)
                
                # Validate response structure
                assert hasattr(encounters_data, 'world_data')
                assert hasattr(encounters_data.world_data, 'zone')
                
                zone = encounters_data.world_data.zone
                assert hasattr(zone, 'id')
                assert hasattr(zone, 'name')
                assert isinstance(zone.id, int)
                assert isinstance(zone.name, str)
                
                # Validate encounters if present
                if zone.encounters:
                    encounter = zone.encounters[0]
                    assert hasattr(encounter, 'id')
                    assert hasattr(encounter, 'name')
                    assert isinstance(encounter.id, int)
                    assert isinstance(encounter.name, str)

    @pytest.mark.asyncio
    async def test_discover_all_encounters_pattern(self, api_client_config):
        """Test the discover all encounters common pattern"""
        async with Client(**api_client_config) as client:
            zones = await client.get_zones()
            
            total_encounters = 0
            for zone in zones.world_data.zones:
                if zone.encounters:
                    assert isinstance(zone.encounters, list)
                    total_encounters += len(zone.encounters)
                    
                    # Validate each encounter
                    for encounter in zone.encounters:
                        assert hasattr(encounter, 'id')
                        assert hasattr(encounter, 'name')
                        assert isinstance(encounter.id, int)
                        assert isinstance(encounter.name, str)
            
            # Should have found some encounters
            assert total_encounters > 0

    @pytest.mark.asyncio
    async def test_analyze_veteran_hard_mode_zones_pattern(self, api_client_config):
        """Test the veteran hard mode analysis common pattern"""
        async with Client(**api_client_config) as client:
            zones = await client.get_zones()
            
            veteran_hm_zones = []
            for zone in zones.world_data.zones:
                if zone.difficulties:
                    assert isinstance(zone.difficulties, list)
                    for difficulty in zone.difficulties:
                        assert hasattr(difficulty, 'name')
                        assert isinstance(difficulty.name, str)
                        if difficulty.name == "Veteran Hard Mode":
                            veteran_hm_zones.append(zone)
                            break
            
            # Should have found some zones with Veteran Hard Mode
            assert len(veteran_hm_zones) > 0
            
            # Validate the zones found
            for zone in veteran_hm_zones:
                assert hasattr(zone, 'id')
                assert hasattr(zone, 'name')
                assert isinstance(zone.id, int)
                assert isinstance(zone.name, str)
                
                # Verify this zone actually has Veteran Hard Mode
                has_vhm = False
                for difficulty in zone.difficulties:
                    if difficulty.name == "Veteran Hard Mode":
                        has_vhm = True
                        break
                assert has_vhm, f"Zone {zone.name} should have Veteran Hard Mode difficulty"

    @pytest.mark.asyncio
    async def test_get_encounters_by_zone_with_invalid_id(self, api_client_config):
        """Test get_encounters_by_zone() with invalid zone ID"""
        async with Client(**api_client_config) as client:
            # Test with an invalid zone ID - this should handle gracefully
            # The GraphQL API may return null/empty data or an error
            try:
                result = await client.get_encounters_by_zone(99999)
                # If it succeeds, the zone should be None or have no encounters
                if result.world_data.zone:
                    # Should still have valid structure even if empty
                    assert hasattr(result.world_data.zone, 'id')
                    assert hasattr(result.world_data.zone, 'name')
            except Exception:
                # It's acceptable for this to raise an exception with invalid ID
                pass

    @pytest.mark.asyncio
    async def test_zone_encounter_consistency(self, api_client_config):
        """Test that zone encounters are consistent between get_zones() and get_encounters_by_zone()"""
        async with Client(**api_client_config) as client:
            zones = await client.get_zones()
            
            # Find a zone with encounters
            test_zone = None
            for zone in zones.world_data.zones:
                if zone.encounters and len(zone.encounters) > 0:
                    test_zone = zone
                    break
            
            if test_zone:
                # Get encounters specifically for this zone
                encounters_data = await client.get_encounters_by_zone(test_zone.id)
                
                if encounters_data.world_data.zone and encounters_data.world_data.zone.encounters:
                    # Both methods should return the same encounters
                    zone_encounters = {e.id for e in test_zone.encounters}
                    specific_encounters = {e.id for e in encounters_data.world_data.zone.encounters}
                    
                    # The encounter sets should be the same
                    assert zone_encounters == specific_encounters