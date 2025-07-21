"""Integration test configuration and shared fixtures."""


import pytest

from esologs.auth import get_access_token
from esologs.client import Client

from .retry_utils import RetryClient

# Register the retry plugin
pytest_plugins = ["tests.integration.pytest_plugins"]


@pytest.fixture(scope="session")
def api_credentials():
    """Get API credentials for integration tests."""
    return {
        "endpoint": "https://www.esologs.com/api/v2/client",
        "access_token": get_access_token(),
    }


@pytest.fixture(scope="session")
def test_data():
    """Shared test data for integration tests."""
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


@pytest.fixture
def integration_test_marker():
    """Marker for integration tests that require real API calls."""
    return pytest.mark.integration


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test requiring real API calls"
    )
    # Configure pytest-rerunfailures for integration tests
    config.option.reruns = 3
    config.option.reruns_delay = 2


def pytest_collection_modifyitems(config, items):
    """Modify test collection to handle integration test markers."""
    for item in items:
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)


@pytest.fixture(autouse=True)
def check_credentials():
    """Ensure API credentials are available for integration tests."""
    try:
        access_token = get_access_token()
        if not access_token:
            pytest.skip("No API credentials available for integration tests")
    except Exception as e:
        pytest.skip(f"Failed to get API credentials: {e}")


@pytest.fixture
def slow_test_marker():
    """Marker for slow integration tests."""
    return pytest.mark.slow


@pytest.fixture
def api_client_config(api_credentials):
    """Configuration for creating API client instances."""
    return {
        "url": api_credentials["endpoint"],
        "headers": {"Authorization": f"Bearer {api_credentials['access_token']}"},
    }


@pytest.fixture
def retry_client(api_credentials):
    """Create a test client with retry logic for handling transient failures."""
    base_client = Client(
        url=api_credentials["endpoint"],
        headers={"Authorization": f"Bearer {api_credentials['access_token']}"},
    )
    return RetryClient(
        base_client,
        max_attempts=3,
        initial_delay=2.0,
        backoff_factor=2.0,
        max_delay=10.0,
    )
