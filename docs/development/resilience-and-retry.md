# Resilience and Retry Patterns

This guide covers best practices for handling transient failures when working with the ESO Logs API.

## Overview

Network requests to external APIs can fail for various reasons:
- Temporary network issues
- API rate limiting
- Server-side timeouts
- Connection drops

The esologs-python library provides several mechanisms to handle these failures gracefully.

## Client Configuration

### Using the Resilient Client Factory

The easiest way to create a client with enhanced resilience is using the factory function:

```python
from esologs.client_factory import create_resilient_client

# Create a client with longer timeouts and retry logic
client = create_resilient_client(
    timeout=60.0,      # 60 second timeout
    max_retries=3,     # Retry failed requests up to 3 times
)

# Use the client normally
async with client:
    guilds = await client.get_guilds(limit=10)
```

### Custom Timeout Configuration

For more control over timeouts:

```python
from esologs.client_factory import create_client_with_timeout

# Create a client with custom timeout
client = create_client_with_timeout(
    timeout=30.0,  # 30 second timeout for all requests
)
```

### Manual httpx Client Configuration

For complete control:

```python
import httpx
from esologs.client import Client
from esologs.auth import get_access_token

# Create custom httpx client
http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(
        timeout=45.0,
        connect=10.0,
        read=45.0,
        write=10.0,
        pool=5.0,
    ),
    limits=httpx.Limits(
        max_connections=100,
        max_keepalive_connections=20,
    ),
)

# Create ESO Logs client with custom httpx client
client = Client(
    url="https://www.esologs.com/api/v2/client",
    headers={"Authorization": f"Bearer {get_access_token()}"},
    http_client=http_client,
)
```

## Retry Patterns

### Basic Retry with Exponential Backoff

```python
import asyncio
from typing import TypeVar, Callable, Any

T = TypeVar('T')

async def retry_with_backoff(
    func: Callable[..., T],
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    *args: Any,
    **kwargs: Any
) -> T:
    """Execute a function with retry logic and exponential backoff."""
    last_exception = None
    delay = initial_delay

    for attempt in range(max_attempts):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < max_attempts - 1:
                await asyncio.sleep(delay)
                delay *= 2  # Exponential backoff

    raise last_exception

# Usage
async def main():
    client = create_resilient_client()

    async with client:
        # Retry getting guild data
        guild = await retry_with_backoff(
            client.get_guild_by_id,
            max_attempts=3,
            guild_id=3468
        )
```

### Selective Exception Retry

Only retry on specific exceptions:

```python
import httpx

async def retry_on_timeout(func, *args, **kwargs):
    """Retry only on timeout errors."""
    for attempt in range(3):
        try:
            return await func(*args, **kwargs)
        except (httpx.ConnectTimeout, httpx.ReadTimeout) as e:
            if attempt == 2:  # Last attempt
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## Integration Testing with Retry

For integration tests, the library provides automatic retry logic:

```python
# tests/integration/test_example.py
import pytest
from esologs.client import Client

class TestIntegration:
    @pytest.mark.asyncio
    async def test_guild_data(self, client):
        """This test will automatically retry on network failures."""
        async with client:
            guild = await client.get_guild_by_id(guild_id=3468)
            assert guild.guild_data.guild is not None

    @pytest.mark.asyncio
    @pytest.mark.retry(max_attempts=5, initial_delay=2.0)
    async def test_large_data_fetch(self, client):
        """Custom retry configuration for specific test."""
        async with client:
            reports = await client.search_reports(limit=100)
            assert len(reports.report_data.reports.data) > 0

    @pytest.mark.asyncio
    @pytest.mark.no_retry
    async def test_quick_operation(self, client):
        """Disable automatic retry for this test."""
        async with client:
            ability = await client.get_ability(id=1)
            assert ability is not None
```

## Best Practices

### 1. Use Appropriate Timeouts

Different operations may need different timeouts:

```python
# Quick lookup - shorter timeout
client = create_client_with_timeout(timeout=15.0)
ability = await client.get_ability(id=123)

# Complex search - longer timeout
client = create_client_with_timeout(timeout=60.0)
reports = await client.search_reports(
    guild_id=3468,
    start_time=start,
    end_time=end,
    limit=100
)
```

### 2. Handle Rate Limiting

Respect API rate limits with delays:

```python
async def fetch_guild_reports(guild_ids: list[int]):
    """Fetch reports for multiple guilds with rate limit awareness."""
    client = create_resilient_client()
    reports = []

    async with client:
        for guild_id in guild_ids:
            try:
                guild_reports = await client.get_guild_reports(
                    guild_id=guild_id,
                    limit=10
                )
                reports.append(guild_reports)

                # Delay between requests to avoid rate limiting
                await asyncio.sleep(0.5)

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Rate limited
                    # Wait longer and retry
                    await asyncio.sleep(5.0)
                    guild_reports = await client.get_guild_reports(
                        guild_id=guild_id,
                        limit=10
                    )
                    reports.append(guild_reports)
                else:
                    raise

    return reports
```

### 3. Circuit Breaker Pattern

For production applications, consider implementing a circuit breaker:

```python
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def call(self, func, *args, **kwargs):
        if self.is_open:
            if datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                self.is_open = False
                self.failure_count = 0
            else:
                raise Exception("Circuit breaker is open")

        try:
            result = func(*args, **kwargs)
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.failure_threshold:
                self.is_open = True

            raise
```

### 4. Graceful Degradation

Design your application to handle API failures gracefully:

```python
async def get_guild_info_with_fallback(guild_id: int) -> dict:
    """Get guild info with fallback to cached data."""
    client = create_resilient_client()

    try:
        async with client:
            guild = await client.get_guild_by_id(guild_id=guild_id)
            if guild.guild_data.guild:
                # Cache the successful response
                cache_guild_data(guild_id, guild.guild_data.guild)
                return guild.guild_data.guild.dict()
    except Exception as e:
        logger.warning(f"Failed to fetch guild {guild_id}: {e}")

        # Fall back to cached data
        cached_data = get_cached_guild_data(guild_id)
        if cached_data:
            return cached_data

        # Return minimal data if no cache
        return {
            "id": guild_id,
            "name": "Unknown",
            "error": "Failed to fetch guild data"
        }
```

## Monitoring and Logging

Always log retry attempts and failures:

```python
import logging

logger = logging.getLogger(__name__)

async def monitored_api_call(client, method_name: str, **kwargs):
    """Make an API call with monitoring and logging."""
    start_time = asyncio.get_event_loop().time()
    attempt = 0

    while attempt < 3:
        try:
            method = getattr(client, method_name)
            result = await method(**kwargs)

            # Log successful call
            duration = asyncio.get_event_loop().time() - start_time
            logger.info(
                f"API call {method_name} succeeded",
                extra={
                    "method": method_name,
                    "attempt": attempt + 1,
                    "duration": duration,
                    "kwargs": kwargs,
                }
            )
            return result

        except Exception as e:
            attempt += 1
            logger.warning(
                f"API call {method_name} failed (attempt {attempt}/3)",
                extra={
                    "method": method_name,
                    "attempt": attempt,
                    "error": str(e),
                    "kwargs": kwargs,
                },
                exc_info=True
            )

            if attempt < 3:
                await asyncio.sleep(2 ** attempt)
            else:
                raise
```

## Summary

Key takeaways for building resilient ESO Logs API integrations:

1. **Configure appropriate timeouts** based on the operation type
2. **Implement retry logic** with exponential backoff
3. **Handle rate limiting** gracefully with delays
4. **Use circuit breakers** for production applications
5. **Implement fallbacks** for critical functionality
6. **Monitor and log** all API interactions

By following these patterns, your application will be more resilient to transient failures and provide a better user experience.
