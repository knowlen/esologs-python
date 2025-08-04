# ESO Logs Python - Suggested Commands

## Development Commands

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run specific test suites
pytest tests/unit/ -v              # Unit tests (no API required)
pytest tests/integration/ -v       # Integration tests (API required)
pytest tests/sanity/ -v            # Sanity tests (API required)
pytest tests/docs/ -v              # Documentation tests (API required)

# Run with coverage
pytest tests/ --cov=esologs --cov-report=html

# Run specific test markers
pytest -m "not oauth2" -v          # Skip OAuth2 tests
pytest -m "not slow" -v            # Skip slow tests
```

### Code Quality
```bash
# Run all pre-commit checks
pre-commit run --all-files

# Individual tools
black .                            # Format code
isort .                            # Sort imports
ruff check --fix .                 # Lint and fix
mypy .                             # Type checking
```

### Documentation
```bash
# Build documentation
mkdocs build --clean

# Serve documentation locally
mkdocs serve

# View at http://127.0.0.1:8000
```

### Code Generation
```bash
# Regenerate GraphQL client code
./scripts/generate_client.sh

# Run post-codegen processing
python scripts/post_codegen.py
```

### Package Management
```bash
# Install development dependencies
pip install -e ".[dev]"

# Install all optional dependencies
pip install -e ".[all]"

# Build package
python -m build

# Check package
twine check dist/*
```

## Environment Variables
```bash
# Required for API access
export ESOLOGS_ID="your_client_id"
export ESOLOGS_SECRET="your_client_secret"

# Alternative: use .env file
echo "ESOLOGS_ID=your_client_id" >> .env
echo "ESOLOGS_SECRET=your_client_secret" >> .env
```

## Git Commands
```bash
# Common workflow
git checkout dev                   # Development branch
git checkout -b feature/my-feature # Create feature branch
git add .
git commit -m "feat: add new feature"
git push -u origin feature/my-feature

# Create PR to dev branch for review
```

## Quick Checks
```bash
# API health check
python scripts/quick_api_check.py

# Validate installation
python -c "import esologs; print(esologs.__version__)"
```
