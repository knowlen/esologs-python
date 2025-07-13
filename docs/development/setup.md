# Development Setup

Get your development environment ready for contributing to ESO Logs Python.

## Prerequisites

- Python 3.8+
- Git
- ESO Logs API credentials (see [Authentication Guide](../authentication.md))

## Quickstart

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/esologs-python.git
cd esologs-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
```

## Development-Specific Tools

### Code Generation

When modifying GraphQL queries:

```bash
# Edit queries in queries.graphql
vim queries.graphql

# Regenerate client code
ariadne-codegen client --config mini.toml
```

### Pre-commit Hooks

The project uses pre-commit hooks for code quality:

```bash
# Run all checks manually
pre-commit run --all-files

# Update hook versions
pre-commit autoupdate
```

### Key Commands

```bash
# Code quality
black .                      # Format code
isort .                      # Sort imports
ruff check --fix .           # Lint and fix
mypy .                       # Type checking

# Documentation
mkdocs serve                 # Local preview at http://127.0.0.1:8000
mkdocs build --clean         # Build static site

# Testing - see Testing Guide for details
pytest tests/unit/           # Quick unit tests (no API needed)
pytest                       # Run all tests
```

## Project Structure

```
esologs-python/
├── esologs/                 # Generated GraphQL client
├── tests/                   # Test suites (see Testing Guide)
├── docs/                    # Documentation source
├── access_token.py          # OAuth2 authentication
├── queries.graphql          # GraphQL queries to generate
├── schema.graphql           # ESO Logs API schema
└── mini.toml               # Code generation config
```

## Next Steps

- Review the [Testing Guide](testing.md) for running tests
- See [Contributing Guidelines](contributing.md) for PR workflow
- Explore the [Architecture Overview](architecture.md) for technical details

!!! tip "Virtual Environments"
    Always use a virtual environment to avoid dependency conflicts with your system Python.