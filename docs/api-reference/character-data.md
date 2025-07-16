# Character Data

Enables the retrieval of single characters or filtered collections of characters. Eg; Character profiles, reports, and performance data

## Overview

- **Coverage**: 5 endpoints implemented
- **Use Cases**: Character analysis, performance tracking, report history, ranking comparison
- **Rate Limit Impact**: 2-5 points per request (varies by complexity)

## Methods

### get_character_by_id()

**Purpose**: Retrieve detailed character profile information

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | *int* | Yes | The character ID to retrieve |

**Returns**: `GetCharacterById` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `character_data.character.id` | *int* | Character ID |
| `character_data.character.name` | *str* | Character name |
| `character_data.character.class_id` | *int* | Character class ID |
| `character_data.character.race_id` | *int* | Character race ID |
| `character_data.character.guild_rank` | *int* | Guild rank (0 if not in guild) |
| `character_data.character.hidden` | *bool* | Whether character profile is hidden |
| `character_data.character.server.name` | *str* | Server name |
| `character_data.character.server.region.name` | *str* | Server region name |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_character_profile():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        character = await client.get_character_by_id(id=314050)

        if character.character_data and character.character_data.character:
            char = character.character_data.character
            print(f"Character: {char.name} (ID: {char.id})")
            print(f"Class ID: {char.class_id}, Race ID: {char.race_id}")
            print(f"Server: {char.server.name} ({char.server.region.name})")
            print(f"Guild Rank: {char.guild_rank}")

asyncio.run(get_character_profile())
```

**Output**:
```
Character: Zalduk Nightsky (ID: 314050)
Class ID: 1, Race ID: 5
Server: Megaserver (Europe)
Guild Rank: 0
```

### get_character_reports()

**Purpose**: Get recent reports for a specific character

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `character_id` | *int* | Yes | The character ID to get reports for |
| `limit` | *int* | No | Number of reports to return (default: 10) |

**Returns**: `GetCharacterReports` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `character_data.character.recent_reports.data` | *List[Report]* | List of report objects |
| `character_data.character.recent_reports.total` | *int* | Total number of reports |
| `character_data.character.recent_reports.per_page` | *int* | Reports per page |
| `character_data.character.recent_reports.current_page` | *int* | Current page number |
| `character_data.character.recent_reports.from_` | *int \| None* | Starting record number |
| `character_data.character.recent_reports.to` | *int \| None* | Ending record number |
| `character_data.character.recent_reports.last_page` | *int* | Last page number |
| `character_data.character.recent_reports.has_more_pages` | *bool* | Whether more pages exist |

**Report Object Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `code` | *str* | Unique report code |
| `start_time` | *float* | Report start timestamp |
| `end_time` | *float* | Report end timestamp |
| `zone.name` | *str* | Zone name where report was recorded |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_character_recent_reports():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        reports = await client.get_character_reports(character_id=314050, limit=5)

        if reports.character_data and reports.character_data.character:
            recent_reports = reports.character_data.character.recent_reports
            if recent_reports:
                print(f"Total reports: {recent_reports.total}")
                print(f"Showing {len(recent_reports.data)} reports:")

                for report in recent_reports.data:
                    if report:
                        zone_name = report.zone.name if report.zone else "Unknown Zone"
                        print(f"- {report.code} in {zone_name}")

asyncio.run(get_character_recent_reports())
```

**Output**:
```
Total reports: 286
Showing 5 reports:
- f2QKpYZdwTVGMq4R in Rockgrove
- 7D2qyThHzv1wMdkQ in Aetherian Archive
```

### get_character_encounter_ranking()

**Purpose**: Get character's ranking for a specific encounter

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `character_id` | *int* | Yes | The character ID |
| `encounter_id` | *int* | Yes | The encounter ID to get rankings for |

**Returns**: `GetCharacterEncounterRanking` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `character_data.character.encounter_rankings` | *Any* | Rankings data (structure varies by encounter) |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_character_encounter_ranking():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        ranking = await client.get_character_encounter_ranking(
            character_id=314050,
            encounter_id=63  # Rockgrove encounter
        )

        if ranking.character_data and ranking.character_data.character:
            rankings = ranking.character_data.character.encounter_rankings
            if rankings:
                print("Character has rankings for this encounter")
                print(f"Available data: {list(rankings.keys())[:5]}")
            else:
                print("No rankings found for this encounter")

asyncio.run(get_character_encounter_ranking())
```

**Output**:
```
Character has rankings for this encounter
Available data: ['bestAmount', 'medianPerformance', 'averagePerformance', 'totalKills', 'fastestKill']
```

### get_character_encounter_rankings()

**Purpose**: Get character's rankings for a specific encounter with filtering options

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `character_id` | *int* | Yes | The character ID |
| `encounter_id` | *int* | Yes | The encounter ID to get rankings for |
| `by_bracket` | *bool* | No | Group rankings by bracket |
| `class_name` | *str* | No | Filter by class name |
| `compare` | *RankingCompareType* | No | Comparison type for rankings |
| `difficulty` | *int* | No | Difficulty level filter |
| `include_combatant_info` | *bool* | No | Include combatant information |
| `include_private_logs` | *bool* | No | Include private logs in rankings |
| `metric` | *CharacterRankingMetricType* | No | Ranking metric type |
| `partition` | *int* | No | Partition number |
| `role` | *RoleType* | No | Role filter (Tank, Healer, DPS) |
| `size` | *int* | No | Number of results to return |
| `spec_name` | *str* | No | Specialization name filter |
| `timeframe` | *RankingTimeframeType* | No | Time period for rankings |

**Returns**: `GetCharacterEncounterRankings` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `character_data.character.encounter_rankings` | *Any* | Detailed rankings data with filters applied |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_character_encounter_rankings():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        rankings = await client.get_character_encounter_rankings(
            character_id=314050,
            encounter_id=63,  # Rockgrove encounter
            include_combatant_info=True
        )

        if rankings.character_data and rankings.character_data.character:
            encounter_rankings = rankings.character_data.character.encounter_rankings
            if encounter_rankings:
                print("Character has detailed encounter rankings")
                print(f"Best score: {encounter_rankings.get('bestAmount', 0)}")
                print(f"Total kills: {encounter_rankings.get('totalKills', 0)}")
                print(f"Number of ranks: {len(encounter_rankings.get('ranks', []))}")
                if encounter_rankings.get('ranks'):
                    first_rank = encounter_rankings['ranks'][0]
                    print(f"Latest performance: {first_rank.get('amount', 0)} points")
                    print(f"Rank percentile: {first_rank.get('rankPercent', 0):.1f}%")
            else:
                print("No detailed rankings found")

asyncio.run(get_character_encounter_rankings())
```

**Output**:
```
Character has detailed encounter rankings
Best score: 296773
Total kills: 11
Number of ranks: 11
Latest performance: 296773 points
Rank percentile: 68.0%
```

### get_character_zone_rankings()

**Purpose**: Get character's rankings for a specific zone with filtering options

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `character_id` | *int* | Yes | The character ID |
| `zone_id` | *int* | No | The zone ID to get rankings for |
| `by_bracket` | *bool* | No | Group rankings by bracket |
| `class_name` | *str* | No | Filter by class name |
| `compare` | *RankingCompareType* | No | Comparison type for rankings |
| `difficulty` | *int* | No | Difficulty level filter |
| `include_private_logs` | *bool* | No | Include private logs in rankings |
| `metric` | *CharacterRankingMetricType* | No | Ranking metric type |
| `partition` | *int* | No | Partition number |
| `role` | *RoleType* | No | Role filter (Tank, Healer, DPS) |
| `size` | *int* | No | Number of results to return |
| `spec_name` | *str* | No | Specialization name filter |
| `timeframe` | *RankingTimeframeType* | No | Time period for rankings |

**Returns**: `GetCharacterZoneRankings` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `character_data.character.zone_rankings` | *Any* | Zone-specific rankings data with filters applied |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_character_zone_rankings():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        rankings = await client.get_character_zone_rankings(
            character_id=314050,
            zone_id=19,  # Ossein Cage zone
            size=5
        )

        if rankings.character_data and rankings.character_data.character:
            zone_rankings = rankings.character_data.character.zone_rankings
            if zone_rankings:
                print("Character has zone rankings")
                print(f"Available metrics: {list(zone_rankings.keys())[:3]}")
            else:
                print("No zone rankings found")

asyncio.run(get_character_zone_rankings())
```

**Output**:
```
Character has zone rankings
Available metrics: ['bestPerformanceAverage', 'medianPerformanceAverage', 'difficulty']
```

## Common Usage Patterns

### Character Profile Analysis

```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def analyze_character(character_id: int):
    """Complete character analysis including profile and recent activity."""
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get character profile
        character = await client.get_character_by_id(id=character_id)

        if character.character_data and character.character_data.character:
            char = character.character_data.character
            print(f"Analyzing: {char.name}")
            print(f"Server: {char.server.name} ({char.server.region.name})")

            # Get recent reports
            reports = await client.get_character_reports(character_id=character_id)
            if reports.character_data and reports.character_data.character:
                recent_reports = reports.character_data.character.recent_reports
                if recent_reports:
                    print(f"Recent activity: {recent_reports.total} reports")

# Run the analysis
asyncio.run(analyze_character(314050))
```

**Output**:
```
Analyzing: Zalduk Nightsky
Server: Megaserver (Europe)
Recent activity: 286 reports
```

### Performance Tracking

```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def track_character_performance(character_id: int, encounter_id: int):
    """Track character performance for a specific encounter."""
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get encounter rankings
        rankings = await client.get_character_encounter_rankings(
            character_id=character_id,
            encounter_id=encounter_id,
            include_combatant_info=True
        )

        if rankings.character_data and rankings.character_data.character:
            encounter_rankings = rankings.character_data.character.encounter_rankings
            if encounter_rankings:
                print("Performance data available for analysis")
                print(f"Best score: {encounter_rankings.get('bestAmount', 0)}")
                print(f"Total kills: {encounter_rankings.get('totalKills', 0)}")
                print(f"Difficulty: {encounter_rankings.get('difficulty', 'Unknown')}")
                ranks = encounter_rankings.get('ranks', [])
                print(f"Number of ranking entries: {len(ranks)}")

                if ranks:
                    # Show recent performance trend
                    recent_scores = [rank.get('amount', 0) for rank in ranks[:3]]
                    print(f"Recent scores: {recent_scores}")
                    avg_recent = sum(recent_scores) / len(recent_scores) if recent_scores else 0
                    print(f"Average recent performance: {avg_recent:.0f}")
            else:
                print("No performance data found for this encounter")

# Run the performance tracking
asyncio.run(track_character_performance(314050, 63))
```

**Output**:
```
Performance data available for analysis
Best score: 296773
Total kills: 11
Difficulty: 122
Number of ranking entries: 11
Recent scores: [296773, 295705, 294120]
Average recent performance: 295533
```

## Error Handling

```python
from esologs.exceptions import GraphQLClientHttpError, GraphQLClientGraphQLMultiError
from pydantic import ValidationError

try:
    character = await client.get_character_by_id(id=999999)  # Non-existent ID
except GraphQLClientGraphQLMultiError as e:
    print(f"GraphQL error: {e}")
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except GraphQLClientHttpError as e:
    if e.status_code == 429:
        print("Rate limit exceeded")
    elif e.status_code == 404:
        print("Character not found")
```

## Rate Limiting Notes

- Character profile requests: 2-3 points
- Character reports: 3-4 points
- Character rankings: 4-5 points
- Add delays between requests: `await asyncio.sleep(0.2)`
- Monitor rate limits using `get_rate_limit_data()`
