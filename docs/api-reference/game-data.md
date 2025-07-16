# Game Data

Access collections of data such as NPCs, classes, abilities, items, maps, etc. Game data only changes when major game patches are released, so you should cache results for as long as possible and only update when new content is released for the game.

## Overview

- **Coverage**: 11 endpoints implemented
- **Use Cases**: item databases, ability id lookup, etc...
- **Rate Limit Impact**: 1-3 points per request (varies by complexity)

## Methods

### get_abilities()

**Purpose**: Retrieve a paginated list of all abilities in ESO

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | *int* | No | Number of abilities to return (default: 100, max: 100) |
| `page` | *int* | No | Page number for pagination (default: 1) |

**Returns**: `GetAbilities` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `game_data.abilities.data` | *List[Ability]* | List of ability objects |
| `game_data.abilities.total` | *int* | Total number of abilities available |
| `game_data.abilities.per_page` | *int* | Number of abilities per page |
| `game_data.abilities.current_page` | *int* | Current page number |
| `game_data.abilities.has_more_pages` | *bool* | Whether more pages are available |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_all_abilities():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get first page of abilities
        abilities = await client.get_abilities(limit=50)
        print(f"Found {len(abilities.game_data.abilities.data)} abilities")

        # Show first few abilities
        for ability in abilities.game_data.abilities.data[:3]:
            print(f"- {ability.name} (ID: {ability.id})")

asyncio.run(get_all_abilities())
```

**Output**:
```
Found 3 abilities
- JUST Apprehend Teleport (ID: 2)
- Attack (ID: 3)
- Tool - Range (ID: 37)
```

**Error Handling**:
```python
from esologs.exceptions import GraphQLClientHttpError, GraphQLClientGraphQLMultiError
from pydantic import ValidationError

try:
    abilities = await client.get_abilities(limit=200)  # Too high
except GraphQLClientGraphQLMultiError as e:
    print(f"GraphQL error: {e}")  # Server-side validation
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except GraphQLClientHttpError as e:
    if e.status_code == 429:
        print("Rate limit exceeded")
```

### get_ability()

**Purpose**: Get detailed information about a specific ability by ID

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | *int* | Yes | The ability ID to retrieve |

**Returns**: `GetAbility` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `game_data.ability.id` | *int* | Ability ID |
| `game_data.ability.name` | *str* | Ability name |
| `game_data.ability.description` | *str \| None* | Ability description (may be None) |
| `game_data.ability.icon` | *str* | Icon filename |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_ability_details():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get a valid ability ID first
        abilities = await client.get_abilities(limit=10)
        valid_ability_id = abilities.game_data.abilities.data[0].id

        # Get specific ability details
        ability = await client.get_ability(id=valid_ability_id)
        if ability.game_data.ability:
            print(f"Ability: {ability.game_data.ability.name}")
            print(f"ID: {ability.game_data.ability.id}")

asyncio.run(get_ability_details())
```

**Output**:
```
Ability: JUST Apprehend Teleport
ID: 2
```

### get_classes()

**Purpose**: Retrieve all character classes available in ESO

**Parameters**: None

**Returns**: `GetClasses` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `game_data.classes` | *List[Class]* | List of class objects (direct list, not paginated) |
| `game_data.classes[].id` | *int* | Class ID |
| `game_data.classes[].name` | *str* | Class name |
| `game_data.classes[].slug` | *str* | URL-friendly class identifier |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def list_character_classes():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get all character classes
        classes = await client.get_classes()
        print("Available character classes:")

        for char_class in classes.game_data.classes:
            print(f"- {char_class.name} (ID: {char_class.id})")

asyncio.run(list_character_classes())
```

**Output**:
```
Available character classes:
- Dragonknight (ID: 1)
- Nightblade (ID: 2)
- Necromancer (ID: 3)
- Sorcerer (ID: 4)
- Templar (ID: 5)
- Warden (ID: 6)
- Arcanist (ID: 7)
```

### get_class()

**Purpose**: Get detailed information about a specific character class

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | *int* | Yes | The class ID to retrieve |

**Returns**: `GetClass` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `game_data.class_.id` | *int* | Class ID |
| `game_data.class_.name` | *str* | Class name |
| `game_data.class_.slug` | *str* | URL-friendly class identifier |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_class_details():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get Sorcerer class details
        sorcerer = await client.get_class(id=1)
        print(f"Class: {sorcerer.game_data.class_.name}")

asyncio.run(get_class_details())
```

**Output**:
```
Class: Dragonknight
```

### get_items()

**Purpose**: Retrieve a paginated list of items with optional filtering

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | *int* | No | Number of items to return (default: 100, max: 100) |
| `page` | *int* | No | Page number for pagination (default: 1) |

**Returns**: `GetItems` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `game_data.items.data` | *List[Item]* | List of item objects |
| `game_data.items.total` | *int* | Total number of items available |
| `game_data.items.per_page` | *int* | Number of items per page |
| `game_data.items.current_page` | *int* | Current page number |
| `game_data.items.has_more_pages` | *bool* | Whether more pages are available |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def browse_items():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get first page of items
        items = await client.get_items(limit=25)
        print(f"Found {len(items.game_data.items.data)} items")

        # Show some item details
        for item in items.game_data.items.data[:5]:
            name = item.name or f"Item_{item.id}"
            print(f"- {name} (ID: {item.id})")

asyncio.run(browse_items())
```

**Output**:
```
Found 3 items
- Item_3 (ID: 3)
- Item_4 (ID: 4)
- Item_5 (ID: 5)
```

### get_item()

**Purpose**: Get detailed information about a specific item by ID

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | *int* | Yes | The item ID to retrieve |

**Returns**: `GetItem` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `game_data.item.id` | *int* | Item ID |
| `game_data.item.name` | *str \| None* | Item name (may be None) |
| `game_data.item.icon` | *str \| None* | Icon filename (may be None) |
| `Additional properties` | *varies* | Additional item properties depending on item type |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_item_details():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get a valid item ID first
        items = await client.get_items(limit=5)
        valid_item_id = items.game_data.items.data[0].id

        # Get specific item details
        item = await client.get_item(id=valid_item_id)
        if item.game_data.item:
            item_name = item.game_data.item.name or f"Item_{item.game_data.item.id}"
            print(f"Item: {item_name}")
            print(f"ID: {item.game_data.item.id}")

asyncio.run(get_item_details())
```

**Output**:
```
Item: Item_3
ID: 3
```

### get_npcs()

**Purpose**: Retrieve a paginated list of NPCs (Non-Player Characters)

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | *int* | No | Number of NPCs to return (default: 100, max: 100) |
| `page` | *int* | No | Page number for pagination (default: 1) |

**Returns**: `GetNPCs` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `game_data.npcs.data` | *List[NPC]* | List of NPC objects |
| `game_data.npcs.total` | *int* | Total number of NPCs available |
| `game_data.npcs.per_page` | *int* | Number of NPCs per page |
| `game_data.npcs.current_page` | *int* | Current page number |
| `game_data.npcs.has_more_pages` | *bool* | Whether more pages are available |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def list_npcs():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get NPCs
        npcs = await client.get_npcs(limit=5)
        print(f"Found {len(npcs.game_data.npcs.data)} NPCs")

        # Show NPC names
        for npc in npcs.game_data.npcs.data:
            print(f"- {npc.name} (ID: {npc.id})")

asyncio.run(list_npcs())
```

**Output**:
```
Found 5 NPCs
- Wheels (ID: 1)
- Heals on Wheels (ID: 2)
- Flame Atronach (ID: 3)
- Argonian Behemoth (ID: 4)
- Clannfear (ID: 5)
```

### get_npc()

**Purpose**: Get detailed information about a specific NPC by ID

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | *int* | Yes | The NPC ID to retrieve |

**Returns**: `GetNPC` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `game_data.npc.id` | *int* | NPC ID |
| `game_data.npc.name` | *str* | NPC name |
| `Additional properties` | *varies* | Additional NPC properties (varies by NPC type) |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_npc_details():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get a valid NPC ID first
        npcs = await client.get_npcs(limit=5)
        valid_npc_id = npcs.game_data.npcs.data[0].id

        # Get specific NPC details
        npc = await client.get_npc(id=valid_npc_id)
        if npc.game_data.npc:
            print(f"NPC: {npc.game_data.npc.name}")
            print(f"ID: {npc.game_data.npc.id}")

asyncio.run(get_npc_details())
```

**Output**:
```
NPC: Wheels
ID: 1
```

### get_maps()

**Purpose**: Retrieve all maps/zones available in ESO

**Parameters**: None

**Returns**: `GetMaps` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `game_data.maps.data` | *List[Map]* | List of map objects |
| `game_data.maps.total` | *int* | Total number of maps available |
| `game_data.maps.per_page` | *int* | Number of maps per page |
| `game_data.maps.current_page` | *int* | Current page number |
| `game_data.maps.has_more_pages` | *bool* | Whether more pages are available |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def list_maps():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get maps (returns first page by default)
        maps = await client.get_maps()
        print(f"Found {len(maps.game_data.maps.data)} maps (first page)")

        # Show first few maps
        for game_map in maps.game_data.maps.data[:5]:
            print(f"- {game_map.name} (ID: {game_map.id})")

asyncio.run(list_maps())
```

**Output**:
```
Found 100 maps (first page)
- Glenumbra (ID: 1)
- Edrald Undercroft (ID: 2)
- Wayrest (ID: 3)
- Stormhaven (ID: 4)
- Alcaire Castle (ID: 5)
```

### get_map()

**Purpose**: Get detailed information about a specific map/zone by ID

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | *int* | Yes | The map ID to retrieve |

**Returns**: `GetMap` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `game_data.map.id` | *int* | Map ID |
| `game_data.map.name` | *str* | Map name |
| `Additional properties` | *varies* | Additional map properties (varies by map type) |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def get_map_details():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get a valid map ID first
        maps = await client.get_maps()
        valid_map_id = maps.game_data.maps.data[0].id

        # Get specific map details
        game_map = await client.get_map(id=valid_map_id)
        if game_map.game_data.map:
            print(f"Map: {game_map.game_data.map.name}")
            print(f"ID: {game_map.game_data.map.id}")

asyncio.run(get_map_details())
```

**Output**:
```
Map: Glenumbra
ID: 1
```

### get_factions()

**Purpose**: Retrieve all factions available in ESO

**Parameters**: None

**Returns**: `GetFactions` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `game_data.factions` | *List[Faction]* | List of faction objects (direct list, not paginated) |
| `game_data.factions[].id` | *int* | Faction ID |
| `game_data.factions[].name` | *str* | Faction name |

**Example**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def list_factions():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get all factions
        factions = await client.get_factions()
        print("Available factions:")

        for faction in factions.game_data.factions:
            print(f"- {faction.name} (ID: {faction.id})")

asyncio.run(list_factions())
```

**Output**:
```
Available factions:
- The Aldmeri Dominion (ID: 1)
- The Daggerfall Covenant (ID: 2)
- The Ebonheart Pact (ID: 3)
```

## Common Patterns

### Building Item Databases

Efficiently collect and store item information for analysis:

```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def build_item_database():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        items_database = []
        page = 1

        while True:
            # Get items in batches
            items_response = await client.get_items(limit=100, page=page)
            items = items_response.game_data.items.data

            if not items:
                break

            # Process each item
            for item in items:
                items_database.append({
                    'id': item.id,
                    'name': item.name or f"Item_{item.id}"  # Handle None names
                })

            print(f"Processed page {page}, total items: {len(items_database)}")
            page += 1

            # Respect rate limits
            await asyncio.sleep(0.1)

        print(f"Database complete: {len(items_database)} items")
        return items_database

asyncio.run(build_item_database())
```

**Output**:
```
Processed page 1, total items: 100
Processed page 2, total items: 200
Processed page 3, total items: 300
...
Database complete: 15000 items
```


## Rate Limiting

Game data endpoints are generally low-cost but consider these guidelines:

- **Basic requests** (get_classes, get_factions): 1 point each
- **Paginated requests** (get_abilities, get_items): 1-2 points each
- **Individual lookups** (get_ability, get_item): 1 point each
- **Batch operations**: Add delays between requests to avoid hitting limits

**Rate Limit Management**:
```python
import asyncio

# For bulk operations, add delays
async def respectful_bulk_operation():
    for item_id in large_item_list:
        item = await client.get_item(id=item_id)
        # Process item
        await asyncio.sleep(0.1)  # 100ms delay between requests
```

**Monitor Your Usage**:
```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def monitor_usage():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Check rate limit status
        rate_limit = await client.get_rate_limit_data()
        print(f"Points used: {rate_limit.rate_limit_data.points_spent_this_hour}/18000")

asyncio.run(monitor_usage())
```
