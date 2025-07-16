# System Endpoints

Monitor API usage, handle rate limits, and manage authentication.

## Overview

- **Coverage**: Core system endpoints for monitoring and management
- **Use Cases**: Rate limit monitoring, authentication validation, error handling
- **Rate Limit Impact**: 1 point per request

## Methods

### get_rate_limit_data()

**Purpose**: Monitor your current API usage and rate limit status

**Parameters**: None

**Returns**: `GetRateLimitData` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `rate_limit_data.points_spent_this_hour` | *float* | Points consumed in current hour |
| `rate_limit_data.limit_per_hour` | *int* | Maximum points allowed per hour (18000) |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def check_rate_limits():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Check current rate limit status
        rate_limit = await client.get_rate_limit_data()

        print(f"Points used this hour: {rate_limit.rate_limit_data.points_spent_this_hour}")
        print(f"Points remaining: {18000 - rate_limit.rate_limit_data.points_spent_this_hour}")
        print(f"Limit per hour: {rate_limit.rate_limit_data.limit_per_hour}")

asyncio.run(check_rate_limits())
```

**Output**:
```
Points used this hour: 371.8
Points remaining: 17628.2
Limit per hour: 18000
```

## Error Handling Patterns

### Authentication Errors

Handle authentication failures and token expiration:

```python
import asyncio
from esologs.client import Client
from esologs.exceptions import GraphQLClientHttpError
from esologs.auth import get_access_token

async def handle_auth_errors():
    try:
        token = get_access_token()
        async with Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": f"Bearer {token}"}
        ) as client:

            # Try to access protected resource
            rate_limit = await client.get_rate_limit_data()
            print("✅ Authentication successful")

    except GraphQLClientHttpError as e:
        if e.status_code == 401:
            print("❌ Authentication failed: Invalid or expired token")
            print("Please check your ESOLOGS_ID and ESOLOGS_SECRET")
        elif e.status_code == 403:
            print("❌ Access forbidden: Insufficient permissions")
        else:
            print(f"❌ HTTP error {e.status_code}: {e}")

asyncio.run(handle_auth_errors())
```

**Output** (success case):
```
✅ Authentication successful
```

**Output** (auth error case):
```
❌ Authentication failed: Invalid or expired token
Please check your ESOLOGS_ID and ESOLOGS_SECRET
```

### Rate Limit Errors

Handle rate limit exceeded scenarios:

```python
import asyncio
from esologs.client import Client
from esologs.exceptions import GraphQLClientHttpError
from esologs.auth import get_access_token

async def handle_rate_limits():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        try:
            # Example: Make multiple requests that might hit rate limit
            for i in range(5):
                abilities = await client.get_abilities(limit=100)
                print(f"Request {i+1}: Got {len(abilities.game_data.abilities.data)} abilities")

                # Check rate limit status
                rate_limit = await client.get_rate_limit_data()
                remaining = 18000 - rate_limit.rate_limit_data.points_spent_this_hour
                print(f"Points remaining: {remaining}")

                if remaining < 10:
                    print("⚠️ Low on rate limit points, slowing down...")
                    await asyncio.sleep(2)

        except GraphQLClientHttpError as e:
            if e.status_code == 429:
                print("❌ Rate limit exceeded. Wait before making more requests.")
                # Could implement exponential backoff here
            else:
                print(f"❌ Unexpected HTTP error: {e}")

asyncio.run(handle_rate_limits())
```

### GraphQL Errors

Handle GraphQL-specific errors from the API:

```python
import asyncio
from esologs.client import Client
from esologs.exceptions import GraphQLClientGraphQLError, GraphQLClientGraphQLMultiError
from pydantic import ValidationError
from esologs.auth import get_access_token

async def handle_graphql_errors():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        try:
            # This might cause a GraphQL validation error
            abilities = await client.get_abilities(limit=200)  # Exceeds max limit

        except GraphQLClientGraphQLMultiError as e:
            print(f"❌ GraphQL validation errors: {e}")
            # Multiple GraphQL errors returned together

        except GraphQLClientGraphQLError as e:
            print(f"❌ GraphQL error: {e.message}")
            # Single GraphQL error

        except ValidationError as e:
            print(f"❌ Client-side validation error: {e}")
            # Pydantic validation before sending request

asyncio.run(handle_graphql_errors())
```

### Network and Connection Errors

Handle network connectivity issues:

```python
import asyncio
import httpx
from esologs.client import Client
from esologs.exceptions import GraphQLClientHttpError
from esologs.auth import get_access_token

async def handle_network_errors():
    token = get_access_token()

    try:
        async with Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": f"Bearer {token}"}
        ) as client:

            rate_limit = await client.get_rate_limit_data()
            print("✅ Connection successful")

    except httpx.TimeoutException:
        print("❌ Request timed out - check network connection")

    except httpx.ConnectError:
        print("❌ Connection failed - check network and API endpoint")

    except GraphQLClientHttpError as e:
        if e.status_code >= 500:
            print(f"❌ Server error {e.status_code} - API temporarily unavailable")
        else:
            print(f"❌ Client error {e.status_code}: {e}")

asyncio.run(handle_network_errors())
```

## Common Patterns

### Rate Limit Monitoring

Monitor your usage throughout a session:

```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

class RateLimitMonitor:
    def __init__(self, client):
        self.client = client
        self.initial_usage = None

    async def start_monitoring(self):
        """Record initial usage"""
        rate_limit = await self.client.get_rate_limit_data()
        self.initial_usage = rate_limit.rate_limit_data.points_spent_this_hour
        print(f"📊 Starting usage: {self.initial_usage}/18000 points")

    async def check_usage(self, operation_name="operation"):
        """Check current usage and calculate points consumed"""
        rate_limit = await self.client.get_rate_limit_data()
        current_usage = rate_limit.rate_limit_data.points_spent_this_hour

        if self.initial_usage is not None:
            consumed = current_usage - self.initial_usage
            print(f"📊 After {operation_name}: {current_usage}/18000 points (+{consumed})")

        remaining = 18000 - current_usage
        if remaining < 100:
            print("⚠️ WARNING: Low on rate limit points!")

        return remaining

async def monitored_session():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        monitor = RateLimitMonitor(client)
        await monitor.start_monitoring()

        # Perform operations with monitoring
        abilities = await client.get_abilities(limit=50)
        await monitor.check_usage("get_abilities")

        classes = await client.get_classes()
        await monitor.check_usage("get_classes")

        items = await client.get_items(limit=25)
        await monitor.check_usage("get_items")

asyncio.run(monitored_session())
```

**Output**:
```
📊 Starting usage: 371.8/18000 points
📊 After get_abilities: 373.8/18000 points (+2.0)
📊 After get_classes: 374.8/18000 points (+1.0)
📊 After get_items: 376.8/18000 points (+2.0)
```

### Robust Error Recovery

Implement retry logic with exponential backoff:

```python
import asyncio
import random
from esologs.client import Client
from esologs.exceptions import GraphQLClientHttpError
from esologs.auth import get_access_token

async def robust_api_call(client, operation, max_retries=3):
    """
    Execute an API operation with retry logic and exponential backoff
    """
    for attempt in range(max_retries):
        try:
            result = await operation()
            return result

        except GraphQLClientHttpError as e:
            if e.status_code == 429:  # Rate limit
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"⏳ Rate limited, waiting {wait_time:.1f}s before retry {attempt + 1}/{max_retries}")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    print("❌ Max retries exceeded for rate limit")
                    raise

            elif e.status_code >= 500:  # Server error
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"⏳ Server error, waiting {wait_time:.1f}s before retry {attempt + 1}/{max_retries}")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    print("❌ Max retries exceeded for server error")
                    raise
            else:
                # Don't retry client errors (4xx except 429)
                raise

async def reliable_data_fetch():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Use robust wrapper for API calls
        abilities = await robust_api_call(
            client,
            lambda: client.get_abilities(limit=50)
        )
        print(f"✅ Successfully fetched {len(abilities.game_data.abilities.data)} abilities")

        classes = await robust_api_call(
            client,
            lambda: client.get_classes()
        )
        print(f"✅ Successfully fetched {len(classes.game_data.classes)} classes")

asyncio.run(reliable_data_fetch())
```

**Output**:
```
✅ Successfully fetched 50 abilities
✅ Successfully fetched 7 classes
```

### Session Management

Manage long-running sessions with periodic health checks:

```python
import asyncio
from esologs.client import Client
from esologs.exceptions import GraphQLClientHttpError
from esologs.auth import get_access_token

class APISession:
    def __init__(self):
        self.client = None
        self.is_healthy = False

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def start(self):
        """Initialize and validate the session"""
        token = get_access_token()
        self.client = Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": f"Bearer {token}"}
        )
        await self.client.__aenter__()

        # Validate session with a simple call
        await self.health_check()

    async def health_check(self):
        """Check if the session is still valid"""
        try:
            await self.client.get_rate_limit_data()
            self.is_healthy = True
            print("✅ Session healthy")
        except GraphQLClientHttpError as e:
            self.is_healthy = False
            if e.status_code == 401:
                print("❌ Session expired - authentication failed")
            else:
                print(f"❌ Session unhealthy - HTTP {e.status_code}")
            raise

    async def close(self):
        """Clean up the session"""
        if self.client:
            await self.client.__aexit__(None, None, None)
            print("🔒 Session closed")

async def long_running_session():
    async with APISession() as session:

        # Perform operations
        for i in range(3):
            print(f"\n--- Operation {i+1} ---")

            # Periodic health check
            if i > 0:
                await session.health_check()

            # Do actual work
            abilities = await session.client.get_abilities(limit=10)
            print(f"Fetched {len(abilities.game_data.abilities.data)} abilities")

            # Small delay between operations
            await asyncio.sleep(1)

asyncio.run(long_running_session())
```

**Output**:
```
✅ Session healthy

--- Operation 1 ---
Fetched 10 abilities

--- Operation 2 ---
✅ Session healthy
Fetched 10 abilities

--- Operation 3 ---
✅ Session healthy
Fetched 10 abilities
🔒 Session closed
```

## Rate Limiting

### Understanding Point Consumption

Different endpoints consume different amounts of your 18,000 points per hour:

- **Simple endpoints**: 1-2 points (get_classes, get_factions, get_rate_limit_data)
- **Paginated endpoints**: 1-3 points (get_abilities, get_items, get_npcs, get_maps)
- **Individual lookups**: 1-2 points (get_ability, get_item, get_npc, get_map)
- **Character data**: 2-5 points (get_character_by_id, get_character_reports)
- **Report analysis**: 3-10 points (get_report_events, get_report_table)
- **Search operations**: 5-15 points (search_reports with complex filters)

### Rate Limit Best Practices

1. **Monitor Usage**: Always check your rate limit status regularly
2. **Batch Requests**: Use pagination to get more data per request
3. **Cache Results**: Store frequently accessed data locally
4. **Add Delays**: Space out requests to avoid bursts that trigger limits
5. **Handle 429 Errors**: Implement proper retry logic with exponential backoff

**Optimal Request Pacing**:
```python
# For bulk operations, aim for ~2-3 requests per second
async def paced_requests():
    for item in large_item_list:
        result = await client.get_item(id=item)
        await asyncio.sleep(0.3)  # 300ms between requests
```

**Rate Limit Headers** (if available):
- Check response headers for `X-RateLimit-Remaining`
- Monitor `X-RateLimit-Reset` for when limits refresh
- Adjust request frequency based on remaining quota
