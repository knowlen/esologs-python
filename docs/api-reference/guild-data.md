# Guild Data

Enables the retrieval of single guilds or filtered collections of guilds. Guild information, member lists, and guild performance data.

## Overview

- **Coverage**: 1 direct endpoint + guild filtering in search
- **Use Cases**: Guild information retrieval, guild identification
- **Rate Limit Impact**: 2 points per request

## Methods

### get_guild_by_id()

**Purpose**: Retrieve detailed guild information by guild ID

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `guild_id` | *int* | Yes | The guild ID to retrieve |

**Returns**: `GetGuildById` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `guild_data.guild.id` | *int* | Guild ID |
| `guild_data.guild.name` | *str* | Guild name |
| `guild_data.guild.description` | *str* | Guild description (may be empty) |
| `guild_data.guild.faction.name` | *str* | Guild faction name |
| `guild_data.guild.server.name` | *str* | Server name |
| `guild_data.guild.server.region.name` | *str* | Server region name |
| `guild_data.guild.tags` | *List[Tag] \| None* | Guild tags/teams (may be empty) |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_guild_info():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        guild = await client.get_guild_by_id(guild_id=3468)
        print(f"Guild: {guild.guild_data.guild.name}")
        print(f"Faction: {guild.guild_data.guild.faction.name}")
        print(f"Server: {guild.guild_data.guild.server.name}")
        print(f"Region: {guild.guild_data.guild.server.region.name}")

asyncio.run(get_guild_info())
```

**Output**:
```
Guild: The Shadow Court
Faction: The Aldmeri Dominion
Server: Megaserver
Region: North America
```


## Guild Filtering in Search Methods

Guild-related filtering is also available in the main search methods:

### search_reports() with Guild Filters

**Guild-specific parameters**:

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `guild_id` | *int \| None* | No | Filter by specific guild ID |
| `guild_name` | *str \| None* | No | Filter by guild name (requires guild_server_slug and guild_server_region) |
| `guild_server_slug` | *str \| None* | No | Guild server slug (required with guild_name) |
| `guild_server_region` | *str \| None* | No | Guild server region (required with guild_name) |
| `guild_tag_id` | *int \| None* | No | Filter by guild tag/team ID |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def search_guild_reports():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Search by guild ID (most common)
        reports = await client.search_reports(guild_id=3468, limit=10)
        print(f"Found {len(reports.report_data.reports.data)} reports")

        # Search by guild name (requires server info)
        reports = await client.search_reports(
            guild_name="The Shadow Court",
            guild_server_slug="megaserver",
            guild_server_region="NA",
            limit=5
        )

asyncio.run(search_guild_reports())
```

**Output**:
```
Found 10 reports
```

## Common Usage Patterns

### Guild Information Retrieval

Retrieve basic guild information:

```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_guild_details():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get guild info
        guild = await client.get_guild_by_id(guild_id=1583)

        print(f"Guild: {guild.guild_data.guild.name}")
        print(f"Faction: {guild.guild_data.guild.faction.name}")
        print(f"Server: {guild.guild_data.guild.server.name}")
        print(f"Region: {guild.guild_data.guild.server.region.name}")

        # Description may be empty
        if guild.guild_data.guild.description:
            print(f"Description: {guild.guild_data.guild.description}")

asyncio.run(get_guild_details())
```

**Output**:
```
Guild: Entropy Rising
Faction: Daggerfall Covenant
Server: Megaserver
Region: North America
```
  Korwyn Sky: 3 reports (Warden Healer)
  R-can-ist: 3 reports (Arcanist StaminaDPS)
  Elara Stormhaven: 2 reports (DragonKnight MagickaDPS)
```

## Error Handling

Guild data API methods have specific error handling patterns that differ from other endpoints.

### Non-existent Guild IDs

Unlike some APIs that throw exceptions for missing data, guild methods return `None` for non-existent guilds:

```python
from esologs.client import Client
from esologs.auth import get_access_token

async def handle_missing_guild():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        guild = await client.get_guild_by_id(guild_id=999999)  # Non-existent guild

        # Check if guild exists
        if guild.guild_data.guild is None:
            print("Guild not found")
        else:
            print(f"Found guild: {guild.guild_data.guild.name}")

asyncio.run(handle_missing_guild())
```

**Output**:
```
Guild not found
```

### Parameter Validation

```python
from esologs.exceptions import GraphQLClientHttpError, GraphQLClientGraphQLMultiError
from esologs.validators import validate_positive_integer
from pydantic import ValidationError

async def validate_guild_parameters():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        try:
            # Validate parameters before making request
            guild_id = 3468
            validate_positive_integer(guild_id, "guild_id")

            guild = await client.get_guild_by_id(guild_id=guild_id)
            if guild.guild_data.guild:
                print(f"Successfully retrieved guild: {guild.guild_data.guild.name}")
            else:
                print("Guild not found")

        except GraphQLClientGraphQLMultiError as e:
            print(f"GraphQL error: {e}")
        except ValidationError as e:
            print(f"Invalid parameters: {e}")
        except GraphQLClientHttpError as e:
            if e.status_code == 403:
                print("Access denied")
            elif e.status_code == 429:
                print("Rate limit exceeded")

asyncio.run(validate_guild_parameters())
```

**Output**:
```
Successfully retrieved guild: The Shadow Court
```

## Best Practices

- **Always check for None**: Guild data can be `None` for non-existent or private guilds
- **Handle rate limits**: Guild operations can be expensive, especially with historical data
- **Validate parameters**: Use the built-in validators before making API calls
- **Graceful degradation**: Design your application to handle missing guild data


## Rate Limiting Considerations

- Guild data endpoints: 2-4 points per request
- Guild member data might require additional report analysis (higher cost)
- Use pagination and delays for bulk operations: `await asyncio.sleep(0.2)`
- Monitor rate limits when analyzing multiple guild reports

## Privacy and Access Considerations

- Some guild data may be private or restricted
- Handle 403 Forbidden responses gracefully
- Not all guilds may have public reports
- Guild member information may require report-level analysis
- Consider guild privacy settings when building applications
