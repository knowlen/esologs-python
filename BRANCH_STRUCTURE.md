# Branch Structure Documentation

This document outlines the branch structure and purpose for the esologs-python repository.

## 🎯 Branch Comparison

| Branch | API Version | Status | Authentication | Features | Use Case |
|--------|-------------|--------|----------------|----------|----------|
| `v2-dev` | v2 GraphQL | ✅ Active | OAuth2 | Full modern stack | **Use this** |
| `main` | v2 GraphQL | ⚠️ Syncing | OAuth2 | Production ready | **Stable** |
| `v1-api` | v1 REST | 🔒 Archived | API Key | Legacy scripts | **Archive only** |

## 🚀 Getting Started

### For New Development
```bash
git clone https://github.com/knowlen/esologs-python.git
cd esologs-python
git checkout v2-dev
pip install -e ".[dev]"
```

### For Historical Research
```bash
git checkout v1-api
# See V1_API_ARCHIVE.md for details
```

## 🌟 Active Development Branches

### `v2-dev` (Primary Development Branch)
- **Purpose**: Main development branch for v2 API implementation
- **Status**: ✅ Active development
- **Features**: 
  - Modern ESO Logs v2 GraphQL API implementation
  - OAuth2 authentication
  - pyproject.toml packaging
  - Unit testing framework
  - Code quality tools (black, isort, ruff, mypy)
  - Pre-commit hooks
- **Use**: All new development should happen here

### `v2/documentation-updates`
- **Purpose**: Current custodial documentation updates
- **Status**: ✅ Active development
- **Features**: Updating documentation to reflect merged PR status
- **Use**: Current branch for documentation maintenance

## 📜 Archive Branches

### `v1-api` (Historical Archive)
- **Purpose**: Preserves original v1 API implementation
- **Status**: 🔒 Archived (deprecated)
- **Features**:
  - Original REST API implementation
  - `scripts/pull_data.py` for v1 data extraction
  - API key authentication
  - Basic JSON responses
- **Use**: Historical reference only - **DO NOT USE FOR NEW DEVELOPMENT**
- **Documentation**: See `V1_API_ARCHIVE.md` in this branch

### `main` 
- **Purpose**: Current default branch (LTS / release) 
- **Status**: Recently updated with v2/report-analysis-api merge

### `v2/security-foundation-fixes`
- **Purpose**: Phase 1 implementation with security fixes
- **Status**: ✅ Complete (merged into v2-dev)
- **Features**: Security fixes, foundation improvements, testing framework
- **Use**: Archived - features merged into v2-dev

### `v2/character-rankings-api`
- **Purpose**: Character rankings API implementation (Phase 2 PR 1)
- **Status**: ✅ Complete (merged into v2-dev)
- **Features**: 
  - Character encounter rankings (`get_character_encounter_rankings()`)
  - Character zone rankings (`get_character_zone_rankings()`)
  - Full support for all ranking metrics (dps, hps, playerscore, etc.)
  - Comprehensive unit tests and integration tests
- **Use**: Archived - features merged into v2-dev

### `v2/report-analysis-api`
- **Purpose**: Report analysis API implementation (Phase 2 PR 2)
- **Status**: ✅ Complete (merged into main and v2-dev)
- **Features**: 
  - Report events analysis (`get_report_events()`)
  - Report graph data (`get_report_graph()`)
  - Report table data (`get_report_table()`)
  - Report rankings (`get_report_rankings()`)
  - Report player details (`get_report_player_details()`)
  - Comprehensive unit tests and integration tests
- **Use**: Archived - features merged into main and v2-dev

### `v2/codegen` 
- **Purpose**: Base v2 GraphQL code generation setup
- **Status**: ✅ Complete (merged into v2-dev)
- **Features**: Basic GraphQL client with ariadne-codegen
- **Use**: Archived - features merged into v2-dev 

## 🔄 Future Plan

### Phase 1: Branch Reorganization (Completed ✅)
1. ✅ Create `v1-api` branch to preserve deprecated code
2. ✅ Establish `v2-dev` as primary development branch
3. ✅ Merge all Phase 1 improvements into v2-dev

### Phase 2: Main Branch Migration (Planned)
1. 🚧 Complete Phase 2 development in v2-dev
2. 🚧 Replace main branch content with v2-dev
3. 🚧 Update default branch to point to modernized main
4. 🚧 Archive old v2/* branches

## 📋 Branch Usage Guidelines

### For Contributors
- **Start new work**: Always branch from `v2-dev`
- **Create PRs**: Target `v2-dev` branch
- **Naming**: Use descriptive branch names like `feature/character-rankings` or `fix/authentication-bug`

### For Users
- **Current development**: Use `v2-dev` branch
- **Stable code**: Wait for main branch migration (coming soon)
- **Historical reference**: `v1-api` branch (deprecated, do not use)


---

**Last Updated**: July 9, 2025  
**Documentation**: This file is maintained in the `v2-dev` branch
