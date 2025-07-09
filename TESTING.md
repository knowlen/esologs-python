# Testing Guide

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
- **52 unit tests** - All validation and API methods
- **67% overall coverage** - With 100% coverage on validation module
- **22 validation tests** - Comprehensive parameter validation testing