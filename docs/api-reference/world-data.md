# World Data API

Access ESO world information including encounters, zones, regions, and dungeon/trial data through the ESO Logs API.

## Overview

- **Coverage**: 3 endpoints implemented
- **Use Cases**: Encounter analysis, zone information, dungeon/trial research, region mapping
- **Rate Limit Impact**: 1-3 points per request (varies by complexity)

## Methods

### get_zones()

**Purpose**: Retrieve all available zones (dungeons, trials, arenas) with their encounters and difficulty settings

**Parameters**: None

**Returns**: `GetZones` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| world_data.zones | List[Zone] | List of zone objects |
| world_data.zones[].id | int | Zone ID |
| world_data.zones[].name | str | Zone name |
| world_data.zones[].frozen | bool | Whether zone rankings are frozen |
| world_data.zones[].expansion | Expansion | Expansion information |
| world_data.zones[].expansion.id | int | Expansion ID |
| world_data.zones[].expansion.name | str | Expansion name |
| world_data.zones[].encounters | List[Encounter] \| None | List of encounters in this zone |
| world_data.zones[].encounters[].id | int | Encounter ID |
| world_data.zones[].encounters[].name | str | Encounter name |
| world_data.zones[].difficulties | List[Difficulty] \| None | Available difficulty levels |
| world_data.zones[].difficulties[].id | int | Difficulty ID |
| world_data.zones[].difficulties[].name | str | Difficulty name (e.g., "Normal", "Veteran", "Veteran Hard Mode") |
| world_data.zones[].difficulties[].sizes | List[int] | Group sizes for this difficulty |
| world_data.zones[].brackets | Brackets \| None | Ranking brackets information |

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def list_zones():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        zones = await client.get_zones()
        print(f"Found {len(zones.world_data.zones)} zones")
        
        # Show first few zones with their encounters
        for zone in zones.world_data.zones[:3]:
            print(f"\n{zone.name} (ID: {zone.id})")
            print(f"  Expansion: {zone.expansion.name}")
            print(f"  Frozen: {zone.frozen}")
            
            if zone.difficulties:
                print(f"  Difficulties: {', '.join([d.name for d in zone.difficulties])}")
            
            if zone.encounters:
                print(f"  Encounters ({len(zone.encounters)}):")
                for encounter in zone.encounters[:3]:
                    print(f"    - {encounter.name} (ID: {encounter.id})")
                if len(zone.encounters) > 3:
                    print(f"    ... and {len(zone.encounters) - 3} more")

asyncio.run(list_zones())
```

**Output**:
```
Found 18 zones

Dungeons (ID: 10)
  Expansion: Test Expansion
  Frozen: False
  Difficulties: Veteran Hard Mode, Veteran, Normal
  Encounters (56):
    - Fungal Grotto I (ID: 2000)
    - Fungal Grotto II (ID: 2001)
    - Spindleclutch I (ID: 2002)
    ... and 53 more

Trials (ID: 20)
  Expansion: Test Expansion
  Frozen: False
  Difficulties: Veteran Hard Mode, Veteran, Normal
  Encounters (16):
    - Aetherian Archive (ID: 1000)
    - Hel Ra Citadel (ID: 1001)
    - Sanctum Ophidia (ID: 1002)
    ... and 13 more

Arenas (ID: 30)
  Expansion: Test Expansion
  Frozen: False
  Difficulties: Veteran, Normal
  Encounters (4):
    - Dragonstar Arena (ID: 3000)
    - Maelstrom Arena (ID: 3001)
    - Blackrose Prison (ID: 3002)
    ... and 1 more
```

### get_regions()

**Purpose**: Retrieve all available regions and their subregions for ESO Logs data

**Parameters**: None

**Returns**: `GetRegions` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| world_data.regions | List[Region] | List of region objects |
| world_data.regions[].id | int | Region ID |
| world_data.regions[].name | str | Region name |
| world_data.regions[].subregions | List[Subregion] \| None | List of subregions |
| world_data.regions[].subregions[].id | int | Subregion ID |
| world_data.regions[].subregions[].name | str | Subregion name |

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def list_regions():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        regions = await client.get_regions()
        print("Available regions:")
        
        for region in regions.world_data.regions:
            print(f"\n{region.name} (ID: {region.id})")
            if region.subregions:
                for subregion in region.subregions:
                    print(f"  - {subregion.name} (ID: {subregion.id})")

asyncio.run(list_regions())
```

**Output**:
```
Available regions:

North America (ID: 1)
  - North America (ID: 1)

Europe (ID: 2)
  - Europe (ID: 2)
```

### get_encounters_by_zone()

**Purpose**: Retrieve all encounters within a specific zone by zone ID

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| zone_id | int | Yes | The zone ID to retrieve encounters for |

**Returns**: `GetEncountersByZone` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| world_data.zone | Zone | Zone information |
| world_data.zone.id | int | Zone ID |
| world_data.zone.name | str | Zone name |
| world_data.zone.encounters | List[Encounter] \| None | List of encounters in this zone |
| world_data.zone.encounters[].id | int | Encounter ID |
| world_data.zone.encounters[].name | str | Encounter name |

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def get_dungeon_encounters():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # First, get all zones to find the Dungeons zone ID
        zones = await client.get_zones()
        dungeon_zone = next((z for z in zones.world_data.zones if z.name == "Dungeons"), None)
        
        if dungeon_zone:
            # Get encounters for the Dungeons zone
            encounters_data = await client.get_encounters_by_zone(dungeon_zone.id)
            zone = encounters_data.world_data.zone
            
            print(f"Encounters in {zone.name}:")
            if zone.encounters:
                for encounter in zone.encounters[:10]:  # Show first 10
                    print(f"  - {encounter.name} (ID: {encounter.id})")
                
                if len(zone.encounters) > 10:
                    print(f"  ... and {len(zone.encounters) - 10} more encounters")
        else:
            print("Dungeons zone not found")

asyncio.run(get_dungeon_encounters())
```

**Output**:
```
Encounters in Dungeons:
  - Fungal Grotto I (ID: 2000)
  - Fungal Grotto II (ID: 2001)
  - Spindleclutch I (ID: 2002)
  - Spindleclutch II (ID: 2003)
  - The Banished Cells I (ID: 2004)
  - The Banished Cells II (ID: 2005)
  - Darkshade Caverns I (ID: 2006)
  - Darkshade Caverns II (ID: 2007)
  - Elden Hollow I (ID: 2008)
  - Elden Hollow II (ID: 2009)
  ... and 46 more encounters
```

## Common Patterns

### Zone and Encounter Discovery

Find all encounters across all zones:

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def discover_all_encounters():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        zones = await client.get_zones()
        
        total_encounters = 0
        for zone in zones.world_data.zones:
            if zone.encounters:
                total_encounters += len(zone.encounters)
                print(f"{zone.name}: {len(zone.encounters)} encounters")
        
        print(f"\nTotal encounters across all zones: {total_encounters}")

asyncio.run(discover_all_encounters())
```

### Difficulty Analysis

Analyze difficulty levels across zones:

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token
from collections import defaultdict

async def analyze_difficulties():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        zones = await client.get_zones()
        
        difficulty_counts = defaultdict(int)
        for zone in zones.world_data.zones:
            if zone.difficulties:
                for difficulty in zone.difficulties:
                    difficulty_counts[difficulty.name] += 1
        
        print("Difficulty distribution across zones:")
        for difficulty, count in sorted(difficulty_counts.items()):
            print(f"  {difficulty}: {count} zones")

asyncio.run(analyze_difficulties())
```