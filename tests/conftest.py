"""Root test configuration for all test suites."""

import pytest

# Register the retry plugin - this applies to all test suites
pytest_plugins = ["tests.integration.pytest_plugins"]


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test requiring real API calls"
    )
    config.addinivalue_line(
        "markers", "no_retry: mark test to disable automatic retry logic"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to handle markers and apply retry logic.

    This ensures retry logic is applied to both integration and docs tests.
    """
    for item in items:
        # Add integration marker for tests in integration directory
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)

        # Apply retry logic to both integration and docs tests that make API calls
        if "integration" in item.nodeid or "docs" in item.nodeid:
            # Skip if explicitly marked with no_retry
            if item.get_closest_marker("no_retry"):
                continue

            # Skip if already has flaky marker (manually configured)
            if item.get_closest_marker("flaky"):
                continue

            # Add flaky marker for automatic retry on network errors
            item.add_marker(
                pytest.mark.flaky(
                    reruns=3,
                    reruns_delay=2,
                    only_rerun=(
                        "httpx.ConnectTimeout",
                        "httpx.ReadTimeout",
                        "httpx.ConnectError",
                        "httpx.NetworkError",
                        "httpx.RemoteProtocolError",
                        "ConnectionError",
                        "TimeoutError",
                        "OSError",
                    ),
                )
            )
