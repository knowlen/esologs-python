<div align="center">
  <img src="esologs_logo.png" alt="ESO Logs Python" width="600">
</div>

# ESO Logs Python Client

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Documentation](https://readthedocs.org/projects/esologs-python/badge/?version=latest)](https://esologs-python.readthedocs.io/)
[![Development Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/knowlen/esologs-python)
[![Tests](https://github.com/knowlen/esologs-python/actions/workflows/ci.yml/badge.svg)](https://github.com/knowlen/esologs-python/actions/workflows/ci.yml)

A comprehensive Python client library for the [ESO Logs API v2](https://www.esologs.com/v2-api-docs/eso/). This library provides both synchronous and asynchronous interfaces to access Elder Scrolls Online combat logging data, with built-in support for data transformation and analysis.

## Project Status

**Current Version:** 0.2.0-alpha
**API Coverage:** ~83% (comprehensive analysis shows 6/8 API sections fully implemented)
**Development Stage:** Active development
**Documentation:** [Read the Docs](https://esologs-python.readthedocs.io/)
**Tests:** 278 tests across unit, integration, documentation, and sanity suites

### Current API Coverage
**Implemented (6/8 sections):**
1. ✅ **gameData** - 13 methods
2. ✅ **characterData** - 5 methods
3. ✅ **reportData** - 9 methods
4. ✅ **worldData** - 4 methods
5. ✅ **rateLimitData** - 1 method
6. 🟡 **guildData** - 2 methods (PARTIAL - missing 4 advanced methods)

**Missing (2/8 sections):**
- ❌ **userData** - 0/3 methods (MISSING - requires user auth)
- ❌ **progressRaceData** - 0/1 method (MISSING - niche racing feature)

### Roadmap
- 🚧 Progress race tracking
- 🚧 User account integration
- 🚧 Client architecture refactor (modular design)

## Installation

**Note**: This package is currently in development and not yet published to PyPI.

### Current Installation Method

```bash
# Clone the repository
git clone https://github.com/knowlen/esologs-python.git
cd esologs-python

# Basic installation
pip install --upgrade pip
pip install -e .
```

### Development Installation

For development with testing, linting, and pre-commit hooks:
```bash
# Development installation
pip install -e ".[dev]"
```

## API Setup

1. **Create an ESO Logs API Client**
   - Visit [ESO Logs API Clients](https://www.esologs.com/api/clients/)
   - Create a new v2 client application
   - Note your Client ID and Client Secret

2. **Set Environment Variables**
   ```bash
   export ESOLOGS_ID="your_client_id_here"
   export ESOLOGS_SECRET="your_client_secret_here"
   ```

3. **Alternative: Use .env file**
   ```bash
   # Create .env file in your project root
   echo "ESOLOGS_ID=your_client_id_here" >> .env
   echo "ESOLOGS_SECRET=your_client_secret_here" >> .env
   ```

## Quickstart

For comprehensive documentation, visit [esologs-python.readthedocs.io](https://esologs-python.readthedocs.io/)

### Basic Usage

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def main():
    # Get authentication token
    token = get_access_token()

    # Create client
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get character information
        character = await client.get_character_by_id(id=12345)
        print(f"Character: {character.character_data.character.name}")  # noqa: T201

        # Get recent reports for character
        reports = await client.get_character_reports(character_id=12345, limit=10)
        for report in reports.character_data.character.recent_reports.data:
            print(f"Report: {report.code} - {report.zone.name}")  # noqa: T201

        # Get game data
        abilities = await client.get_abilities(limit=50, page=1)
        for ability in abilities.game_data.abilities.data:
            print(f"Ability: {ability.name}")  # noqa: T201

# Run the async function
asyncio.run(main())
```

### Authentication Only

```python
from access_token import get_access_token

# Using environment variables
token = get_access_token()

# Using explicit credentials
token = get_access_token(
    client_id="your_client_id",
    client_secret="your_client_secret"
)
```

### Character Rankings (NEW)

```python
import asyncio
from esologs.client import Client
from esologs.enums import CharacterRankingMetricType, RoleType
from access_token import get_access_token

async def main():
    token = get_access_token()

    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get character encounter rankings with filtering
        encounter_rankings = await client.get_character_encounter_rankings(
            character_id=12345,
            encounter_id=27,
            metric=CharacterRankingMetricType.dps,
            role=RoleType.DPS,
            difficulty=125
        )

        # Get zone-wide character leaderboards
        zone_rankings = await client.get_character_zone_rankings(
            character_id=12345,
            zone_id=1,
            metric=CharacterRankingMetricType.playerscore
        )

        # Access ranking data
        if encounter_rankings.character_data.character.encounter_rankings:
            rankings_data = encounter_rankings.character_data.character.encounter_rankings
            print(f"Best DPS: {rankings_data.get('bestAmount', 0)}")
            print(f"Total Kills: {rankings_data.get('totalKills', 0)}")

asyncio.run(main())
```

### Advanced Report Search (NEW)

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def main():
    token = get_access_token()

    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Search reports with flexible criteria
        reports = await client.search_reports(
            guild_id=123,
            zone_id=456,
            start_time=1672531200000,  # Jan 1, 2023
            end_time=1672617600000,    # Jan 2, 2023
            limit=25,
            page=1
        )

        # Convenience methods for common searches
        guild_reports = await client.get_guild_reports(
            guild_id=123,
            limit=50
        )

        user_reports = await client.get_user_reports(
            user_id=789,
            zone_id=456,
            limit=20
        )

        # Process search results
        if reports.report_data and reports.report_data.reports:
            for report in reports.report_data.reports.data:
                print(f"Report: {report.code} - {report.zone.name}")
                print(f"Duration: {report.end_time - report.start_time}ms")

asyncio.run(main())
```

## Available API Methods

### Game Data
- `get_ability(id)` - Get specific ability information
- `get_abilities(limit, page)` - List abilities with pagination
- `get_class(id)` - Get character class information
- `get_classes(faction_id, zone_id)` - List character classes
- `get_factions()` - Get available factions
- `get_item(id)` - Get specific item information
- `get_items(limit, page)` - List items with pagination
- `get_item_set(id)` - Get item set information
- `get_item_sets(limit, page)` - List item sets with pagination
- `get_map(id)` - Get map information
- `get_maps(limit, page)` - List maps with pagination
- `get_npc(id)` - Get NPC information
- `get_npcs(limit, page)` - List NPCs with pagination

### Character Data
- `get_character_by_id(id)` - Get character profile
- `get_character_reports(character_id, limit)` - Get character's reports
- `get_character_encounter_ranking(character_id, encounter_id)` - Get character rankings (legacy)
- `get_character_encounter_rankings(character_id, encounter_id, **kwargs)` - **NEW**: Advanced encounter rankings with full filtering
- `get_character_zone_rankings(character_id, zone_id, **kwargs)` - **NEW**: Zone-wide character leaderboards

### Guild Data
- `get_guild_by_id(guild_id)` - Get guild information

### World Data
- `get_world_data()` - Get comprehensive world information
- `get_regions()` - Get available regions
- `get_zones()` - Get available zones
- `get_encounters_by_zone(zone_id)` - Get encounters in specific zone

### Report Data
- `get_report_by_code(code)` - Get specific report by code
- `get_reports(**kwargs)` - **NEW**: Advanced report search with comprehensive filtering
- `search_reports(**kwargs)` - **NEW**: Flexible report search with multiple criteria
- `get_guild_reports(guild_id, **kwargs)` - **NEW**: Convenience method for guild reports
- `get_user_reports(user_id, **kwargs)` - **NEW**: Convenience method for user reports
- `get_report_events(code, **kwargs)` - Get event-by-event combat log data with comprehensive filtering
- `get_report_graph(code, **kwargs)` - Get time-series performance graphs and metrics
- `get_report_table(code, **kwargs)` - Get tabular analysis data with sorting and filtering
- `get_report_rankings(code, **kwargs)` - Get report rankings and leaderboard data
- `get_report_player_details(code, **kwargs)` - Get detailed player performance data from reports

### System
- `get_rate_limit_data()` - Check API usage and rate limits

## Development

### Setup Development Environment

```bash
# Clone and install
git clone https://github.com/knowlen/esologs-python.git
cd esologs-python

# Production installation
pip install -e .

# Development installation with all tools
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

### Code Quality Tools

This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Fast Python linting
- **MyPy**: Static type checking
- **pytest**: Testing framework
- **pre-commit**: Git hooks for code quality

### Project Structure

```
esologs-python/
├── esologs/                 # Main package
│   ├── client.py           # Main client implementation
│   ├── async_base_client.py # Base async GraphQL client
│   ├── exceptions.py       # Custom exceptions
│   ├── validators.py       # Parameter validation utilities
│   └── get_*.py           # Generated GraphQL query modules
├── tests/                  # Test suite (278 tests)
│   ├── unit/              # Unit tests (76 tests)
│   ├── integration/       # Integration tests (85 tests)
│   ├── docs/              # Documentation tests (98 tests)
│   └── sanity/            # Sanity tests (19 tests)
├── docs/                  # Documentation source
├── access_token.py        # OAuth2 authentication
├── schema.graphql         # GraphQL schema
├── queries.graphql        # GraphQL queries
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

## API Reference

### GraphQL Schema
The complete GraphQL schema is available at: https://www.esologs.com/v2-api-docs/eso/

### Rate Limiting
- The ESO Logs API uses rate limiting based on points per hour
- Use `get_rate_limit_data()` to check your current usage
- The client includes automatic retry logic for rate limit errors

### Data Models
All API responses are validated using Pydantic models for type safety and data validation.

## Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install dependencies (`pip install -e ".[dev]"`)
4. Make your changes
5. Run tests (`pytest`)
6. Run code quality checks (`pre-commit run --all-files`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Development Roadmap

- **Phase 1** ✅: Security fixes and foundation improvements
- **Phase 2** 🚧: Core architecture and missing API functionality
  - ✅ PR #1: Character Rankings Implementation (Merged)
  - ✅ PR #2: Report Analysis Implementation (Merged)
  - ✅ PR #3: Integration Test Suite (Merged)
  - ✅ PR #4: Advanced Report Search (Merged)
  - 🚧 PR #5: Client Architecture Refactor (Next)
- **Phase 3** 🚧: Data transformation and pandas integration
- **Phase 4** ✅: Comprehensive testing and documentation (278 tests)
- **Phase 5** 🚧: Performance optimization and caching

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [ESO Logs](https://www.esologs.com/) for providing the API
- [ariadne-codegen](https://github.com/mirumee/ariadne-codegen) for GraphQL code generation
- The Elder Scrolls Online community

## Support

- **Issues**: [GitHub Issues](https://github.com/knowlen/esologs-python/issues)
- **Documentation**: [Read the Docs](https://esologs-python.readthedocs.io/)
- **ESO Logs API**: [Official Documentation](https://www.esologs.com/v2-api-docs/eso/)

---

**Note**: This library is not officially affiliated with ESO Logs or ZeniMax Online Studios.
