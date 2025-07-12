# Guild Data API Documentation Plan

## Task Overview
Create comprehensive API reference documentation for Guild Data endpoints in the ESO Logs Python library, following established patterns and standards.

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
**Primary**: `docs/api-reference/guild-data.md`
**Tests**: `tests/docs/test_guild_data_examples.py`

## API Methods to Document
Based on the existing client, document these guild-related methods:

1. `get_guild()` - Get guild information
2. `get_guild_reports()` - Get reports for a guild  
3. `get_guild_members()` - Get guild member list
4. Additional guild methods (inspect `esologs/client.py` for complete list)

## Required Methodology

### 1. API Method Discovery
```bash
# Find all guild-related methods in the client
grep -n "async def.*guild" esologs/client.py
grep -n "get_guild" esologs/client.py
```

### 2. Type Validation (CRITICAL)
For each method, run live API calls to validate return types:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def inspect_guild_methods():
    token = get_access_token()
    async with Client(
        url='https://www.esologs.com/api/v2/client',
        headers={'Authorization': f'Bearer {token}'}
    ) as client:
        
        # Test each method and inspect actual return types
        result = await client.get_guild(id=123)
        print(f'Type: {type(result).__name__}')
        # Document actual field types using type() on each field
```

### 3. Documentation Structure
Follow the exact pattern from `docs/api-reference/game-data.md`:

```markdown
# Guild Data API

Access ESO guild information, member lists, and guild performance data through the ESO Logs API.

## Overview

- **Coverage**: X endpoints implemented
- **Use Cases**: Guild management, member tracking, guild performance analysis
- **Rate Limit Impact**: 2-4 points per request (varies by complexity)

## Methods

### get_guild()

**Purpose**: Retrieve detailed guild information

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| id | int | Yes | The guild ID to retrieve |

**Returns**: `GetGuild` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| guild_data.guild.id | int | Guild ID |
| guild_data.guild.name | str | Guild name |
| [Add actual fields after type validation] | | |

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def get_guild_info():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        guild = await client.get_guild(id=12345)
        print(f"Guild: {guild.guild_data.guild.name}")

asyncio.run(get_guild_info())
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

### 5. Guild-Specific Considerations
- Guild data may include member lists with pagination
- Consider guild privacy settings that might affect data access
- Document any authentication requirements for guild data

## Testing Requirements

### Create Test File
**File**: `tests/docs/test_guild_data_examples.py`

Follow the pattern from `tests/docs/test_game_data_examples.py`:

```python
"""
Tests for examples in docs/api-reference/guild-data.md

Validates that all code examples in the guild data API documentation 
execute correctly and return expected data structures.
"""

import pytest
import asyncio
from esologs.client import Client
from access_token import get_access_token

class TestGuildDataExamples:
    """Test all examples from guild-data.md documentation"""

    @pytest.mark.asyncio
    async def test_get_guild_example(self, api_client_config):
        """Test the get_guild() basic example"""
        async with Client(**api_client_config) as client:
            # Find a valid guild ID first
            # Then test the method
            pass
```

### Test Strategy for Guild Data
```python
# Note: Guild data might require specific guild IDs that are public
# Consider using well-known public guilds for testing
# Handle cases where guild data might be private/restricted
```

## Workflow Steps

### Phase 1: Discovery & Exploration
1. Examine `esologs/client.py` for all guild-related methods
2. Run live API calls to understand available data
3. Identify valid guild IDs for testing (use public guilds)
4. Understand any privacy/permissions constraints

### Phase 2: Type Validation
1. For EACH method, run actual API calls
2. Use `type()` to verify field types
3. Document exact return structures
4. Note nullable fields (`| None`)
5. Test with multiple guild IDs to understand data variations

### Phase 3: Documentation Creation
1. Create `docs/api-reference/guild-data.md`
2. Follow established table format exactly
3. Include complete, executable examples
4. Add real output sections
5. Document any authentication/permissions requirements

### Phase 4: Test Creation
1. Create `tests/docs/test_guild_data_examples.py`
2. Write tests for every example
3. Handle potential privacy/access restrictions gracefully
4. Ensure all tests pass

### Phase 5: Validation
```bash
# Build documentation
mkdocs build --clean

# Run all tests
pytest tests/docs/test_guild_data_examples.py -v

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
| id | int | Yes | The guild ID to retrieve |

**Returns**: `GetGuild` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| guild_data.guild.id | int | Guild ID |
| guild_data.guild.name | str | Guild name |
```

## Common Patterns for Guild Data
Consider including patterns for:
- **Guild Member Analysis**: If member data is available
- **Guild Performance Tracking**: If guild-level metrics exist
- **Member Progression**: If historical member data is accessible

Only include patterns that demonstrate legitimate relationships between guild data fields.

## Error Handling Considerations
```python
# Guild data might have additional error cases:
# - Private guilds (403 Forbidden)
# - Non-existent guilds (404 Not Found)
# - Member data requiring permissions

try:
    guild = await client.get_guild(id=guild_id)
except GraphQLClientHttpError as e:
    if e.status_code == 403:
        print("Guild data is private")
    elif e.status_code == 404:
        print("Guild not found")
```

## Git Workflow
```bash
# Stage changes
git add docs/api-reference/guild-data.md tests/docs/test_guild_data_examples.py

# Commit with single-line message (NO AI attribution)
git commit -m "Add guild data API reference documentation"

# Push to branch
git push origin v2/update-main-before-refactor
```

## Important Constraints
- ✅ **Type accuracy**: ALL types must be verified against live API
- ✅ **Executable examples**: Every code block must run without modification
- ✅ **Real outputs**: Include actual command results
- ✅ **Complete imports**: All examples must be copy-pasteable
- ✅ **Privacy awareness**: Handle private/restricted guild data gracefully
- ✅ **Single-line commits**: No AI attribution in git messages

## Success Criteria
- [ ] Complete documentation for all guild data methods
- [ ] All return types validated against live API
- [ ] All examples executable and tested
- [ ] Comprehensive test suite created
- [ ] Documentation builds successfully
- [ ] All tests pass
- [ ] Privacy/access restrictions properly documented

## Rate Limiting Considerations
- Guild data endpoints: 2-4 points per request
- Member list endpoints might be higher cost
- Total budget: 18,000 points/hour (points are floats)
- Add delays for bulk testing: `await asyncio.sleep(0.2)`

## Next Steps After Completion
After completing this section, the agent should:
1. Verify all tests pass
2. Build documentation successfully
3. Commit and push changes
4. Update project status in CLAUDE.md if needed

This plan provides complete technical specifications for implementing the Guild Data API documentation following established project standards.