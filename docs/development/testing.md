# Testing Guide

ESO Logs Python uses a comprehensive testing framework with 278 tests across four test suites.

## Test Suite Overview

| Test Suite | Tests | API Required | Purpose |
|-----------|-------|--------------|---------|
| **Unit** | 76 | ❌ No | Validation logic, no external dependencies |
| **Integration** | 85 | ✅ Yes | Live API endpoint testing |
| **Documentation** | 98 | ✅ Yes | Validate all code examples |
| **Sanity** | 19 | ✅ Yes | Quick API health check |

## Running Tests

```bash
# Prerequisites for API tests
export ESOLOGS_ID="your_client_id"
export ESOLOGS_SECRET="your_client_secret"

# Quick development feedback (no API needed)
pytest tests/unit/ -v

# Full test suite
pytest

# Specific test suites
pytest tests/integration/    # API endpoint tests
pytest tests/docs/           # Documentation examples
pytest tests/sanity/         # API health check

# Useful options
pytest -x                    # Stop on first failure
pytest --lf                  # Run last failed tests
pytest -k "test_character"   # Run tests matching pattern
pytest --cov=esologs         # Generate coverage report
```

## Test Categories

### Unit Tests (Fast, No API)
- Parameter validation
- OAuth2 authentication logic
- Method signatures
- Error handling

### Integration Tests (Live API)
- All API endpoints (~75% coverage)
- Error responses
- Rate limiting
- Complex workflows

### Documentation Tests
- Every code example from docs
- Prevents documentation drift
- Copy-paste validation

### Sanity Tests
- Broad API coverage
- Quick health verification
- Living documentation

## Test Data

All suites share consistent test data:

```python
TEST_DATA = {
    "character_id": 34663,
    "guild_id": 3660,
    "report_code": "VfxqaX47HGC98rAp",
    "zone_id": 8,
    "ability_id": 1084
}
```

## Writing Tests

### Test Structure

```python
import pytest
from esologs.exceptions import ValidationError

class TestNewFeature:
    """Test suite for new feature."""

    @pytest.mark.asyncio
    async def test_basic_functionality(self, authenticated_client):
        """Test basic functionality works correctly."""
        result = await authenticated_client.new_method()
        assert result is not None
        assert result.data is not None

    def test_validation(self):
        """Test parameter validation."""
        with pytest.raises(ValidationError):
            validate_parameter(-1)  # Invalid input
```

### Adding Tests

1. **Unit tests** for all validation logic
2. **Integration tests** for new API endpoints
3. **Documentation tests** for new examples
4. **Update sanity tests** for new API categories

## Troubleshooting

### Common Issues

```bash
# Authentication failed
export ESOLOGS_ID="your_client_id"
export ESOLOGS_SECRET="your_client_secret"

# Rate limit exceeded (HTTP 429)
# Wait and retry with different credentials

# Network issues
# Check internet connection and API status
```

### Debug Mode

```bash
# Verbose output
pytest -v -s

# Show local variables on failure
pytest --tb=long

# Debug specific test
pytest path/to/test.py::test_name -v -s
```

## Performance

- **Unit tests**: < 5 seconds
- **Integration tests**: ~30 seconds
- **Documentation tests**: ~25 seconds
- **Sanity tests**: ~15 seconds
- **Total**: ~75 seconds

!!! tip "Development Workflow"
    Run unit tests frequently during development for fast feedback.
    Use integration tests before committing to validate API changes.
