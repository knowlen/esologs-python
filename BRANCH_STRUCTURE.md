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
