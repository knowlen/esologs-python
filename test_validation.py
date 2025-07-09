#!/usr/bin/env python3
"""Test validation functionality with real API calls."""

import asyncio
import os

from access_token import get_access_token
from esologs.client import Client
from esologs.exceptions import ValidationError


async def test_validation():
    """Test parameter validation with report analysis methods."""
    print("Testing parameter validation functionality...")

    # Get authentication token
    token = get_access_token()

    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"},
    ) as client:

        print("\n1. Testing valid parameters - should work:")
        try:
            # This should work with valid parameters
            events = await client.get_report_events(
                code="ABC123",  # This will likely fail with ReportNotFoundError, but validation should pass
                limit=100,
                start_time=0.0,
                end_time=60000.0,
            )
            print("✅ Valid parameters accepted")
        except ValidationError as e:
            print(f"❌ Unexpected validation error: {e}")
        except Exception as e:
            # Expected - likely ReportNotFoundError or similar
            print(f"✅ Validation passed, got expected API error: {type(e).__name__}")

        print("\n2. Testing invalid report code - should fail validation:")
        try:
            events = await client.get_report_events(
                code="", limit=100  # Empty code should fail validation
            )
            print("❌ Empty report code was accepted (should have failed)")
        except ValidationError as e:
            print(f"✅ Validation caught empty report code: {e}")
        except Exception as e:
            print(f"❌ Got unexpected error: {e}")

        print("\n3. Testing invalid ability_id - should fail validation:")
        try:
            events = await client.get_report_events(
                code="ABC123", ability_id=123.5  # Float that's not a whole number
            )
            print("❌ Invalid ability_id was accepted (should have failed)")
        except ValidationError as e:
            print(f"✅ Validation caught invalid ability_id: {e}")
        except Exception as e:
            print(f"❌ Got unexpected error: {e}")

        print("\n4. Testing invalid time range - should fail validation:")
        try:
            events = await client.get_report_events(
                code="ABC123", start_time=100.0, end_time=50.0  # End before start
            )
            print("❌ Invalid time range was accepted (should have failed)")
        except ValidationError as e:
            print(f"✅ Validation caught invalid time range: {e}")
        except Exception as e:
            print(f"❌ Got unexpected error: {e}")

        print("\n5. Testing invalid limit - should fail validation:")
        try:
            await client.get_report_events(
                code="ABC123", limit=20000  # Too large
            )
            print("❌ Invalid limit was accepted (should have failed)")
        except ValidationError as e:
            print(f"✅ Validation caught invalid limit: {e}")
        except Exception as e:
            print(f"❌ Got unexpected error: {e}")

        print("\n6. Testing fight_ids validation:")
        try:
            await client.get_report_events(
                code="ABC123", fight_i_ds=[1, "2", 3]  # Invalid ID type
            )
            print("❌ Invalid fight_ids were accepted (should have failed)")
        except ValidationError as e:
            print(f"✅ Validation caught invalid fight_ids: {e}")
        except Exception as e:
            print(f"❌ Got unexpected error: {e}")

        print("\n7. Testing report graph validation:")
        try:
            await client.get_report_graph(
                code="TEST123", start_time=0.0, end_time=300000.0  # Valid format
            )
            print("✅ Graph validation passed")
        except ValidationError as e:
            print(f"❌ Unexpected validation error: {e}")
        except Exception as e:
            # Expected - likely ReportNotFoundError or similar
            print(
                f"✅ Graph validation passed, got expected API error: {type(e).__name__}"
            )

    print("\n✅ All validation tests completed!")


if __name__ == "__main__":
    asyncio.run(test_validation())
