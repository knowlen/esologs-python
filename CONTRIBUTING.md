# Contributing to ESO Logs Python

Thank you for your interest in contributing to the ESO Logs Python library!

## Branch Naming and PR Guidelines

### Branch Protection and Workflow

This repository follows a strict branching strategy to ensure code quality and proper release management:

1. **`main` branch**: Production-ready code only
   - Protected branch with strict rules
   - Only accepts PRs from branches with `release` prefix
   - Requires all status checks to pass
   - Direct pushes are disabled

2. **`dev` branch**: Active development
   - All feature branches should target this branch
   - Integration testing happens here
   - Default target for new PRs

### Targeting Main Branch

**ONLY** branches with `release` prefix can create PRs to `main`:
- ✅ `release/v0.3.0`
- ✅ `release/hotfix-auth`
- ❌ `feature/new-api`
- ❌ `fix/bug-123`

### Development Workflow

1. **Feature Development**
   ```bash
   git checkout dev
   git checkout -b feature/your-feature-name
   # Make changes
   git push origin feature/your-feature-name
   # Create PR to dev branch
   ```

2. **Bug Fixes**
   ```bash
   git checkout dev
   git checkout -b fix/issue-description
   # Make changes
   git push origin fix/issue-description
   # Create PR to dev branch
   ```

3. **Releases**
   ```bash
   git checkout dev
   git checkout -b release/v0.3.0
   # Update version numbers, changelog, etc.
   git push origin release/v0.3.0
   # Create PR to main branch
   ```

4. **Hotfixes** (critical production fixes)
   ```bash
   git checkout main
   git checkout -b release/hotfix-description
   # Make minimal changes
   git push origin release/hotfix-description
   # Create PR to main branch
   # After merge, backport to dev
   ```

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install development dependencies: `pip install -e ".[dev]"`
5. Install pre-commit hooks: `pre-commit install`

## Code Standards

- All code must pass pre-commit hooks (black, isort, ruff, mypy)
- Tests must pass: `pytest`
- Coverage should not decrease
- Update documentation for new features

## Testing

- Write unit tests for new functionality
- Update integration tests if changing API interactions
- Run tests locally before pushing: `pytest`
- Check coverage: `pytest --cov=esologs`

## Documentation

- Update docstrings for new/modified functions
- Update `docs/` for user-facing changes
- Include examples in documentation
- Update changelog for notable changes
