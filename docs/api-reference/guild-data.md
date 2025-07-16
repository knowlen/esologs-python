# Guild Data

Enables the retrieval of single guilds or filtered collections of guilds. Guild information, member lists, and guild performance data.

## Overview

- **Coverage**: 2 direct endpoints + guild filtering in search
- **Use Cases**: Guild management, member tracking, guild performance analysis
- **Rate Limit Impact**: 2-4 points per request (varies by complexity)

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


### get_guild_reports()

**Purpose**: Get paginated reports for a specific guild (convenience method)

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `guild_id` | *int* | Yes | The guild ID to search for |
| `limit` | *int \| None* | No | Number of reports per page (1-25, default 16) |
| `page` | *int \| None* | No | Page number (default 1) |
| `start_time` | *float \| None* | No | Start time filter (UNIX timestamp with milliseconds) |
| `end_time` | *float \| None* | No | End time filter (UNIX timestamp with milliseconds) |
| `zone_id` | *int \| None* | No | Filter by specific zone |

**Returns**: `GetReports` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `report_data.reports.data` | *List[Report]* | List of report objects |
| `report_data.reports.total` | *int* | Total number of reports |
| `report_data.reports.per_page` | *int* | Number of reports per page |
| `report_data.reports.current_page` | *int* | Current page number |
| `report_data.reports.has_more_pages` | *bool* | Whether more pages are available |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_guild_reports():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get recent reports for guild
        reports = await client.get_guild_reports(guild_id=3468, limit=5)
        print(f"Found {len(reports.report_data.reports.data)} reports")

        # Show report details
        for report in reports.report_data.reports.data:
            print(f"- {report.title} ({report.code})")
            print(f"  Guild: {report.guild.name}")

asyncio.run(get_guild_reports())
```

**Output**:
```
Found 5 reports
- vLC HM attempt 7-12-25 (2GqxNpHnQVLDfyak)
  Guild: The Shadow Court
- Saturday Training (1A2B3C4D5E6F7G8H)
  Guild: The Shadow Court
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

### Guild Performance Analysis

Track guild performance over time:

```python
import asyncio
from datetime import datetime, timedelta
from esologs.client import Client
from esologs.auth import get_access_token

async def analyze_guild_performance():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get guild info
        guild = await client.get_guild_by_id(guild_id=1583)
        print(f"Analyzing guild: {guild.guild_data.guild.name}")

        # Get reports from last 30 days
        end_time = datetime.now().timestamp() * 1000
        start_time = (datetime.now() - timedelta(days=30)).timestamp() * 1000

        reports = await client.get_guild_reports(
            guild_id=1583,
            start_time=start_time,
            end_time=end_time,
            limit=25
        )

        print(f"Reports in last 30 days: {len(reports.report_data.reports.data)}")

        # Analyze by zone
        zones = {}
        for report in reports.report_data.reports.data:
            if hasattr(report, 'zone') and report.zone:
                zone_name = report.zone.name
                zones[zone_name] = zones.get(zone_name, 0) + 1

        print("Activity by zone:")
        for zone, count in sorted(zones.items(), key=lambda x: x[1], reverse=True):
            print(f"  {zone}: {count} reports")

asyncio.run(analyze_guild_performance())
```

**Output**:
```
Analyzing guild: Entropy Rising
Reports in last 30 days: 12
Activity by zone:
  Veteran Maw of Lorkhaj: 5 reports
  Veteran Cloudrest: 3 reports
  Veteran Sunspire: 2 reports
  Veteran Kyne's Aegis: 2 reports
```

### Guild Member Activity Tracking

Monitor guild member participation using report rankings data:

```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def track_member_activity():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get recent guild reports
        reports = await client.get_guild_reports(guild_id=1583, limit=5)

        # Collect unique participants across reports
        all_members = {}

        for report in reports.report_data.reports.data:
            print(f"\nReport: {report.title}")

            # Get report rankings to see participant details
            rankings = await client.get_report_rankings(code=report.code)

            if rankings.report_data and rankings.report_data.report.rankings:
                fights = rankings.report_data.report.rankings['data']

                # Process first fight to get participants
                if fights:
                    fight = fights[0]
                    roles = fight.get('roles', {})

                    # Extract members from all roles
                    for role_name, role_data in roles.items():
                        if 'characters' in role_data:
                            for char in role_data['characters']:
                                char_name = char['name']
                                char_class = char['class']
                                char_spec = char['spec']

                                # Track member participation
                                if char_name not in all_members:
                                    all_members[char_name] = {
                                        'class': char_class,
                                        'spec': char_spec,
                                        'reports': []
                                    }
                                all_members[char_name]['reports'].append(report.title)

                                print(f"  - {char_name} ({char_class} {char_spec})")

            # Add delay for rate limiting
            await asyncio.sleep(0.2)

        # Summary of most active members
        print(f"\n=== Guild Activity Summary ===")
        print(f"Total unique members: {len(all_members)}")

        # Sort by participation count
        sorted_members = sorted(all_members.items(),
                              key=lambda x: len(x[1]['reports']),
                              reverse=True)

        print("\nMost active members:")
        for name, data in sorted_members[:5]:
            report_count = len(data['reports'])
            print(f"  {name}: {report_count} reports ({data['class']} {data['spec']})")

asyncio.run(track_member_activity())
```

**Output**:
```

Report: vMoL HM Progress - 7/13/25
  - Rosenwynn (DragonKnight Tank)
  - Korwyn Sky (Warden Healer)
  - Elara Stormhaven (DragonKnight MagickaDPS)
  - Vera Caisser (Arcanist StaminaDPS)
  - R-can-ist (Arcanist StaminaDPS)

Report: Cloudrest Clear - 7/12/25
  - Rosenwynn (DragonKnight Tank)
  - A Kat Has No Name (Nightblade Healer)
  - Guzica Klovn (Necromancer MagickaDPS)
  - Unleash The Beam (Arcanist StaminaDPS)

=== Guild Activity Summary ===
Total unique members: 12
Most active members:
  Rosenwynn: 5 reports (DragonKnight Tank)
  Vera Caisser: 4 reports (Arcanist StaminaDPS)
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
from esologs.validators import validate_positive_integer, validate_limit_parameter
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
            limit = 25
            validate_positive_integer(guild_id, "guild_id")
            validate_limit_parameter(limit)

            reports = await client.get_guild_reports(guild_id=guild_id, limit=limit)
            print(f"Successfully retrieved {len(reports.report_data.reports.data)} reports")

        except GraphQLClientGraphQLMultiError as e:
            print(f"GraphQL error: {e}")
        except ValidationError as e:
            print(f"Invalid parameters: {e}")
        except GraphQLClientHttpError as e:
            if e.status_code == 403:
                print("Access to guild reports denied")
            elif e.status_code == 429:
                print("Rate limit exceeded")

asyncio.run(validate_guild_parameters())
```

**Output**:
```
Successfully retrieved 5 reports
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
