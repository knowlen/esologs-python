"""Integration tests for Character Rankings API methods."""

import asyncio
import pytest
import os
from typing import Optional

from esologs.client import Client
from esologs.enums import CharacterRankingMetricType
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
def test_encounter_id():
    """Test encounter ID for integration tests."""
    return 27


@pytest.fixture  
def test_zone_id():
    """Test zone ID for integration tests."""
    return 8


class TestCharacterRankingsIntegration:
    """Integration tests for character rankings functionality."""

    @pytest.mark.asyncio
    async def test_get_character_encounter_rankings_basic(self, client, test_character_id, test_encounter_id):
        """Test basic character encounter rankings retrieval."""
        async with client:
            response = await client.get_character_encounter_rankings(
                character_id=test_character_id,
                encounter_id=test_encounter_id,
                metric=CharacterRankingMetricType.dps
            )
            
            assert response is not None
            assert hasattr(response, 'character_data')
            if response.character_data and response.character_data.character:
                assert response.character_data.character.encounter_rankings is not None

    @pytest.mark.asyncio
    async def test_get_character_encounter_rankings_with_filters(self, client, test_character_id, test_encounter_id):
        """Test character encounter rankings with additional filters."""
        async with client:
            response = await client.get_character_encounter_rankings(
                character_id=test_character_id,
                encounter_id=test_encounter_id,
                metric=CharacterRankingMetricType.hps,
                difficulty=1,
                size=8
            )
            
            assert response is not None
            assert hasattr(response, 'character_data')

    @pytest.mark.asyncio
    async def test_get_character_zone_rankings_basic(self, client, test_character_id, test_zone_id):
        """Test basic character zone rankings retrieval."""
        async with client:
            response = await client.get_character_zone_rankings(
                character_id=test_character_id,
                zone_id=test_zone_id,
                metric=CharacterRankingMetricType.playerscore
            )
            
            assert response is not None
            assert hasattr(response, 'character_data')
            if response.character_data and response.character_data.character:
                assert response.character_data.character.zone_rankings is not None

    @pytest.mark.asyncio
    async def test_get_character_zone_rankings_with_filters(self, client, test_character_id, test_zone_id):
        """Test character zone rankings with additional filters."""
        async with client:
            response = await client.get_character_zone_rankings(
                character_id=test_character_id,
                zone_id=test_zone_id,
                metric=CharacterRankingMetricType.dps,
                difficulty=1,
                size=8
            )
            
            assert response is not None
            assert hasattr(response, 'character_data')

    @pytest.mark.asyncio
    async def test_get_character_encounter_rankings_all_metrics(self, client, test_character_id, test_encounter_id):
        """Test character encounter rankings with different metrics."""
        metrics_to_test = [
            CharacterRankingMetricType.dps,
            CharacterRankingMetricType.hps,
            CharacterRankingMetricType.playerscore
        ]
        
        async with client:
            for metric in metrics_to_test:
                response = await client.get_character_encounter_rankings(
                    character_id=test_character_id,
                    encounter_id=test_encounter_id,
                    metric=metric
                )
                
                assert response is not None
                assert hasattr(response, 'character_data')

    @pytest.mark.asyncio
    async def test_get_character_zone_rankings_all_metrics(self, client, test_character_id, test_zone_id):
        """Test character zone rankings with different metrics."""
        metrics_to_test = [
            CharacterRankingMetricType.dps,
            CharacterRankingMetricType.hps, 
            CharacterRankingMetricType.playerscore
        ]
        
        async with client:
            for metric in metrics_to_test:
                response = await client.get_character_zone_rankings(
                    character_id=test_character_id,
                    zone_id=test_zone_id,
                    metric=metric
                )
                
                assert response is not None
                assert hasattr(response, 'character_data')

    @pytest.mark.asyncio
    async def test_rankings_with_invalid_character_id(self, client, test_encounter_id):
        """Test rankings with invalid character ID."""
        invalid_character_id = 999999999
        
        async with client:
            response = await client.get_character_encounter_rankings(
                character_id=invalid_character_id,
                encounter_id=test_encounter_id,
                metric=CharacterRankingMetricType.dps
            )
            
            # Should return valid response structure even with invalid ID
            assert response is not None
            assert hasattr(response, 'character_data')

    @pytest.mark.asyncio
    async def test_rankings_with_invalid_encounter_id(self, client, test_character_id):
        """Test rankings with invalid encounter ID."""
        invalid_encounter_id = 999999999
        
        async with client:
            response = await client.get_character_encounter_rankings(
                character_id=test_character_id,
                encounter_id=invalid_encounter_id,
                metric=CharacterRankingMetricType.dps
            )
            
            # Should return valid response structure even with invalid ID
            assert response is not None
            assert hasattr(response, 'character_data')

    @pytest.mark.asyncio
    async def test_rankings_with_invalid_zone_id(self, client, test_character_id):
        """Test rankings with invalid zone ID."""
        invalid_zone_id = 999999999
        
        async with client:
            response = await client.get_character_zone_rankings(
                character_id=test_character_id,
                zone_id=invalid_zone_id,
                metric=CharacterRankingMetricType.playerscore
            )
            
            # Should return valid response structure even with invalid ID
            assert response is not None
            assert hasattr(response, 'character_data')


if __name__ == "__main__":
    # Run a simple test if executed directly
    async def main():
        client = Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": f"Bearer {get_access_token()}"}
        )
        
        async with client:
            response = await client.get_character_encounter_rankings(
                character_id=34663,
                encounter_id=27,
                metric=CharacterRankingMetricType.dps
            )
            print("Character Rankings Integration Test Result:", response)
    
    asyncio.run(main())