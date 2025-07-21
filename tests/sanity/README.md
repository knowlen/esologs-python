# Sanity Test Suite

Comprehensive API coverage tests that serve as both sanity checks and living documentation of the ESO Logs Python client library.

## Purpose

The sanity tests provide:
- **Broad API Coverage**: Tests all major endpoints to ensure basic functionality
- **Living Documentation**: Working examples of how to use each API method
- **Quick Validation**: Fast way to verify overall API health
- **Coverage Reporting**: Metrics on which features are working

## Test Structure

### Test Classes

- **`TestGameDataAPISanity`**: Game data endpoints (abilities, classes, items, NPCs, etc.)
- **`TestWorldDataAPISanity`**: World data endpoints (zones, regions, encounters)
- **`TestCharacterDataAPISanity`**: Character data endpoints (profiles, rankings)
- **`TestGuildDataAPISanity`**: Guild data endpoints (basic guild info)
- **`TestReportDataAPISanity`**: Report data endpoints (reports, analysis, search)
- **`TestSystemAPISanity`**: System endpoints (rate limiting)
- **`TestAPICoverageReport`**: Comprehensive coverage reporting

### Features Tested

✅ **Game Data (5 features)**
- Abilities API (single + list)
- Classes API (single + list)
- Factions API
- Items API (single + list)
- NPCs API (single + list)

✅ **World Data (2 features)**
- Zones API
- Regions API

✅ **Character Data (2 features)**
- Character profiles
- Character rankings (encounter + zone)

✅ **Guild Data (1 feature)**
- Basic guild information (get_guild_by_id)

✅ **Report Data (3 features)**
- Individual reports
- Report analysis (events, tables, rankings, player details)
- Advanced report search

✅ **System Data (1 feature)**
- Rate limiting information

## Running Sanity Tests

### Run All Sanity Tests
```bash
pytest tests/sanity/ -v
```

### Run Specific Test Category
```bash
# Game data tests only
pytest tests/sanity/test_api_sanity.py::TestGameDataAPISanity -v

# Report search tests only
pytest tests/sanity/test_api_sanity.py::TestReportDataAPISanity::test_report_search_api -v
```

### Run Coverage Report
```bash
# Get API coverage summary
pytest tests/sanity/test_api_sanity.py::TestAPICoverageReport::test_api_coverage_summary -v -s
```

## Requirements

- **API Credentials**: Must set `ESOLOGS_ID` and `ESOLOGS_SECRET` environment variables
- **Internet Access**: Tests make real API calls to ESO Logs
- **Test Data**: Uses same test data as integration tests (guild 3660, character 34663, etc.)

## vs. Other Test Suites

| Test Suite | Purpose | Scope | Speed |
|-----------|---------|-------|-------|
| **Unit Tests** | Logic validation | Narrow, isolated | Fast |
| **Integration Tests** | Deep API testing | Focused, detailed | Medium |
| **Sanity Tests** | Broad API coverage | Wide, shallow | Medium |

## Benefits

1. **Development Tool**: Quick way to verify API connectivity across all endpoints
2. **Documentation**: Shows working examples of every major API method
3. **Debugging**: Helps identify which API areas are working vs. broken
4. **Onboarding**: New developers can see the full scope of library functionality
5. **CI/CD**: Can be used as smoke tests in deployment pipelines

## Example Output

```
=== API Coverage Report ===
game_data: 5 features - ['abilities', 'classes', 'factions', 'items', 'npcs']
world_data: 2 features - ['zones', 'regions']
character_data: 2 features - ['character_profiles', 'character_rankings']
guild_data: 1 features - ['guild_basic_info']
report_data: 3 features - ['individual_reports', 'report_analysis', 'report_search']
system_data: 1 features - ['rate_limiting']
Total API features working: 14+
```

This shows that 14+ major API features are working correctly, providing confidence in the overall library health.
