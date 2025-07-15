# Branch Structure Documentation

This document outlines the branch structure and purpose for the esologs-python repository.

## 🎯 Branch Comparison

| Branch | API Version | Status | Authentication | Features | Use Case |
|--------|-------------|--------|----------------|----------|----------|
| `v2/update-main-before-refactor` | v2 GraphQL | ✅ Active | OAuth2 | Full API docs + comprehensive testing | **Use this** |
| `v2-dev` | v2 GraphQL | 📦 Archived | OAuth2 | Previous dev branch | **Historical** |
| `main` | v2 GraphQL | ⚠️ Syncing | OAuth2 | Production ready | **Stable** |
| `v1-api` | v1 REST | 🔒 Archived | API Key | Legacy scripts | **Archive only** |

## 🚀 Getting Started

### For New Development
```bash
git clone https://github.com/knowlen/esologs-python.git
cd esologs-python
git checkout v2/update-main-before-refactor
pip install -e ".[dev]"
```

### For Historical Research
```bash
git checkout v1-api
# See V1_API_ARCHIVE.md for details
```

## 🌟 Active Development Branches

### `v2/update-main-before-refactor` (Primary Development Branch)
- **Purpose**: Current active development branch with complete API documentation
- **Status**: ✅ Active development
- **Features**:
  - Modern ESO Logs v2 GraphQL API implementation (~75% coverage)
  - Complete API reference documentation for all endpoints
  - Comprehensive test suite (203+ tests across unit/integration/docs/sanity)
  - OAuth2 authentication
  - pyproject.toml packaging
  - Code quality tools (black, isort, ruff, mypy)
  - Pre-commit hooks
- **Use**: All new development should happen here

### `v2-dev` (Previous Development Branch)
- **Purpose**: Previous main development branch
- **Status**: 📦 Archived - superseded by v2/update-main-before-refactor
- **Use**: Historical reference only

## 📜 Archive Branches

### `main`
- **Purpose**: Current default branch (LTS / release)
- **Status**: ⚠️ Syncing with v2-dev
- **Features**: Production ready v2 GraphQL API with OAuth2
- **Use**: Stable release branch

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

## 📋 Branch Usage Guidelines

### For Contributors
- **Start new work**: Always branch from `v2/update-main-before-refactor`
- **Create PRs**: Target `v2/update-main-before-refactor` branch
- **Naming**: Use descriptive branch names like `feature/character-rankings` or `fix/authentication-bug`

### For Users
- **Current development**: Use `v2/update-main-before-refactor` branch
- **Stable code**: Wait for main branch migration (coming soon)
- **Historical reference**: `v1-api` branch (deprecated, do not use)


---

**Last Updated**: July 13, 2025
**Documentation**: This file is maintained in the `v2/update-main-before-refactor` branch
