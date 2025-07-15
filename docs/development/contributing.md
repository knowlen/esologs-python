# Contributing Guidelines

Thank you for contributing to ESO Logs Python! This guide covers the contribution workflow and standards.

## Workflow

### 1. Fork and Branch

```bash
# Fork on GitHub, then clone
git clone https://github.com/YOUR_USERNAME/esologs-python.git
cd esologs-python

# Add upstream remote
git remote add upstream https://github.com/knowlen/esologs-python.git

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow these patterns:
- Match existing code style
- Add comprehensive tests
- Update documentation for new features
- Use type hints for all public methods

### 3. Commit

```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "Add character ranking filters"

# Push to your fork
git push origin feature/your-feature-name
```

### 4. Pull Request

- Target the `v2-dev` branch
- Provide clear description
- Link related issues
- Ensure CI passes

## Code Standards

### Python Style

```python
async def get_character_by_id(self, id: int) -> CharacterResponse:
    """Get character information by ID.

    Args:
        id: Character ID to retrieve

    Returns:
        Character data including profile and server

    Raises:
        ValidationError: If character ID is invalid
        GraphQLClientHttpError: If API request fails
    """
    # Implementation
```

- Use Google-style docstrings
- Type hints required for public methods
- Follow Black formatting
- Keep methods focused and testable

### GraphQL Development

When adding new API endpoints:

1. Update `queries.graphql`:
   ```graphql
   query GetNewData($param: Int!) {
       gameData {
           newData(param: $param) {
               id
               name
           }
       }
   }
   ```

2. Regenerate client:
   ```bash
   ariadne-codegen client --config mini.toml
   ```

3. Add tests and documentation

### Testing Requirements

- **Unit tests** for validation logic
- **Integration tests** for API endpoints
- **Documentation tests** for examples
- Aim for 80%+ coverage

## Pull Request Checklist

- [ ] Tests pass (`pytest`)
- [ ] Code quality checks pass (`pre-commit run --all-files`)
- [ ] Documentation updated
- [ ] Changelog entry added (for significant changes)
- [ ] PR targets `v2-dev` branch

## CI/CD Pipeline

GitHub Actions runs automatically:

```yaml
jobs:
  test:
    - Unit tests (fast, no API)
    - Integration tests (with API)
    - Documentation tests
    - Code quality checks
```

## Quick Reference

```bash
# Development setup
pip install -e ".[dev]"
pre-commit install

# Before committing
pytest                          # Run all tests
pre-commit run --all-files      # Code quality

# Documentation
mkdocs serve                    # Preview docs
pytest tests/docs/              # Test examples

# GraphQL updates
ariadne-codegen client --config mini.toml
```

## Getting Help

- Check existing [issues](https://github.com/knowlen/esologs-python/issues)
- Review [Architecture Overview](architecture.md) for technical details
- Follow patterns in existing code

!!! tip "First Contribution?"
    Start with documentation improvements or small bug fixes to get familiar
    with the codebase and workflow.
