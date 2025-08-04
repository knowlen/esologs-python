# Changelog

All notable changes to ESO Logs Python will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0b1] - 2025-08-03

**First Beta Release!** This marks the transition from alpha to beta status with 100% API coverage.

### Added

- **100% API Coverage Achieved!** All 42/42 ESO Logs API methods now implemented
- **User Data Endpoints**: Implemented OAuth2 user authentication and 3 UserData methods:
  - `get_user_by_id(user_id)` - Get specific user information
  - `get_current_user()` - Get authenticated user (requires /api/v2/user endpoint)
  - `get_user_data()` - Get userData root object
- **OAuth2 Authentication Module** (`user_auth.py`):
  - Full Authorization Code flow implementation
  - Both synchronous and asynchronous support (`OAuth2Flow` and `AsyncOAuth2Flow`)
  - Token management with expiration checking
  - Helper functions for auth URL generation and token exchange
  - Support for token persistence and refresh
  - Security enhancements (CSRF protection, redirect URI validation)
- **Progress Race Tracking**: Implemented `get_progress_race()` method for world/realm first achievement race tracking
  - Supports filtering by guild, zone, competition, difficulty, size, and server
  - Returns flexible JSON data that adapts to active race formats
- **Documentation Improvements**:
  - Added comprehensive troubleshooting guide
  - Added OAuth2 examples (sync, async, Flask, FastAPI)
  - Reorganized docs structure (Getting Started and Development sections)
- **Testing**: Total test count increased from 322 to 428 tests
  - Added 10 unit tests for OAuth2 functionality
  - Added 8 integration tests for UserData methods
  - Added 8 integration tests for progress race functionality

### Changed

- **Major Client Refactoring**: Reduced `client.py` from 1,610 lines to 86 lines (95% reduction)
  - Implemented factory pattern with mixins for better code organization
  - Created modular architecture with clear separation of concerns
  - Method factory functions for dynamic method generation
  - Parameter builders for complex parameter handling
  - Mixins organizing methods by functional area
  - Centralized GraphQL queries storage
- **Dual Authentication Support**: Client now supports both client credentials and user tokens
- Updated Client to detect and warn about endpoint/authentication mismatches
- Enhanced authentication documentation with OAuth2 examples
- Moved all auto-generated code to `_generated/` subdirectory for cleaner structure
- Improved error messages to show available parameters when missing
- Added comprehensive documentation for method registration and naming conventions
- Cached regex patterns for performance improvement

### Fixed

- Type annotations now satisfy mypy without `# type: ignore` comments
- Parameter validation errors now provide more helpful context
- Fixed kwargs passthrough issue in report methods preventing HTTP client errors
- Fixed markdown formatting issues in authentication documentation

## [0.2.0a2] - 2025-07-16

### Fixed

- **CRITICAL**: Moved authentication module (`access_token.py`) into the package as `esologs.auth` so it's included in pip distributions
- Updated all imports to use `from esologs.auth import get_access_token` or `from esologs import get_access_token`
- Authentication is now properly packaged and accessible when installing from PyPI

## [0.2.0a1] - 2025-07-15

This is the first alpha release of version 0.2.0, featuring major architectural improvements and new API methods.

### Added

#### Character Rankings & Performance
- **Character Encounter Rankings**: Advanced encounter rankings with comprehensive filtering
  - Support for metric types (DPS, HPS, tank performance)
  - Role-based filtering (DPS, Healer, Tank)
  - Difficulty and encounter-specific rankings
  - Historical performance tracking
- **Zone-wide Rankings**: Character leaderboards across entire zones
  - Cross-encounter performance comparison
  - Server and faction-based rankings
  - Player score and achievement metrics

#### Advanced Report Analysis
- **Event-by-event Analysis**: Detailed combat log parsing
  - Full event filtering with ability, actor, and target filters
  - Time-based event windowing and analysis
  - Comprehensive damage, healing, and buff tracking
- **Performance Graphs**: Time-series data visualization
  - Multiple graph types (damage, healing, resources)
  - Customizable time intervals and metrics
  - Player-specific performance tracking
- **Tabular Data Analysis**: Structured report data
  - Sortable and filterable data tables
  - Multiple table types (damage, healing, buffs, deaths)
  - Player detail breakdowns and comparisons
- **Report Rankings**: Comprehensive ranking system
  - Multiple ranking metrics and categories
  - Player performance comparisons
  - Encounter-specific leaderboards

#### Advanced Report Search
- **Flexible Search API**: Multi-criteria report filtering
  - Guild, user, and zone-based searches
  - Time range filtering with validation
  - Comprehensive parameter validation
- **Convenience Methods**: Simplified search interfaces
  - `get_guild_reports()` for guild-specific searches
  - `get_user_reports()` for user activity tracking
  - `search_reports()` for complex filtering scenarios
- **Pagination & Performance**: Efficient data handling
  - Built-in pagination support
  - Parameter validation and security features
  - Optimized query performance

### Enhanced

#### Code Quality & Testing
- **Comprehensive Test Suite**: 428 tests with extensive coverage
  - 164 unit tests covering core functionality
  - 129 integration tests with real API validation
  - 117 documentation tests validating all examples
  - 18 sanity tests for quick verification
  - Test fixtures and shared utilities
- **GitHub Actions Optimization**: 75% reduction in CI minutes
  - Parallel test execution
  - Smart dependency caching
  - Optimized workflow triggers
- **Code Quality Tools**: Enhanced development experience
  - Pre-commit hooks with comprehensive linting
  - Type safety with full mypy coverage
  - Automated code formatting and import sorting

#### Security & Validation
- **Parameter Validation**: Comprehensive input validation
  - UNSET type handling for GraphQL responses
  - Timestamp and pagination validation
  - Security-focused parameter checking
- **Error Handling**: Robust error management
  - Detailed error messages and context
  - Proper exception hierarchy
  - Authentication and rate limit handling

#### Documentation
- **Complete Documentation Website**: Full mkdocs-based documentation
  - Comprehensive API reference with 7 complete sections and examples
  - Step-by-step installation, authentication, and quickstart guides
  - 98 automated documentation tests validating all code examples
  - Best practices and usage patterns
- **Testing Documentation**: Comprehensive testing infrastructure
  - 4 complete test suites with detailed README guides
  - Automated CI/CD integration with GitHub Actions
  - Test environment setup and contribution guidelines

### Technical Improvements

#### Architecture
- **GraphQL Code Generation**: Updated ariadne-codegen integration
  - Improved type safety and validation
  - Better error handling for generated code
  - Enhanced performance and reliability
- **Async/Await Patterns**: Optimized async operations
  - Proper context manager usage
  - Resource cleanup and connection management
  - Performance optimization for concurrent requests

#### Dependencies
- **Updated Core Dependencies**: Latest versions for security and performance
  - `httpx>=0.24.0` for enhanced async HTTP support
  - `pydantic>=2.0.0` for improved data validation
  - `pytest>=6.0.0` with async testing support

### API Coverage Progress

**Completed (65% → 83% API Coverage - 6/8 API sections, 33 methods)**:
- **Game Data APIs**: 13 methods - abilities, classes, items, NPCs, maps, factions (COMPLETE)
- **Character APIs**: 5 methods - profiles, reports, rankings (COMPLETE)
- **Report APIs**: 9 methods - analysis, search, events, graphs, tables (COMPLETE)
- **Guild APIs**: 2 methods - basic guild information and reports (PARTIAL)
- **World APIs**: 4 methods - regions, zones, encounters (COMPLETE)
- **System APIs**: 1 method - rate limiting and authentication (COMPLETE)

**Missing (17% - 2/8 API sections)**:
- **User Account APIs**: 0/3 methods - requires user OAuth2 authentication
- **Progress Race Data**: 0/1 method - niche racing feature
- **Enhanced Guild Features**: 4 methods - advanced guild management
- **Data Integration**: Pandas DataFrame support (planned enhancement)

### Breaking Changes

**Note**: This release maintains backward compatibility. The upcoming v0.3.0 (PR #5) will include architectural refactoring with breaking changes.

### Known Issues

- GraphQL UNSET type requires special handling in validators
- Some GitHub Actions may show "Expected -- Waiting" status without synchronize trigger
- Pre-commit hooks require virtual environment for consistent behavior

### Migration Guide

No migration required for this release. All existing code continues to work with enhanced functionality.

---

## [0.1.0] - 2023-XX-XX

### Added
- Initial release with basic API coverage
- OAuth2 authentication support
- Core game data queries
- Basic character and guild information
- Rate limiting and error handling
- GraphQL code generation with ariadne-codegen

### Technical Details
- Python 3.8+ support
- Async/await API design
- Type safety with Pydantic models
- Comprehensive test coverage

---

## Development Releases

### Phase 2 Development (Current)
- **PR #1**: Character Rankings Implementation (Merged)
- **PR #2**: Report Analysis Implementation (Merged)
- **PR #3**: Integration Test Suite (Merged)
- **PR #4**: Advanced Report Search (Merged)
- **PR #5**: Client Architecture Refactor (Next - Breaking Changes)

### Upcoming Phases
- **Phase 3**: Data transformation and pandas integration
- **Phase 4**: Performance optimization and caching
- **Phase 5**: Enhanced documentation and examples

---

## Links

- **GitHub Repository**: [https://github.com/knowlen/esologs-python](https://github.com/knowlen/esologs-python)
- **Documentation**: [https://esologs-python.readthedocs.io/](https://esologs-python.readthedocs.io/)
- **ESO Logs API**: [https://www.esologs.com/v2-api-docs/eso/](https://www.esologs.com/v2-api-docs/eso/)

---

*This changelog is automatically updated with each release. For the most current development status, see the [project repository](https://github.com/knowlen/esologs-python).*
