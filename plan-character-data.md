# Character Data API Documentation Plan

## Task Overview
Create comprehensive API reference documentation for Character Data endpoints in the ESO Logs Python library, following established patterns and standards.

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
**Primary**: `docs/api-reference/character-data.md`
**Tests**: `tests/docs/test_character_data_examples.py`

## API Methods to Document
Based on the existing client, document these character-related methods:

1. `get_character_by_id()` - Get character profile by ID
2. `get_character_reports()` - Get reports for a character
3. `get_character_rankings()` - Get character rankings/performance
4. Additional character methods (inspect `esologs/client.py` for complete list)

## Required Methodology

### 1. API Method Discovery
```bash
# Find all character-related methods in the client
grep -n "async def.*character" esologs/client.py
grep -n "get_character" esologs/client.py
```

### 2. Type Validation (CRITICAL)
For each method, run live API calls to validate return types:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def inspect_character_methods():
    token = get_access_token()
    async with Client(
        url='https://www.esologs.com/api/v2/client',
        headers={'Authorization': f'Bearer {token}'}
    ) as client:
        
        # Test each method and inspect actual return types
        result = await client.get_character_by_id(id=123)
        print(f'Type: {type(result).__name__}')
        # Document actual field types
```

### 3. Documentation Structure
Follow the exact pattern from `docs/api-reference/game-data.md`:

```markdown
# Character Data API

Access ESO character profiles, reports, and performance data through the ESO Logs API.

## Overview

- **Coverage**: X endpoints implemented
- **Use Cases**: Character analysis, performance tracking, report history
- **Rate Limit Impact**: 2-5 points per request (varies by complexity)

## Methods

### get_character_by_id()

**Purpose**: Retrieve detailed character profile information

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| id | int | Yes | The character ID to retrieve |

**Returns**: `GetCharacterById` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| character_data.character.id | int | Character ID |
| character_data.character.name | str | Character name |
| [Add actual fields after type validation] | | |

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def get_character_profile():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        character = await client.get_character_by_id(id=12345)
        print(f"Character: {character.character_data.character.name}")

asyncio.run(get_character_profile())
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

### 5. CSS Styling (Already Configured)
The following CSS is already configured in `docs/stylesheets/extra.css`:
- Parameter names automatically bold
- Table column separators
- Consistent formatting with existing pages

## Testing Requirements

### Create Test File
**File**: `tests/docs/test_character_data_examples.py`

Follow the pattern from `tests/docs/test_game_data_examples.py`:

```python
"""
Tests for examples in docs/api-reference/character-data.md

Validates that all code examples in the character data API documentation 
execute correctly and return expected data structures.
"""

import pytest
import asyncio
from esologs.client import Client
from access_token import get_access_token

class TestCharacterDataExamples:
    """Test all examples from character-data.md documentation"""

    @pytest.mark.asyncio
    async def test_get_character_by_id_example(self, api_client_config):
        """Test the get_character_by_id() basic example"""
        async with Client(**api_client_config) as client:
            # Find a valid character ID first
            # Then test the method
            pass
```

### Test Validation
```bash
# Run tests to ensure all examples work
pytest tests/docs/test_character_data_examples.py -v
```

## Workflow Steps

### Phase 1: Discovery & Exploration
1. Examine `esologs/client.py` for all character-related methods
2. Run live API calls to understand available data
3. Identify valid character IDs for testing

### Phase 2: Type Validation
1. For EACH method, run actual API calls
2. Use `type()` to verify field types
3. Document exact return structures
4. Note nullable fields (`| None`)

### Phase 3: Documentation Creation
1. Create `docs/api-reference/character-data.md`
2. Follow established table format exactly
3. Include complete, executable examples
4. Add real output sections

### Phase 4: Test Creation
1. Create `tests/docs/test_character_data_examples.py`
2. Write tests for every example
3. Ensure all tests pass

### Phase 5: Validation
```bash
# Build documentation
mkdocs build --clean

# Run all tests
pytest tests/docs/test_character_data_examples.py -v

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
| id | int | Yes | The character ID to retrieve |

**Returns**: `GetCharacterById` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| character_data.character.id | int | Character ID |
| character_data.character.name | str | Character name |
```

## Git Workflow
```bash
# Stage changes
git add docs/api-reference/character-data.md tests/docs/test_character_data_examples.py

# Commit with single-line message (NO AI attribution)
git commit -m "Add character data API reference documentation"

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
- [ ] Complete documentation for all character data methods
- [ ] All return types validated against live API
- [ ] All examples executable and tested
- [ ] Comprehensive test suite created
- [ ] Documentation builds successfully
- [ ] All tests pass

## Rate Limiting Considerations
- Character data endpoints: 2-5 points per request
- Total budget: 18,000 points/hour (points are floats)
- Add delays for bulk testing: `await asyncio.sleep(0.2)`

## Next Steps After Completion
After completing this section, the agent should:
1. Verify all tests pass
2. Build documentation successfully
3. Commit and push changes
4. Update project status in CLAUDE.md if needed

This plan provides complete technical specifications for implementing the Character Data API documentation following established project standards.