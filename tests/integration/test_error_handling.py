"""Integration tests for error handling and edge cases."""

import asyncio
import pytest
from typing import Optional

from esologs.client import Client
from esologs.enums import (
    CharacterRankingMetricType,
    EventDataType,
    GraphDataType,
    TableDataType,
    ReportRankingMetricType
)
from esologs.exceptions import ValidationError
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


class TestErrorHandlingIntegration:
    """Integration tests for error handling and edge cases."""

    @pytest.mark.asyncio
    async def test_invalid_character_id(self, client):
        """Test handling of invalid character ID."""
        invalid_id = 999999999
        
        async with client:
            # Should not raise exception, but return empty/null data
            response = await client.get_character_by_id(id=invalid_id)
            assert response is not None
            assert hasattr(response, 'character_data')

    @pytest.mark.asyncio
    async def test_invalid_guild_id(self, client):
        """Test handling of invalid guild ID."""
        invalid_id = 999999999
        
        async with client:
            # Should not raise exception, but return empty/null data
            response = await client.get_guild_by_id(guild_id=invalid_id)
            assert response is not None
            assert hasattr(response, 'guild_data')

    @pytest.mark.asyncio
    async def test_invalid_report_code(self, client):
        """Test handling of invalid report code."""
        invalid_code = "INVALID_CODE_123"
        
        async with client:
            # Should not raise exception, but return empty/null data
            response = await client.get_report_by_code(code=invalid_code)
            assert response is not None
            assert hasattr(response, 'report_data')

    @pytest.mark.asyncio
    async def test_invalid_encounter_id(self, client):
        """Test handling of invalid encounter ID."""
        invalid_id = 999999999
        test_character_id = 34663
        
        async with client:
            # Should not raise exception, but return empty/null data
            response = await client.get_character_encounter_ranking(
                character_id=test_character_id,
                encounter_id=invalid_id
            )
            assert response is not None
            assert hasattr(response, 'character_data')

    @pytest.mark.asyncio
    async def test_invalid_zone_id(self, client):
        """Test handling of invalid zone ID."""
        invalid_id = 999999999
        
        async with client:
            # Should not raise exception, but return empty/null data
            response = await client.get_encounters_by_zone(zone_id=invalid_id)
            assert response is not None
            assert hasattr(response, 'world_data')

    @pytest.mark.asyncio
    async def test_invalid_ability_id(self, client):
        """Test handling of invalid ability ID."""
        invalid_id = 999999999
        
        async with client:
            # Should not raise exception, but return empty/null data
            response = await client.get_ability(id=invalid_id)
            assert response is not None
            assert hasattr(response, 'game_data')

    @pytest.mark.asyncio
    async def test_invalid_item_id(self, client):
        """Test handling of invalid item ID."""
        invalid_id = 999999999
        
        async with client:
            # Should not raise exception, but return empty/null data
            response = await client.get_item(id=invalid_id)
            assert response is not None
            assert hasattr(response, 'game_data')

    @pytest.mark.asyncio
    async def test_invalid_pagination_parameters(self, client):
        """Test handling of invalid pagination parameters."""
        async with client:
            # Test with very large page number
            response = await client.get_abilities(limit=10, page=999999)
            assert response is not None
            assert hasattr(response, 'game_data')

    @pytest.mark.asyncio
    async def test_invalid_time_range_parameters(self, client):
        """Test handling of invalid time range parameters."""
        test_report_code = "VfxqaX47HGC98rAp"
        
        async with client:
            # Test with invalid time range (start > end)
            response = await client.get_report_events(
                code=test_report_code,
                data_type=EventDataType.DamageDone,
                start_time=60000.0,
                end_time=30000.0
            )
            assert response is not None
            assert hasattr(response, 'report_data')

    @pytest.mark.asyncio
    async def test_negative_parameters(self, client):
        """Test handling of negative parameters."""
        async with client:
            # Test with negative limit
            response = await client.get_abilities(limit=-10, page=1)
            assert response is not None
            assert hasattr(response, 'game_data')

    @pytest.mark.asyncio
    async def test_zero_parameters(self, client):
        """Test handling of zero parameters."""
        async with client:
            # Test with zero limit
            response = await client.get_abilities(limit=0, page=1)
            assert response is not None
            assert hasattr(response, 'game_data')

    @pytest.mark.asyncio
    async def test_very_large_limit_parameters(self, client):
        """Test handling of very large limit parameters."""
        async with client:
            # Test with extremely large limit
            response = await client.get_abilities(limit=999999, page=1)
            assert response is not None
            assert hasattr(response, 'game_data')

    @pytest.mark.asyncio
    async def test_malformed_report_code(self, client):
        """Test handling of malformed report codes."""
        malformed_codes = [
            "",  # Empty string
            "123",  # Too short
            "A" * 100,  # Too long
            "INVALID!@#$%",  # Special characters
            "spaces in code"  # Spaces
        ]
        
        async with client:
            for code in malformed_codes:
                response = await client.get_report_by_code(code=code)
                assert response is not None
                assert hasattr(response, 'report_data')

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, client):
        """Test handling of concurrent API requests."""
        async with client:
            # Make multiple concurrent requests
            tasks = []
            for i in range(5):
                task = client.get_classes()
                tasks.append(task)
            
            # Wait for all requests to complete
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Verify all requests completed successfully
            for response in responses:
                assert not isinstance(response, Exception)
                assert response is not None
                assert hasattr(response, 'game_data')

    @pytest.mark.asyncio
    async def test_rate_limit_handling(self, client):
        """Test rate limit handling with rapid requests."""
        async with client:
            # Make rapid requests to test rate limiting
            for i in range(10):
                response = await client.get_rate_limit_data()
                assert response is not None
                assert hasattr(response, 'rate_limit_data')
                
                # Small delay to avoid overwhelming the API
                await asyncio.sleep(0.1)

    @pytest.mark.asyncio
    async def test_connection_resilience(self, client):
        """Test connection resilience with various operations."""
        async with client:
            # Test sequence of different operations
            operations = [
                client.get_classes(),
                client.get_factions(),
                client.get_zones(),
                client.get_rate_limit_data(),
                client.get_character_by_id(id=34663)
            ]
            
            for operation in operations:
                response = await operation
                assert response is not None

    @pytest.mark.asyncio
    async def test_edge_case_character_rankings(self, client):
        """Test edge cases for character rankings."""
        test_character_id = 34663
        
        async with client:
            # Test with invalid metrics combination
            response = await client.get_character_encounter_rankings(
                character_id=test_character_id,
                encounter_id=27,
                metric=CharacterRankingMetricType.dps,
                difficulty=999,  # Invalid difficulty
                size=999  # Invalid size
            )
            assert response is not None
            assert hasattr(response, 'character_data')

    @pytest.mark.asyncio
    async def test_edge_case_report_analysis(self, client):
        """Test edge cases for report analysis."""
        test_report_code = "VfxqaX47HGC98rAp"
        
        async with client:
            # Test with extreme time ranges
            response = await client.get_report_events(
                code=test_report_code,
                data_type=EventDataType.DamageDone,
                start_time=0.0,
                end_time=999999999.0  # Very large end time
            )
            assert response is not None
            assert hasattr(response, 'report_data')

    @pytest.mark.asyncio
    async def test_client_context_manager_error_handling(self, client):
        """Test client context manager error handling."""
        # Test that client handles errors gracefully within context manager
        async with client:
            try:
                # This should not raise an exception even with invalid data
                response = await client.get_character_by_id(id=999999999)
                assert response is not None
            except Exception as e:
                pytest.fail(f"Unexpected exception in context manager: {e}")

    @pytest.mark.asyncio
    async def test_mixed_valid_invalid_workflow(self, client):
        """Test workflow mixing valid and invalid requests."""
        async with client:
            # Valid request
            valid_response = await client.get_classes()
            assert valid_response is not None
            
            # Invalid request
            invalid_response = await client.get_character_by_id(id=999999999)
            assert invalid_response is not None
            
            # Another valid request
            another_valid_response = await client.get_factions()
            assert another_valid_response is not None


if __name__ == "__main__":
    # Run a simple test if executed directly
    async def main():
        client = Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": f"Bearer {get_access_token()}"}
        )
        
        async with client:
            # Test invalid character ID
            response = await client.get_character_by_id(id=999999999)
            print("Error Handling Integration Test Result:", response)
    
    asyncio.run(main())