<div align="center">
  <picture>
    <source type="image/webp" srcset="docs/assets/logo.webp">
    <img src="docs/assets/logo.png" alt="ESO Logs Python" width="300">
  </picture>
</div>

# ESO Logs Python Client - Elder Scrolls Online Combat Log Analysis

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/esologs-python.svg)](https://pypi.org/project/esologs-python/)
[![Documentation](https://readthedocs.org/projects/esologs-python/badge/?version=latest)](https://esologs-python.readthedocs.io/)
[![Development Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/knowlen/esologs-python)
[![Tests](https://github.com/knowlen/esologs-python/actions/workflows/ci.yml/badge.svg)](https://github.com/knowlen/esologs-python/actions/workflows/ci.yml)

**esologs-python** is a comprehensive Python client library for the [ESO Logs API v2](https://www.esologs.com/v2-api-docs/eso/), designed for Elder Scrolls Online (ESO) players and developers who want to analyze combat logs, track performance metrics, and build tools for the ESO community. This library provides both synchronous and asynchronous interfaces to access ESO Logs data, with built-in support for data transformation and analysis.

## Project Status

| Metric | Status |
|--------|--------|
| **Current Version** | 0.2.0a3 |
| **API Coverage** | **100%** (42/42 methods implemented) |
| **Development Stage** | Active development |
| **Documentation** | [Read the Docs](https://esologs-python.readthedocs.io/) |
| **Tests** | 404 tests across unit, integration, documentation, and sanity suites |

### Current API Coverage
**Complete Coverage (8/8 sections):**
1. ✅ **gameData** - 13 methods (COMPLETE)
2. ✅ **characterData** - 5 methods (COMPLETE)
3. ✅ **reportData** - 10 methods (COMPLETE)
4. ✅ **worldData** - 4 methods (COMPLETE)
5. ✅ **rateLimitData** - 1 method (COMPLETE)
6. ✅ **guildData** - 5 methods (COMPLETE)
7. ✅ **progressRaceData** - 1 method (COMPLETE)
8. ✅ **userData** - 3 methods (COMPLETE - OAuth2 user authentication)

### Features Complete
- ✅ Progress race tracking
- ✅ User account integration with OAuth2 flow
- ✅ Client architecture refactor (modular design with mixins)
- ✅ **100% API Coverage** - All ESO Logs API methods implemented!

## Installation

```bash
# Install from PyPI (recommended)
pip install esologs-python

# For development or latest features
pip install git+https://github.com/knowlen/esologs-python.git@main
```

### Development Installation

```bash
# Clone for development
git clone https://github.com/knowlen/esologs-python.git
cd esologs-python
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
from esologs.auth import get_access_token

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
from esologs.auth import get_access_token

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
from esologs.auth import get_access_token

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

### Guild Data

```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

async def main():
    token = get_access_token()

    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Get guild information by ID
        guild = await client.get_guild_by_id(guild_id=123)

        if guild.guild_data.guild:
            print(f"Guild: {guild.guild_data.guild.name}")
            print(f"Server: {guild.guild_data.guild.server.name}")
            print(f"Faction: {guild.guild_data.guild.faction.name}")

        # Search for guilds on a specific server
        guilds = await client.get_guilds(
            server_slug="megaserver",
            server_region="NA",
            limit=10
        )

        # Get guild attendance for raids
        attendance = await client.get_guild_attendance(
            guild_id=123,
            zone_id=38,  # e.g., Dreadsail Reef
            limit=20
        )

        # Get guild members
        members = await client.get_guild_members(guild_id=123, limit=50)

asyncio.run(main())
```

### Progress Race Tracking (NEW)

```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token
from esologs._generated.exceptions import GraphQLClientGraphQLMultiError

async def main():
    token = get_access_token()

    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        try:
            # Get progress race data for a specific zone
            race_data = await client.get_progress_race(
                zone_id=40,      # Lucent Citadel
                difficulty=2,    # Veteran
                size=12         # 12-person
            )

            if race_data.progress_race_data.progress_race:
                print("Active race data:", race_data.progress_race_data.progress_race)
            else:
                print("No active race data available")

        except GraphQLClientGraphQLMultiError as e:
            # Expected when no race is active
            if "No race supported for this game currently" in str(e):
                print("No active race for Elder Scrolls Online")
            else:
                print(f"GraphQL error: {e}")

asyncio.run(main())
```

### OAuth2 User Authentication (NEW)

```python
from esologs.user_auth import (
    generate_authorization_url,
    exchange_authorization_code,
    UserToken
)
from esologs.client import Client

# Step 1: Generate authorization URL
auth_url = generate_authorization_url(
    client_id="your_client_id",
    redirect_uri="http://localhost:8000/callback",
    scopes=["view-user-profile"]
)
# Redirect user to auth_url

# Step 2: After user authorizes, exchange code for token
user_token = exchange_authorization_code(
    client_id="your_client_id",
    client_secret="your_client_secret",
    code="auth_code_from_callback",
    redirect_uri="http://localhost:8000/callback"
)

# Step 3: Use token with client
async def get_user_info():
    async with Client(
        url="https://www.esologs.com/api/v2/user",  # Note: /user endpoint
        user_token=user_token
    ) as client:
        # Get current user
        current_user = await client.get_current_user()
        print(f"Logged in as: {current_user.user_data.current_user.name}")

        # Get user's guilds and characters
        for guild in current_user.user_data.current_user.guilds:
            print(f"Guild: {guild.name}")

        # Get specific user by ID
        user = await client.get_user_by_id(user_id=12345)
        print(f"User: {user.user_data.user.name}")

asyncio.run(get_user_info())
```

### Advanced Report Search (NEW)

```python
import asyncio
from esologs.client import Client
from esologs.auth import get_access_token

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
- `get_guild_by_id(guild_id)` - Get guild information by ID
- `get_guild(guild_id=None, guild_name=None, guild_server_slug=None, guild_server_region=None)` - Flexible guild lookup
- `get_guilds(server_id=None, server_slug=None, server_region=None, limit=None, page=None)` - List/search guilds
- `get_guild_attendance(guild_id, zone_id=None, encounter_id=None, difficulty=None, ...)` - Get guild raid attendance
- `get_guild_members(guild_id, limit=None, page=None)` - Get guild member list

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

### Progress Race
- `get_progress_race(**kwargs)` - Get world/realm first achievement race tracking data

### User Data (OAuth2 Required)
- `get_user_by_id(user_id)` - Get specific user information
- `get_current_user()` - Get authenticated user (requires /api/v2/user endpoint)
- `get_user_data()` - Get userData root object

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
│   ├── client.py           # Main client (86 lines, uses mixins)
│   ├── method_factory.py   # Dynamic method generation (349 lines)
│   ├── param_builders.py   # Parameter validation & builders (330 lines)
│   ├── queries.py          # Centralized GraphQL queries (770 lines)
│   ├── auth.py             # OAuth2 authentication module
│   ├── validators.py       # Parameter validation utilities
│   ├── mixins/             # Modular API functionality
│   │   ├── game_data.py    # Game data methods (abilities, items, etc.)
│   │   ├── character.py    # Character methods (info, rankings)
│   │   ├── world_data.py   # World data methods (zones, regions)
│   │   ├── guild.py        # Guild methods
│   │   └── report.py       # Report methods (search, analysis)
│   └── _generated/         # Auto-generated GraphQL modules
│       ├── async_base_client.py  # Base async GraphQL client
│       ├── exceptions.py         # Custom exceptions
│       └── get_*.py             # Generated query/response models
├── tests/                  # Test suite (369 tests)
│   ├── unit/              # Unit tests (111 tests)
│   ├── integration/       # Integration tests (93 tests)
│   ├── docs/              # Documentation tests (106 tests)
│   └── sanity/            # Sanity tests (19 tests)
├── docs/                  # Documentation source
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
  - ✅ PR #5: Client Architecture Refactor (Merged)
  - ✅ PR #28: Progress Race Implementation (In Review)
- **Phase 3** 🚧: Data transformation and pandas integration
- **Phase 4** ✅: Comprehensive testing and documentation (369 tests)
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

## Related Projects and Resources

- **ESO Logs**: [esologs.com](https://www.esologs.com/) - The premier Elder Scrolls Online combat logging service
- **Elder Scrolls Online**: [elderscrollsonline.com](https://www.elderscrollsonline.com/) - Official ESO website
- **Python Package Index**: [pypi.org/project/esologs-python](https://pypi.org/project/esologs-python/)

## Search Terms

Elder Scrolls Online API, ESO combat logs, ESO Logs Python, ESO performance analysis, Elder Scrolls Online DPS meter, ESO raid analysis, MMORPG combat analysis Python, ESO Logs API client, Elder Scrolls Online data analysis
