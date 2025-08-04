# Enums

## Overview

Enums (Enumerations) in ESO Logs Python provide type-safe constants for various API parameters. They represent fixed sets of allowed values defined by the ESO Logs GraphQL schema, ensuring that your code uses valid options and catches errors at development time rather than runtime.

### Why Use Enums?

1. **Type Safety**: Your IDE and type checker will catch invalid values before you run your code
2. **Autocomplete**: Get intelligent suggestions as you type, showing all valid options
3. **Self-Documenting**: Enum names clearly indicate what values are acceptable
4. **Validation**: The API will reject invalid values, but using enums prevents these errors entirely

### Basic Usage

```python
from esologs import Client, EventDataType, HostilityType
from esologs.auth import get_access_token

async def analyze_combat():
    token = get_access_token()
    client = Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Using enums for type-safe queries
    events = await client.get_report_events(
        code="abc123",
        data_type=EventDataType.DamageDone,  # ✅ Type-safe with autocomplete
        hostility_type=HostilityType.Enemies  # ✅ IDE will show available options
    )

    # String values also work but lose benefits
    events2 = await client.get_report_events(
        code="abc123",
        data_type="DamageDone",  # ⚠️ Works but no validation/autocomplete
    )
```

### Importing Enums

All enums are available from the main package:

```python
from esologs import (
    EventDataType,
    TableDataType,
    GraphDataType,
    CharacterRankingMetricType,
    HostilityType,
    RoleType,
    KillType,
    # ... and more
)
```

---

## Available Enums

### CharacterRankingMetricType

Metrics available for character rankings and leaderboards.

**Values:**

- `dps` - Damage per second
- `hps` - Healing per second
- `playerscore` - Overall performance score
- `playerspeed` - Clear time performance

**Used by:**
- [`get_character_encounter_rankings`](character-data.md#get_character_encounter_rankings)
- [`get_character_zone_rankings`](character-data.md#get_character_zone_rankings)

---

### EventDataType

Types of events that can be filtered when retrieving report events.

**Values:**

- `All` - All event types
- `Buffs` - Buff application events
- `Casts` - Ability cast events
- `CombatantInfo` - Combatant information
- `DamageDone` - Damage dealt events
- `DamageTaken` - Damage received events
- `Deaths` - Death events
- `Debuffs` - Debuff application events
- `Dispels` - Dispel events
- `Healing` - Healing events
- `Interrupts` - Interrupt events
- `Resources` - Resource changes (magicka, stamina)
- `Summons` - Pet/summon events
- `Threat` - Threat/aggro events

**Used by:**
- [`get_report_events`](report-data.md#get_report_events)

---

### ExternalBuffRankFilter

Filter for rankings based on external buff usage.

**Values:**

- `include` - Include rankings with external buffs
- `exclude` - Exclude rankings with external buffs
- `require` - Only show rankings with external buffs

**Used by:**
- [`get_character_encounter_rankings`](character-data.md#get_character_encounter_rankings)
- [`get_character_zone_rankings`](character-data.md#get_character_zone_rankings)

---

### FightRankingMetricType

Metrics available for fight-specific rankings.

**Values:**

- `default` - Default ranking metric
- `bossdps` - Boss damage per second
- `bossrdps` - Boss rDPS (raid-contributing DPS)
- `execution` - Execution score
- `feats` - Feats of strength
- `krsi` - Kill speed index
- `playerscore` - Player performance score
- `playerspeed` - Clear time performance
- `speed` - Clear speed

**Used by:**
- [`get_report_rankings`](report-data.md#get_report_rankings)

---

### GraphDataType

Types of data available for time-series graphs.

**Values:**

- `Buffs` - Buff uptime over time
- `Casts` - Cast timeline
- `DamageDone` - Damage output graph
- `DamageTaken` - Damage taken graph
- `Deaths` - Death timeline
- `Debuffs` - Debuff uptime over time
- `Dispels` - Dispel timeline
- `Healing` - Healing output graph
- `Interrupts` - Interrupt timeline
- `Resources` - Resource levels over time
- `Summons` - Summon timeline
- `Threat` - Threat over time

**Used by:**
- [`get_report_graph`](report-data.md#get_report_graph)

---

### GuildRank

Guild member rank levels.

**Values:**

- `Recruit` - New guild member
- `Member` - Standard member
- `Officer` - Guild officer
- `GuildMaster` - Guild leader

**Used by:**
- [`get_guild_members`](guild-data.md#get_guild_members)

---

### HardModeLevelRankFilter

Filter for rankings based on hard mode completion.

**Values:**

- `any` - Any difficulty level
- `highest` - Highest difficulty only
- `lowest` - Base difficulty only

**Used by:**
- [`get_character_encounter_rankings`](character-data.md#get_character_encounter_rankings)
- [`get_character_zone_rankings`](character-data.md#get_character_zone_rankings)

---

### HostilityType

Filter events by hostility relationship.

**Values:**

- `Friendlies` - Friendly targets (allies, self)
- `Enemies` - Hostile targets

**Used by:**
- [`get_report_events`](report-data.md#get_report_events)
- [`get_report_graph`](report-data.md#get_report_graph)
- [`get_report_table`](report-data.md#get_report_table)

---

### KillType

Filter data by encounter outcome.

**Values:**

- `Encounters` - All encounter attempts
- `Kills` - Successful kills only
- `Wipes` - Failed attempts only

**Used by:**
- [`get_report_events`](report-data.md#get_report_events)
- [`get_report_graph`](report-data.md#get_report_graph)
- [`get_report_table`](report-data.md#get_report_table)

---

### LeaderboardRank

Leaderboard ranking tiers.

**Values:**

- `Any` - Any rank
- `Blue` - Blue rank (uncommon)
- `Gold` - Gold rank (legendary)
- `Green` - Green rank (common)
- `Orange` - Orange rank (rare)
- `Purple` - Purple rank (epic)

**Used by:**
- [`get_character_encounter_rankings`](character-data.md#get_character_encounter_rankings)
- [`get_character_zone_rankings`](character-data.md#get_character_zone_rankings)

---

### RankingCompareType

How to compare rankings.

**Values:**

- `Rankings` - Compare by rank position
- `Parses` - Compare by performance percentile

**Used by:**
- [`get_character_encounter_rankings`](character-data.md#get_character_encounter_rankings)
- [`get_character_zone_rankings`](character-data.md#get_character_zone_rankings)

---

### RankingTimeframeType

Time period for rankings.

**Values:**

- `Current` - Current patch/season
- `Historical` - All-time historical

**Used by:**
- [`get_character_encounter_rankings`](character-data.md#get_character_encounter_rankings)
- [`get_character_zone_rankings`](character-data.md#get_character_zone_rankings)

---

### ReportRankingMetricType

Metrics for report-level rankings.

**Values:**

- `bossdps` - Boss damage per second
- `bossrdps` - Boss rDPS
- `default` - Default metric
- `dps` - Damage per second
- `hps` - Healing per second
- `krsi` - Kill speed index
- `playerscore` - Player score
- `rdps` - Raid-contributing DPS
- `tankhps` - Tank healing per second

**Used by:**
- [`get_report_rankings`](report-data.md#get_report_rankings)
- [`get_report_player_details`](report-data.md#get_report_player_details)

---

### RoleType

Character role classifications.

**Values:**

- `Tank` - Tank role
- `Healer` - Healer role
- `DPS` - Damage dealer role

**Used by:**
- [`get_character_encounter_rankings`](character-data.md#get_character_encounter_rankings)
- [`get_character_zone_rankings`](character-data.md#get_character_zone_rankings)

---

### SubscriptionStatus

User subscription status levels.

**Values:**

- `Free` - Free tier user
- `Silver` - Silver subscription
- `Gold` - Gold subscription
- `Platinum` - Platinum subscription
- `LegacyGold` - Legacy gold status
- `LegacyPlatinum` - Legacy platinum status

**Used by:**
- [`get_current_user`](user-data.md#get_current_user)
- [`get_user_by_id`](user-data.md#get_user_by_id)

---

### TableDataType

Types of data available in tabular format.

**Values:**

- `Buffs` - Buff uptime statistics
- `Casts` - Cast counts and timings
- `DamageDone` - Damage dealt breakdown
- `DamageTaken` - Damage taken analysis
- `Deaths` - Death log
- `Debuffs` - Debuff uptime statistics
- `Dispels` - Dispel counts
- `Healing` - Healing breakdown
- `Interrupts` - Interrupt counts
- `Resources` - Resource generation/usage
- `Summons` - Summon statistics
- `Threat` - Threat generation

**Used by:**
- [`get_report_table`](report-data.md#get_report_table)

---

### ViewType

Perspective for viewing data.

**Values:**

- `Default` - Default view
- `Ability` - Group by ability
- `Source` - Group by source
- `Target` - Group by target

**Used by:**
- [`get_report_graph`](report-data.md#get_report_graph)
- [`get_report_table`](report-data.md#get_report_table)

---

## Best Practices

### 1. Always Import What You Need

```python
# Good - explicit imports
from esologs import EventDataType, HostilityType

# Avoid - importing everything
from esologs import *
```

### 2. Use Enums for Type Safety

```python
# Good - type-safe with IDE support
events = await client.get_report_events(
    code="abc",
    data_type=EventDataType.DamageDone
)

# Less ideal - no compile-time checking
events = await client.get_report_events(
    code="abc",
    data_type="DamageDone"
)
```

### 3. Leverage Your IDE

Modern IDEs will show available enum values as you type:

```python
# Type "EventDataType." and your IDE shows:
# - EventDataType.All
# - EventDataType.Buffs
# - EventDataType.Casts
# ... etc
```

### 4. Enum Values Are Strings

All enum values are strings, so you can use them anywhere a string is expected:

```python
# This works
print(f"Fetching {EventDataType.DamageDone} events...")
# Output: "Fetching DamageDone events..."

# Comparison works
if data_type == EventDataType.DamageDone:
    print("Processing damage events")
```
