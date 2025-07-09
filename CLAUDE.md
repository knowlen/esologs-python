# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview
Python client library for ESO Logs API v2. GraphQL-based interface using `ariadne-codegen`. 
- **Status**: v0.2.0-alpha, ~35% API coverage (Report Analysis recently added)
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
python test.py               # Integration tests (requires API credentials)
pytest tests/unit/           # Unit tests
```

### Code Quality
```bash
pre-commit run --all-files   # All checks
black . && isort . && ruff check --fix . && mypy .
```

## API Coverage & Architecture
**Current (~35%)**:
- **Game Data**: abilities, classes, factions, items, maps, NPCs
- **Character Data**: profiles, reports, rankings
- **World Data**: regions, zones, encounters
- **Guild Data**: basic info
- **Report Data**: individual reports, **analysis (NEW)**
- **System**: rate limiting

**Recently Added**: Report Analysis API with comprehensive event, graph, table, ranking, and player detail analysis

**Missing (~65%)**: Advanced search, user accounts, progress tracking, report collections

## Configuration Files
- **`pyproject.toml`**: Dependencies, dev tools, code quality config
- **`mini.toml`**: ariadne-codegen configuration  
- **`schema.graphql`**: GraphQL schema
- **`queries.graphql`**: GraphQL queries for code generation

## Key Implementation Details
- Generated files (get_*.py) excluded from code quality checks
- All API responses validated with Pydantic models
- OAuth2 authentication via `access_token.py`
- Comprehensive test coverage for new features
- GraphQL queries embedded as strings in client methods

## Current Phase 2 Development
- ✅ **PR 1**: Character Rankings (COMPLETED - merged)
- ✅ **PR 2**: Report Analysis (COMPLETED - events, graphs, tables, rankings, player details)
- 🚧 **PR 3**: Advanced Report Search (PLANNED)
- 🚧 **PR 4**: Client Architecture Refactor (PLANNED)

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