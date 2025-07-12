# Report Search API Documentation Plan

## Task Overview
Create comprehensive API reference documentation for Report Search endpoints in the ESO Logs Python library, following established patterns and standards.

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
**Primary**: `docs/api-reference/report-search.md`
**Tests**: `tests/docs/test_report_search_examples.py`

## API Methods to Document
Based on the existing client and CLAUDE.md mentioning "Advanced Report Search", document these search methods:

1. `search_reports()` - Main search method with filters
2. Additional search methods with specific filters
3. Search convenience methods (inspect `esologs/client.py` for complete list)

## Required Methodology

### 1. API Method Discovery
```bash
# Find all search-related methods in the client
grep -n "async def.*search" esologs/client.py
grep -n "search_report" esologs/client.py
```

### 2. Type Validation (CRITICAL)
For each method, run live API calls to validate return types:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def inspect_search_methods():
    token = get_access_token()
    async with Client(
        url='https://www.esologs.com/api/v2/client',
        headers={'Authorization': f'Bearer {token}'}
    ) as client:
        
        # Test search with basic parameters
        results = await client.search_reports(limit=10)
        print(f'Search results type: {type(results).__name__}')
        # Document actual field types using type() on each field
```

### 3. Documentation Structure
Follow the exact pattern from `docs/api-reference/game-data.md`:

```markdown
# Report Search API

Search and filter ESO combat reports with advanced criteria including guilds, encounters, players, and performance metrics through the ESO Logs API.

## Overview

- **Coverage**: X endpoints implemented  
- **Use Cases**: Finding specific reports, performance research, guild analysis
- **Rate Limit Impact**: 5-15 points per request (varies by filter complexity)

## Methods

### search_reports()

**Purpose**: Search for reports with flexible filtering and pagination

| Parameters | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | int | No | Number of reports to return (default: 25, max: 100) |
| page | int | No | Page number for pagination (default: 1) |
| guild_id | int | No | Filter by guild ID |
| encounter_id | int | No | Filter by encounter ID |
| start_time | int | No | Earliest report timestamp |
| end_time | int | No | Latest report timestamp |
| [Add actual parameters after inspection] | | | |

**Returns**: `SearchReports` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| report_data.reports.data | List[Report] | List of matching reports |
| report_data.reports.total | int | Total number of matching reports |
| report_data.reports.per_page | int | Number of reports per page |
| report_data.reports.current_page | int | Current page number |
| report_data.reports.has_more_pages | bool | Whether more pages are available |
| [Add actual fields after type validation] | | |

**Example**:
```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def search_guild_reports():
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Search for recent reports from a specific guild
        reports = await client.search_reports(
            guild_id=12345,
            limit=10
        )
        
        print(f"Found {len(reports.report_data.reports.data)} reports")
        
        for report in reports.report_data.reports.data:
            print(f"- {report.title} ({report.start_time})")

asyncio.run(search_guild_reports())
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

### 5. Report Search Specific Considerations
- Search endpoints are likely high cost (5-15+ points)
- Complex filters might increase cost significantly
- Pagination is essential for large result sets
- Date/time filters might use Unix timestamps
- Different filter combinations might return different data structures

## Testing Requirements

### Create Test File
**File**: `tests/docs/test_report_search_examples.py`

Follow the pattern from `tests/docs/test_game_data_examples.py`:

```python
"""
Tests for examples in docs/api-reference/report-search.md

Validates that all code examples in the report search API documentation 
execute correctly and return expected data structures.
"""

import pytest
import asyncio
from esologs.client import Client
from access_token import get_access_token

class TestReportSearchExamples:
    """Test all examples from report-search.md documentation"""

    @pytest.mark.asyncio
    async def test_search_reports_basic_example(self, api_client_config):
        """Test the search_reports() basic example"""
        async with Client(**api_client_config) as client:
            # Test basic search functionality
            results = await client.search_reports(limit=5)
            
            # Validate response structure
            assert hasattr(results, 'report_data')
            assert hasattr(results.report_data, 'reports')
            assert hasattr(results.report_data.reports, 'data')
```

### Test Strategy for Report Search
```python
# Search requires careful testing:
# - Test basic search without filters
# - Test individual filter types
# - Test pagination
# - Handle cases where searches return no results
# - Test edge cases (invalid dates, etc.)
```

## Workflow Steps

### Phase 1: Discovery & Exploration
1. Examine `esologs/client.py` for all search-related methods
2. Run live API calls to understand search capabilities
3. Test different filter combinations
4. Understand pagination and result limits
5. Document search performance characteristics

### Phase 2: Type Validation
1. For EACH method, run actual API calls with various filters
2. Use `type()` to verify field types
3. Document exact return structures
4. Note nullable fields (`| None`)
5. Test edge cases (empty results, invalid filters)

### Phase 3: Documentation Creation
1. Create `docs/api-reference/report-search.md`
2. Follow established table format exactly
3. Include complete, executable examples
4. Add real output sections
5. Document filter options and performance considerations

### Phase 4: Test Creation
1. Create `tests/docs/test_report_search_examples.py`
2. Write tests for every example
3. Test various filter combinations
4. Ensure all tests pass

### Phase 5: Validation
```bash
# Build documentation
mkdocs build --clean

# Run all tests
pytest tests/docs/test_report_search_examples.py -v

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
| guild_id | int | No | Filter by guild ID |

**Returns**: `SearchReports` object with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| report_data.reports.data | List[Report] | List of matching reports |
| report_data.reports.total | int | Total number of matching reports |
```

## Common Patterns for Report Search
Consider including patterns for:
- **Advanced Filtering**: Combining multiple search criteria
- **Performance Research**: Finding reports by performance metrics
- **Guild Monitoring**: Tracking guild activity and performance
- **Encounter Analysis**: Finding reports for specific encounters

Only include patterns that demonstrate legitimate search use cases.

## Data Structure Expectations
Report search data might include:
- **Pagination**: Standard pagination with total, per_page, current_page
- **Report Metadata**: Title, start/end times, guild, encounter
- **Performance Data**: DPS metrics, completion status
- **Filter Results**: Matching criteria and result counts

## Advanced Search Examples
Consider documenting:
```python
# Complex search with multiple filters
reports = await client.search_reports(
    guild_id=12345,
    encounter_id=67890,
    start_time=1640995200,  # Unix timestamp
    end_time=1641081600,
    limit=50
)

# Performance-based search (if available)
high_dps_reports = await client.search_reports(
    min_dps=100000,
    encounter_id=67890,
    limit=25
)
```

## Error Handling Considerations
```python
# Search might have specific error cases:
# - Invalid filter combinations
# - Date ranges too large
# - Rate limiting due to expensive queries
# - No results found vs. error conditions

try:
    reports = await client.search_reports(guild_id=invalid_id)
except GraphQLClientHttpError as e:
    if e.status_code == 400:
        print("Invalid search parameters")
    elif e.status_code == 429:
        print("Rate limit exceeded - search is expensive")
```

## Git Workflow
```bash
# Stage changes
git add docs/api-reference/report-search.md tests/docs/test_report_search_examples.py

# Commit with single-line message (NO AI attribution)
git commit -m "Add report search API reference documentation"

# Push to branch
git push origin v2/update-main-before-refactor
```

## Important Constraints
- ✅ **Type accuracy**: ALL types must be verified against live API
- ✅ **Executable examples**: Every code block must run without modification
- ✅ **Real outputs**: Include actual command results
- ✅ **Complete imports**: All examples must be copy-pasteable
- ✅ **Filter documentation**: Document all available search filters
- ✅ **Performance awareness**: Document high-cost operations
- ✅ **Single-line commits**: No AI attribution in git messages

## Success Criteria
- [ ] Complete documentation for all search methods
- [ ] All return types validated against live API
- [ ] All examples executable and tested
- [ ] Comprehensive test suite created
- [ ] Documentation builds successfully
- [ ] All tests pass
- [ ] Search filters and performance considerations documented

## Rate Limiting Considerations
- Search endpoints: 5-15+ points per request
- Complex filters significantly increase cost
- Large result sets cost more than small ones
- Total budget: 18,000 points/hour (points are floats)
- Add delays for testing: `await asyncio.sleep(0.5)`
- Test with small limits first to conserve points

## Next Steps After Completion
After completing this section, the agent should:
1. Verify all tests pass
2. Build documentation successfully
3. Commit and push changes
4. Update project status in CLAUDE.md if needed

This plan provides complete technical specifications for implementing the Report Search API documentation following established project standards.