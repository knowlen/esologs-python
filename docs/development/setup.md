# Development Setup

Set up your development environment for contributing to ESO Logs Python.

## Prerequisites

- **Python**: 3.8 or higher
- **Git**: For version control
- **Virtual Environment**: Recommended for isolation

## Quick Setup

=== "Development Installation"

    ```bash
    # Clone the repository
    git clone https://github.com/knowlen/esologs-python.git
    cd esologs-python
    
    # Create virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    # Install with development dependencies
    pip install --upgrade pip
    pip install -e ".[dev]"
    
    # Set up pre-commit hooks
    pre-commit install
    ```

=== "From Fork"

    ```bash
    # Fork the repository on GitHub first, then:
    git clone https://github.com/YOUR_USERNAME/esologs-python.git
    cd esologs-python
    
    # Add upstream remote
    git remote add upstream https://github.com/knowlen/esologs-python.git
    
    # Set up development environment
    python -m venv venv
    source venv/bin/activate
    pip install -e ".[dev]"
    pre-commit install
    ```

## API Credentials

Set up authentication for testing:

```bash
# Required for integration tests
export ESOLOGS_ID="your_client_id"
export ESOLOGS_SECRET="your_client_secret"
```

Get credentials from [ESO Logs API Clients](https://www.esologs.com/api/clients/).

## Development Commands

### Code Generation

```bash
# Regenerate GraphQL client code
ariadne-codegen client --config mini.toml
```

### Testing

```bash
# Quick verification
python test.py

# All test suites
pytest tests/unit/           # Unit tests (76 tests)
pytest tests/integration/    # Integration tests (85 tests) - requires API credentials
pytest tests/docs/           # Documentation tests (98 tests) - requires API credentials  
pytest tests/sanity/         # Sanity tests (19 tests) - requires API credentials

# Run all tests
pytest
```

### Code Quality

```bash
# Run all quality checks
pre-commit run --all-files

# Individual tools
black .                      # Format code
isort .                      # Sort imports
ruff check --fix .           # Lint and fix
mypy .                       # Type checking
```

### Documentation

```bash
# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build --clean

# Test documentation examples
pytest tests/docs/ -v
```

## Project Structure

```
esologs-python/
├── esologs/                 # Main package
│   ├── client.py           # Generated GraphQL client
│   ├── models/             # Pydantic models
│   └── exceptions.py       # Custom exceptions
├── tests/                  # Test suites
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   ├── docs/              # Documentation tests
│   └── sanity/            # Sanity tests
├── docs/                  # Documentation source
├── access_token.py        # Authentication utilities
├── mini.toml             # ariadne-codegen config
├── schema.graphql        # GraphQL schema
├── queries.graphql       # GraphQL queries
└── pyproject.toml        # Project configuration
```

## Development Workflow

### 1. Create Feature Branch

```bash
# Update main branch
git checkout v2-dev
git pull upstream v2-dev

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow existing code patterns
- Add comprehensive tests
- Update documentation
- Run quality checks

### 3. Test Your Changes

```bash
# Verify all tests pass
pytest

# Check code quality
pre-commit run --all-files

# Test documentation
pytest tests/docs/ -v
```

### 4. Submit Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Create PR on GitHub targeting v2-dev
```

## Configuration Files

### pyproject.toml

Main project configuration with dependencies, dev tools, and build settings.

### mini.toml

ariadne-codegen configuration for GraphQL client generation:

```toml
[tool.ariadne-codegen]
schema_path = "schema.graphql"
queries_path = "queries.graphql"
target_package_path = "esologs"
target_package_name = "esologs"
client_name = "Client"
plugins = ["ariadne_codegen.contrib.shorter_results"]
```

### .pre-commit-config.yaml

Pre-commit hooks for code quality:

- **black**: Code formatting
- **isort**: Import sorting
- **ruff**: Fast Python linting
- **mypy**: Static type checking

## Common Development Tasks

### Adding New API Methods

1. Update `queries.graphql` with new GraphQL queries
2. Run `ariadne-codegen client --config mini.toml`
3. Add tests in appropriate test suite
4. Update documentation with examples
5. Add to API reference docs

### Updating Dependencies

```bash
# Update development dependencies
pip install --upgrade pip
pip install -e ".[dev]" --upgrade

# Update pre-commit hooks
pre-commit autoupdate
```

### Regenerating Test Data

```bash
# Update integration test fixtures
python -m tests.integration.conftest
```

## Troubleshooting

### Common Issues

#### Pre-commit Hook Failures

```bash
# Reset hooks
pre-commit uninstall
pre-commit install
pre-commit run --all-files
```

#### GraphQL Generation Errors

```bash
# Check schema and queries
ariadne-codegen client --config mini.toml --verbose
```

#### Import Errors

```bash
# Reinstall in editable mode
pip uninstall esologs-python
pip install -e ".[dev]"
```

#### Test Failures

```bash
# Check API credentials
echo $ESOLOGS_ID
echo $ESOLOGS_SECRET

# Run specific test
pytest tests/integration/test_game_data.py::test_get_abilities -v
```

### Getting Help

- **Documentation**: Check existing docs and examples
- **Issues**: Search [GitHub issues](https://github.com/knowlen/esologs-python/issues)
- **Code Patterns**: Look at existing implementations
- **API Reference**: [ESO Logs API Documentation](https://www.esologs.com/v2-api-docs/eso/)

## Performance Tips

### Development

- Use virtual environments to avoid dependency conflicts
- Use `-x` flag to stop on first test failure
- Use `--lf` flag to run only last-failed tests
- Cache pre-commit environments for faster execution

### Testing

- Run unit tests first for quick feedback
- Use integration tests for API validation
- Documentation tests ensure examples work
- Sanity tests for quick verification

## Next Steps

- **[Testing Guide](testing.md)** - Comprehensive testing documentation
- **[Contributing Guidelines](contributing.md)** - Contribution workflow and standards
- **[Architecture Overview](architecture.md)** - Technical implementation details

!!! tip "Development Environment"
    Keep your development environment clean by using virtual environments and 
    regularly updating dependencies. The pre-commit hooks will catch most issues 
    before they reach the repository.

!!! warning "API Credentials"
    Never commit API credentials to the repository. Use environment variables 
    and ensure `.env` files are in `.gitignore`.