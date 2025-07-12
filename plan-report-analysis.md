# Report Analysis API Documentation Plan

## Task Overview
Create comprehensive API reference documentation for Report Analysis endpoints in the ESO Logs Python library, following established patterns and standards.

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
**Primary**: `docs/api-reference/report-analysis.md`
**Tests**: `tests/docs/test_report_analysis_examples.py`

## API Methods to Document
Based on the existing client, document these report analysis methods:

1. `get_report_events()` - Get detailed event data from reports
2. `get_report_graph()` - Get graphical data (DPS, healing, etc.)
3. `get_report_table()` - Get tabular analysis data
4. `get_report_rankings()` - Get performance rankings from reports
5. `get_report_player_details()` - Get detailed player performance
6. Additional report analysis methods (inspect `esologs/client.py` for complete list)

## Required Methodology

### 1. API Method Discovery
```bash
# Find all report analysis methods in the client
grep -n "async def.*report" esologs/client.py
grep -n "get_report" esologs/client.py
```

### 2. Type Validation (CRITICAL)
For each method, run live API calls to validate return types:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def inspect_report_analysis_methods():
    token = get_access_token()
    async with Client(
        url='https://www.esologs.com/api/v2/client',
        headers={'Authorization': f'Bearer {token}'}
    ) as client:
        
        # Need to find a valid report ID first
        # Test each method and inspect actual return types
        events = await client.get_report_events(report_id="abc123")
        print(f'Events type: {type(events).__name__}')
        # Document actual field types using type() on each field
```

### 3. Documentation Structure
Follow the exact pattern from `docs/api-reference/game-data.md`:

```markdown
# Report Analysis API

Access detailed ESO combat log analysis including events, performance graphs, tables, and rankings through the ESO Logs API.

## Overview

- **Coverage**: X endpoints implemented
- **Use Cases**: Combat analysis, performance optimization, encounter research
- **Rate Limit Impact**: 3-10 points per request (varies by complexity and data volume)

## Methods

### get_report_events()

**Purpose**: Retrieve detailed event data from a combat log report

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| report_id | str | Yes | The report ID to analyze |
| start_time | int | No | Start time in milliseconds |
| end_time | int | No | End time in milliseconds |
| [Add actual parameters after inspection] | | | |

**Returns**: `GetReportEvents` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| report_data.events | List[Event] | List of combat events |
| report_data.events[].timestamp | int | Event timestamp |
| report_data.events[].type | str | Event type |
| [Add actual fields after type validation] | | |

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def analyze_report_events():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Analyze events from a specific report
        events = await client.get_report_events(report_id="abc123")
        print(f"Found {len(events.report_data.events)} events")
        
        # Show first few events
        for event in events.report_data.events[:3]:
            print(f"- {event.type} at {event.timestamp}")

asyncio.run(analyze_report_events())
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

### 5. Report Analysis Specific Considerations
- Report analysis endpoints are likely the highest cost (3-10+ points)
- Report IDs must be valid and accessible
- Some data might require specific time ranges
- Performance data might have complex nested structures
- Consider different report types (trials, dungeons, etc.)

## Testing Requirements

### Create Test File
**File**: `tests/docs/test_report_analysis_examples.py`

Follow the pattern from `tests/docs/test_game_data_examples.py`:

```python
"""
Tests for examples in docs/api-reference/report-analysis.md

Validates that all code examples in the report analysis API documentation 
execute correctly and return expected data structures.
"""

import pytest
import asyncio
from esologs.client import Client
from access_token import get_access_token

class TestReportAnalysisExamples:
    """Test all examples from report-analysis.md documentation"""

    @pytest.mark.asyncio
    async def test_get_report_events_example(self, api_client_config):
        """Test the get_report_events() basic example"""
        async with Client(**api_client_config) as client:
            # Need to find a valid public report ID first
            # Then test the method
            pass
```

### Test Strategy for Report Analysis
```python
# Report analysis requires valid report IDs
# Use publicly accessible reports for testing
# Handle cases where reports might be private
# Test with different report types (trial, dungeon, etc.)
```

## Workflow Steps

### Phase 1: Discovery & Exploration
1. Examine `esologs/client.py` for all report analysis methods
2. Find valid, public report IDs for testing
3. Run live API calls to understand available data
4. Understand different report types and their data structures

### Phase 2: Type Validation
1. For EACH method, run actual API calls with valid report IDs
2. Use `type()` to verify field types
3. Document exact return structures
4. Note nullable fields (`| None`)
5. Test with different report types to understand variations

### Phase 3: Documentation Creation
1. Create `docs/api-reference/report-analysis.md`
2. Follow established table format exactly
3. Include complete, executable examples
4. Add real output sections
5. Document performance considerations and rate limits

### Phase 4: Test Creation
1. Create `tests/docs/test_report_analysis_examples.py`
2. Write tests for every example
3. Handle potential privacy/access restrictions gracefully
4. Ensure all tests pass

### Phase 5: Validation
```bash
# Build documentation
mkdocs build --clean

# Run all tests
pytest tests/docs/test_report_analysis_examples.py -v

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
| report_id | str | Yes | The report ID to analyze |

**Returns**: `GetReportEvents` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| report_data.events | List[Event] | List of combat events |
| report_data.events[].timestamp | int | Event timestamp |
```

## Common Patterns for Report Analysis
Consider including patterns for:
- **Performance Analysis**: Combining different analysis methods
- **Encounter Breakdown**: Analyzing specific encounter phases
- **Player Comparison**: Comparing player performance within reports

Only include patterns that demonstrate legitimate relationships between report analysis data.

## Data Structure Expectations
Report analysis data might include:
- **Events**: Damage, healing, buff/debuff applications
- **Graphs**: Time-series performance data
- **Tables**: Aggregated statistics and rankings
- **Player Details**: Individual performance breakdowns
- **Timestamps**: Precise timing information

## Error Handling Considerations
```python
# Report analysis might have additional error cases:
# - Private reports (403 Forbidden)
# - Invalid report IDs (404 Not Found)
# - Large data requests timing out
# - Rate limiting due to high cost

try:
    events = await client.get_report_events(report_id=report_id)
except GraphQLClientHttpError as e:
    if e.status_code == 403:
        print("Report is private")
    elif e.status_code == 404:
        print("Report not found")
    elif e.status_code == 429:
        print("Rate limit exceeded - report analysis is expensive")
```

## Git Workflow
```bash
# Stage changes
git add docs/api-reference/report-analysis.md tests/docs/test_report_analysis_examples.py

# Commit with single-line message (NO AI attribution)
git commit -m "Add report analysis API reference documentation"

# Push to branch
git push origin v2/update-main-before-refactor
```

## Important Constraints
- ✅ **Type accuracy**: ALL types must be verified against live API
- ✅ **Executable examples**: Every code block must run without modification
- ✅ **Real outputs**: Include actual command results
- ✅ **Complete imports**: All examples must be copy-pasteable
- ✅ **Privacy awareness**: Handle private/restricted reports gracefully
- ✅ **Rate limit awareness**: Document high-cost operations
- ✅ **Single-line commits**: No AI attribution in git messages

## Success Criteria
- [ ] Complete documentation for all report analysis methods
- [ ] All return types validated against live API
- [ ] All examples executable and tested
- [ ] Comprehensive test suite created
- [ ] Documentation builds successfully
- [ ] All tests pass
- [ ] Performance and rate limit considerations documented

## Rate Limiting Considerations
- Report analysis endpoints: 3-10+ points per request
- These are the highest cost endpoints in the API
- Total budget: 18,000 points/hour (points are floats)
- Add longer delays for testing: `await asyncio.sleep(0.5)`
- Consider testing with smaller data sets first

## Next Steps After Completion
After completing this section, the agent should:
1. Verify all tests pass
2. Build documentation successfully
3. Commit and push changes
4. Update project status in CLAUDE.md if needed

This plan provides complete technical specifications for implementing the Report Analysis API documentation following established project standards.