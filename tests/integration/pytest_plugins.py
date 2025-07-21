"""Pytest plugin for automatic retry logic on integration tests."""

import pytest


def pytest_configure(config):
    """Add custom markers for retry configuration."""
    config.addinivalue_line(
        "markers", "no_retry: mark test to disable automatic retry logic"
    )


def pytest_collection_modifyitems(config, items):
    """
    Automatically configure retry for integration tests.

    Uses pytest-rerunfailures to retry tests that fail due to network issues.
    """
    for item in items:
        # Skip if not an integration test
        if "integration" not in item.nodeid:
            continue

        # Skip if explicitly marked with no_retry
        if item.get_closest_marker("no_retry"):
            continue

        # Skip if already has flaky marker (manually configured)
        if item.get_closest_marker("flaky"):
            continue

        # Add flaky marker for automatic retry on network errors
        # This uses pytest-rerunfailures functionality
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
