# Report Analysis API

Access detailed ESO combat log analysis including events, performance graphs, tables, rankings, and player details through the ESO Logs API.

## Overview

- **Coverage**: 5 endpoints implemented
- **Use Cases**: Combat analysis, performance optimization, encounter research, damage/healing optimization
- **Rate Limit Impact**: 3-10 points per request (varies by complexity and data volume)

## Methods

### get_report_events()

**Purpose**: Retrieve detailed event data from a combat log report

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| code | str | Yes | The report code to analyze |
| ability_id | float | No | Filter events by specific ability ID |
| data_type | EventDataType | No | Type of events to retrieve (DamageDone, Healing, Deaths, etc.) |
| death | int | No | Filter to specific death number |
| difficulty | int | No | Difficulty level filter |
| encounter_id | int | No | Filter to specific encounter |
| end_time | float | No | End time in milliseconds relative to report start |
| fight_i_ds | List[int] | No | List of fight IDs to include |
| filter_expression | str | No | Advanced filter expression |
| hostility_type | HostilityType | No | Filter by hostility type (Enemies, Friendlies) |
| include_resources | bool | No | Include resource events |
| kill_type | KillType | No | Filter by kill type |
| limit | int | No | Maximum number of events to return |
| source_auras_absent | str | No | Filter events where source lacks specific auras |
| source_auras_present | str | No | Filter events where source has specific auras |
| source_class | str | No | Filter by source character class |
| source_id | int | No | Filter by specific source actor ID |
| source_instance_id | int | No | Filter by source instance ID |
| start_time | float | No | Start time in milliseconds relative to report start |
| target_auras_absent | str | No | Filter events where target lacks specific auras |
| target_auras_present | str | No | Filter events where target has specific auras |
| target_class | str | No | Filter by target character class |
| target_id | int | No | Filter by specific target actor ID |
| target_instance_id | int | No | Filter by target instance ID |
| translate | bool | No | Translate ability names to localized strings |
| use_ability_i_ds | bool | No | Use ability IDs instead of names |
| use_actor_i_ds | bool | No | Use actor IDs instead of names |
| view_options | int | No | View option flags |
| wipe_cutoff | int | No | Wipe cutoff percentage |

**Returns**: `GetReportEvents` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| report_data.report.events.data | Any | List of event objects containing timestamps, abilities, damage/healing values |
| report_data.report.events.next_page_timestamp | float \| None | Timestamp for pagination to next page |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.enums import EventDataType
from access_token import get_access_token

async def analyze_report_events():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Analyze damage events from a specific report
        events = await client.get_report_events(
            code="VfxqaX47HGC98rAp",
            data_type=EventDataType.DamageDone,
            start_time=0.0,
            end_time=60000.0  # First minute
        )
        
        print(f"Retrieved events data: {type(events.report_data.report.events.data)}")
        if events.report_data.report.events.next_page_timestamp:
            print(f"More data available after: {events.report_data.report.events.next_page_timestamp}")

asyncio.run(analyze_report_events())
```

**Output**:
```
Retrieved events data: <class 'list'>
```

### get_report_graph()

**Purpose**: Get graphical performance data for visualization (DPS over time, healing charts, etc.)

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| code | str | Yes | The report code to analyze |
| ability_id | float | No | Filter by specific ability ID |
| data_type | GraphDataType | No | Type of graph data (DamageDone, Healing, DamageTaken, etc.) |
| death | int | No | Filter to specific death number |
| difficulty | int | No | Difficulty level filter |
| encounter_id | int | No | Filter to specific encounter |
| end_time | float | No | End time in milliseconds |
| fight_i_ds | List[int] | No | List of fight IDs to include |
| filter_expression | str | No | Advanced filter expression |
| hostility_type | HostilityType | No | Filter by hostility type |
| kill_type | KillType | No | Filter by kill type |
| source_auras_absent | str | No | Filter where source lacks specific auras |
| source_auras_present | str | No | Filter where source has specific auras |
| source_class | str | No | Filter by source character class |
| source_id | int | No | Filter by specific source actor ID |
| source_instance_id | int | No | Filter by source instance ID |
| start_time | float | No | Start time in milliseconds |
| target_auras_absent | str | No | Filter where target lacks specific auras |
| target_auras_present | str | No | Filter where target has specific auras |
| target_class | str | No | Filter by target character class |
| target_id | int | No | Filter by specific target actor ID |
| target_instance_id | int | No | Filter by target instance ID |
| translate | bool | No | Translate ability names |
| view_options | int | No | View option flags |
| view_by | ViewType | No | View aggregation method |
| wipe_cutoff | int | No | Wipe cutoff percentage |

**Returns**: `GetReportGraph` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| report_data.report.graph | dict | Graph data containing time-series performance data |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.enums import GraphDataType
from access_token import get_access_token

async def get_damage_graph():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Get DPS graph data
        graph = await client.get_report_graph(
            code="VfxqaX47HGC98rAp",
            data_type=GraphDataType.DamageDone,
            start_time=0.0,
            end_time=300000.0  # First 5 minutes
        )
        
        print(f"Graph data keys: {list(graph.report_data.report.graph.keys())}")
        if 'data' in graph.report_data.report.graph:
            print(f"Graph data type: {type(graph.report_data.report.graph['data'])}")

asyncio.run(get_damage_graph())
```

**Output**:
```
Graph data keys: ['data']
Graph data type: <class 'dict'>
```

### get_report_table()

**Purpose**: Get tabular analysis data for summary statistics and performance breakdowns

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| code | str | Yes | The report code to analyze |
| ability_id | float | No | Filter by specific ability ID |
| data_type | TableDataType | No | Type of table data (DamageDone, Healing, Deaths, etc.) |
| death | int | No | Filter to specific death number |
| difficulty | int | No | Difficulty level filter |
| encounter_id | int | No | Filter to specific encounter |
| end_time | float | No | End time in milliseconds |
| fight_i_ds | List[int] | No | List of fight IDs to include |
| filter_expression | str | No | Advanced filter expression |
| hostility_type | HostilityType | No | Filter by hostility type |
| kill_type | KillType | No | Filter by kill type |
| source_auras_absent | str | No | Filter where source lacks specific auras |
| source_auras_present | str | No | Filter where source has specific auras |
| source_class | str | No | Filter by source character class |
| source_id | int | No | Filter by specific source actor ID |
| source_instance_id | int | No | Filter by source instance ID |
| start_time | float | No | Start time in milliseconds |
| target_auras_absent | str | No | Filter where target lacks specific auras |
| target_auras_present | str | No | Filter where target has specific auras |
| target_class | str | No | Filter by target character class |
| target_id | int | No | Filter by specific target actor ID |
| target_instance_id | int | No | Filter by target instance ID |
| translate | bool | No | Translate ability names |
| view_options | int | No | View option flags |
| view_by | ViewType | No | View aggregation method |
| wipe_cutoff | int | No | Wipe cutoff percentage |

**Returns**: `GetReportTable` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| report_data.report.table | dict | Table data containing aggregated statistics and performance metrics |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.enums import TableDataType
from access_token import get_access_token

async def get_damage_table():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Get damage summary table
        table = await client.get_report_table(
            code="VfxqaX47HGC98rAp",
            data_type=TableDataType.DamageDone,
            start_time=0.0,
            end_time=300000.0
        )
        
        print(f"Table data keys: {list(table.report_data.report.table.keys())}")
        if 'data' in table.report_data.report.table:
            print(f"Table data type: {type(table.report_data.report.table['data'])}")

asyncio.run(get_damage_table())
```

**Output**:
```
Table data keys: ['data']
Table data type: <class 'dict'>
```

### get_report_rankings()

**Purpose**: Get performance rankings from combat reports

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| code | str | Yes | The report code to analyze |
| compare | RankingCompareType | No | Comparison method for rankings |
| difficulty | int | No | Difficulty level filter |
| encounter_id | int | No | Filter to specific encounter |
| fight_i_ds | List[int] | No | List of fight IDs to include |
| player_metric | ReportRankingMetricType | No | Ranking metric (dps, hps, playerscore, etc.) |
| timeframe | RankingTimeframeType | No | Time frame for ranking comparison |

**Returns**: `GetReportRankings` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| report_data.report.rankings | dict | Rankings data containing performance comparisons and percentiles |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.enums import ReportRankingMetricType
from access_token import get_access_token

async def get_dps_rankings():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Get DPS rankings for the report
        rankings = await client.get_report_rankings(
            code="VfxqaX47HGC98rAp",
            player_metric=ReportRankingMetricType.dps
        )
        
        print(f"Rankings data keys: {list(rankings.report_data.report.rankings.keys())}")
        if 'data' in rankings.report_data.report.rankings:
            data = rankings.report_data.report.rankings['data']
            print(f"Rankings data type: {type(data)}")
            if isinstance(data, list):
                print(f"Number of ranking entries: {len(data)}")

asyncio.run(get_dps_rankings())
```

**Output**:
```
Rankings data keys: ['data']
Rankings data type: <class 'list'>
Number of ranking entries: 10
```

### get_report_player_details()

**Purpose**: Get detailed player performance information from reports

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| code | str | Yes | The report code to analyze |
| difficulty | int | No | Difficulty level filter |
| encounter_id | int | No | Filter to specific encounter |
| end_time | float | No | End time in milliseconds |
| fight_i_ds | List[int] | No | List of fight IDs to include |
| kill_type | KillType | No | Filter by kill type |
| start_time | float | No | Start time in milliseconds |
| translate | bool | No | Translate ability names |
| include_combatant_info | bool | No | Include detailed combatant information |

**Returns**: `GetReportPlayerDetails` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| report_data.report.player_details | dict | Player details containing individual performance breakdowns |

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def get_player_performance():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Get detailed player performance data
        player_details = await client.get_report_player_details(
            code="VfxqaX47HGC98rAp",
            start_time=0.0,
            end_time=300000.0,
            include_combatant_info=True
        )
        
        print(f"Player details keys: {list(player_details.report_data.report.player_details.keys())}")
        if 'data' in player_details.report_data.report.player_details:
            print(f"Player details data type: {type(player_details.report_data.report.player_details['data'])}")

asyncio.run(get_player_performance())
```

**Output**:
```
Player details keys: ['data']
Player details data type: <class 'dict'>
```

## Error Handling

Report analysis endpoints may have specific error cases due to their high cost and data complexity:

```python
from esologs.exceptions import GraphQLClientHttpError, GraphQLClientGraphQLMultiError
from pydantic import ValidationError

try:
    events = await client.get_report_events(
        code="invalid_code",
        data_type=EventDataType.DamageDone
    )
except GraphQLClientHttpError as e:
    if e.status_code == 403:
        print("Report is private or access denied")
    elif e.status_code == 404:
        print("Report not found")
    elif e.status_code == 429:
        print("Rate limit exceeded - report analysis is expensive (3-10+ points)")
except GraphQLClientGraphQLMultiError as e:
    print(f"GraphQL error: {e}")
except ValidationError as e:
    print(f"Invalid parameters: {e}")
```

## Common Analysis Patterns

### Performance Analysis Workflow

Combine different analysis methods for comprehensive performance review:

```python
async def comprehensive_analysis(client, report_code):
    # Get basic report info
    report = await client.get_report_by_code(code=report_code)
    
    # Analyze damage over time
    damage_graph = await client.get_report_graph(
        code=report_code,
        data_type=GraphDataType.DamageDone
    )
    
    # Get damage summary statistics
    damage_table = await client.get_report_table(
        code=report_code,
        data_type=TableDataType.DamageDone
    )
    
    # Compare performance rankings
    rankings = await client.get_report_rankings(
        code=report_code,
        player_metric=ReportRankingMetricType.dps
    )
    
    # Get individual player breakdowns
    player_details = await client.get_report_player_details(
        code=report_code
    )
    
    return {
        'report': report,
        'damage_graph': damage_graph,
        'damage_table': damage_table,
        'rankings': rankings,
        'player_details': player_details
    }
```

### Encounter Phase Analysis

Analyze specific phases of boss encounters:

```python
async def analyze_encounter_phase(client, report_code, encounter_id, phase_start, phase_end):
    # Get events for specific phase
    events = await client.get_report_events(
        code=report_code,
        encounter_id=encounter_id,
        start_time=phase_start,
        end_time=phase_end,
        data_type=EventDataType.DamageDone
    )
    
    # Get phase performance graph
    graph = await client.get_report_graph(
        code=report_code,
        encounter_id=encounter_id,
        start_time=phase_start,
        end_time=phase_end,
        data_type=GraphDataType.DamageDone
    )
    
    return {'events': events, 'graph': graph}
```

## Rate Limiting Considerations

- **High Cost**: Report analysis endpoints are the most expensive (3-10+ points per request)
- **Total Budget**: 18,000 points/hour (points are floats)
- **Recommendation**: Add delays between requests: `await asyncio.sleep(0.5)`
- **Strategy**: Test with smaller time ranges first, then expand analysis scope
- **Monitoring**: Check rate limit status with `get_rate_limit_data()` method

## Data Structure Notes

- **Events**: Raw event data is returned as flexible `Any` type due to varied event structures
- **Graphs/Tables**: Performance data returned as `dict` with 'data' key containing analysis results
- **Rankings**: Returns list of ranking objects with percentile and performance data
- **Player Details**: Comprehensive player statistics as structured dictionary data
- **Timestamps**: All times are in milliseconds relative to report start
- **Pagination**: Events support pagination via `next_page_timestamp` field