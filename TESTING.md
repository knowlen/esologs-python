# Testing Guide

## Test Suites Overview

| Test Suite | Purpose | API Required | Speed | Coverage |
|-----------|---------|--------------|-------|----------|
| **Unit Tests** | Logic validation | No | Fast | Narrow, deep |
| **Integration Tests** | Detailed API testing | Yes | Medium | Focused, thorough |
| **Sanity Tests** | Broad API coverage | Yes | Medium | Wide, shallow |

## Running Tests

### Unit Tests
Run all unit tests (no API credentials needed):
```bash
pytest tests/unit/ -v
```

### Integration Tests
For integration tests that require API access, set environment variables:
```bash
export ESOLOGS_ID="your_client_id"
export ESOLOGS_SECRET="your_client_secret"
pytest tests/integration/ -v
```

### Sanity Tests
Comprehensive API coverage tests (requires API credentials):
```bash
export ESOLOGS_ID="your_client_id"
export ESOLOGS_SECRET="your_client_secret"
pytest tests/sanity/ -v
```

### Legacy Simple Test
Quick validation script (requires API credentials):
```bash
export ESOLOGS_ID="your_client_id"
export ESOLOGS_SECRET="your_client_secret"
python test.py
```

### Validation Testing
The parameter validation is thoroughly tested in `tests/unit/test_validators.py` with 22 test cases covering:
- Report code validation
- Ability ID validation
- Time range validation
- Fight IDs validation
- Limit parameter validation
- Required string validation

## Security Notes

**⚠️ NEVER commit API credentials to version control!**

Always use environment variables or local configuration files (added to .gitignore) for sensitive data:

```bash
# Good: Environment variables
export ESOLOGS_ID="your_id"
export ESOLOGS_SECRET="your_secret"

# Good: .env file (add to .gitignore)
echo "ESOLOGS_ID=your_id" >> .env
echo "ESOLOGS_SECRET=your_secret" >> .env
```

## Test Coverage

Current test coverage:
- **21 unit tests** - Parameter validation and method logic
- **14 integration tests** - Detailed API functionality testing
- **7 sanity test classes** - Comprehensive API coverage validation
- **1 legacy test script** - Simple validation and examples

### Sanity Test Details

The sanity tests provide broad API coverage and serve as living documentation:

```bash
# Run API coverage report
pytest tests/sanity/test_api_sanity.py::TestAPICoverageReport::test_api_coverage_summary -v -s
```

**Coverage Areas:**
- **Game Data**: abilities, classes, factions, items, NPCs (5 features)
- **World Data**: zones, regions (2 features)
- **Character Data**: profiles, rankings (2 features)
- **Guild Data**: basic info (1 feature)
- **Report Data**: individual reports, analysis, search (3 features)
- **System Data**: rate limiting (1 feature)

**Total: 13+ major API features tested**
