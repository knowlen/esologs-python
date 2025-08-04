# Unit Test Suite

Isolated unit tests for the esologs-python library that verify individual functions and methods without external dependencies. These tests focus on logic validation, parameter validation, and method behavior in isolation.

## Purpose

The unit tests provide:
- **Logic Validation**: Ensure individual functions work correctly in isolation
- **Parameter Validation**: Test input validation and error handling
- **Fast Feedback**: Quick execution without API calls or external dependencies
- **Edge Case Coverage**: Test boundary conditions and error scenarios
- **Mocking & Isolation**: Verify behavior using mocks and stubs

## Test Structure

### Core Test Files

- **`test_validators.py`**: Parameter validation functions (22 test classes)
- **`test_access_token.py`**: Tests for auth module - OAuth2 token handling and credential validation
- **`test_character_rankings.py`**: Character ranking method logic and validation
- **`test_report_analysis.py`**: Report analysis method signatures and validation
- **`test_report_search.py`**: Report search validation, date parsing, and method logic
- **`test_method_factory.py`**: Method factory pattern tests (11 tests)
- **`test_param_builders.py`**: Parameter builder pattern tests (20 tests)

### Test Categories

#### Validation Tests (`test_validators.py`)
- **Report Code Validation**: ESO Logs report code format verification
- **Ability ID Validation**: Numeric ability ID parameter checking
- **Time Range Validation**: Start/end time parameter validation
- **Positive Integer Validation**: ID parameter boundary testing
- **Limit Parameter Validation**: Pagination limit validation
- **Fight ID Validation**: Fight ID list validation
- **Required String Validation**: Non-empty string validation

#### Authentication Tests (`test_access_token.py` - tests `esologs.auth` module)
- **Credential Handling**: Environment variable and parameter validation
- **Error Scenarios**: Missing credentials and invalid responses
- **OAuth Flow**: Mock testing of token request/response cycle

#### Method Logic Tests
- **Parameter Processing**: Input transformation and validation
- **Error Conditions**: Invalid input handling and error messages
- **Method Signatures**: Ensure methods accept correct parameters
- **Date Parsing**: Multiple date format support and timestamp conversion

## Running Unit Tests

### Prerequisites

**No external dependencies required** - unit tests run in complete isolation.

```bash
# Install test dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific test file
pytest tests/unit/test_validators.py -v

# Run specific test class
pytest tests/unit/test_validators.py::TestValidateReportCode -v

# Run specific test method
pytest tests/unit/test_validators.py::TestValidateReportCode::test_valid_codes -v

# Run with coverage
pytest tests/unit/ --cov=esologs --cov-report=html

# Run tests in parallel (if pytest-xdist installed)
pytest tests/unit/ -n auto
```

### Test Markers

- `@pytest.mark.unit`: All unit tests (implicit)
- `@pytest.mark.parametrize`: Parameterized tests with multiple inputs
- `@pytest.mark.mock`: Tests using mocking/stubbing

## Test Coverage

### Current Coverage (164 tests)

| Component | Tests | Coverage Focus |
|-----------|-------|----------------|
| **Validators** | 49 tests | All validation functions and edge cases |
| **Access Token** | 8 tests | OAuth2 flow and credential handling |
| **Character Rankings** | 8 tests | Method logic and parameter validation |
| **Report Analysis** | 8 tests | Method signatures and basic validation |
| **Report Search** | 18 tests | Advanced validation, date parsing, and search methods |
| **Method Factory** | 11 tests | Dynamic method generation and factory patterns |
| **Parameter Builders** | 20 tests | Parameter builder patterns and validation |

### Validation Test Coverage
- ✅ **Report Codes**: Valid/invalid format testing
- ✅ **Ability IDs**: Numeric validation and range checking
- ✅ **Time Ranges**: Start/end time validation and ordering
- ✅ **Positive Integers**: ID validation and boundary conditions
- ✅ **Limits**: Pagination parameter validation
- ✅ **Fight IDs**: List validation and type checking
- ✅ **Required Strings**: Non-empty string validation

## Testing Philosophy

### Isolation Principles
- **No API Calls**: Tests never make external network requests
- **Mocked Dependencies**: External dependencies stubbed/mocked
- **Pure Functions**: Focus on input/output behavior
- **Deterministic**: Same inputs always produce same outputs

### Test Organization
- **One Class Per Function**: Each validation function gets its own test class
- **Edge Cases First**: Boundary conditions and error cases prioritized
- **Clear Test Names**: Descriptive test method names explain what's being tested
- **Minimal Setup**: Tests require minimal fixture setup

### Error Testing
- **Exception Types**: Verify correct exception types are raised
- **Error Messages**: Validate error message content and clarity
- **Invalid Inputs**: Test all types of invalid input data
- **Boundary Conditions**: Test min/max values and edge cases

## Benefits

1. **Fast Execution**: Complete test suite runs in seconds
2. **Reliable**: No external dependencies to cause flaky tests
3. **Comprehensive**: High coverage of validation and logic paths
4. **Maintainable**: Isolated tests are easy to understand and modify
5. **Development Aid**: Quick feedback during development

## vs. Other Test Suites

| Test Suite | Dependencies | Speed | Focus | Coverage |
|-----------|-------------|-------|-------|----------|
| **Unit Tests** | None | Very Fast | Logic & Validation | Deep, Narrow |
| **Integration Tests** | API Access | Medium | API Behavior | Focused, Thorough |
| **Sanity Tests** | API Access | Medium | API Health | Broad, Shallow |

## Contributing

When adding new functionality:

1. **Add Unit Tests First**: Write tests before implementation (TDD)
2. **Test Edge Cases**: Include boundary conditions and error scenarios
3. **Use Descriptive Names**: Test names should explain what's being tested
4. **Keep Tests Isolated**: No external dependencies or API calls
5. **Update This README**: Document new test categories and coverage

## Example Test Structure

```python
class TestNewFeature:
    """Test new feature validation and logic."""

    def test_valid_inputs(self):
        """Test that valid inputs work correctly."""
        # Test implementation

    def test_invalid_inputs(self):
        """Test that invalid inputs raise appropriate errors."""
        # Test implementation

    @pytest.mark.parametrize("input,expected", [
        ("valid1", True),
        ("valid2", True),
        ("invalid", False),
    ])
    def test_multiple_cases(self, input, expected):
        """Test multiple input/output combinations."""
        # Test implementation
```

## Debugging Failed Tests

1. **Read Error Messages**: Unit test errors are usually clear and specific
2. **Check Input Values**: Verify test data matches expected formats
3. **Run Single Tests**: Isolate failing tests to understand issues
4. **Use Print Debugging**: Add print statements to see intermediate values
5. **Check Mocks**: Ensure mocked dependencies return expected values

Unit tests provide the foundation for confident development by ensuring all core logic works correctly in isolation.
