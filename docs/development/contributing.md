# Contributing Guidelines

Thank you for considering contributing to ESO Logs Python! This guide will help you get started with contributing to the project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git for version control
- ESO Logs API credentials for testing
- Familiarity with async/await patterns

### Development Setup

1. **Fork and Clone**

   ```bash
   # Fork the repository on GitHub, then:
   git clone https://github.com/YOUR_USERNAME/esologs-python.git
   cd esologs-python
   
   # Add upstream remote
   git remote add upstream https://github.com/knowlen/esologs-python.git
   ```

2. **Environment Setup**

   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   pip install --upgrade pip
   pip install -e ".[dev]"
   
   # Set up pre-commit hooks
   pre-commit install
   ```

3. **API Credentials**

   ```bash
   # Required for integration tests
   export ESOLOGS_ID="your_client_id"
   export ESOLOGS_SECRET="your_client_secret"
   ```

   Get credentials from [ESO Logs API Clients](https://www.esologs.com/api/clients/).

## Development Workflow

### 1. Create Feature Branch

```bash
# Stay up to date with upstream
git checkout v2-dev
git pull upstream v2-dev

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow these guidelines when making changes:

- **Code Style**: Follow existing patterns and conventions
- **Type Safety**: Use type hints and Pydantic models
- **Testing**: Add comprehensive tests for new functionality
- **Documentation**: Update docs and add examples

### 3. Testing

Run the complete test suite:

```bash
# Unit tests (fast, no API required)
pytest tests/unit/ -v

# Integration tests (API credentials required)
pytest tests/integration/ -v

# Documentation tests (validates all examples)
pytest tests/docs/ -v

# Sanity tests (quick health check)
pytest tests/sanity/ -v

# All tests with coverage
pytest tests/ --cov=esologs --cov-report=html
```

### 4. Code Quality

Ensure code quality before committing:

```bash
# Run all quality checks
pre-commit run --all-files

# Individual tools
black .                      # Format code
isort .                      # Sort imports
ruff check --fix .           # Lint and fix issues
mypy .                       # Type checking
```

### 5. Documentation

Update documentation for new features:

```bash
# Test documentation examples
pytest tests/docs/ -v

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build --clean
```

### 6. Commit and Push

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add character ranking filters"

# Push to your fork
git push origin feature/your-feature-name
```

### 7. Create Pull Request

- Open PR on GitHub targeting `v2-dev` branch
- Provide clear description of changes
- Link any related issues
- Ensure CI checks pass

## Contribution Types

### Bug Fixes

1. **Identify the Issue**
   - Search existing issues
   - Reproduce the bug
   - Create issue if it doesn't exist

2. **Fix Implementation**
   - Write failing test first (TDD)
   - Implement fix
   - Ensure all tests pass

3. **Testing**
   - Add regression test
   - Verify fix with integration tests
   - Update documentation if needed

### New Features

1. **API Endpoints**
   - Update `queries.graphql` with new GraphQL queries
   - Run `ariadne-codegen client --config mini.toml`
   - Add comprehensive tests
   - Update API reference documentation

2. **Helper Methods**
   - Add to appropriate client module
   - Include parameter validation
   - Add unit and integration tests
   - Document with examples

3. **Enhancement Features**
   - Follow existing architectural patterns
   - Maintain backward compatibility
   - Add comprehensive test coverage

### Documentation

1. **API Reference**
   - Add complete examples for new methods
   - Include error handling patterns
   - Test all code examples

2. **Guides and Tutorials**
   - Write clear, actionable content
   - Include working code examples
   - Add automated tests for examples

3. **Code Comments**
   - Document complex logic
   - Explain GraphQL query structures
   - Add type hints and docstrings

## Code Standards

### Python Style

- **Formatting**: Use Black for code formatting
- **Imports**: Use isort for import sorting
- **Linting**: Follow ruff recommendations
- **Type Hints**: Required for all public methods
- **Docstrings**: Use Google style docstrings

```python
async def get_character_by_id(self, id: int) -> CharacterResponse:
    """Get character information by ID.
    
    Args:
        id: Character ID to retrieve
        
    Returns:
        Character data including profile and server information
        
    Raises:
        ValidationError: If character ID is invalid
        GraphQLClientHttpError: If API request fails
    """
    # Implementation here
```

### Testing Standards

- **Test Coverage**: Aim for 80%+ code coverage
- **Test Types**: Include unit, integration, and documentation tests
- **Naming**: Use descriptive test names explaining what's being tested
- **Isolation**: Tests should be independent and repeatable

```python
@pytest.mark.asyncio
async def test_get_character_by_id_valid_input(authenticated_client):
    """Test getting character with valid ID returns expected data."""
    character_id = 34663
    
    result = await authenticated_client.get_character_by_id(id=character_id)
    
    assert result.character_data is not None
    assert result.character_data.character.id == character_id
```

### Documentation Standards

- **Completeness**: Document all public methods with examples
- **Accuracy**: Test all code examples with automated tests
- **Clarity**: Use clear, actionable language
- **Examples**: Include realistic, working examples

## GraphQL Development

### Adding New Queries

1. **Update queries.graphql**

   ```graphql
   query GetNewData($param: Int!) {
       gameData {
           newData(param: $param) {
               id
               name
               description
           }
       }
   }
   ```

2. **Regenerate Client**

   ```bash
   ariadne-codegen client --config mini.toml
   ```

3. **Add Client Method**

   ```python
   async def get_new_data(self, param: int) -> NewDataResponse:
       """Get new data by parameter."""
       variables = {"param": param}
       response = await self.execute(
           query=GET_NEW_DATA,
           variables=variables
       )
       return NewDataResponse.model_validate(response)
   ```

### Query Guidelines

- **Efficient Queries**: Request only needed fields
- **Pagination**: Include pagination for list queries
- **Error Handling**: Handle GraphQL errors appropriately
- **Validation**: Validate all input parameters

## Testing Guidelines

### Test Structure

```
tests/
├── unit/                   # Unit tests (no API calls)
│   ├── test_validation.py  # Parameter validation
│   └── test_auth.py        # Authentication logic
├── integration/            # Integration tests (live API)
│   ├── test_game_data.py   # Game data endpoints
│   └── test_characters.py  # Character endpoints
├── docs/                   # Documentation tests
│   └── test_examples.py    # All doc examples
└── sanity/                 # Sanity tests
    └── test_coverage.py    # API coverage check
```

### Writing Tests

1. **Unit Tests**: Test validation logic and error handling
2. **Integration Tests**: Test real API interactions
3. **Documentation Tests**: Validate all code examples
4. **Sanity Tests**: Broad coverage and health checks

### Test Data

Use consistent test data across test suites:

```python
TEST_DATA = {
    "character_id": 34663,
    "guild_id": 3660,
    "report_code": "VfxqaX47HGC98rAp",
    "zone_id": 8,
    "ability_id": 1084
}
```

## Documentation Guidelines

### API Reference

- **Complete Examples**: Every method needs working examples
- **Error Handling**: Show how to handle common errors
- **Parameter Documentation**: Document all parameters with types
- **Return Values**: Document response structure

### Code Examples

- **Runnable Code**: All examples must be tested and working
- **Realistic Data**: Use real character/guild IDs when possible
- **Error Handling**: Include try/catch blocks
- **Best Practices**: Demonstrate proper async patterns

### Writing Style

- **Clear and Concise**: Use simple, direct language
- **Action-Oriented**: Focus on what users can do
- **Complete**: Include all necessary setup and context
- **Updated**: Keep examples current with API changes

## Release Process

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Changelog

Update `docs/changelog.md` with:

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

## Getting Help

### Resources

- **Documentation**: [esologs-python.readthedocs.io](https://esologs-python.readthedocs.io/)
- **API Reference**: [ESO Logs API Docs](https://www.esologs.com/v2-api-docs/eso/)
- **Issues**: [GitHub Issues](https://github.com/knowlen/esologs-python/issues)

### Communication

- **Bug Reports**: Use GitHub issues with reproduction steps
- **Feature Requests**: Use GitHub issues with clear use cases
- **Questions**: Check existing issues and documentation first

### Code Review

All contributions go through code review:

- **Automated Checks**: CI must pass (tests, linting, type checking)
- **Manual Review**: Maintainer reviews code quality and design
- **Feedback**: Address review comments promptly
- **Approval**: Two approvals required for merge

## Code of Conduct

### Our Standards

- **Respectful**: Be respectful and considerate in communications
- **Constructive**: Provide constructive feedback and criticism
- **Inclusive**: Welcome newcomers and different perspectives
- **Professional**: Maintain professionalism in all interactions

### Unacceptable Behavior

- Harassment or discrimination of any kind
- Offensive, derogatory, or inappropriate comments
- Personal attacks or trolling
- Publishing private information without permission

## Recognition

Contributors are recognized in:

- **Changelog**: Credited for significant contributions
- **Documentation**: Listed in acknowledgments
- **GitHub**: Contributor statistics and history

## Quick Reference

### Essential Commands

```bash
# Development setup
pip install -e ".[dev]"
pre-commit install

# Testing
pytest tests/unit/ -v           # Fast unit tests
pytest tests/integration/ -v    # Full API tests
pytest tests/docs/ -v           # Doc examples

# Code quality
pre-commit run --all-files     # All checks
black . && isort . && ruff check --fix . && mypy .

# Documentation
mkdocs serve                   # Local docs server
pytest tests/docs/ -v          # Test examples

# GraphQL
ariadne-codegen client --config mini.toml  # Regenerate client
```

### File Locations

- **Source Code**: `esologs/`
- **Tests**: `tests/`
- **Documentation**: `docs/`
- **Configuration**: `pyproject.toml`, `mini.toml`
- **GraphQL**: `schema.graphql`, `queries.graphql`

Thank you for contributing to ESO Logs Python! Your contributions help make the library better for everyone.

!!! tip "First Time Contributors"
    Start with documentation improvements or small bug fixes to get familiar with the 
    codebase and development workflow before tackling larger features.

!!! info "Questions?"
    Don't hesitate to ask questions in GitHub issues. We're here to help and welcome 
    contributors of all experience levels.