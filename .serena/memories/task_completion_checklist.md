# ESO Logs Python - Task Completion Checklist

## When You Complete a Task

### 1. Code Quality Checks
```bash
# Run all pre-commit checks
pre-commit run --all-files

# If any fail, fix and re-run until all pass
```

### 2. Run Tests
```bash
# Run unit tests (always)
pytest tests/unit/ -v

# Run integration tests if API-related
pytest tests/integration/ -v

# Run full test suite for major changes
pytest tests/ -v
```

### 3. Type Checking
```bash
# Ensure no type errors
mypy .
```

### 4. Update Documentation
- Update docstrings for new/modified functions
- Update README.md if adding new features
- Update API documentation if changing public API
- Add/update code examples

### 5. Check for Common Issues
- [ ] No print statements in code
- [ ] No hardcoded credentials
- [ ] All imports are absolute (not relative)
- [ ] New files have proper headers
- [ ] Tests added for new functionality
- [ ] Edge cases handled

### 6. Git Workflow
```bash
# Stage changes
git add .

# Check what's being committed
git status
git diff --cached

# Commit with descriptive message
git commit -m "type: description"

# Push to feature branch
git push origin feature/branch-name
```

### 7. PR Checklist
- [ ] All tests pass
- [ ] Code follows style conventions
- [ ] Documentation updated
- [ ] No merge conflicts with target branch
- [ ] PR description explains changes
- [ ] Linked to relevant issues

## Commit Message Format
```
type: subject

body (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

## Important Notes
- **Never push directly to main or dev branches**
- **Always create feature branches**
- **Get PR reviewed before merging**
- **Keep commits focused and atomic**
- **Run tests before committing**
