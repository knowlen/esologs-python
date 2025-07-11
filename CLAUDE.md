# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview
Python client library for ESO Logs API v2. GraphQL-based interface using `ariadne-codegen`. 
- **Status**: v0.2.0-alpha, ~60% API coverage (Advanced Report Search recently added)
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
pytest tests/unit/           # Unit tests
pytest tests/integration/    # Comprehensive integration tests (requires API credentials)
```

### Code Quality
```bash
pre-commit run --all-files   # All checks
black . && isort . && ruff check --fix . && mypy .
```

## API Coverage & Architecture
**Current (~60%)**:
- **Game Data**: abilities, classes, factions, items, maps, NPCs
- **Character Data**: profiles, reports, rankings
- **World Data**: regions, zones, encounters
- **Guild Data**: basic info
- **Report Data**: individual reports, analysis, **search (NEW)**
- **System**: rate limiting

**Recently Added**: Advanced Report Search API with flexible filtering, pagination, and convenience methods

**Missing (~40%)**: User accounts, progress tracking, enhanced guild features

## Configuration Files
- **`pyproject.toml`**: Dependencies, dev tools, code quality config
- **`mini.toml`**: ariadne-codegen configuration  
- **`schema.graphql`**: GraphQL schema
- **`queries.graphql`**: GraphQL queries for code generation

## Key Implementation Details
- Generated files (get_*.py) excluded from code quality checks
- All API responses validated with Pydantic models
- OAuth2 authentication via `access_token.py`
- Comprehensive test coverage: 70+ integration tests + unit tests
- GraphQL queries embedded as strings in client methods
- Centralized fixtures and test data management

## Current Phase 2 Development
- ✅ **PR 1**: Character Rankings (COMPLETED - merged)
- ✅ **PR 2**: Report Analysis (COMPLETED - events, graphs, tables, rankings, player details)
- ✅ **PR 3**: Integration Test Suite (COMPLETED - 70+ comprehensive tests)
- ✅ **PR 4**: Advanced Report Search (COMPLETED - search, filtering, pagination)
- 🚧 **PR 5**: Client Architecture Refactor (NEXT PRIORITY)

## Environment Variables
```bash
export ESOLOGS_ID="your_client_id"
export ESOLOGS_SECRET="your_client_secret"
```

## Development Workflow
1. Branch from `v2-dev` 
2. Implement with comprehensive tests
3. Update documentation
4. PR to `v2-dev` for review
5. Merge after approval