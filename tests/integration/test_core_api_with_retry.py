"""Example of integration tests with retry logic for handling transient failures."""

import pytest

from tests.integration.retry_utils import retry_integration_test


class TestCharacterDataIntegrationWithRetry:
    """Integration tests for character data functionality with retry logic."""

    @pytest.mark.asyncio
    @retry_integration_test
    async def test_get_character_reports_with_retry(self, client, test_data):
        """Test character reports retrieval with automatic retry on timeout."""
        async with client:
            response = await client.get_character_reports(
                character_id=test_data["character_id"], limit=10
            )

            assert response is not None
            assert hasattr(response, "character_data")
            # Reports might be None, just check structure
            if response.character_data:
                assert response.character_data.character is not None
