# ESO Logs Python Project Overview

## Purpose
esologs-python is a comprehensive Python client library for the ESO Logs API v2, designed for Elder Scrolls Online (ESO) players and developers. It provides both synchronous and asynchronous interfaces to access ESO Logs data for analyzing combat logs, tracking performance metrics, and building tools for the ESO community.

## Current Status
- **Version**: 0.2.0b1 (Beta)
- **API Coverage**: 100% (42/42 methods implemented)
- **Package Name**: esologs-python (on PyPI)
- **Documentation**: https://esologs-python.readthedocs.io/
- **Repository**: https://github.com/knowlen/esologs-python

## Tech Stack
- **Language**: Python 3.8+
- **Core Dependencies**:
  - requests (HTTP client)
  - httpx (async HTTP client)
  - pydantic (data validation)
  - ariadne-codegen (GraphQL code generation)
  - aiofiles (async file operations)
- **Development Tools**:
  - pytest (testing framework)
  - black (code formatter)
  - isort (import sorter)
  - ruff (linter)
  - mypy (type checker)
  - pre-commit (git hooks)
  - mkdocs (documentation)

## Architecture
- **Modular Client Design**: Uses Factory Method and Mixin patterns
- **Main client reduced from 1,610 to 86 lines** through refactoring
- **Code Organization**:
  - `esologs/client.py` - Main client (86 lines)
  - `esologs/mixins/` - API method mixins (7 files)
  - `esologs/method_factory.py` - Dynamic method generation
  - `esologs/_generated/` - Auto-generated GraphQL code
  - `esologs/validators.py` - Input validation
  - `esologs/param_builders.py` - Parameter processing
  - `esologs/queries.py` - GraphQL queries

## API Features
1. **Game Data** - 13 methods (abilities, classes, items, NPCs, maps, factions)
2. **Character Data** - 5 methods (info, reports, rankings)
3. **Report Data** - 10 methods (events, tables, rankings, search)
4. **World Data** - 4 methods (regions, zones, encounters, expansions)
5. **Guild Data** - 5 methods (info, reports, attendance, members)
6. **Rate Limit** - 1 method
7. **Progress Race** - 1 method (world/realm first tracking)
8. **User Data** - 3 methods (OAuth2 authenticated endpoints)

## Testing Strategy
- **428 total tests** across 4 suites:
  - Unit Tests (164) - Logic validation, no API required
  - Integration Tests (129) - Live API testing
  - Documentation Tests (117) - Code example validation
  - Sanity Tests (18) - API health check
