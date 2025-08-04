# ESO Logs Python - Code Style and Conventions

## Python Version
- Target: Python 3.8+
- Use modern Python features but maintain 3.8 compatibility

## Code Formatting
- **Black**: Line length 88 characters
- **isort**: Black-compatible profile
- **Indentation**: 4 spaces (no tabs)
- **No trailing whitespace**
- **Files end with newline**

## Import Style
- **Absolute imports only** (no relative imports)
- **Import order** (via isort):
  1. Standard library
  2. Third-party packages
  3. Local application imports
- **Example**:
  ```python
  import asyncio
  from typing import Dict, List, Optional

  import httpx
  from pydantic import BaseModel

  from esologs.client import Client
  from esologs.validators import validate_parameters
  ```

## Type Hints
- **Required for all functions and methods**
- **Use typing module for complex types**
- **Pydantic models for data validation**
- **mypy strict mode compliance**
- **Example**:
  ```python
  async def get_report_events(
      self,
      code: str,
      start_time: Optional[float] = None,
      end_time: Optional[float] = None,
  ) -> ReportEventsResponse:
      """Get events from a report."""
  ```

## Docstrings
- **Google-style docstrings**
- **Required for all public functions/classes**
- **Include parameters, returns, and examples**
- **Example**:
  ```python
  def validate_bearer_token_format(token: str) -> str:
      """Validate and format a bearer token.

      Args:
          token: The token to validate (with or without 'Bearer' prefix)

      Returns:
          The formatted token with 'Bearer' prefix

      Raises:
          ValueError: If token format is invalid
      """
  ```

## Naming Conventions
- **Classes**: PascalCase (e.g., `ReportEventsResponse`)
- **Functions/Methods**: snake_case (e.g., `get_report_events`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `BEARER_TOKEN_PATTERN`)
- **Private methods**: Leading underscore (e.g., `_validate_input`)

## Error Handling
- **Use specific exceptions** (not bare except)
- **Provide helpful error messages**
- **Handle API errors gracefully**
- **Example**:
  ```python
  if not token:
      raise ValueError("Token cannot be empty")
  ```

## Testing
- **Test file naming**: `test_*.py`
- **Test function naming**: `test_descriptive_name()`
- **Use pytest fixtures for common setup**
- **Include edge cases and error scenarios**

## Architecture Patterns
- **Factory Method Pattern**: For dynamic method generation
- **Mixin Pattern**: For organizing API methods by category
- **Protocol Types**: For type safety with dynamic methods

## Generated Code
- **Location**: `esologs/_generated/`
- **Do not edit manually** - use ariadne-codegen
- **Excluded from formatting/linting tools**

## Security
- **Never commit credentials**
- **Use environment variables for secrets**
- **Validate all user input**
- **No print statements in production code**

## Performance
- **Use async/await for I/O operations**
- **Implement streaming for large datasets**
- **Cache static data when appropriate**

## Documentation
- **Update docs with every feature**
- **Include code examples**
- **Keep README current**
- **Use MkDocs for documentation site**
