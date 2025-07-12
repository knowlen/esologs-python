# World Data API Documentation Plan

## Task Overview
Create comprehensive API reference documentation for World Data endpoints in the ESO Logs Python library, following established patterns and standards.

## Project Context
- **Repository**: ESO Logs Python v0.2.0-alpha (~65% API coverage)
- **Branch**: `v2/update-main-before-refactor` (DO NOT push to v2-dev directly)
- **Working Directory**: `/home/nknowles/projects/esologs-python/esologs-python/`
- **Virtual Environment**: `venv/` (activate with `source venv/bin/activate`)

## Environment Setup
```bash
cd /home/nknowles/projects/esologs-python/esologs-python
source venv/bin/activate
export ESOLOGS_ID="9f59cb5f-fabd-47e6-9529-f9797d5b38b2"
export ESOLOGS_SECRET="6hpMm9nbbfPKqF589dg8l16kxNV8jzFlERDXQIhl"
```

## File to Create
**Primary**: `docs/api-reference/world-data.md`
**Tests**: `tests/docs/test_world_data_examples.py`

## API Methods to Document
Based on the existing client, document these world/encounter-related methods:

1. `get_encounters()` - Get encounter definitions
2. `get_encounter()` - Get specific encounter details
3. `get_zones()` - Get zone information  
4. `get_zone()` - Get specific zone details
5. Additional world/encounter methods (inspect `esologs/client.py` for complete list)

## Required Methodology

### 1. API Method Discovery
```bash
# Find all world/encounter-related methods in the client
grep -n "async def.*encounter" esologs/client.py
grep -n "async def.*zone" esologs/client.py
grep -n "get_encounter\|get_zone" esologs/client.py
```

### 2. Type Validation (CRITICAL)
For each method, run live API calls to validate return types:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def inspect_world_methods():
    token = get_access_token()
    async with Client(
        url='https://www.esologs.com/api/v2/client',
        headers={'Authorization': f'Bearer {token}'}
    ) as client:
        
        # Test each method and inspect actual return types
        encounters = await client.get_encounters()
        print(f'Encounters type: {type(encounters).__name__}')
        
        if encounters.world_data.encounters:
            encounter = encounters.world_data.encounters[0]
            print(f'Encounter type: {type(encounter).__name__}')
            # Document actual field types using type() on each field
```

### 3. Documentation Structure
Follow the exact pattern from `docs/api-reference/game-data.md`:

```markdown
# World Data API

Access ESO world information including encounters, zones, and dungeon/trial data through the ESO Logs API.

## Overview

- **Coverage**: X endpoints implemented
- **Use Cases**: Encounter analysis, zone information, dungeon/trial research
- **Rate Limit Impact**: 1-3 points per request (varies by complexity)

## Methods

### get_encounters()

**Purpose**: Retrieve all available encounters (bosses, trials, dungeons)

**Parameters**: None

**Returns**: `GetEncounters` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| world_data.encounters | List[Encounter] | List of encounter objects |
| world_data.encounters[].id | int | Encounter ID |
| world_data.encounters[].name | str | Encounter name |
| [Add actual fields after type validation] | | |

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def list_encounters():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        encounters = await client.get_encounters()
        print("Available encounters:")
        
        for encounter in encounters.world_data.encounters[:5]:
            print(f"- {encounter.name} (ID: {encounter.id})")

asyncio.run(list_encounters())
```

**Output**:
```
[Add actual output after testing]
```
```

### 4. Table Formatting Standards
- **Parameters**: Use "Parameters" (plural) in header
- **Return Fields**: Use proper type annotations (`str | None`, `List[Type]`)
- **Parameter names**: Will be automatically bold via CSS
- **No "Parameters:" line** above tables (removed for space)

### 5. World Data Specific Considerations
- Encounters might be categorized by type (trial, dungeon, arena)
- Zone data might include difficulty levels or variations
- Consider relationships between zones and encounters
- Some encounters might have multiple difficulties

## Testing Requirements

### Create Test File
**File**: `tests/docs/test_world_data_examples.py`

Follow the pattern from `tests/docs/test_game_data_examples.py`:

```python
"""
Tests for examples in docs/api-reference/world-data.md

Validates that all code examples in the world data API documentation 
execute correctly and return expected data structures.
"""

import pytest
import asyncio
from esologs.client import Client
from access_token import get_access_token

class TestWorldDataExamples:
    """Test all examples from world-data.md documentation"""

    @pytest.mark.asyncio
    async def test_get_encounters_example(self, api_client_config):
        """Test the get_encounters() basic example"""
        async with Client(**api_client_config) as client:
            encounters = await client.get_encounters()
            
            # Validate response structure
            assert hasattr(encounters, 'world_data')
            assert hasattr(encounters.world_data, 'encounters')
            assert len(encounters.world_data.encounters) > 0
            
            # Validate encounter structure
            encounter = encounters.world_data.encounters[0]
            assert hasattr(encounter, 'id')
            assert hasattr(encounter, 'name')
```

### Test Strategy for World Data
```python
# World data should be fairly stable and public
# Test various encounter types if available
# Validate zone/encounter relationships
```

## Workflow Steps

### Phase 1: Discovery & Exploration
1. Examine `esologs/client.py` for all world/encounter-related methods
2. Run live API calls to understand available data
3. Identify encounter and zone data structures
4. Understand relationships between different world data types

### Phase 2: Type Validation
1. For EACH method, run actual API calls
2. Use `type()` to verify field types
3. Document exact return structures
4. Note nullable fields (`| None`)
5. Test with different encounter/zone IDs to understand variations

### Phase 3: Documentation Creation
1. Create `docs/api-reference/world-data.md`
2. Follow established table format exactly
3. Include complete, executable examples
4. Add real output sections
5. Document encounter categories and zone types

### Phase 4: Test Creation
1. Create `tests/docs/test_world_data_examples.py`
2. Write tests for every example
3. Ensure all tests pass
4. Test edge cases (invalid IDs, etc.)

### Phase 5: Validation
```bash
# Build documentation
mkdocs build --clean

# Run all tests
pytest tests/docs/test_world_data_examples.py -v

# Run full doc test suite to ensure no regressions
pytest tests/docs/ -v
```

## Reference Examples

### Existing File References
- **Pattern to follow**: `docs/api-reference/game-data.md`
- **Test pattern**: `tests/docs/test_game_data_examples.py`
- **CSS styling**: `docs/stylesheets/extra.css` (already configured)

### Table Format Example
```markdown
| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| id | int | Yes | The encounter ID to retrieve |

**Returns**: `GetEncounter` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| world_data.encounter.id | int | Encounter ID |
| world_data.encounter.name | str | Encounter name |
```

## Common Patterns for World Data
Consider including patterns for:
- **Encounter Discovery**: Finding encounters by zone or difficulty
- **Zone Analysis**: Understanding zone structure and encounters
- **Trial/Dungeon Mapping**: If relationships exist between zones and encounters

Only include patterns that demonstrate legitimate relationships between world data fields.

## Data Structure Expectations
World data might include:
- **Encounters**: Boss fights, trial encounters, arena rounds
- **Zones**: Dungeons, trials, overworld zones
- **Difficulties**: Normal, veteran, hard mode variations
- **Categories**: Trial, dungeon, arena, etc.

## Git Workflow
```bash
# Stage changes
git add docs/api-reference/world-data.md tests/docs/test_world_data_examples.py

# Commit with single-line message (NO AI attribution)
git commit -m "Add world data API reference documentation"

# Push to branch
git push origin v2/update-main-before-refactor
```

## Important Constraints
- ✅ **Type accuracy**: ALL types must be verified against live API
- ✅ **Executable examples**: Every code block must run without modification
- ✅ **Real outputs**: Include actual command results
- ✅ **Complete imports**: All examples must be copy-pasteable
- ✅ **No artificial patterns**: Only include legitimate use cases
- ✅ **Single-line commits**: No AI attribution in git messages

## Success Criteria
- [ ] Complete documentation for all world data methods
- [ ] All return types validated against live API
- [ ] All examples executable and tested
- [ ] Comprehensive test suite created
- [ ] Documentation builds successfully
- [ ] All tests pass
- [ ] Encounter and zone relationships properly documented

## Rate Limiting Considerations
- World data endpoints: 1-3 points per request
- Generally lower cost than character/report data
- Total budget: 18,000 points/hour (points are floats)
- Add delays for bulk testing: `await asyncio.sleep(0.1)`

## Next Steps After Completion
After completing this section, the agent should:
1. Verify all tests pass
2. Build documentation successfully
3. Commit and push changes
4. Update project status in CLAUDE.md if needed

This plan provides complete technical specifications for implementing the World Data API documentation following established project standards.