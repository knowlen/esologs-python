# Documentation Tests

Tests to verify that code examples in documentation work correctly.

## Overview

This directory contains tests that validate code examples from:
- `docs/quickstart.md` - Ensures all code blocks execute without errors
- `docs/authentication.md` - Validates authentication setup and error handling
- `docs/api-reference/` - All 7 API reference documentation files with comprehensive examples
  - `game-data.md`, `character-data.md`, `guild-data.md`, `world-data.md`
  - `report-analysis.md`, `report-search.md`, `system.md`

## Purpose

- **Prevent documentation drift**: Ensures examples stay current with API changes
- **User confidence**: Guarantees copy-paste examples work as expected
- **CI/CD integration**: Automated validation of documentation accuracy

## Test Structure

- `test_quickstart_examples.py` - Tests all code blocks from quickstart guide
- `test_authentication_examples.py` - Tests all code blocks from authentication guide
- `test_game_data_examples.py` - Tests all examples from game data API reference
- `test_character_data_examples.py` - Tests all examples from character data API reference
- `test_guild_data_examples.py` - Tests all examples from guild data API reference
- `test_world_data_examples.py` - Tests all examples from world data API reference
- `test_report_analysis_examples.py` - Tests all examples from report analysis API reference
- `test_report_search_examples.py` - Tests all examples from report search API reference
- `test_system_examples.py` - Tests all examples from system API reference
- `conftest.py` - Shared test fixtures and configuration

**Total: 98 tests** across all documentation files

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
