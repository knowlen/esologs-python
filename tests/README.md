# ESO Logs Python Test Suite

Comprehensive testing framework for the esologs-python library, providing three complementary test suites that ensure code quality, API functionality, and overall system health.

## Test Suite Overview

| Test Suite | Purpose | API Required | Speed | Coverage | Test Count |
|-----------|---------|--------------|-------|----------|------------|
| **[Unit Tests](unit/)** | Logic validation | ❌ No | Very Fast | Deep, Narrow | 76 tests |
| **[Integration Tests](integration/)** | API functionality | ✅ Yes | Medium | Focused, Thorough | 85 tests |
| **[Sanity Tests](sanity/)** | API health check | ✅ Yes | Medium | Broad, Shallow | 19 tests |

## Quick Start

### Running All Tests
```bash
# Unit tests (no API required)
pytest tests/unit/ -v

# Integration tests (API credentials required)
export ESOLOGS_ID="your_client_id"
export ESOLOGS_SECRET="your_client_secret"
pytest tests/integration/ -v

# Sanity tests (API credentials required)
export ESOLOGS_ID="your_client_id"
export ESOLOGS_SECRET="your_client_secret"
pytest tests/sanity/ -v

# All tests
pytest tests/ -v
```

### Coverage Report
```bash
pytest tests/ --cov=esologs --cov-report=html
```

## Test Suite Details

### 🔧 [Unit Tests](unit/) - Logic & Validation
**Purpose**: Test individual functions and methods in complete isolation

- **✅ No External Dependencies**: Runs without API access or network calls
- **⚡ Fast Execution**: Complete suite runs in seconds
- **🎯 Deep Coverage**: Comprehensive testing of validation logic and edge cases
- **🔍 Error Testing**: Validates error handling and boundary conditions

**Key Areas**:
- Parameter validation (49 tests)
- OAuth2 authentication logic (8 tests)
- Method signatures and logic (24 tests)
- Date parsing and transformation
- Input sanitization and error handling

[→ View Unit Test Details](unit/README.md)

### 🔌 [Integration Tests](integration/) - API Functionality
**Purpose**: Verify the library works correctly with the real ESO Logs API

- **🌐 Live API Testing**: Makes actual API calls to ESO Logs
- **📊 Comprehensive Coverage**: Tests ~60% of available API endpoints
- **🛡️ Error Handling**: Validates API error responses and edge cases
- **⚙️ Real-World Scenarios**: Tests complex workflows and data processing

**Key Areas**:
- Game data APIs (abilities, classes, items, NPCs, maps)
- Character data and rankings
- Report analysis (events, tables, rankings, player details)
- Advanced report search functionality
- Error handling and rate limiting

[→ View Integration Test Details](integration/README.md)

### 🩺 [Sanity Tests](sanity/) - API Health Check
**Purpose**: Broad API coverage testing and living documentation

- **📋 API Coverage Report**: Tests 13+ major API features across 6 categories
- **📚 Living Documentation**: Working examples of every API method
- **🚀 Quick Validation**: Fast way to verify overall API health
- **🎯 Smoke Testing**: Ideal for CI/CD pipelines and deployment verification

**Coverage Areas**:
- Game Data: abilities, classes, factions, items, NPCs (5 features)
- World Data: zones, regions (2 features)
- Character Data: profiles, rankings (2 features)
- Guild Data: basic info (1 feature)
- Report Data: reports, analysis, search (3 features)
- System Data: rate limiting (1 feature)

[→ View Sanity Test Details](sanity/README.md)

## Testing Strategy

### Development Workflow
1. **🔧 Unit Tests First**: Write and run unit tests during development
2. **🔌 Integration Testing**: Verify API integration works correctly
3. **🩺 Sanity Check**: Ensure overall system health before deployment

### Test Selection Guide
```bash
# During development - fast feedback
pytest tests/unit/

# Before committing - verify API integration
pytest tests/integration/

# Before deployment - overall health check
pytest tests/sanity/

# Full validation - comprehensive testing
pytest tests/
```

## Test Data & Fixtures

All test suites share common test data for consistency:

```python
test_data = {
    "character_id": 34663,        # Test character
    "guild_id": 3660,             # Test guild
    "report_code": "VfxqaX47HGC98rAp",  # Test report
    "encounter_id": 27,           # Test encounter
    "zone_id": 8,                 # Test zone
    "ability_id": 1084,           # Test ability
    "item_id": 19,                # Test item
    "class_id": 1,                # Test class
    "map_id": 1,                  # Test map
    "npc_id": 1                   # Test NPC
}
```

## API Credentials

Integration and sanity tests require ESO Logs API credentials:

```bash
# Set environment variables
export ESOLOGS_ID="your_client_id"
export ESOLOGS_SECRET="your_client_secret"

# Or create .env file (add to .gitignore)
echo "ESOLOGS_ID=your_client_id" >> .env
echo "ESOLOGS_SECRET=your_client_secret" >> .env
```

**⚠️ Security**: Never commit API credentials to version control!

## Coverage Goals

### Current Coverage
- **Unit Tests**: 100% coverage of validation logic
- **Integration Tests**: ~65% API endpoint coverage
- **Sanity Tests**: 13+ major API features validated
- **Overall**: 70% code coverage with high-quality tests

### Target Coverage
- **Unit Tests**: Maintain 100% validation coverage
- **Integration Tests**: Expand to 90% API coverage
- **Sanity Tests**: Cover all major API categories
- **Overall**: Achieve 80%+ code coverage

## Contributing

### Adding New Tests

1. **Unit Tests**: Add for all new validation logic and methods
2. **Integration Tests**: Add for new API endpoints and workflows
3. **Sanity Tests**: Update coverage report for new API features
4. **Documentation**: Update relevant README files

### Test Guidelines

- **Descriptive Names**: Test names should explain what's being tested
- **Clear Assertions**: Use specific assertions with helpful error messages
- **Isolated Tests**: Each test should be independent and repeatable
- **Edge Cases**: Include boundary conditions and error scenarios
- **Documentation**: Update README files when adding new test categories

### Running Pre-commit Checks

```bash
# Run all quality checks
pre-commit run --all-files

# Run specific checks
black . && isort . && ruff check --fix . && mypy .
```

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run Unit Tests
  run: pytest tests/unit/ -v

- name: Run Integration Tests
  env:
    ESOLOGS_ID: ${{ secrets.ESOLOGS_ID }}
    ESOLOGS_SECRET: ${{ secrets.ESOLOGS_SECRET }}
  run: pytest tests/integration/ -v

- name: Run Sanity Tests
  env:
    ESOLOGS_ID: ${{ secrets.ESOLOGS_ID }}
    ESOLOGS_SECRET: ${{ secrets.ESOLOGS_SECRET }}
  run: pytest tests/sanity/ -v
```

## Test Performance

| Suite | Execution Time | Tests | Purpose |
|-------|---------------|-------|---------|
| Unit | < 5 seconds | 81 | Development feedback |
| Integration | ~30 seconds | 67 | API validation |
| Sanity | ~15 seconds | 18 | Health check |
| **Total** | **~60 seconds** | **180** | **Complete validation** |

The test suite provides comprehensive coverage while maintaining fast execution times for efficient development workflows.
