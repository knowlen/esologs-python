"""Factory functions for creating ESO Logs clients with custom configurations."""

from typing import Any, Optional

import httpx

from esologs.auth import get_access_token
from esologs.client import Client


def create_client_with_timeout(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    timeout: float = 30.0,
    **kwargs: Any,
) -> Client:
    """
    Create an ESO Logs client with custom timeout configuration.

    Args:
        client_id: OAuth client ID (can also be set via ESOLOGS_ID env var)
        client_secret: OAuth client secret (can also be set via ESOLOGS_SECRET env var)
        timeout: Request timeout in seconds (default: 30.0)
        **kwargs: Additional arguments passed to Client constructor

    Returns:
        Configured Client instance with custom timeout
    """
    # Get access token
    access_token = get_access_token(client_id=client_id, client_secret=client_secret)

    # Create httpx client with custom timeout
    http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            timeout=timeout,
            connect=10.0,  # Connection timeout
            read=timeout,  # Read timeout
            write=10.0,  # Write timeout
            pool=5.0,  # Pool timeout
        ),
        limits=httpx.Limits(
            max_connections=100,
            max_keepalive_connections=20,
            keepalive_expiry=30.0,
        ),
    )

    # Set up headers
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {access_token}"

    # Create client with custom http_client
    return Client(
        url=kwargs.pop("url", "https://www.esologs.com/api/v2/client"),
        headers=headers,
        http_client=http_client,
        **kwargs,
    )


def create_resilient_client(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    timeout: float = 60.0,
    max_retries: int = 3,
    **kwargs: Any,
) -> Client:
    """
    Create an ESO Logs client with enhanced resilience features.

    This client is configured with:
    - Longer timeouts for slow API responses
    - Connection pooling for better performance
    - Retry logic via transport adapter

    Args:
        client_id: OAuth client ID (can also be set via ESOLOGS_ID env var)
        client_secret: OAuth client secret (can also be set via ESOLOGS_SECRET env var)
        timeout: Request timeout in seconds (default: 60.0)
        max_retries: Maximum number of retries (default: 3)
        **kwargs: Additional arguments passed to Client constructor

    Returns:
        Configured Client instance with resilience features
    """
    # Get access token
    access_token = get_access_token(client_id=client_id, client_secret=client_secret)

    # Create transport with retry logic
    transport = httpx.AsyncHTTPTransport(
        retries=max_retries,
        limits=httpx.Limits(
            max_connections=100,
            max_keepalive_connections=20,
            keepalive_expiry=30.0,
        ),
    )

    # Create httpx client with custom configuration
    http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            timeout=timeout,
            connect=15.0,  # Longer connection timeout
            read=timeout,  # Read timeout
            write=15.0,  # Write timeout
            pool=10.0,  # Pool timeout
        ),
        transport=transport,
        follow_redirects=True,
    )

    # Set up headers
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {access_token}"

    # Create client
    return Client(
        url=kwargs.pop("url", "https://www.esologs.com/api/v2/client"),
        headers=headers,
        http_client=http_client,
        **kwargs,
    )
