# Report Analysis

Access detailed (behavioral) combat log data including events, performance graphs, tables, rankings, and player details.

## Overview

- **Coverage**: 5 endpoints implemented
- **Use Cases**: Combat analysis, performance optimization, encounter research, damage/healing optimization
- **Rate Limit Impact**: 3-10 points per request (varies by complexity and data volume)

## Methods

### get_report_events()

**Purpose**: Retrieve detailed event data from a combat log report

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `code` | *str* | Yes | The report code to analyze |
| `ability_id` | *float* | No | Filter events by specific ability ID |
| `data_type` | *EventDataType* | No | Type of events to retrieve (DamageDone, Healing, Deaths, etc.) |
| `death` | *int* | No | Filter to specific death number |
| `difficulty` | *int* | No | Difficulty level filter |
| `encounter_id` | *int* | No | Filter to specific encounter |
| `end_time` | *float* | No | End time in milliseconds relative to report start |
| `fight_i_ds` | *List[int]* | No | List of fight IDs to include |
| `filter_expression` | *str* | No | Advanced filter expression |
| `hostility_type` | *HostilityType* | No | Filter by hostility type (Enemies, Friendlies) |
| `include_resources` | *bool* | No | Include resource events |
| `kill_type` | *KillType* | No | Filter by kill type |
| `limit` | *int* | No | Maximum number of events to return |
| `source_auras_absent` | *str* | No | Filter events where source lacks specific auras |
| `source_auras_present` | *str* | No | Filter events where source has specific auras |
| `source_class` | *str* | No | Filter by source character class |
| `source_id` | *int* | No | Filter by specific source actor ID |
| `source_instance_id` | *int* | No | Filter by source instance ID |
| `start_time` | *float* | No | Start time in milliseconds relative to report start |
| `target_auras_absent` | *str* | No | Filter events where target lacks specific auras |
| `target_auras_present` | *str* | No | Filter events where target has specific auras |
| `target_class` | *str* | No | Filter by target character class |
| `target_id` | *int* | No | Filter by specific target actor ID |
| `target_instance_id` | *int* | No | Filter by target instance ID |
| `translate` | *bool* | No | Translate ability names to localized strings |
| `use_ability_i_ds` | *bool* | No | Use ability IDs instead of names |
| `use_actor_i_ds` | *bool* | No | Use actor IDs instead of names |
| `view_options` | *int* | No | View option flags |
| `wipe_cutoff` | *int* | No | Wipe cutoff percentage |

**Returns**: `GetReportEvents` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `report_data.report.events.data` | *Any* | List of event objects containing timestamps, abilities, damage/healing values |
| `report_data.report.events.next_page_timestamp` | *float \| None* | Timestamp for pagination to next page |

> **Note**: The triple nesting (`report_data.report.events`) reflects the ESO Logs GraphQL API structure where all report queries are grouped under `reportData` with individual reports accessed via `report(code)`. This structure will be simplified in a future refactor to provide more direct access patterns.

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

        # Analyze damage events from a specific fight
        events = await client.get_report_events(
            code="VFnNYQjxC3RwGqg1",
            data_type=EventDataType.DamageDone,
            fight_i_ds=[5],  # Specific fight: Red Witch Gedna Relvel
            start_time=259178.0,
            end_time=270000.0
        )

        if events.report_data.report.events.data:
            print(f"Found {len(events.report_data.report.events.data)} events")
            # Show first few events
            for i, event in enumerate(events.report_data.report.events.data[:3]):
                print(f"Event {i+1}: {event}")

            if events.report_data.report.events.next_page_timestamp:
                print(f"More data available after: {events.report_data.report.events.next_page_timestamp}")
        else:
            print("No event data available for this fight")

asyncio.run(analyze_report_events())
```

**Output**:
```
Found 300 events
Event 1: {'timestamp': 259781, 'type': 'damage', 'sourceID': 10, 'sourceIsFriendly': True, 'targetID': 49, 'targetIsFriendly': False, 'abilityGameID': 88802, 'fight': 5, 'buffs': '76518.61687.88509.58955.80469.99875.92503.147417.61666.61771.147226.61799.45135.45513.61898.61665.61662.64509.86196.172621.', 'hitType': 1, 'amount': 1218, 'tick': True}
Event 2: {'timestamp': 259781, 'type': 'damage', 'sourceID': 10, 'sourceIsFriendly': True, 'targetID': 49, 'targetIsFriendly': False, 'abilityGameID': 88801, 'fight': 5, 'buffs': '76518.61687.88509.58955.80469.99875.92503.147417.61666.61771.147226.61799.45135.45513.61898.61665.61662.64509.86196.172621.', 'hitType': 10, 'amount': 0}
Event 3: {'timestamp': 259781, 'type': 'damage', 'sourceID': 10, 'sourceIsFriendly': True, 'targetID': 49, 'targetIsFriendly': False, 'abilityGameID': 21481, 'fight': 5, 'buffs': '76518.61687.88509.58955.80469.99875.92503.147417.61666.61771.147226.61799.45135.45513.61898.61665.61662.64509.86196.172621.', 'hitType': 1, 'amount': 1850}
More data available after: 264591.0
```

### get_report_graph()

**Purpose**: Get graphical performance data for visualization (DPS over time, healing charts, etc.)

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `code` | *str* | Yes | The report code to analyze |
| `ability_id` | *float* | No | Filter by specific ability ID |
| `data_type` | *GraphDataType* | No | Type of graph data (DamageDone, Healing, DamageTaken, etc.) |
| `death` | *int* | No | Filter to specific death number |
| `difficulty` | *int* | No | Difficulty level filter |
| `encounter_id` | *int* | No | Filter to specific encounter |
| `end_time` | *float* | No | End time in milliseconds |
| `fight_i_ds` | *List[int]* | No | List of fight IDs to include |
| `filter_expression` | *str* | No | Advanced filter expression |
| `hostility_type` | *HostilityType* | No | Filter by hostility type |
| `kill_type` | *KillType* | No | Filter by kill type |
| `source_auras_absent` | *str* | No | Filter where source lacks specific auras |
| `source_auras_present` | *str* | No | Filter where source has specific auras |
| `source_class` | *str* | No | Filter by source character class |
| `source_id` | *int* | No | Filter by specific source actor ID |
| `source_instance_id` | *int* | No | Filter by source instance ID |
| `start_time` | *float* | No | Start time in milliseconds |
| `target_auras_absent` | *str* | No | Filter where target lacks specific auras |
| `target_auras_present` | *str* | No | Filter where target has specific auras |
| `target_class` | *str* | No | Filter by target character class |
| `target_id` | *int* | No | Filter by specific target actor ID |
| `target_instance_id` | *int* | No | Filter by target instance ID |
| `translate` | *bool* | No | Translate ability names |
| `view_options` | *int* | No | View option flags |
| `view_by` | *ViewType* | No | View aggregation method |
| `wipe_cutoff` | *int* | No | Wipe cutoff percentage |

**Returns**: `GetReportGraph` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `report_data.report.graph` | *dict* | Graph data containing time-series performance data |

> **Note**: The triple nesting (`report_data.report.graph`) reflects the ESO Logs GraphQL API structure where all report queries are grouped under `reportData` with individual reports accessed via `report(code)`. This structure will be simplified in a future refactor to provide more direct access patterns.

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
            code="VFnNYQjxC3RwGqg1",
            data_type=GraphDataType.DamageDone,
            start_time=0.0,
            end_time=300000.0  # First 5 minutes
        )

        graph_data = graph.report_data.report.graph['data']
        print(f"Number of player series: {len(graph_data['series'])}")

        # Show first player's data
        first_player = graph_data['series'][0]
        print(f"Player: {first_player['name']} ({first_player['type']})")
        print(f"Total damage: {first_player['total']:,}")
        print(f"Data points: {len(first_player['data'])}")

asyncio.run(get_damage_graph())
```

**Output**:
```
Number of player series: 8
Player: Rünebladés-Beam-Sister (Arcanist)
Total damage: 8,947,598
Data points: 240
```

### get_report_table()

**Purpose**: Get tabular analysis data for summary statistics and performance breakdowns

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `code` | *str* | Yes | The report code to analyze |
| `ability_id` | *float* | No | Filter by specific ability ID |
| `data_type` | *TableDataType* | No | Type of table data (DamageDone, Healing, Deaths, etc.) |
| `death` | *int* | No | Filter to specific death number |
| `difficulty` | *int* | No | Difficulty level filter |
| `encounter_id` | *int* | No | Filter to specific encounter |
| `end_time` | *float* | No | End time in milliseconds |
| `fight_i_ds` | *List[int]* | No | List of fight IDs to include |
| `filter_expression` | *str* | No | Advanced filter expression |
| `hostility_type` | *HostilityType* | No | Filter by hostility type |
| `kill_type` | *KillType* | No | Filter by kill type |
| `source_auras_absent` | *str* | No | Filter where source lacks specific auras |
| `source_auras_present` | *str* | No | Filter where source has specific auras |
| `source_class` | *str* | No | Filter by source character class |
| `source_id` | *int* | No | Filter by specific source actor ID |
| `source_instance_id` | *int* | No | Filter by source instance ID |
| `start_time` | *float* | No | Start time in milliseconds |
| `target_auras_absent` | *str* | No | Filter where target lacks specific auras |
| `target_auras_present` | *str* | No | Filter where target has specific auras |
| `target_class` | *str* | No | Filter by target character class |
| `target_id` | *int* | No | Filter by specific target actor ID |
| `target_instance_id` | *int* | No | Filter by target instance ID |
| `translate` | *bool* | No | Translate ability names |
| `view_options` | *int* | No | View option flags |
| `view_by` | *ViewType* | No | View aggregation method |
| `wipe_cutoff` | *int* | No | Wipe cutoff percentage |

**Returns**: `GetReportTable` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `report_data.report.table` | *dict* | Table data containing aggregated statistics and performance metrics |

> **Note**: The triple nesting (`report_data.report.table`) reflects the ESO Logs GraphQL API structure where all report queries are grouped under `reportData` with individual reports accessed via `report(code)`. This structure will be simplified in a future refactor to provide more direct access patterns.

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
            code="VFnNYQjxC3RwGqg1",
            data_type=TableDataType.DamageDone,
            start_time=0.0,
            end_time=300000.0
        )

        entries = table.report_data.report.table['data']['entries']
        print(f"Number of players: {len(entries)}")

        # Show top 3 damage dealers
        for i, player in enumerate(entries[:3]):
            print(f"{i+1}. {player['name']} ({player['type']}): {player['total']:,} damage")

asyncio.run(get_damage_table())
```

**Output**:
```
Number of players: 10
1. Rÿañ Røsè (Nightblade): 1,521,248 damage
2. Gabibich (Necromancer): 949,418 damage
3. Zalduk Nightsky (DragonKnight): 498,434 damage
```

### get_report_rankings()

**Purpose**: Get performance rankings from combat reports

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `code` | *str* | Yes | The report code to analyze |
| `compare` | *RankingCompareType* | No | Comparison method for rankings |
| `difficulty` | *int* | No | Difficulty level filter |
| `encounter_id` | *int* | No | Filter to specific encounter |
| `fight_i_ds` | *List[int]* | No | List of fight IDs to include |
| `player_metric` | *ReportRankingMetricType* | No | Ranking metric (dps, hps, playerscore, etc.) |
| `timeframe` | *RankingTimeframeType* | No | Time frame for ranking comparison |

**Returns**: `GetReportRankings` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `report_data.report.rankings` | *dict* | Rankings data containing performance comparisons and percentiles |

> **Note**: The triple nesting (`report_data.report.rankings`) reflects the ESO Logs GraphQL API structure where all report queries are grouped under `reportData` with individual reports accessed via `report(code)`. This structure will be simplified in a future refactor to provide more direct access patterns.

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
            code="VFnNYQjxC3RwGqg1",
            player_metric=ReportRankingMetricType.dps
        )

        ranking_data = rankings.report_data.report.rankings['data'][0]
        encounter = ranking_data['encounter']
        print(f"Encounter: {encounter['name']}")
        print(f"Duration: {ranking_data['duration'] / 1000:.1f} seconds")

        # Show top DPS players
        dps_players = ranking_data['roles']['dps']['characters'][:3]
        print("\nTop DPS Players:")
        for i, player in enumerate(dps_players):
            print(f"{i+1}. {player['name']} ({player['class']}): {player['amount']:,.0f} DPS")

asyncio.run(get_dps_rankings())
```

**Output**:
```
Encounter: Hall of Fleshcraft
Duration: 172.8 seconds

Top DPS Players:
1. Gzerrog (Arcanist): 170,266 DPS
2. Ugabugaugabugaugabugaugab (Arcanist): 158,153 DPS
3. Maciek osmiornica (Arcanist): 150,955 DPS
```

### get_report_player_details()

**Purpose**: Get detailed player performance information from reports

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `code` | *str* | Yes | The report code to analyze |
| `difficulty` | *int* | No | Difficulty level filter |
| `encounter_id` | *int* | No | Filter to specific encounter |
| `end_time` | *float* | No | End time in milliseconds |
| `fight_i_ds` | *List[int]* | No | List of fight IDs to include |
| `kill_type` | *KillType* | No | Filter by kill type |
| `start_time` | *float* | No | Start time in milliseconds |
| `translate` | *bool* | No | Translate ability names |
| `include_combatant_info` | *bool* | No | Include detailed combatant information |

**Returns**: `GetReportPlayerDetails` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `report_data.report.player_details` | *dict* | Player details containing individual performance breakdowns |

> **Note**: The triple nesting (`report_data.report.player_details`) reflects the ESO Logs GraphQL API structure where all report queries are grouped under `reportData` with individual reports accessed via `report(code)`. This structure will be simplified in a future refactor to provide more direct access patterns.

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
            code="VFnNYQjxC3RwGqg1",
            start_time=0.0,
            end_time=300000.0,
            include_combatant_info=True
        )

        details = player_details.report_data.report.player_details['data']['playerDetails']

        # Show healers
        healers = details['healers']
        print(f"Healers ({len(healers)}):")
        for healer in healers:
            print(f"  {healer['name']} (@{healer['displayName']}) - {healer['type']}")

asyncio.run(get_player_performance())
```

**Output**:
```
Healers (2):
  Rÿañ Røsè (@RyanRose) - Nightblade
  Gabibich (@gabibich) - Necromancer
```

## Error Handling

Report analysis endpoints may have specific error cases due to their high cost and data complexity:

```python
from esologs.exceptions import GraphQLClientHttpError, GraphQLClientGraphQLMultiError
from pydantic import ValidationError

try:
    events = await client.get_report_events(
        code="invalid_code",
        data_type=EventDataType.DamageDone,
        start_time=0.0,
        end_time=60000.0
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
import asyncio
from esologs.client import Client
from esologs.enums import GraphDataType, TableDataType, ReportRankingMetricType
from access_token import get_access_token

async def comprehensive_analysis():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        report_code = "VFnNYQjxC3RwGqg1"

        # Get basic report info
        report = await client.get_report_by_code(code=report_code)
        print(f"Report: {report.report_data.report.title}")
        print(f"Zone: {report.report_data.report.zone.name}")

        # Analyze damage over time
        damage_graph = await client.get_report_graph(
            code=report_code,
            data_type=GraphDataType.DamageDone,
            start_time=0.0,
            end_time=300000.0
        )

        # Get damage summary statistics
        damage_table = await client.get_report_table(
            code=report_code,
            data_type=TableDataType.DamageDone,
            start_time=0.0,
            end_time=300000.0
        )

        # Compare performance rankings
        rankings = await client.get_report_rankings(
            code=report_code,
            player_metric=ReportRankingMetricType.dps
        )

        # Get individual player breakdowns
        player_details = await client.get_report_player_details(
            code=report_code,
            start_time=0.0,
            end_time=300000.0
        )

        # Analyze results
        entries = damage_table.report_data.report.table['data']['entries']
        top_dps = entries[0]
        print(f"Top DPS: {top_dps['name']} with {top_dps['total']:,} damage")

        return {
            'report': report,
            'damage_graph': damage_graph,
            'damage_table': damage_table,
            'rankings': rankings,
            'player_details': player_details
        }

asyncio.run(comprehensive_analysis())
```

**Output**:
```
Report: 12/26/24 - Lucent Citadel
Zone: Lucent Citadel
Top DPS: Rÿañ Røsè with 1,521,248 damage
```

### Encounter Phase Analysis

Analyze specific phases of boss encounters:

```python
import asyncio
from esologs.client import Client
from esologs.enums import EventDataType, GraphDataType
from access_token import get_access_token

async def analyze_encounter_phase():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        report_code = "VFnNYQjxC3RwGqg1"
        fight_id = 5  # Red Witch Gedna Relvel
        phase_start = 259178.0
        phase_end = 270000.0  # First part of fight

        print(f"Analyzing fight {fight_id} phase: {phase_start/1000:.1f}-{phase_end/1000:.1f}s")

        # Get events for specific phase
        events = await client.get_report_events(
            code=report_code,
            fight_i_ds=[fight_id],
            start_time=phase_start,
            end_time=phase_end,
            data_type=EventDataType.DamageDone
        )

        # Display event analysis
        if events.report_data.report.events.data:
            event_count = len(events.report_data.report.events.data)
            print(f"Events found: {event_count}")

            # Analyze damage amounts
            damage_amounts = [e['amount'] for e in events.report_data.report.events.data if 'amount' in e]
            if damage_amounts:
                avg_damage = sum(damage_amounts) / len(damage_amounts)
                max_damage = max(damage_amounts)
                print(f"Average damage per event: {avg_damage:.0f}")
                print(f"Maximum single hit: {max_damage:,}")

        # Get phase performance graph
        graph = await client.get_report_graph(
            code=report_code,
            fight_i_ds=[fight_id],
            start_time=phase_start,
            end_time=phase_end,
            data_type=GraphDataType.DamageDone
        )

        # Display graph analysis
        if graph.report_data.report.graph['data']['series']:
            players = graph.report_data.report.graph['data']['series']
            print(f"Players active: {len(players)}")

            # Show top damage dealer in this phase
            if players:
                top_player = max(players, key=lambda p: p['total'])
                print(f"Top damage: {top_player['name']} ({top_player['total']:,})")

asyncio.run(analyze_encounter_phase())
```

**Output**:
```
Analyzing fight 5 phase: 259.2-270.0s
Events found: 300
Average damage per event: 16,237
Maximum single hit: 125,240
Players active: 13
Top damage: Gzerrog (87,312)
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
