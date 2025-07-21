# Integration Tests

This directory contains comprehensive integration tests for the esologs-python library. These tests verify that the library works correctly with the actual ESO Logs API.

## Test Structure

### Core Test Files

- **`test_core_api.py`**: Tests for fundamental API endpoints (game data, character data, world data, etc.)
- **`test_character_rankings.py`**: Tests for character rankings functionality (PR #1)
- **`test_report_analysis.py`**: Tests for report analysis functionality (PR #2)
- **`test_report_search.py`**: Tests for advanced report search functionality (PR #4)
- **`test_error_handling.py`**: Tests for error handling and edge cases
- **`conftest.py`**: Shared fixtures and configuration

### Test Categories

#### Game Data Tests
- Abilities, classes, factions, items, NPCs, maps
- Pagination and filtering
- Data integrity validation

#### Character Data Tests
- Character profiles and reports
- Character rankings (encounter and zone)
- Performance metrics validation

#### Report Analysis Tests
- Event data retrieval
- Graph and table data analysis
- Report rankings and player details
- Comprehensive workflow testing

#### Error Handling Tests
- Invalid IDs and parameters
- Malformed inputs
- Rate limiting scenarios
- Connection resilience

## Running Integration Tests

### Prerequisites

1. **API Credentials**: Set environment variables:
   ```bash
   export ESOLOGS_ID="your_client_id"
   export ESOLOGS_SECRET="your_client_secret"
   ```

2. **Dependencies**: Install test dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests

```bash
# Run all integration tests
pytest tests/integration/

# Run specific test file
pytest tests/integration/test_character_rankings.py

# Run with verbose output
pytest tests/integration/ -v

# Run tests with coverage
pytest tests/integration/ --cov=esologs

# Run only fast tests (skip slow tests)
pytest tests/integration/ -m "not slow"
```

### Test Markers

- `@pytest.mark.integration`: All integration tests
- `@pytest.mark.slow`: Slow tests that may be skipped
- `@pytest.mark.asyncio`: Async tests requiring asyncio

## Test Data

Tests use fixed test data defined in `conftest.py`:

- **Character ID**: 34663
- **Guild ID**: 3660
- **Report Code**: VfxqaX47HGC98rAp
- **Encounter ID**: 27
- **Zone ID**: 8

## API Coverage Testing

Integration tests verify ~60% API coverage across:

### ✅ Currently Tested
- **Game Data**: abilities, classes, factions, items, maps, NPCs
- **Character Data**: profiles, reports, rankings (encounter & zone)
- **World Data**: regions, zones, encounters
- **Guild Data**: basic guild information (get_guild_by_id)
- **Report Data**: individual reports, comprehensive analysis, advanced search
- **System Data**: rate limiting

### 🚧 Future Coverage
- User account integration
- Progress race tracking
- Enhanced guild features

## Test Reliability

### Stable Test Data
- Uses established characters, guilds, and reports
- Validates response structure without relying on specific values
- Handles API changes gracefully

### Error Handling
- Tests invalid inputs without causing failures
- Verifies graceful degradation
- Validates error response structures

### Rate Limiting
- Includes delays between requests
- Tests rate limit awareness
- Validates concurrent request handling

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

1. **Fast Tests**: Core functionality validation
2. **Comprehensive Tests**: Full API coverage verification
3. **Error Tests**: Edge case and resilience testing

## Contributing

When adding new API methods:

1. Add integration tests in appropriate test file
2. Update test data in `conftest.py` if needed
3. Ensure tests handle both success and error cases
4. Update this README with new test coverage

## Performance Considerations

- Tests include rate limiting awareness
- Concurrent request testing validates performance
- Large dataset handling verified
- Memory usage patterns tested

## Security

- API credentials handled securely
- No sensitive data in test outputs
- Proper credential validation before test execution
