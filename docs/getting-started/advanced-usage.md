# Advanced Usage

This guide covers advanced features that help you get the most out of the ESO Logs API while minimizing API calls and maximizing performance.

## Filter Expressions

Filter expressions are one of the most powerful features of the ESO Logs API. They allow you to write SQL-like queries to filter events, dramatically reducing the number of API calls needed and improving performance.

### Why Use Filter Expressions?

Consider this common scenario: You want to track the uptime of multiple buffs during a fight. Without filter expressions, you'd need to make separate API calls for each buff:

```python
# ❌ Inefficient: Multiple API calls
major_courage = await client.get_report_table(
    code="xb7TKHXR8DJByp4Q",
    fight_i_ds=[17],
    ability_id=109966  # Major Courage
)

minor_courage = await client.get_report_table(
    code="xb7TKHXR8DJByp4Q",
    fight_i_ds=[17],
    ability_id=109967  # Minor Courage
)

major_force = await client.get_report_table(
    code="xb7TKHXR8DJByp4Q",
    fight_i_ds=[17],
    ability_id=40225  # Major Force
)
```

With filter expressions, you can get all this data in a single API call:

```python
# ✅ Efficient: Single API call
events = await client.get_report_events(
    code="xb7TKHXR8DJByp4Q",
    fight_i_ds=[17],
    filter_expression="type in ('applybuff', 'removebuff') and ability.id in (109966, 109967, 40225)"
)
```

### Filter Expression Syntax

Filter expressions use a SQL-like syntax with the following operators:

#### Comparison Operators
- `=` - Equals
- `!=` - Not equals
- `<`, `>`, `<=`, `>=` - Numeric comparisons
- `in` - Value is in a list
- `not in` - Value is not in a list

#### Logical Operators
- `and` - Both conditions must be true
- `or` - Either condition must be true
- `not` - Negates a condition
- `()` - Group conditions

#### Available Fields

Common fields you can filter on:

- **Event Fields**
  - `type` - Event type (damage, heal, applybuff, removebuff, death, etc.)
  - `timestamp` - When the event occurred

- **Ability Fields**
  - `ability.id` - Numeric ability ID
  - `ability.name` - Ability name (string)
  - `ability.type` - Ability type

- **Actor Fields**
  - `source.id` - Source actor ID
  - `source.name` - Source actor name
  - `source.type` - Actor type (Player, NPC, etc.)
  - `target.id` - Target actor ID
  - `target.name` - Target actor name
  - `target.type` - Target actor type

### Common Filter Expression Patterns

#### 1. Track Multiple Buffs/Debuffs

```python
# Get all buff/debuff events for specific abilities
filter_expr = """
    type in ('applybuff', 'removebuff', 'applydebuff', 'removedebuff')
    and ability.id in (109966, 109967, 40225, 61737)
"""

events = await client.get_report_events(
    code=report_code,
    filter_expression=filter_expr
)
```

#### 2. Find Damage from Specific Source

```python
# All damage done by a specific player
filter_expr = """
    type = 'damage'
    and source.name = 'PlayerName'
"""

# All damage done by players (not NPCs)
filter_expr = """
    type = 'damage'
    and source.type = 'Player'
"""
```

#### 3. Track Specific Mechanics

```python
# Find all applications of a specific debuff
filter_expr = """
    type = 'applydebuff'
    and ability.name = 'Baneful Mark'
"""

# Find deaths from specific ability
filter_expr = """
    type = 'death'
    and ability.name = 'Poison Injection'
"""
```

#### 4. Complex Filtering

```python
# Healing done by healers excluding self-healing
filter_expr = """
    type = 'heal'
    and source.type = 'Player'
    and source.id != target.id
    and source.name in ('Healer1', 'Healer2')
"""

# Major buffs on tanks only
filter_expr = """
    type = 'applybuff'
    and ability.name like 'Major %'
    and target.name in ('Tank1', 'Tank2')
"""
```

### Complete Example: Buff Uptime Tracker

Here's a complete example that tracks buff uptimes efficiently:

```python
import asyncio
from typing import Dict, List
from esologs import Client
from esologs.auth import get_access_token

async def calculate_buff_uptimes(
    events: List[Dict],
    start_time: float,
    end_time: float
) -> Dict[int, Dict[int, float]]:
    """Calculate buff uptimes from event data."""
    # Track active buffs: source_id -> ability_id -> timestamp
    active_buffs: Dict[int, Dict[int, float]] = {}
    # Track total uptimes: source_id -> ability_id -> seconds
    uptimes: Dict[int, Dict[int, float]] = {}

    for event in events:
        source_id = event.get('sourceID', 0)
        ability_id = event.get('abilityGameID', 0)
        timestamp = event.get('timestamp', 0)
        event_type = event.get('type', '')

        if source_id == 0 or ability_id == 0:
            continue

        # Initialize tracking dicts
        if source_id not in active_buffs:
            active_buffs[source_id] = {}
            uptimes[source_id] = {}
        if ability_id not in uptimes[source_id]:
            uptimes[source_id][ability_id] = 0.0

        if event_type == 'applybuff':
            # Start tracking this buff
            active_buffs[source_id][ability_id] = timestamp
        elif event_type == 'removebuff':
            # Calculate duration and add to total
            if ability_id in active_buffs[source_id]:
                duration = (timestamp - active_buffs[source_id][ability_id]) / 1000.0
                uptimes[source_id][ability_id] += duration
                del active_buffs[source_id][ability_id]

    # Handle buffs still active at fight end
    for source_id, buffs in active_buffs.items():
        for ability_id, start in buffs.items():
            duration = (end_time - start) / 1000.0
            uptimes[source_id][ability_id] += duration

    return uptimes

async def main():
    # Setup
    token = get_access_token()
    client = Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Report parameters
    report_code = "xb7TKHXR8DJByp4Q"
    fight_id = 17
    start_time = 2614035
    end_time = 2777081

    # Track multiple buffs efficiently
    buff_ids = [
        109966,  # Major Courage
        109967,  # Minor Courage
        40225,   # Major Force
        61737,   # Minor Force
    ]

    # Build filter expression
    filter_expr = f"""
        type in ('applybuff', 'removebuff')
        and ability.id in ({','.join(map(str, buff_ids))})
    """

    # Single API call for all buffs
    response = await client.get_report_events(
        code=report_code,
        fight_i_ds=[fight_id],
        start_time=start_time,
        end_time=end_time,
        filter_expression=filter_expr
    )

    # Calculate uptimes
    events = response.report_data.report.events.data
    uptimes = await calculate_buff_uptimes(events, start_time, end_time)

    # Display results
    fight_duration = (end_time - start_time) / 1000.0
    print(f"Fight Duration: {fight_duration:.1f}s\n")

    for source_id, buffs in uptimes.items():
        print(f"Player {source_id}:")
        for ability_id, uptime in buffs.items():
            percentage = (uptime / fight_duration) * 100
            print(f"  Ability {ability_id}: {uptime:.1f}s ({percentage:.1f}%)")

if __name__ == "__main__":
    asyncio.run(main())
```

### Performance Benefits

Using filter expressions provides several performance benefits:

1. **Reduced API Calls**: Get data for multiple conditions in one request
2. **Lower API Point Usage**: Each API call consumes points based on data processed
3. **Faster Response Times**: Server-side filtering is more efficient
4. **Simplified Code**: Less code to maintain and debug

### Tips for Writing Filter Expressions

1. **Test with Small Datasets First**: Start with short time ranges to verify your filter works correctly

2. **Use Specific Conditions**: The more specific your filter, the less data returned and processed

3. **Combine Related Queries**: If you need multiple types of related data, try to get them in one call

4. **Watch for Typos**: Filter expressions are strings, so typos won't be caught until runtime

5. **Check API Documentation**: The [ESO Logs API documentation](https://www.esologs.com/v2-api-docs/eso/) has the complete list of filterable fields

### When to Use Filter Expressions

Filter expressions are ideal for:
- Tracking multiple buffs/debuffs
- Analyzing specific mechanics
- Finding events from specific sources
- Complex event analysis
- Reducing API call count

They may not be necessary for:
- Simple single-ability queries
- When you need all events anyway
- Initial data exploration (start broad, then filter)

## Other Advanced Features

### Pagination for Large Datasets

When dealing with reports that have thousands of events:

```python
# Use limit and startTime for pagination
all_events = []
start_time = fight_start
batch_size = 1000

while True:
    response = await client.get_report_events(
        code=report_code,
        start_time=start_time,
        limit=batch_size
    )

    events = response.report_data.report.events.data
    if not events:
        break

    all_events.extend(events)

    # Get the timestamp of the last event for next batch
    start_time = events[-1]['timestamp'] + 1

    # Avoid infinite loops
    if len(events) < batch_size:
        break
```

### Using Multiple Data Types

Some methods support multiple data types in a single call:

```python
from esologs import EventDataType

# Get both damage and healing in one call
response = await client.get_report_events(
    code=report_code,
    filter_expression="type in ('damage', 'heal')"
)
```

### Time-Window Analysis

Analyze specific phases of a fight:

```python
# Boss phase 2 only (timestamps in milliseconds)
phase2_start = start_time + (60 * 1000)  # 1 minute in
phase2_end = start_time + (180 * 1000)   # 3 minutes in

events = await client.get_report_events(
    code=report_code,
    start_time=phase2_start,
    end_time=phase2_end,
    filter_expression="type = 'damage' and target.name = 'Boss Name'"
)
```

## Next Steps

- Explore the [API Reference](../api-reference/index.md) for detailed method documentation
- Check out the [examples directory](https://github.com/knowlen/esologs-python/tree/main/examples) for more complex usage patterns
- Join the [ESO Logs Discord](https://discord.gg/esologs) for API discussions and help
