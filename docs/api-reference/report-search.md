# Report Search API

Search and filter ESO combat reports with advanced criteria including guilds, encounters, players, and performance metrics through the ESO Logs API.

## Overview

- **Coverage**: 3 endpoints implemented  
- **Use Cases**: Finding specific reports, performance research, guild analysis
- **Rate Limit Impact**: 5-15 points per request (varies by filter complexity)

## Methods

### search_reports()

**Purpose**: Search for reports with flexible filtering and pagination

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| guild_id | int | No | Filter by specific guild ID |
| guild_name | str | No | Filter by guild name (requires guild_server_slug and guild_server_region) |
| guild_server_slug | str | No | Guild server slug (required with guild_name) |
| guild_server_region | str | No | Guild server region (required with guild_name) |
| guild_tag_id | int | No | Filter by guild tag/team ID |
| user_id | int | No | Filter by specific user ID |
| zone_id | int | No | Filter by zone ID |
| game_zone_id | int | No | Filter by game zone ID |
| start_time | float | No | Earliest report timestamp (UNIX timestamp with milliseconds) |
| end_time | float | No | Latest report timestamp (UNIX timestamp with milliseconds) |
| limit | int | No | Number of reports per page (1-25, default: 16) |
| page | int | No | Page number for pagination (default: 1) |

**Returns**: `GetReports` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| report_data.reports.data | List[Report] | List of matching reports |
| report_data.reports.total | int | Total number of matching reports (-1 if unknown) |
| report_data.reports.per_page | int | Number of reports per page |
| report_data.reports.current_page | int | Current page number |
| report_data.reports.last_page | int | Last page number (-1 if unknown) |
| report_data.reports.has_more_pages | bool | Whether more pages are available |
| report_data.reports.from_ | int | Starting record number |
| report_data.reports.to | int | Ending record number |

**Report Data Structure**:

| Field | Type | Description |
|-------|------|-------------|
| code | str | Unique report code |
| title | str | Report title |
| start_time | float | Report start timestamp |
| end_time | float | Report end timestamp |
| zone | Zone \| None | Zone information (if available) |
| guild | Guild \| None | Guild information (if available) |
| owner | Owner \| None | Report owner information (if available) |

> **Nested Object Structures:**
> 
> **Zone Structure**:
> 
> | Field | Type | Description |
> |-------|------|-------------|
> | id | int | Zone ID |
> | name | str | Zone name |
> 
> **Guild Structure**:
> 
> | Field | Type | Description |
> |-------|------|-------------|
> | id | int | Guild ID |
> | name | str | Guild name |
> | server.name | str | Server name |
> | server.slug | str | Server slug |
> | server.region.name | str | Region name |
> | server.region.slug | str | Region slug |
> 
> **Owner Structure**:
> 
> | Field | Type | Description |
> |-------|------|-------------|
> | id | int | User ID |
> | name | str | User name |

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def search_recent_reports():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Search for recent reports with pagination
        reports = await client.search_reports(limit=5)
        
        print(f"Found {len(reports.report_data.reports.data)} reports")
        print(f"Page {reports.report_data.reports.current_page}")
        print(f"Has more pages: {reports.report_data.reports.has_more_pages}")
        
        for report in reports.report_data.reports.data:
            print(f"- {report.title} ({report.code})")
            if report.zone:
                print(f"  Zone: {report.zone.name}")
            if report.owner:
                print(f"  Owner: {report.owner.name}")

asyncio.run(search_recent_reports())
```

**Output**:
```
Found 5 reports
Page 1
Has more pages: True
- Dreadsail Reef (DzwyZ9n34Q1rHXvb)
  Zone: Dreadsail Reef
  Owner: No.Skill
- Sunspire (Bzh4XnN17QRP8YvA)
  Zone: Sunspire
  Owner: Example.Player
- Kyne's Aegis (CxN2M8w9qRvP1bYz)
  Zone: Kyne's Aegis
  Owner: Test.User
- Cloudrest (DmK5N2xPqR8wYbvC)
  Zone: Cloudrest
  Owner: Demo.Player
- Hel Ra Citadel (ExL6O3yQrS9zCdwD)
  Zone: Hel Ra Citadel
  Owner: Sample.User
```

**Advanced Filtering Example**:
```python
import asyncio
import time
from esologs.client import Client
from access_token import get_access_token

async def search_with_filters():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Search for Dreadsail Reef reports from last 7 days
        seven_days_ago = (time.time() - 7 * 24 * 3600) * 1000
        
        reports = await client.search_reports(
            zone_id=16,  # Dreadsail Reef
            start_time=seven_days_ago,
            limit=10
        )
        
        print(f"Found {len(reports.report_data.reports.data)} recent Dreadsail Reef reports")
        
        for report in reports.report_data.reports.data:
            print(f"- {report.title}")
            print(f"  Started: {report.start_time}")
            if report.guild:
                print(f"  Guild: {report.guild.name}")

asyncio.run(search_with_filters())
```

**Output**:
```
Found 3 recent Dreadsail Reef reports
- Dreadsail Reef
  Started: 1752368615346.0
  Guild: Example Guild
- Dreadsail Reef - HM
  Started: 1752360234567.0
  Guild: Test Guild
- Dreadsail Reef
  Started: 1752355123456.0
  Guild: Demo Guild
```

**Error Handling**:
```python
from esologs.exceptions import GraphQLClientHttpError, GraphQLClientGraphQLMultiError
from pydantic import ValidationError

try:
    reports = await client.search_reports(limit=0)  # Invalid limit
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except GraphQLClientHttpError as e:
    if e.status_code == 429:
        print("Rate limit exceeded - search operations are expensive")
    elif e.status_code == 400:
        print("Invalid search parameters")
```

### get_guild_reports()

**Purpose**: Convenience method to get reports for a specific guild

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| guild_id | int | Yes | The guild ID to search for |
| limit | int | No | Number of reports per page (1-25, default: 16) |
| page | int | No | Page number for pagination (default: 1) |
| start_time | float | No | Start time filter (UNIX timestamp with milliseconds) |
| end_time | float | No | End time filter (UNIX timestamp with milliseconds) |
| zone_id | int | No | Filter by specific zone |

**Returns**: `GetReports` object with the same structure as `search_reports()`

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def get_guild_activity():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Get recent reports for a specific guild
        reports = await client.get_guild_reports(guild_id=123, limit=10)
        
        print(f"Guild has {len(reports.report_data.reports.data)} recent reports")
        
        for report in reports.report_data.reports.data:
            print(f"- {report.title}")
            if report.zone:
                print(f"  Zone: {report.zone.name}")

asyncio.run(get_guild_activity())
```

**Output**:
```
Guild has 10 recent reports
- Dreadsail Reef
  Zone: Dreadsail Reef
- Sunspire
  Zone: Sunspire
- Kyne's Aegis
  Zone: Kyne's Aegis
```

### get_user_reports()

**Purpose**: Convenience method to get reports for a specific user

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | int | Yes | The user ID to search for |
| limit | int | No | Number of reports per page (1-25, default: 16) |
| page | int | No | Page number for pagination (default: 1) |
| start_time | float | No | Start time filter (UNIX timestamp with milliseconds) |
| end_time | float | No | End time filter (UNIX timestamp with milliseconds) |
| zone_id | int | No | Filter by specific zone |

**Returns**: `GetReports` object with the same structure as `search_reports()`

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def get_user_activity():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Get recent reports for a specific user
        reports = await client.get_user_reports(user_id=1781, limit=5)
        
        print(f"User has {len(reports.report_data.reports.data)} recent reports")
        
        for report in reports.report_data.reports.data:
            print(f"- {report.title}")
            if report.zone:
                print(f"  Zone: {report.zone.name}")

asyncio.run(get_user_activity())
```

**Output**:
```
User has 5 recent reports
- Dreadsail Reef
  Zone: Dreadsail Reef
- Sunspire
  Zone: Sunspire
- Kyne's Aegis
  Zone: Kyne's Aegis
- Cloudrest
  Zone: Cloudrest
- Hel Ra Citadel
  Zone: Hel Ra Citadel
```

## Advanced Usage Patterns

### Pagination
```python
async def get_all_guild_reports(guild_id: int):
    """Get all reports for a guild using pagination."""
    all_reports = []
    page = 1
    
    while True:
        reports = await client.get_guild_reports(
            guild_id=guild_id,
            page=page,
            limit=25  # Maximum per page
        )
        
        current_page_reports = reports.report_data.reports.data
        all_reports.extend(current_page_reports)
        
        if not reports.report_data.reports.has_more_pages:
            break
            
        page += 1
        await asyncio.sleep(0.5)  # Rate limiting courtesy
    
    return all_reports
```

> **Why use pagination?** When a guild has hundreds or thousands of reports, you can't retrieve them all in a single request due to API limits (max 25 per page). This pattern automatically handles pagination by checking `has_more_pages` and incrementing the page number until all reports are retrieved. The sleep delay prevents hitting rate limits.

### Date Range Filtering
```python
import time

# Last 30 days
thirty_days_ago = (time.time() - 30 * 24 * 3600) * 1000
reports = await client.search_reports(
    start_time=thirty_days_ago,
    limit=25
)

# Specific date range
start_date = 1640995200000  # Jan 1, 2022
end_date = 1672531200000    # Jan 1, 2023
reports = await client.search_reports(
    start_time=start_date,
    end_time=end_date,
    limit=25
)
```

> **Understanding timestamps:** ESO Logs uses UNIX timestamps in milliseconds (not seconds). The first example calculates 30 days ago by subtracting seconds from current time, then multiplying by 1000 to convert to milliseconds. Date ranges are useful for analyzing performance trends over specific periods or studying historical data.

### Common Use Cases

**Guild Performance Tracking**:
```python
# Monitor guild activity in specific zones
reports = await client.search_reports(
    guild_id=5363,
    zone_id=16,  # Dreadsail Reef
    limit=5
)

print(f"Found {len(reports.report_data.reports.data)} guild reports in Dreadsail Reef")
for report in reports.report_data.reports.data:
    print(f"- {report.title}")
    if report.guild:
        print(f"  Guild: {report.guild.name}")
    if report.zone:
        print(f"  Zone: {report.zone.name}")
```

**Output**:
```
Found 0 guild reports in Dreadsail Reef
```

**Player Activity Analysis**:
```python
# Track user's recent activity
reports = await client.get_user_reports(
    user_id=43829,
    limit=5
)

print(f"User has {len(reports.report_data.reports.data)} recent reports")
for report in reports.report_data.reports.data:
    print(f"- {report.title}")
    if report.zone:
        print(f"  Zone: {report.zone.name}")
    if report.owner:
        print(f"  Owner: {report.owner.name}")
```

**Output**:
```
User has 5 recent reports
- Dungeons
  Zone: Dungeons
  Owner: jay
- Rockgrove
  Zone: Rockgrove
  Owner: jay
- Ossein Cage
  Zone: Ossein Cage
  Owner: jay
- (Untitled Report)
  Owner: jay
- (Untitled Report)
  Owner: jay
```

**Zone-Specific Research**:
```python
# Study activity in a specific zone
reports = await client.search_reports(
    zone_id=16,  # Dreadsail Reef
    limit=5
)

print(f"Found {len(reports.report_data.reports.data)} reports in Dreadsail Reef")
for report in reports.report_data.reports.data:
    print(f"- {report.title}")
    if report.zone:
        print(f"  Zone: {report.zone.name}")
    if report.owner:
        print(f"  Owner: {report.owner.name}")
```

**Output**:
```
Found 5 reports in Dreadsail Reef
- Checkbox Crusaders 2 DSR HM Day 6
  Zone: Dreadsail Reef
  Owner: banyux
- vDSR
  Zone: Dreadsail Reef
  Owner: nor'easter
- Dreadsail Reef
  Zone: Dreadsail Reef
  Owner: No.Skill
- ETU II - Dreadsail Reef Trial
  Zone: Dreadsail Reef
  Owner: nurrender
- Dreadsail Reef
  Zone: Dreadsail Reef
  Owner: No.Skill
```

**Recent Activity Monitoring**:
```python
# Get latest reports across all criteria
reports = await client.search_reports(limit=5)

print(f"Found {len(reports.report_data.reports.data)} recent reports")
for report in reports.report_data.reports.data:
    print(f"- {report.title}")
    if report.zone:
        print(f"  Zone: {report.zone.name}")
    if report.owner:
        print(f"  Owner: {report.owner.name}")
```

**Output**:
```
Found 5 recent reports
- vOC 7/12
  Zone: Ossein Cage
  Owner: IRiceKrispies
- Dungeons
  Zone: Dungeons
  Owner: jay
- vSS HM Prog
  Zone: Sunspire
  Owner: tomstock
- Wolfy PB
  Owner: mrmuffin210
- Frog Prog Day 67 portal 2
  Owner: mudosheep
```

## Best Practices
- **Use pagination**: Limit results to conserve rate limit points
- **Add delays**: Include `await asyncio.sleep(0.5)` between requests
- **Filter wisely**: More specific filters may increase cost
- **Monitor rate limits**: Use smaller limits during development and testing
