# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview
Python client library for ESO Logs API v2. GraphQL-based interface using `ariadne-codegen`.
- **Status**: v0.2.0-alpha, ~65% API coverage (Advanced Report Search recently added)
- **Target**: 95%+ API coverage
- **Authentication**: OAuth2 with `ESOLOGS_ID` and `ESOLOGS_SECRET` environment variables

## Essential Commands

### Installation
```bash
pip install -e .              # Production
pip install -e ".[dev]"       # Development with all tools
```

### Code Generation
```bash
ariadne-codegen client --config mini.toml
```

### Testing
```bash
python test.py               # Simple integration test (requires API credentials)
pytest tests/unit/           # Unit tests (76 tests)
pytest tests/integration/    # Integration tests (85 tests, requires API credentials)
pytest tests/docs/           # Documentation tests (49 tests, requires API credentials)
pytest tests/sanity/         # Sanity tests (19 tests, requires API credentials)
```

### Documentation Testing
```bash
pytest tests/docs/              # All documentation examples
pytest tests/docs/test_quickstart_examples.py -v
pytest tests/docs/test_authentication_examples.py -v
```

### Code Quality
```bash
pre-commit run --all-files   # All checks
black . && isort . && ruff check --fix . && mypy .
```

## API Coverage & Architecture
**Current (~65%)**:
- **Game Data**: abilities, classes, factions, items, maps, NPCs
- **Character Data**: profiles, reports, rankings
- **World Data**: regions, zones, encounters
- **Guild Data**: basic info
- **Report Data**: individual reports, analysis, **search (NEW)**
- **System**: rate limiting

**Recently Added**: Advanced Report Search API with flexible filtering, pagination, and convenience methods

**Missing (~35%)**: User accounts, progress tracking, enhanced guild features

## Configuration Files
- **`pyproject.toml`**: Dependencies, dev tools, code quality config, docs dependencies
- **`mini.toml`**: ariadne-codegen configuration
- **`schema.graphql`**: GraphQL schema
- **`queries.graphql`**: GraphQL queries for code generation
- **`mkdocs.yml`**: Documentation site configuration
- **`tests/docs/conftest.py`**: Documentation testing fixtures

## Key Implementation Details
- Generated files (get_*.py) excluded from code quality checks
- All API responses validated with Pydantic models
- OAuth2 authentication via `access_token.py`
- Comprehensive test coverage: 229+ tests (unit, integration, docs, sanity)
- GraphQL queries embedded as strings in client methods
- Centralized fixtures and test data management
- Documentation examples validated with automated testing

## Current Phase 2 Development
- ✅ **PR 1**: Character Rankings (COMPLETED - merged)
- ✅ **PR 2**: Report Analysis (COMPLETED - events, graphs, tables, rankings, player details)
- ✅ **PR 3**: Integration Test Suite (COMPLETED - 85 comprehensive tests)
- ✅ **PR 4**: Advanced Report Search (COMPLETED - search, filtering, pagination)
- ✅ **Documentation Infrastructure**: Comprehensive docs with automated testing (23 tests)
- 🚧 **PR 5**: Client Architecture Refactor (NEXT PRIORITY)
- 📝 **API Reference Documentation**: Method docs with examples (planned)

## Environment Variables
```bash
# Use working credentials from this file for testing:
export ESOLOGS_ID="9f59cb5f-fabd-47e6-9529-f9797d5b38b2"
export ESOLOGS_SECRET="6hpMm9nbbfPKqF589dg8l16kxNV8jzFlERDXQIhl"
```

## Development Workflow
1. Branch from `v2-dev`
2. Implement with comprehensive tests
3. Update documentation and add examples
4. Validate documentation with `pytest tests/docs/`
5. PR to `v2-dev` for review
6. Merge after approval

### Documentation Updates
- All code examples must be complete and runnable
- New documentation must include pytest tests
- Follow naming convention: `test_[doc-name]_examples.py`
- Examples must pass automated validation

## Documentation Structure
- **Getting Started**: Installation, authentication, quickstart (complete)
- **API Reference**: Method docs with integrated examples (planned)
- **Development**: Setup, testing, contributing, architecture (planned)
- **Documentation Testing**: All code examples validated with pytest

### Documentation Commands
```bash
mkdocs serve                 # Local documentation server
mkdocs build --clean         # Build static documentation
pytest tests/docs/ -v        # Validate all documentation examples
```
