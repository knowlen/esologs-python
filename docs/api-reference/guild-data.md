# Guild Data API

Access ESO guild information, member lists, and guild performance data through the ESO Logs API.

## Overview

- **Coverage**: 2 direct endpoints + guild filtering in search
- **Use Cases**: Guild management, member tracking, guild performance analysis
- **Rate Limit Impact**: 2-4 points per request (varies by complexity)

## Methods

### get_guild_by_id()

**Purpose**: Retrieve detailed guild information by guild ID

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| guild_id | int | Yes | The guild ID to retrieve |

**Returns**: `GetGuildById` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| guild_data.guild.id | int | Guild ID |
| guild_data.guild.name | str | Guild name |
| guild_data.guild.description | str | Guild description (may be empty) |
| guild_data.guild.faction.name | str | Guild faction name |
| guild_data.guild.server.name | str | Server name |
| guild_data.guild.server.region.name | str | Server region name |
| guild_data.guild.tags | List[Tag] \| None | Guild tags/teams (may be empty) |

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

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

**Error Handling**:
```python
from esologs.exceptions import GraphQLClientHttpError, GraphQLClientGraphQLMultiError
from pydantic import ValidationError

try:
    guild = await client.get_guild_by_id(guild_id=999999)  # Non-existent guild
    
    # Check if guild exists
    if guild.guild_data.guild is None:
        print("Guild not found")
    else:
        print(f"Found guild: {guild.guild_data.guild.name}")
        
except GraphQLClientGraphQLMultiError as e:
    print(f"GraphQL error: {e}")
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except GraphQLClientHttpError as e:
    if e.status_code == 403:
        print("Guild data is private")
    elif e.status_code == 429:
        print("Rate limit exceeded")
```

### get_guild_reports()

**Purpose**: Get paginated reports for a specific guild (convenience method)

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| guild_id | int | Yes | The guild ID to search for |
| limit | int \| None | No | Number of reports per page (1-25, default 16) |
| page | int \| None | No | Page number (default 1) |
| start_time | float \| None | No | Start time filter (UNIX timestamp with milliseconds) |
| end_time | float \| None | No | End time filter (UNIX timestamp with milliseconds) |
| zone_id | int \| None | No | Filter by specific zone |

**Returns**: `GetReports` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| report_data.reports.data | List[Report] | List of report objects |
| report_data.reports.total | int | Total number of reports |
| report_data.reports.per_page | int | Number of reports per page |
| report_data.reports.current_page | int | Current page number |
| report_data.reports.has_more_pages | bool | Whether more pages are available |

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

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

**Error Handling**:
```python
from esologs.exceptions import GraphQLClientHttpError, GraphQLClientGraphQLMultiError
from esologs.validators import validate_positive_integer, validate_limit_parameter

try:
    # Validate parameters before making request
    validate_positive_integer(guild_id, "guild_id")
    validate_limit_parameter(limit)
    
    reports = await client.get_guild_reports(guild_id=guild_id, limit=limit)
except GraphQLClientGraphQLMultiError as e:
    print(f"GraphQL error: {e}")
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except GraphQLClientHttpError as e:
    if e.status_code == 403:
        print("Access to guild reports denied")
```

## Guild Filtering in Search Methods

Guild-related filtering is also available in the main search methods:

### search_reports() with Guild Filters

**Guild-specific parameters**:

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| guild_id | int \| None | No | Filter by specific guild ID |
| guild_name | str \| None | No | Filter by guild name (requires guild_server_slug and guild_server_region) |
| guild_server_slug | str \| None | No | Guild server slug (required with guild_name) |
| guild_server_region | str \| None | No | Guild server region (required with guild_name) |
| guild_tag_id | int \| None | No | Filter by guild tag/team ID |

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

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

## Common Usage Patterns

### Guild Performance Analysis

Track guild performance over time:

```python
import asyncio
from datetime import datetime, timedelta
from esologs.client import Client
from access_token import get_access_token

async def analyze_guild_performance():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Get guild info
        guild = await client.get_guild_by_id(guild_id=3468)
        print(f"Analyzing guild: {guild.guild_data.guild.name}")
        
        # Get reports from last 30 days
        end_time = datetime.now().timestamp() * 1000
        start_time = (datetime.now() - timedelta(days=30)).timestamp() * 1000
        
        reports = await client.get_guild_reports(
            guild_id=3468,
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

### Guild Member Activity Tracking

Monitor guild member participation:

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def track_member_activity():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Get recent guild reports
        reports = await client.get_guild_reports(guild_id=3468, limit=20)
        
        # Collect unique participants across reports
        members = set()
        for report in reports.report_data.reports.data:
            # Get detailed report data to see participants
            report_details = await client.get_report_by_code(code=report.code)
            if report_details.report_data and report_details.report_data.report:
                # Note: This example shows the pattern - actual member extraction
                # would depend on the specific report structure
                print(f"Report: {report.title}")
            
            # Add small delay for rate limiting
            await asyncio.sleep(0.1)

asyncio.run(track_member_activity())
```

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