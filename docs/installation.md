# Installation

Get ESO Logs Python up and running in your environment.

## Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: Automatically installed with the package

## Installation Methods

### PyPI Installation (Recommended)

ESO Logs Python is available on PyPI:

=== "Latest Alpha"

    ```bash
    # Install the latest alpha release
    pip install esologs-python
    ```

=== "Any Version"

    ```bash
    # Install any available version (including pre-releases)
    pip install esologs-python
    ```

### Development Installation

=== "Basic Installation"

    ```bash
    # Clone the repository
    git clone https://github.com/knowlen/esologs-python.git
    cd esologs-python

    # Install the package
    pip install --upgrade pip
    pip install -e .
    ```

=== "Development with Tools"

    For contributing or development work, install with development dependencies:

    ```bash
    # Clone the repository
    git clone https://github.com/knowlen/esologs-python.git
    cd esologs-python

    # Install with development tools
    pip install --upgrade pip
    pip install -e ".[dev]"

    # Set up pre-commit hooks
    pre-commit install
    ```

=== "Virtual Environment"

    **Recommended**: Use a virtual environment to avoid dependency conflicts:

    ```bash
    # Create virtual environment
    python -m venv esologs-env

    # Activate virtual environment
    # On Windows:
    esologs-env\Scripts\activate
    # On macOS/Linux:
    source esologs-env/bin/activate

    # Clone and install
    git clone https://github.com/knowlen/esologs-python.git
    cd esologs-python
    pip install -e .
    ```

## Verification

Verify your installation by running a simple test:

```python
# test_installation.py
import esologs
from esologs.auth import get_access_token

# Check version
print(f"ESO Logs Python version: {esologs.__version__}")

# Test authentication (requires API credentials)
try:
    token = get_access_token()
    print("✅ Authentication successful")
except Exception as e:
    print(f"❌ Authentication failed: {e}")
    print("Make sure to set ESOLOGS_ID and ESOLOGS_SECRET environment variables")
```

## Core Dependencies

ESO Logs Python automatically installs these core dependencies:

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | ≥2.25.0 | HTTP client for authentication |
| `httpx` | ≥0.24.0 | Async HTTP client for API calls |
| `pydantic` | ≥2.0.0 | Data validation and serialization |
| `ariadne-codegen` | ≥0.6.0 | GraphQL code generation |

## Development Dependencies

When installing with `[dev]`, these additional tools are included:

| Package | Purpose |
|---------|---------|
| `pytest` | Testing framework |
| `pytest-asyncio` | Async test support |
| `pytest-cov` | Coverage reporting |
| `black` | Code formatting |
| `isort` | Import sorting |
| `ruff` | Fast Python linting |
| `mypy` | Static type checking |
| `pre-commit` | Git hooks for code quality |

## Troubleshooting

### Common Issues

#### Python Version Error

```
ERROR: This package requires Python >=3.8
```

**Solution**: Upgrade to Python 3.8 or higher:

```bash
# Check your Python version
python --version

# Install Python 3.8+ from python.org or use pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

#### Permission Errors

```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Solution**: Use a virtual environment or `--user` flag:

```bash
# Option 1: Virtual environment (recommended)
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
pip install -e .

# Option 2: User installation
pip install --user -e .
```

#### Git Not Found

```
ERROR: Git is not installed
```

**Solution**: Install Git:

- **Windows**: Download from [git-scm.com](https://git-scm.com/)
- **macOS**: `brew install git` or Xcode Command Line Tools
- **Ubuntu/Debian**: `sudo apt-get install git`
- **CentOS/RHEL**: `sudo yum install git`

#### Network Issues

```
ERROR: Could not fetch URL
```

**Solution**: Check network connectivity and proxy settings:

```bash
# Test connectivity
ping github.com

# Configure pip proxy if needed
pip install --proxy http://user:password@proxy.server:port -e .
```

### Development Setup Issues

#### Pre-commit Hook Failures

```bash
# Reset and reinstall hooks
pre-commit uninstall
pre-commit install
pre-commit run --all-files
```

#### Import Errors in Development

```bash
# Reinstall in editable mode
pip uninstall esologs-python
pip install -e .
```

## Next Steps

Once installation is complete:

1. **[Set up authentication](authentication.md)** - Configure your ESO Logs API credentials
2. **[Follow the quickstart guide](quickstart.md)** - Make your first API calls
3. **[Explore the API reference](api-reference/game-data.md)** - Learn methods and usage patterns

!!! tip "Development Environment"
    If you plan to contribute to the project, see our [development setup guide](development/setup.md)
    for additional configuration and testing instructions.

!!! question "Need Help?"
    If you encounter issues not covered here, please:

    - Search [existing issues](https://github.com/knowlen/esologs-python/issues)
    - Create a [new issue](https://github.com/knowlen/esologs-python/issues/new) with your system details
