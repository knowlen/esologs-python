"""Configuration for sanity tests."""


import pytest

from access_token import get_access_token
from esologs.client import Client


@pytest.fixture(scope="session")
def api_credentials():
    """Get API credentials for sanity tests."""
    return {
        "endpoint": "https://www.esologs.com/api/v2/client",
        "access_token": get_access_token(),
    }


@pytest.fixture(scope="session")
def test_data():
    """Shared test data for sanity tests."""
    return {
        "character_id": 34663,
        "guild_id": 3660,
        "report_code": "VfxqaX47HGC98rAp",
        "encounter_id": 27,
        "zone_id": 8,
        "ability_id": 1084,
        "item_id": 19,
        "item_set_id": 19,
        "class_id": 1,
        "map_id": 1,
        "npc_id": 1,
    }


@pytest.fixture
def client(api_credentials):
    """Create a test client with real API credentials."""
    return Client(
        url=api_credentials["endpoint"],
        headers={"Authorization": f"Bearer {api_credentials['access_token']}"},
    )


@pytest.fixture(scope="module")
def sanity_test_marker():
    """Marker for sanity tests that do comprehensive API validation."""
    return pytest.mark.sanity
