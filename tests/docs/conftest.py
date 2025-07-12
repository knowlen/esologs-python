"""Shared test configuration for documentation tests."""

import pytest
import os
from access_token import get_access_token


@pytest.fixture(scope="session")
def api_credentials():
    """Ensure API credentials are available."""
    client_id = os.environ.get("ESOLOGS_ID")
    client_secret = os.environ.get("ESOLOGS_SECRET")
    
    if not client_id or not client_secret:
        pytest.skip("ESO Logs API credentials not available in environment")
    
    return {"client_id": client_id, "client_secret": client_secret}


@pytest.fixture(scope="session")
def access_token(api_credentials):
    """Get access token for API calls."""
    try:
        token = get_access_token()
        return token
    except Exception as e:
        pytest.skip(f"Could not obtain access token: {e}")


@pytest.fixture
def api_client_config(access_token):
    """Standard client configuration for tests."""
    return {
        "url": "https://www.esologs.com/api/v2/client",
        "headers": {"Authorization": f"Bearer {access_token}"}
    }


# Test data fixtures
@pytest.fixture
def test_character_id():
    """Test character ID from documentation examples."""
    return 12345


@pytest.fixture
def test_guild_id():
    """Test guild ID from documentation examples."""
    return 123


@pytest.fixture
def test_zone_id():
    """Test zone ID from documentation examples."""
    return 456