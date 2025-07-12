# Documentation Tests

Tests to verify that code examples in documentation work correctly.

## Overview

This directory contains tests that validate code examples from:
- `docs/quickstart.md` - Ensures all code blocks execute without errors
- `docs/authentication.md` - Validates authentication setup and error handling
- Future documentation files as needed

## Purpose

- **Prevent documentation drift**: Ensures examples stay current with API changes
- **User confidence**: Guarantees copy-paste examples work as expected
- **CI/CD integration**: Automated validation of documentation accuracy

## Test Structure

- `test_quickstart_examples.py` - Tests all code blocks from quickstart guide (14 tests)
- `test_authentication_examples.py` - Tests all code blocks from authentication guide (9 tests)
- `conftest.py` - Shared test fixtures and configuration

## Running Tests

```bash
# Run documentation tests only
pytest tests/docs/

# Run with verbose output
pytest tests/docs/ -v

# Run specific test file
pytest tests/docs/test_quickstart_examples.py -v
pytest tests/docs/test_authentication_examples.py -v

# Run specific test
pytest tests/docs/test_quickstart_examples.py::test_first_api_call -v
```

## Requirements

- Valid ESO Logs API credentials in environment variables
- All project dependencies installed
- Network connectivity to ESO Logs API