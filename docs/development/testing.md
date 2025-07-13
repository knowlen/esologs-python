# Testing Guide

Comprehensive testing framework for ESO Logs Python with four complementary test suites ensuring code quality, API functionality, and documentation accuracy.

## Test Suite Overview

| Test Suite | Purpose | API Required | Speed | Coverage | Test Count |
|-----------|---------|--------------|-------|----------|------------|
| **[Unit Tests](#unit-tests)** | Logic validation | ❌ No | Very Fast | Deep, Narrow | 76 tests |
| **[Integration Tests](#integration-tests)** | API functionality | ✅ Yes | Medium | Focused, Thorough | 85 tests |
| **[Documentation Tests](#documentation-tests)** | Code examples validation | ✅ Yes | Fast | Examples, Accuracy | 98 tests |
| **[Sanity Tests](#sanity-tests)** | API health check | ✅ Yes | Medium | Broad, Shallow | 19 tests |

**Total: 278 tests** providing comprehensive validation across all aspects of the library.

## Quick Start

### Prerequisites

```bash
# Install development dependencies
pip install -e ".[dev]"

# Set API credentials (for integration, docs, and sanity tests)
export ESOLOGS_ID="your_client_id"
export ESOLOGS_SECRET="your_client_secret"
```

### Running Tests

=== "Individual Test Suites"

    ```bash
    # Unit tests (no API required - fastest)
    pytest tests/unit/ -v
    
    # Integration tests (API credentials required)
    pytest tests/integration/ -v
    
    # Documentation tests (API credentials required)
    pytest tests/docs/ -v
    
    # Sanity tests (API credentials required)
    pytest tests/sanity/ -v
    ```

=== "All Tests"

    ```bash
    # Run all test suites
    pytest tests/ -v
    
    # With coverage report
    pytest tests/ --cov=esologs --cov-report=html
    
    # Parallel execution (faster)
    pytest tests/ -n auto
    ```

=== "Development Workflow"

    ```bash
    # Quick development feedback
    pytest tests/unit/ -x  # Stop on first failure
    
    # Test specific functionality
    pytest tests/integration/test_game_data.py -v
    
    # Last failed tests only
    pytest --lf
    ```

## Unit Tests

**Purpose**: Test individual functions and methods in complete isolation

- **✅ No External Dependencies**: Runs without API access or network calls
- **⚡ Fast Execution**: Complete suite runs in seconds
- **🎯 Deep Coverage**: Comprehensive testing of validation logic and edge cases
- **🔍 Error Testing**: Validates error handling and boundary conditions

### Key Areas

| Category | Tests | Coverage |
|----------|-------|----------|
| Parameter validation | 49 tests | Input sanitization, type checking |
| OAuth2 authentication | 8 tests | Token handling, credential validation |
| Method signatures | 24 tests | Function interfaces, return types |
| Error handling | Various | Boundary conditions, edge cases |

### Running Unit Tests

```bash
# All unit tests
pytest tests/unit/ -v

# Specific test files
pytest tests/unit/test_parameter_validation.py -v
pytest tests/unit/test_oauth_authentication.py -v

# Test specific function
pytest tests/unit/test_parameter_validation.py::test_character_id_validation -v
```

### Unit Test Example

```python
def test_character_id_validation():
    """Test character ID parameter validation."""
    # Valid IDs should pass
    assert validate_character_id(12345) == 12345
    
    # Invalid IDs should raise ValidationError
    with pytest.raises(ValidationError):
        validate_character_id(-1)
    
    with pytest.raises(ValidationError):
        validate_character_id("not_a_number")
```

## Integration Tests

**Purpose**: Verify the library works correctly with the real ESO Logs API

- **🌐 Live API Testing**: Makes actual API calls to ESO Logs
- **📊 Comprehensive Coverage**: Tests ~75% of available API endpoints
- **🛡️ Error Handling**: Validates API error responses and edge cases
- **⚙️ Real-World Scenarios**: Tests complex workflows and data processing

### Key Areas

| Category | Coverage |
|----------|----------|
| Game Data APIs | Abilities, classes, items, NPCs, maps, factions |
| Character Data | Profiles, reports, rankings |
| Report Analysis | Events, graphs, tables, rankings, player details |
| Advanced Search | Multi-criteria filtering, pagination |
| Error Handling | Rate limiting, authentication, not found |

### Running Integration Tests

```bash
# All integration tests (requires API credentials)
pytest tests/integration/ -v

# Specific API categories
pytest tests/integration/test_game_data.py -v
pytest tests/integration/test_character_data.py -v
pytest tests/integration/test_report_analysis.py -v
pytest tests/integration/test_report_search.py -v

# Test specific functionality
pytest tests/integration/test_game_data.py::test_get_abilities_with_pagination -v
```

### Integration Test Example

```python
@pytest.mark.asyncio
async def test_get_character_by_id(authenticated_client):
    """Test retrieving character information."""
    character_id = 34663  # Test character
    
    result = await authenticated_client.get_character_by_id(id=character_id)
    
    # Validate response structure
    assert result.character_data is not None
    assert result.character_data.character is not None
    
    character = result.character_data.character
    assert character.id == character_id
    assert character.name is not None
    assert character.server is not None
```

## Documentation Tests

**Purpose**: Ensure documentation code examples are accurate and executable

- **📋 Example Validation**: Tests all code blocks from documentation
- **🔄 Prevents Documentation Drift**: Ensures examples stay current with API changes
- **✅ User Confidence**: Guarantees copy-paste examples work as expected
- **🤖 CI/CD Integration**: Automated validation of documentation accuracy

### Key Areas

| Documentation File | Tests | Purpose |
|-------------------|-------|---------|
| API Reference | 70 tests | All API method examples |
| Quickstart Guide | 12 tests | Getting started examples |
| Authentication | 8 tests | Auth setup and usage |
| Installation | 4 tests | Setup verification |
| Error Handling | 4 tests | Exception patterns |

### Running Documentation Tests

```bash
# All documentation tests
pytest tests/docs/ -v

# Specific documentation files
pytest tests/docs/test_quickstart_examples.py -v
pytest tests/docs/test_authentication_examples.py -v
pytest tests/docs/test_api_reference_examples.py -v

# Test specific example
pytest tests/docs/test_quickstart_examples.py::test_hello_esologs_example -v
```

### Documentation Test Example

```python
@pytest.mark.asyncio
async def test_quickstart_example(authenticated_client):
    """Test the main quickstart example works."""
    # This example is taken directly from docs/quickstart.md
    
    rate_limit = await authenticated_client.get_rate_limit_data()
    
    # Verify the example produces expected results
    assert rate_limit.rate_limit_data is not None
    assert rate_limit.rate_limit_data.limit_per_hour > 0
    assert rate_limit.rate_limit_data.points_spent_this_hour >= 0
```

## Sanity Tests

**Purpose**: Broad API coverage testing and living documentation

- **📋 API Coverage Report**: Tests 13+ major API features across 6 categories
- **📚 Living Documentation**: Working examples of every API method
- **🚀 Quick Validation**: Fast way to verify overall API health
- **🎯 Smoke Testing**: Ideal for CI/CD pipelines and deployment verification

### Coverage Areas

| Category | Features | Tests |
|----------|----------|-------|
| Game Data | Abilities, classes, factions, items, NPCs | 5 tests |
| World Data | Zones, regions | 2 tests |
| Character Data | Profiles, rankings | 2 tests |
| Guild Data | Basic info | 1 test |
| Report Data | Reports, analysis, search | 3 tests |
| System Data | Rate limiting | 1 test |

### Running Sanity Tests

```bash
# All sanity tests
pytest tests/sanity/ -v

# Specific categories
pytest tests/sanity/test_game_data_sanity.py -v
pytest tests/sanity/test_character_data_sanity.py -v
pytest tests/sanity/test_report_data_sanity.py -v

# Quick health check
pytest tests/sanity/test_api_health.py -v
```

### Sanity Test Example

```python
@pytest.mark.asyncio
async def test_game_data_api_coverage(authenticated_client):
    """Test major game data API endpoints."""
    
    # Test abilities
    abilities = await authenticated_client.get_abilities(limit=5)
    assert len(abilities.game_data.abilities.data) > 0
    
    # Test classes
    classes = await authenticated_client.get_classes()
    assert len(classes.game_data.classes) > 0
    
    # Test items
    items = await authenticated_client.get_items(limit=5)
    assert len(items.game_data.items.data) > 0
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

### Shared Fixtures

```python
@pytest.fixture
async def authenticated_client():
    """Provides authenticated client for tests."""
    token = get_access_token()
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        yield client
```

## Development Workflow

### Test-Driven Development

```bash
# 1. Write unit tests first
pytest tests/unit/test_new_feature.py -v

# 2. Implement functionality
# ... code implementation ...

# 3. Verify integration
pytest tests/integration/test_new_feature.py -v

# 4. Add documentation examples
pytest tests/docs/test_new_feature_examples.py -v

# 5. Update sanity tests if needed
pytest tests/sanity/ -v
```

### Pre-commit Testing

```bash
# Quick validation during development
pytest tests/unit/ -x

# Before committing changes
pytest tests/integration/ tests/docs/ -v

# Full validation before push
pytest tests/ --cov=esologs
```

## API Credentials

Integration, documentation, and sanity tests require ESO Logs API credentials:

### Setting Credentials

=== "Environment Variables"

    ```bash
    export ESOLOGS_ID="your_client_id"
    export ESOLOGS_SECRET="your_client_secret"
    ```

=== "`.env` File"

    ```bash
    # Create .env file (add to .gitignore)
    echo "ESOLOGS_ID=your_client_id" >> .env
    echo "ESOLOGS_SECRET=your_client_secret" >> .env
    ```

=== "GitHub Actions"

    ```yaml
    env:
      ESOLOGS_ID: ${{ secrets.ESOLOGS_ID }}
      ESOLOGS_SECRET: ${{ secrets.ESOLOGS_SECRET }}
    ```

### Getting Credentials

1. Create account at [esologs.com](https://www.esologs.com/)
2. Visit [API Clients](https://www.esologs.com/api/clients/)
3. Create new client application
4. Copy Client ID and Client Secret

!!! warning "Security"
    Never commit API credentials to version control! Use environment variables or `.env` files (gitignored).

## Coverage Goals

### Current Coverage

- **Unit Tests**: 100% coverage of validation logic
- **Integration Tests**: ~75% API endpoint coverage
- **Documentation Tests**: 100% documentation example coverage
- **Sanity Tests**: 13+ major API features validated
- **Overall**: 70% code coverage with high-quality tests

### Target Coverage

- **Unit Tests**: Maintain 100% validation coverage
- **Integration Tests**: Expand to 90% API coverage
- **Documentation Tests**: Maintain 100% example coverage
- **Sanity Tests**: Cover all major API categories
- **Overall**: Achieve 80%+ code coverage

## Test Performance

| Suite | Execution Time | Tests | Purpose |
|-------|---------------|-------|---------|
| Unit | < 5 seconds | 76 | Development feedback |
| Integration | ~30 seconds | 85 | API validation |
| Documentation | ~25 seconds | 98 | Examples validation |
| Sanity | ~15 seconds | 19 | Health check |
| **Total** | **~75 seconds** | **278** | **Complete validation** |

## CI/CD Integration

### GitHub Actions Configuration

```yaml
name: Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
    
    - name: Run Unit Tests
      run: pytest tests/unit/ -v
    
    - name: Run Integration Tests
      env:
        ESOLOGS_ID: ${{ secrets.ESOLOGS_ID }}
        ESOLOGS_SECRET: ${{ secrets.ESOLOGS_SECRET }}
      run: pytest tests/integration/ -v
    
    - name: Run Documentation Tests
      env:
        ESOLOGS_ID: ${{ secrets.ESOLOGS_ID }}
        ESOLOGS_SECRET: ${{ secrets.ESOLOGS_SECRET }}
      run: pytest tests/docs/ -v
    
    - name: Run Sanity Tests
      env:
        ESOLOGS_ID: ${{ secrets.ESOLOGS_ID }}
        ESOLOGS_SECRET: ${{ secrets.ESOLOGS_SECRET }}
      run: pytest tests/sanity/ -v
```

### Optimization Tips

- **Test Selection**: Use `pytest -k pattern` to run specific tests
- **Caching**: Cache dependencies and test environments
- **Fail Fast**: Use `-x` flag to stop on first failure during development
- **Verbose Output**: Use `-v` for detailed test information

## Troubleshooting

### Common Issues

#### API Credentials Not Set

```
pytest tests/integration/ 
# Error: Authentication failed

# Solution:
export ESOLOGS_ID="your_client_id"
export ESOLOGS_SECRET="your_client_secret"
```

#### Rate Limit Exceeded

```
GraphQLClientHttpError: HTTP status code: 429

# Solution: Wait and retry, or use different credentials
pytest tests/integration/ --maxfail=1 --tb=short
```

#### Network Connection Issues

```
httpx.ConnectError: [Errno -2] Name or service not known

# Solution: Check internet connection and ESO Logs API status
curl -I https://www.esologs.com/api/v2/client
```

### Debug Mode

Enable verbose output for debugging:

```bash
# Verbose output
pytest tests/integration/ -v -s

# Debug specific test
pytest tests/integration/test_game_data.py::test_get_abilities -v -s

# Show local variables on failure
pytest tests/integration/ --tb=long
```

## Adding New Tests

### Test Categories

1. **Unit Tests**: Add for all new validation logic and methods
2. **Integration Tests**: Add for new API endpoints and workflows
3. **Documentation Tests**: Add for new code examples in documentation
4. **Sanity Tests**: Update coverage report for new API features

### Test Guidelines

- **Descriptive Names**: Test names should explain what's being tested
- **Clear Assertions**: Use specific assertions with helpful error messages
- **Isolated Tests**: Each test should be independent and repeatable
- **Edge Cases**: Include boundary conditions and error scenarios
- **Documentation**: Update this guide when adding new test categories

### Example Test Structure

```python
import pytest
from esologs.client import Client
from access_token import get_access_token

class TestNewFeature:
    """Test suite for new feature functionality."""
    
    @pytest.mark.asyncio
    async def test_basic_functionality(self, authenticated_client):
        """Test basic functionality works correctly."""
        result = await authenticated_client.new_method()
        
        assert result is not None
        assert result.data is not None
    
    @pytest.mark.asyncio
    async def test_error_handling(self, authenticated_client):
        """Test error handling for invalid input."""
        with pytest.raises(ValidationError):
            await authenticated_client.new_method(invalid_param=-1)
    
    @pytest.mark.asyncio
    async def test_edge_cases(self, authenticated_client):
        """Test edge cases and boundary conditions."""
        # Test with minimum values
        result = await authenticated_client.new_method(limit=1)
        assert len(result.data) <= 1
        
        # Test with maximum values
        result = await authenticated_client.new_method(limit=25)
        assert len(result.data) <= 25
```

## Next Steps

- **[Contributing Guidelines](contributing.md)** - Contribution workflow and standards
- **[Development Setup](setup.md)** - Environment setup and tools
- **[Architecture Overview](architecture.md)** - Technical implementation details

!!! tip "Testing Best Practices"
    - Run unit tests frequently during development for fast feedback
    - Use integration tests to validate API changes
    - Documentation tests ensure examples stay current
    - Sanity tests provide quick overall health checks

!!! info "Performance"
    The complete test suite runs in ~75 seconds, making it suitable for CI/CD pipelines 
    while providing comprehensive validation of all library functionality.