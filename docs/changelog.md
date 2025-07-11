# Changelog

All notable changes to ESO Logs Python will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-01-XX (Upcoming Release)

### Added

#### 🏆 Character Rankings & Performance
- **Character Encounter Rankings**: Advanced encounter rankings with comprehensive filtering
  - Support for metric types (DPS, HPS, tank performance)
  - Role-based filtering (DPS, Healer, Tank)
  - Difficulty and encounter-specific rankings
  - Historical performance tracking
- **Zone-wide Rankings**: Character leaderboards across entire zones
  - Cross-encounter performance comparison
  - Server and faction-based rankings
  - Player score and achievement metrics

#### 📊 Advanced Report Analysis
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

#### 🔍 Advanced Report Search
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

#### 🔧 Code Quality & Testing
- **Comprehensive Test Suite**: 180+ tests with extensive coverage
  - 76 unit tests covering core functionality
  - 85 integration tests with real API validation
  - 19 sanity tests for quick verification
  - Test fixtures and shared utilities
- **GitHub Actions Optimization**: 75% reduction in CI minutes
  - Parallel test execution
  - Smart dependency caching
  - Optimized workflow triggers
- **Code Quality Tools**: Enhanced development experience
  - Pre-commit hooks with comprehensive linting
  - Type safety with full mypy coverage
  - Automated code formatting and import sorting

#### 🛡️ Security & Validation
- **Parameter Validation**: Comprehensive input validation
  - UNSET type handling for GraphQL responses
  - Timestamp and pagination validation
  - Security-focused parameter checking
- **Error Handling**: Robust error management
  - Detailed error messages and context
  - Proper exception hierarchy
  - Authentication and rate limit handling

#### 📚 Documentation
- **Comprehensive Guides**: Complete usage documentation
  - API reference with examples
  - Step-by-step tutorials
  - Best practices and patterns
- **Testing Documentation**: Detailed testing guides
  - Unit and integration test examples
  - Test environment setup
  - CI/CD integration instructions

### Technical Improvements

#### 🏗️ Architecture
- **GraphQL Code Generation**: Updated ariadne-codegen integration
  - Improved type safety and validation
  - Better error handling for generated code
  - Enhanced performance and reliability
- **Async/Await Patterns**: Optimized async operations
  - Proper context manager usage
  - Resource cleanup and connection management
  - Performance optimization for concurrent requests

#### 🔧 Dependencies
- **Updated Core Dependencies**: Latest versions for security and performance
  - `httpx>=0.24.0` for enhanced async HTTP support
  - `pydantic>=2.0.0` for improved data validation
  - `pytest>=6.0.0` with async testing support

### API Coverage Progress

**Completed (65% → 65% API Coverage)**:
- ✅ **Game Data APIs**: Abilities, classes, items, NPCs, maps, factions
- ✅ **Character APIs**: Profiles, reports, rankings (enhanced)
- ✅ **Report APIs**: Analysis, search, events, graphs, tables (new)
- ✅ **Guild APIs**: Basic guild information and reports
- ✅ **World APIs**: Regions, zones, encounters
- ✅ **System APIs**: Rate limiting and authentication

**In Progress (Target: 95% by v1.0)**:
- 🚧 **User Account APIs**: Account management and preferences
- 🚧 **Progress Tracking**: Race and achievement tracking
- 🚧 **Enhanced Guild Features**: Advanced guild management
- 🚧 **Data Integration**: Pandas DataFrame support

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
- ✅ **PR #1**: Character Rankings Implementation (Merged)
- ✅ **PR #2**: Report Analysis Implementation (Merged)  
- ✅ **PR #3**: Integration Test Suite (Merged)
- ✅ **PR #4**: Advanced Report Search (Merged)
- 🚧 **PR #5**: Client Architecture Refactor (Next - Breaking Changes)

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