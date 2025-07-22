# Progress Race API

Access world/realm first achievement race tracking data in ESO.

## Overview

| Feature | Details |
|---------|---------|
| **API Coverage** | 1/1 endpoints (100%) |
| **Common Use Cases** | Track world first races, monitor guild progression, analyze competition standings |
| **Rate Limit Impact** | Low - 1 point per query |

The Progress Race API provides access to real-time tracking data for world/realm first achievement races in Elder Scrolls Online. This data is particularly valuable during new content releases when guilds compete to be the first to complete challenging content.

!!! warning "API Availability"
    Progress race data is only available when there is an active race. Outside of active progression periods, the API will raise a `GraphQLClientGraphQLMultiError` with the message "No race supported for this game currently".

## Methods

### get_progress_race()

Retrieve progress race data with flexible filtering options.

**Purpose**: Get current standings and completion times for world/realm first races.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| guild_id | int | No | Filter to a specific guild |
| zone_id | int | No | Zone to check (defaults to latest) |
| competition_id | int | No | Specific competition (defaults to world first) |
| difficulty | int | No | Difficulty level (defaults to highest) |
| size | int | No | Raid size (defaults to standard for difficulty) |
| server_region | str | No | Server region (e.g., "NA", "EU") |
| server_subregion | str | No | Server subregion (requires server_region) |
| server_slug | str | No | Server identifier |
| guild_name | str | No | Guild name (use with server filters) |

**Returns**: Progress race data as JSON (format varies based on active race)

**Example**:

```python
import asyncio
from esologs import Client

async def track_progress_race():
    async with Client(
        client_id="your_client_id",
        client_secret="your_client_secret"
    ) as client:
        # Get current progress race standings
        race_data = await client.get_progress_race(
            zone_id=40,  # Lucent Citadel
            difficulty=2,  # Veteran
            size=12        # 12-person
        )

        if race_data.progress_race_data.progress_race:
            print("Active race data:", race_data.progress_race_data.progress_race)
        else:
            print("No active race for these parameters")

asyncio.run(track_progress_race())
```

**Output**:

```json
{
    "rankings": [
        {
            "guild": {
                "id": 123,
                "name": "Elite Guild",
                "faction": "Aldmeri Dominion"
            },
            "duration": 3600000,
            "completionTime": 1640000000000,
            "rank": 1
        }
    ]
}
```

## Common Usage Patterns

### Track Guild Progress

Monitor a specific guild's progress in the current race:

```python
async def track_guild_progress(guild_id: int):
    async with Client(
        client_id="your_client_id",
        client_secret="your_client_secret"
    ) as client:
        # Check guild's standing
        result = await client.get_progress_race(
            guild_id=guild_id,
            zone_id=40  # Current progression zone
        )

        if result.progress_race_data.progress_race:
            data = result.progress_race_data.progress_race
            print(f"Guild progress data: {data}")
        else:
            print("Guild has not completed or no active race")
```

### Monitor Server Competition

Track progress race standings for a specific server:

```python
async def monitor_server_race(region: str = "NA"):
    async with Client(
        client_id="your_client_id",
        client_secret="your_client_secret"
    ) as client:
        # Get server-specific standings
        result = await client.get_progress_race(
            server_region=region,
            server_slug="megaserver",
            zone_id=40,
            difficulty=2,
            size=12
        )

        if result.progress_race_data.progress_race:
            standings = result.progress_race_data.progress_race
            print(f"{region} server standings:", standings)
```

### Check Multiple Difficulties

Compare progress across different difficulty levels:

```python
async def compare_difficulties(zone_id: int):
    async with Client(
        client_id="your_client_id",
        client_secret="your_client_secret"
    ) as client:
        difficulties = {
            1: "Normal",
            2: "Veteran"
        }

        for diff_id, diff_name in difficulties.items():
            result = await client.get_progress_race(
                zone_id=zone_id,
                difficulty=diff_id,
                size=12
            )

            if result.progress_race_data.progress_race:
                print(f"{diff_name} standings:",
                      result.progress_race_data.progress_race)
```

## Error Handling

Progress race queries will raise `GraphQLClientGraphQLMultiError` when no race is active:

```python
from esologs._generated.exceptions import GraphQLClientGraphQLMultiError

async def safe_progress_check():
    async with Client(
        client_id="your_client_id",
        client_secret="your_client_secret"
    ) as client:
        try:
            result = await client.get_progress_race(zone_id=40)

            # Process race data if available
            if result.progress_race_data.progress_race:
                race_data = result.progress_race_data.progress_race
                print(f"Race data: {race_data}")
            else:
                print("No race data in response")

        except GraphQLClientGraphQLMultiError as e:
            # This is expected when no race is active
            if "No race supported for this game currently" in str(e):
                print("No active race for Elder Scrolls Online")
            else:
                print(f"GraphQL error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
```

## Best Practices

1. **Handle GraphQL Errors**: Always catch `GraphQLClientGraphQLMultiError` when calling progress race methods
2. **Check for Active Races**: The API will throw an error when no race is active for the game
3. **Cache Results**: During active races, cache results for a few minutes to reduce API calls
4. **Use Appropriate Filters**: Apply zone and difficulty filters to get relevant data
5. **Handle Dynamic Schema**: The JSON response format may vary - write flexible parsing code

## Rate Limiting

Progress race queries are lightweight:

- Each query costs 1 point
- Safe to poll periodically during active races
- Consider caching results for 5-10 minutes during competitions

## Notes

- Progress race data is only available during active world/realm first competitions
- When no race is active, the API raises `GraphQLClientGraphQLMultiError` with message "No race supported for this game currently"
- The JSON response structure is not frozen and may change without notice
- Competition IDs and their meanings are not documented in the public API
- Default values (latest zone, highest difficulty) are applied when parameters are omitted
