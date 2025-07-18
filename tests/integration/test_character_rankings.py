"""Integration tests for Character Rankings API methods."""

import asyncio

import pytest

from esologs._generated.enums import CharacterRankingMetricType
from esologs.auth import get_access_token
from esologs.client import Client

# Fixtures are now centralized in conftest.py


class TestCharacterRankingsIntegration:
    """Integration tests for character rankings functionality."""

    @pytest.mark.asyncio
    async def test_get_character_encounter_rankings_basic(self, client, test_data):
        """Test basic character encounter rankings retrieval."""
        async with client:
            response = await client.get_character_encounter_rankings(
                character_id=test_data["character_id"],
                encounter_id=test_data["encounter_id"],
                metric=CharacterRankingMetricType.dps,
            )

            assert response is not None
            assert hasattr(response, "character_data")
            if response.character_data and response.character_data.character:
                assert response.character_data.character.encounter_rankings is not None

    @pytest.mark.asyncio
    async def test_get_character_encounter_rankings_with_filters(
        self, client, test_data
    ):
        """Test character encounter rankings with additional filters."""
        async with client:
            response = await client.get_character_encounter_rankings(
                character_id=test_data["character_id"],
                encounter_id=test_data["encounter_id"],
                metric=CharacterRankingMetricType.hps,
                difficulty=1,
                size=8,
            )

            assert response is not None
            assert hasattr(response, "character_data")

    @pytest.mark.asyncio
    async def test_get_character_zone_rankings_basic(self, client, test_data):
        """Test basic character zone rankings retrieval."""
        async with client:
            response = await client.get_character_zone_rankings(
                character_id=test_data["character_id"],
                zone_id=test_data["zone_id"],
                metric=CharacterRankingMetricType.playerscore,
            )

            assert response is not None
            assert hasattr(response, "character_data")
            if response.character_data and response.character_data.character:
                assert response.character_data.character.zone_rankings is not None

    @pytest.mark.asyncio
    async def test_get_character_zone_rankings_with_filters(self, client, test_data):
        """Test character zone rankings with additional filters."""
        async with client:
            response = await client.get_character_zone_rankings(
                character_id=test_data["character_id"],
                zone_id=test_data["zone_id"],
                metric=CharacterRankingMetricType.dps,
                difficulty=1,
                size=8,
            )

            assert response is not None
            assert hasattr(response, "character_data")

    @pytest.mark.asyncio
    async def test_get_character_encounter_rankings_all_metrics(
        self, client, test_data
    ):
        """Test character encounter rankings with different metrics."""
        metrics_to_test = [
            CharacterRankingMetricType.dps,
            CharacterRankingMetricType.hps,
            CharacterRankingMetricType.playerscore,
        ]

        async with client:
            for metric in metrics_to_test:
                response = await client.get_character_encounter_rankings(
                    character_id=test_data["character_id"],
                    encounter_id=test_data["encounter_id"],
                    metric=metric,
                )

                assert response is not None
                assert hasattr(response, "character_data")

    @pytest.mark.asyncio
    async def test_get_character_zone_rankings_all_metrics(self, client, test_data):
        """Test character zone rankings with different metrics."""
        metrics_to_test = [
            CharacterRankingMetricType.dps,
            CharacterRankingMetricType.hps,
            CharacterRankingMetricType.playerscore,
        ]

        async with client:
            for metric in metrics_to_test:
                response = await client.get_character_zone_rankings(
                    character_id=test_data["character_id"],
                    zone_id=test_data["zone_id"],
                    metric=metric,
                )

                assert response is not None
                assert hasattr(response, "character_data")

    @pytest.mark.asyncio
    async def test_rankings_with_invalid_character_id(self, client, test_data):
        """Test rankings with invalid character ID."""
        invalid_character_id = 999999999

        async with client:
            response = await client.get_character_encounter_rankings(
                character_id=invalid_character_id,
                encounter_id=test_data["encounter_id"],
                metric=CharacterRankingMetricType.dps,
            )

            # Should return valid response structure even with invalid ID
            assert response is not None
            assert hasattr(response, "character_data")

    @pytest.mark.asyncio
    async def test_rankings_with_invalid_encounter_id(self, client, test_data):
        """Test rankings with invalid encounter ID."""
        invalid_encounter_id = 999999999

        async with client:
            response = await client.get_character_encounter_rankings(
                character_id=test_data["character_id"],
                encounter_id=invalid_encounter_id,
                metric=CharacterRankingMetricType.dps,
            )

            # Should return valid response structure even with invalid ID
            assert response is not None
            assert hasattr(response, "character_data")

    @pytest.mark.asyncio
    async def test_rankings_with_invalid_zone_id(self, client, test_data):
        """Test rankings with invalid zone ID."""
        invalid_zone_id = 999999999

        async with client:
            response = await client.get_character_zone_rankings(
                character_id=test_data["character_id"],
                zone_id=invalid_zone_id,
                metric=CharacterRankingMetricType.playerscore,
            )

            # Should return valid response structure even with invalid ID
            assert response is not None
            assert hasattr(response, "character_data")


if __name__ == "__main__":
    # Run a simple test if executed directly
    async def main():
        client = Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": f"Bearer {get_access_token()}"},
        )

        async with client:
            await client.get_character_encounter_rankings(
                character_id=34663,
                encounter_id=27,
                metric=CharacterRankingMetricType.dps,
            )
            # Character Rankings Integration Test Result logged via pytest

    asyncio.run(main())
