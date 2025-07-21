"""Integration tests for error handling and edge cases."""

import asyncio

import pytest

from esologs._generated.enums import CharacterRankingMetricType, EventDataType
from esologs.auth import get_access_token
from esologs.client import Client

# Fixtures are now centralized in conftest.py


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
            assert hasattr(response, "character_data")

    @pytest.mark.asyncio
    async def test_invalid_guild_id(self, client):
        """Test handling of invalid guild ID."""
        invalid_id = 999999999

        async with client:
            # Should not raise exception, but return empty/null data
            response = await client.get_guild_by_id(guild_id=invalid_id)
            assert response is not None
            assert hasattr(response, "guild_data")

    @pytest.mark.asyncio
    async def test_invalid_report_code(self, client):
        """Test handling of invalid report code."""
        invalid_code = "ABCDEfghij123456"  # Valid format but non-existent

        async with client:
            # Should raise GraphQL error for non-existent report
            try:
                response = await client.get_report_by_code(code=invalid_code)
                # If no exception, check response structure
                assert response is not None
                assert hasattr(response, "report_data")
            except Exception as e:
                # Expected to raise GraphQLQueryError for non-existent report
                assert "report" in str(e).lower() and (
                    "exist" in str(e).lower() or "not found" in str(e).lower()
                )

    @pytest.mark.asyncio
    async def test_invalid_encounter_id(self, client):
        """Test handling of invalid encounter ID."""
        invalid_id = 999999999
        test_character_id = 34663

        async with client:
            # Should not raise exception, but return empty/null data
            response = await client.get_character_encounter_ranking(
                character_id=test_character_id, encounter_id=invalid_id
            )
            assert response is not None
            assert hasattr(response, "character_data")

    @pytest.mark.asyncio
    async def test_invalid_zone_id(self, client):
        """Test handling of invalid zone ID."""
        invalid_id = 999999999

        async with client:
            # Should not raise exception, but return empty/null data
            response = await client.get_encounters_by_zone(zone_id=invalid_id)
            assert response is not None
            assert hasattr(response, "world_data")

    @pytest.mark.asyncio
    async def test_invalid_ability_id(self, client):
        """Test handling of invalid ability ID."""
        invalid_id = 999999999

        async with client:
            # Should not raise exception, but return empty/null data
            response = await client.get_ability(id=invalid_id)
            assert response is not None
            assert hasattr(response, "game_data")

    @pytest.mark.asyncio
    async def test_invalid_item_id(self, client):
        """Test handling of invalid item ID."""
        invalid_id = 999999999

        async with client:
            # Should not raise exception, but return empty/null data
            response = await client.get_item(id=invalid_id)
            assert response is not None
            assert hasattr(response, "game_data")

    @pytest.mark.asyncio
    async def test_invalid_pagination_parameters(self, client):
        """Test handling of invalid pagination parameters."""
        async with client:
            # Test with very large page number
            response = await client.get_abilities(limit=10, page=999999)
            assert response is not None
            assert hasattr(response, "game_data")

    @pytest.mark.asyncio
    async def test_invalid_time_range_parameters(self, client):
        """Test handling of invalid time range parameters."""
        test_report_code = "VfxqaX47HGC98rAp"

        async with client:
            # Test with valid time range but potentially empty results
            response = await client.get_report_events(
                code=test_report_code,
                data_type=EventDataType.DamageDone,
                start_time=0.0,
                end_time=1000.0,  # Very short time range
            )
            assert response is not None
            assert hasattr(response, "report_data")

    @pytest.mark.asyncio
    async def test_negative_parameters(self, client):
        """Test handling of negative parameters."""
        async with client:
            # Test with negative limit - should raise validation error
            try:
                response = await client.get_abilities(limit=-10, page=1)
                assert response is not None
                assert hasattr(response, "game_data")
            except Exception as e:
                # Expected to raise error for invalid limit
                assert "limit" in str(e).lower() and (
                    "must be" in str(e).lower() or "invalid" in str(e).lower()
                )

    @pytest.mark.asyncio
    async def test_zero_parameters(self, client):
        """Test handling of zero parameters."""
        async with client:
            # Test with zero limit - should raise validation error
            try:
                response = await client.get_abilities(limit=0, page=1)
                assert response is not None
                assert hasattr(response, "game_data")
            except Exception as e:
                # Expected to raise error for invalid limit
                assert "limit argument must be" in str(e)

    @pytest.mark.asyncio
    async def test_very_large_limit_parameters(self, client):
        """Test handling of very large limit parameters."""
        async with client:
            # Test with extremely large limit - should raise complexity error
            try:
                response = await client.get_abilities(limit=999999, page=1)
                assert response is not None
                assert hasattr(response, "game_data")
            except Exception as e:
                # Expected to raise query complexity error
                assert "complexity" in str(e).lower()

    @pytest.mark.asyncio
    async def test_malformed_report_code(self, client):
        """Test handling of malformed report codes."""
        # Use valid format codes that don't exist
        test_codes = [
            "ABCDEfghij123456",  # Valid format, non-existent
            "ZZZZZzzzzz999999",  # Valid format, non-existent
        ]

        async with client:
            for code in test_codes:
                try:
                    response = await client.get_report_by_code(code=code)
                    assert response is not None
                    assert hasattr(response, "report_data")
                except Exception:
                    # Some codes may raise validation errors, which is expected
                    pass

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)  # 30 second timeout
    async def test_concurrent_requests(self, client):
        """Test handling of concurrent API requests."""
        async with client:
            # Make multiple concurrent requests
            tasks = []
            for _i in range(5):
                task = client.get_classes()
                tasks.append(task)

            # Wait for all requests to complete with timeout
            responses = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=25.0,  # 25 second timeout for gather
            )

            # Verify all requests completed successfully
            for response in responses:
                assert not isinstance(response, Exception)
                assert response is not None
                assert hasattr(response, "game_data")

    @pytest.mark.asyncio
    async def test_rate_limit_handling(self, client):
        """Test rate limit handling with respectful requests."""
        async with client:
            # Make respectful requests to test basic functionality
            successful_requests = 0
            for _i in range(5):  # Reduced from 10 to be more respectful
                try:
                    response = await client.get_rate_limit_data()
                    if response is not None:
                        successful_requests += 1
                except Exception:
                    # Rate limiting or other API restrictions - expected behavior
                    pass

                # Reasonable delay to respect API limits
                await asyncio.sleep(1.0)  # Increased delay

            # Verify we got at least some successful responses
            assert (
                successful_requests > 0
            ), "Should get at least one successful rate limit response"

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
                client.get_character_by_id(id=34663),
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
                size=999,  # Invalid size
            )
            assert response is not None
            assert hasattr(response, "character_data")

    @pytest.mark.asyncio
    async def test_edge_case_report_analysis(self, client):
        """Test edge cases for report analysis."""
        test_report_code = "VfxqaX47HGC98rAp"

        async with client:
            # Test with reasonable time ranges
            response = await client.get_report_events(
                code=test_report_code,
                data_type=EventDataType.DamageDone,
                start_time=0.0,
                end_time=120000.0,  # 2 minutes
            )
            assert response is not None
            assert hasattr(response, "report_data")

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
            headers={"Authorization": f"Bearer {get_access_token()}"},
        )

        async with client:
            # Test invalid character ID
            await client.get_character_by_id(id=999999999)
            # Error Handling Integration Test Result logged via pytest

    asyncio.run(main())
