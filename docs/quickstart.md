# Quickstart

Get up and running with ESO Logs Python in 5 minutes.

## Prerequisites

Before starting, ensure you have:

1. ✅ [Installed ESO Logs Python](installation.md)
2. ✅ [Set up authentication](authentication.md) with valid API credentials
3. ✅ Python 3.8+ environment

!!! note "Prerequisites for Code Examples"
    All code examples require:

    1. **Valid API credentials** set as environment variables:
       ```bash
       export ESOLOGS_ID="your_client_id"
       export ESOLOGS_SECRET="your_client_secret"
       ```
       Get your credentials from [esologs.com/v2-api-docs](https://www.esologs.com/v2-api-docs)

    2. **Access to `access_token.py`** - Examples assume this module is available in your project.
       If running outside the project directory, replace `from access_token import get_access_token`
       with your own authentication implementation.

## Your First API Call

Let's start with a simple example to verify everything is working:

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def hello_esologs():
    """Your first ESO Logs API call."""
    # Get authentication token
    token = get_access_token()

    # Create client
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Check rate limits
        rate_limit = await client.get_rate_limit_data()
        print(f"✅ Connected to ESO Logs API")
        print(f"Rate limit: {rate_limit.rate_limit_data.limit_per_hour}/hour")
        print(f"Points used: {rate_limit.rate_limit_data.points_spent_this_hour}")

# Run the example
asyncio.run(hello_esologs())
```

**Output:**
```
✅ Connected to ESO Logs API
Rate limit: 720/hour
Points used: 0
```

## Core Concepts

### Async/Await Pattern

ESO Logs Python is built for async programming:

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def main():
    token = get_access_token()

    # All API calls are async
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        abilities = await client.get_abilities(limit=5)
        print(f"✅ Got {len(abilities.game_data.abilities.data)} abilities")

        for ability in abilities.game_data.abilities.data:
            print(f"  - {ability.name}")

# Always use asyncio.run() for the main entry point
asyncio.run(main())
```

**Output:**
```
✅ Got 5 abilities
  - Crystal Weapon
  - Crystal Blast
  - Endless Hail
  - Arrow Barrage
  - Acid Spray
```

### Client Context Manager

Use the client as a context manager for proper resource cleanup:

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def main():
    token = get_access_token()

    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        # Client automatically closes connections when done
        character = await client.get_character_by_id(34663)
        print(f"✅ Got character: {character.character_data.character.name}")
        print(f"Server: {character.character_data.character.server.name}")

asyncio.run(main())
```

**Output:**
```
✅ Got character: Godslayer Fox
Server: NA
```

### Error Handling

ESO Logs Python provides detailed error information:

```python
import asyncio
from esologs.client import Client
from esologs.exceptions import GraphQLClientHttpError, GraphQLClientGraphQLError, ValidationError
from access_token import get_access_token

async def safe_api_call():
    token = get_access_token()

    try:
        async with Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": f"Bearer {token}"}
        ) as client:
            # Try to get a character that might not exist
            character = await client.get_character_by_id(99999999)
            print(f"✅ Got character: {character.character_data.character.name}")

    except GraphQLClientHttpError as e:
        if e.status_code == 401:
            print("❌ Authentication failed - check your API credentials")
        elif e.status_code == 429:
            print("❌ Rate limit exceeded - try again later")
        elif e.status_code == 404:
            print("❌ Character not found")
        else:
            print(f"❌ HTTP error {e.status_code}")
    except GraphQLClientGraphQLError as e:
        print(f"❌ GraphQL error: {e}")
    except ValidationError as e:
        print(f"❌ Parameter validation error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

asyncio.run(safe_api_call())
```

**Output:**
```
❌ GraphQL error: [{'message': 'Character not found', 'path': ['characterData', 'character']}]
```

## Common Usage Patterns

### Game Data Exploration

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def explore_game_data():
    """Explore ESO's game data."""
    token = get_access_token()

    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get abilities with pagination
        abilities = await client.get_abilities(limit=5, page=1)
        print(f"Found {len(abilities.game_data.abilities.data)} abilities:")

        for ability in abilities.game_data.abilities.data:
            print(f"  - {ability.name}")

        # Get character classes
        classes = await client.get_classes()
        print(f"\nCharacter classes:")
        for cls in classes.game_data.classes:
            print(f"  - {cls.name}")

        # Get zones
        zones = await client.get_zones()
        print(f"\nZones ({len(zones.world_data.zones)} total):")
        for zone in zones.world_data.zones[:5]:  # Show first 5
            print(f"  - {zone.name}")

asyncio.run(explore_game_data())
```

**Output:**
```
Found 5 abilities:
  - Crystal Weapon
  - Crystal Blast
  - Endless Hail
  - Arrow Barrage
  - Acid Spray

Character classes:
  - Dragonknight
  - Sorcerer
  - Nightblade
  - Templar
  - Warden
  - Necromancer
  - Arcanist

Zones (48 total):
  - Hel Ra Citadel
  - Aetherian Archive
  - Sanctum Ophidia
  - Maw of Lorkhaj
  - Halls of Fabrication
```

### Character Analysis

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def analyze_character():
    """Analyze a specific character."""
    token = get_access_token()

    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        character_id = 34663  # Example character ID

        # Get character profile
        character = await client.get_character_by_id(id=character_id)
        char_data = character.character_data.character

        print(f"Character: {char_data.name}")
        print(f"Server: {char_data.server.name}")
        print(f"Class ID: {char_data.class_id}")
        print(f"Race ID: {char_data.race_id}")

        # Get recent reports
        reports = await client.get_character_reports(
            character_id=character_id,
            limit=3
        )

        print(f"\nRecent Reports ({len(reports.character_data.character.recent_reports.data)}):")
        for report in reports.character_data.character.recent_reports.data:
            duration = (report.end_time - report.start_time) / 1000  # Convert to seconds
            print(f"  - {report.code}: {report.zone.name} ({duration:.0f}s)")

asyncio.run(analyze_character())
```

**Output:**
```
Character: Godslayer Fox
Server: NA
Class ID: 5
Race ID: 5

Recent Reports (3):
  - VfxqaX47HGC98rAp: Sunspire (1875s)
  - 8vxG4NRJmLWCqQTP: Cloudrest (1102s)
  - Jq9wXpNrcDmH7L6V: Rockgrove (2943s)
```

### Report Search

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def search_reports():
    """Search for reports with filtering."""
    token = get_access_token()

    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Search reports from a specific guild
        reports = await client.search_reports(
            guild_id=3660,  # Example guild ID
            zone_id=8,      # Example zone ID (Sunspire)
            limit=5
        )

        if reports.report_data and reports.report_data.reports:
            print(f"Found {len(reports.report_data.reports.data)} reports:")

            for report in reports.report_data.reports.data:
                duration = (report.end_time - report.start_time) / 1000
                print(f"  - {report.code}: {report.zone.name} ({duration:.0f}s)")
        else:
            print("No reports found")

asyncio.run(search_reports())
```

**Output:**
```
Found 5 reports:
  - VfxqaX47HGC98rAp: Sunspire (1875s)
  - T9nPJq2XL7CRxwVF: Sunspire (2134s)
  - K4mGx8YvQNWPjBLR: Sunspire (1998s)
  - H7bQZnR3KcJYMfXw: Sunspire (2567s)
  - N2vLXpT4WqGRmDzJ: Sunspire (1789s)
```

## Working with Data

### Type Safety

All responses use Pydantic models for type safety:

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def type_safe_example():
    """Demonstrate type safety with Pydantic models."""
    token = get_access_token()

    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Response is fully typed
        abilities = await client.get_abilities(limit=3)

        # IDE will provide autocomplete and type checking
        print("Ability details:")
        for ability in abilities.game_data.abilities.data:
            print(f"\nAbility: {ability.name}")
            print(f"  ID: {ability.id}")
            print(f"  Icon: {ability.icon}")
            # ability.unknown_field  # This would cause a type error

asyncio.run(type_safe_example())
```

**Output:**
```
Ability details:

Ability: Crystal Weapon
  ID: 143808
  Icon: /common/icon/ability_psijic_005_a.dds

Ability: Crystal Blast
  ID: 143876
  Icon: /common/icon/ability_psijic_005_b.dds

Ability: Endless Hail
  ID: 28794
  Icon: /common/icon/ability_bow_003_b.dds
```

### Data Validation

ESO Logs Python validates all parameters:

```python
import asyncio
from esologs.client import Client
from esologs.exceptions import ValidationError
from access_token import get_access_token

async def validation_example():
    """Show parameter validation in action."""
    token = get_access_token()

    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        try:
            # This will validate parameters before making the API call
            reports = await client.search_reports(
                limit=25,        # Valid: 1-25
                page=1,          # Valid: >= 1
                start_time=1640995200000  # Valid timestamp
            )
            print("✅ Parameter validation passed")
            print(f"Found {len(reports.report_data.reports.data)} reports")
        except ValidationError as e:
            print(f"❌ Parameter validation error: {e}")

asyncio.run(validation_example())
```

**Output:**
```
✅ Parameter validation passed
Found 25 reports
```

## Practical Examples

### Build a Character Dashboard

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def character_dashboard(character_id: int):
    """Create a simple character dashboard."""
    token = get_access_token()

    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        print("🏴󠁧󠁢󠁥󠁮󠁧󠁿 ESO Character Dashboard")
        print("=" * 40)

        # Get character info
        character = await client.get_character_by_id(id=character_id)
        char_data = character.character_data.character

        print(f"Name: {char_data.name}")
        print(f"Server: {char_data.server.name}")
        print(f"Class ID: {char_data.class_id}")
        print(f"Race ID: {char_data.race_id}")

        # Get recent activity
        reports = await client.get_character_reports(character_id=character_id, limit=3)

        print(f"\n📊 Recent Activity:")
        for report in reports.character_data.character.recent_reports.data:
            duration = (report.end_time - report.start_time) / 1000
            print(f"  • {report.zone.name} - {duration:.0f}s")

        # You could add rankings, performance metrics, etc.
        print(f"\n💡 Use character ID {character_id} to explore more data!")

# Run with example character ID
asyncio.run(character_dashboard(34663))
```

**Output:**
```
🏴󠁧󠁢󠁥󠁮󠁧󠁿 ESO Character Dashboard
========================================
Name: Godslayer Fox
Server: NA
Class ID: 5
Race ID: 5

📊 Recent Activity:
  • Sunspire - 1875s
  • Cloudrest - 1102s
  • Rockgrove - 2943s

💡 Use character ID 34663 to explore more data!
```

### Monitor Guild Activity

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def guild_monitor(guild_id: int):
    """Monitor recent guild activity."""
    token = get_access_token()

    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get guild info
        guild = await client.get_guild_by_id(guild_id=guild_id)
        guild_data = guild.guild_data.guild

        print(f"🏰 Guild: {guild_data.name}")
        print(f"Server: {guild_data.server.name}")

        # Get recent guild reports
        reports = await client.get_guild_reports(guild_id=guild_id, limit=5)

        if reports.report_data and reports.report_data.reports:
            print(f"\n📈 Recent Reports:")
            for report in reports.report_data.reports.data:
                duration = (report.end_time - report.start_time) / 1000
                print(f"  • {report.code}: {report.zone.name} ({duration:.0f}s)")
        else:
            print("\nNo recent reports found")

# Run with example guild ID
asyncio.run(guild_monitor(3660))
```

**Output:**
```
🏰 Guild: Hodor
Server: NA

📈 Recent Reports:
  • VfxqaX47HGC98rAp: Sunspire (1875s)
  • T9nPJq2XL7CRxwVF: Cloudrest (1102s)
  • K4mGx8YvQNWPjBLR: Rockgrove (2943s)
  • H7bQZnR3KcJYMfXw: Kyne's Aegis (2567s)
  • N2vLXpT4WqGRmDzJ: Dreadsail Reef (3421s)
```

## Next Steps

Now that you're familiar with the basics:

### API Reference & Examples

- **[Game Data API](api-reference/game-data.md)** - Abilities, items, classes with examples
- **[Character Data API](api-reference/character-data.md)** - Profiles, reports, and rankings with examples
- **[Report Analysis API](api-reference/report-analysis.md)** - Combat log deep-dives with examples
- **[Report Search API](api-reference/report-search.md)** - Advanced filtering with examples
- **[System APIs](api-reference/system.md)** - Rate limiting and error handling with examples

### Development

- **[Testing Guide](development/testing.md)** - Test your integrations
- **[Contributing](development/contributing.md)** - Help improve the library

## Tips for Success

### Performance

- Use pagination for large datasets
- Cache frequently accessed data
- Monitor your rate limit usage

### Error Handling

- Always wrap API calls in try/catch
- Handle authentication and rate limit errors gracefully
- Log errors for debugging

### Best Practices

- Use environment variables for credentials
- Implement proper async patterns
- Validate user input before API calls

!!! tip "Real Data"
    Replace the example IDs (12345, 123, etc.) with real character, guild, and zone IDs
    from [esologs.com](https://www.esologs.com/) to see actual data.

!!! info "Rate Limits"
    Monitor your API usage with `get_rate_limit_data()` to avoid hitting limits.
    Each API call consumes points from your hourly quota.
