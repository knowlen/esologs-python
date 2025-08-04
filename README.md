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
[![Development Status](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/knowlen/esologs-python)
[![Tests](https://github.com/knowlen/esologs-python/actions/workflows/ci.yml/badge.svg)](https://github.com/knowlen/esologs-python/actions/workflows/ci.yml)

**esologs-python** is a comprehensive Python client library for the [ESO Logs API v2](https://www.esologs.com/v2-api-docs/eso/), designed for Elder Scrolls Online (ESO) players and developers who want to analyze combat logs, track performance metrics, and build tools for the ESO community. This library provides both synchronous and asynchronous interfaces to access ESO Logs data, with built-in support for data transformation and analysis.

## Project Status

| Metric | Status |
|--------|--------|
| **Current Version** | 0.2.0b1 |
| **API Coverage** | **100%** (42/42 methods implemented) |
| **Development Stage** | Active development |
| **Documentation** | [Read the Docs](https://esologs-python.readthedocs.io/) |
| **Tests** | 404 tests across unit, integration, documentation, and sanity suites |


## Installation

```bash
# Install from PyPI (recommended)
pip install esologs-python
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

Output:
```
Character: ExamplePlayer
Report: X7mLQ8kF - Dreadsail Reef
Report: Y9nPR2jG - Rockgrove
Ability: Elemental Weapon
Ability: Barbed Trap
Ability: Deadly Cloak
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

print(f"Token: {token[:20]}...")
print(f"Token length: {len(token)} characters")
```

Output:
```
Token: eyJ0eXAiOiJKV1QiLCJh...
Token length: 1087 characters
```

### Character Rankings

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

Output:
```
Best DPS: 125483.7
Total Kills: 47
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

Output:
```
Guild: Legendary Raiders
Server: PC-NA
Faction: Aldmeri Dominion
```

### Progress Race Tracking

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

Output:
```
No active race for Elder Scrolls Online
```

### OAuth2 User Authentication

To integrate with individual user accounts from the website, ESO Logs Python now supports both synchronous and asynchronous OAuth2 authentication flows:

#### Quick Start with OAuth2Flow
```python
from esologs import OAuth2Flow, Client
import asyncio

# Simplified OAuth2 flow
oauth_flow = OAuth2Flow(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="http://localhost:8765/callback"
)

# This opens your browser and handles the callback automatically
user_token = oauth_flow.authorize(scopes=["view-user-profile"])

# Use the token
async def main():
    async with Client(
        url="https://www.esologs.com/api/v2/user",
        user_token=user_token
    ) as client:
        current_user = await client.get_current_user()
        print(f"Logged in as: {current_user.user_data.current_user.name}")

asyncio.run(main())
```

Output:
```
Logged in as: YourPlayerName
```

#### Async OAuth2 Flow
```python
from esologs import AsyncOAuth2Flow, Client
import asyncio

async def main():
    # Use async OAuth2 flow for better performance
    oauth_flow = AsyncOAuth2Flow(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="http://localhost:8765/callback"
    )

    # Authorize asynchronously
    user_token = await oauth_flow.authorize(scopes=["view-user-profile"])

    # Use the token
    async with Client(
        url="https://www.esologs.com/api/v2/user",
        user_token=user_token
    ) as client:
        current_user = await client.get_current_user()
        print(f"Logged in as: {current_user.user_data.current_user.name}")

asyncio.run(main())
```

Output:
```
Logged in as: YourPlayerName
```

#### Manual Flow (for web apps)
```python
from esologs.user_auth import (
    generate_authorization_url,
    exchange_authorization_code_async,
    refresh_access_token_async
)

# Step 1: Generate authorization URL
auth_url = generate_authorization_url(
    client_id="your_client_id",
    redirect_uri="http://localhost:8000/callback",
    scopes=["view-user-profile"]
)

# Step 2: After callback, exchange code (async)
user_token = await exchange_authorization_code_async(
    client_id="your_client_id",
    client_secret="your_client_secret",
    code="auth_code_from_callback",
    redirect_uri="http://localhost:8000/callback"
)

# Step 3: Refresh when needed (async)
if user_token.is_expired:
    new_token = await refresh_access_token_async(
        client_id="your_client_id",
        client_secret="your_client_secret",
        refresh_token=user_token.refresh_token
    )
```

Output:
```python
# auth_url will be:
"https://www.esologs.com/oauth/authorize?client_id=your_client_id&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcallback&response_type=code&scope=view-user-profile&state=cN37P5g..."

# user_token will contain:
UserToken(
    access_token="eyJ0eXAiOiJKV1QiLCJhbGc...",
    token_type="Bearer",
    expires_in=3600,
    refresh_token="def50200a9bf924...",
    scope="view-user-profile"
)
```

### Advanced Report Search

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

Output:
```
Report: a7K9mNpL - Sanity's Edge
Duration: 3542000ms
Report: b8L0nOqM - Rockgrove
Duration: 2891000ms
```

## Available API Methods

### Game Data
- [`get_ability`](https://esologs-python.readthedocs.io/en/latest/api-reference/game-data/#get_ability) - Get specific ability information
- [`get_abilities`](https://esologs-python.readthedocs.io/en/latest/api-reference/game-data/#get_abilities) - List abilities with pagination
- [`get_class`](https://esologs-python.readthedocs.io/en/latest/api-reference/game-data/#get_class) - Get character class information
- [`get_classes`](https://esologs-python.readthedocs.io/en/latest/api-reference/game-data/#get_classes) - List character classes with optional filtering
- [`get_factions`](https://esologs-python.readthedocs.io/en/latest/api-reference/game-data/#get_factions) - Get available factions
- [`get_item`](https://esologs-python.readthedocs.io/en/latest/api-reference/game-data/#get_item) - Get specific item information
- [`get_items`](https://esologs-python.readthedocs.io/en/latest/api-reference/game-data/#get_items) - List items with pagination
- [`get_item_set`](https://esologs-python.readthedocs.io/en/latest/api-reference/game-data/#get_item_set) - Get item set information
- [`get_item_sets`](https://esologs-python.readthedocs.io/en/latest/api-reference/game-data/#get_item_sets) - List item sets with pagination
- [`get_map`](https://esologs-python.readthedocs.io/en/latest/api-reference/game-data/#get_map) - Get map information
- [`get_maps`](https://esologs-python.readthedocs.io/en/latest/api-reference/game-data/#get_maps) - List maps with pagination
- [`get_npc`](https://esologs-python.readthedocs.io/en/latest/api-reference/game-data/#get_npc) - Get NPC information
- [`get_npcs`](https://esologs-python.readthedocs.io/en/latest/api-reference/game-data/#get_npcs) - List NPCs with pagination

### Character Data
- [`get_character_by_id`](https://esologs-python.readthedocs.io/en/latest/api-reference/character-data/#get_character_by_id) - Get character profile
- [`get_character_reports`](https://esologs-python.readthedocs.io/en/latest/api-reference/character-data/#get_character_reports) - Get character's reports
- [`get_character_encounter_ranking`](https://esologs-python.readthedocs.io/en/latest/api-reference/character-data/#get_character_encounter_ranking) - Get character rankings (legacy)
- [`get_character_encounter_rankings`](https://esologs-python.readthedocs.io/en/latest/api-reference/character-data/#get_character_encounter_rankings) - Advanced encounter rankings with full filtering
- [`get_character_zone_rankings`](https://esologs-python.readthedocs.io/en/latest/api-reference/character-data/#get_character_zone_rankings) - Zone-wide character leaderboards

### Guild Data
- [`get_guild_by_id`](https://esologs-python.readthedocs.io/en/latest/api-reference/guild-data/#get_guild_by_id) - Get guild information by ID
- [`get_guild`](https://esologs-python.readthedocs.io/en/latest/api-reference/guild-data/#get_guild) - Flexible guild lookup
- [`get_guilds`](https://esologs-python.readthedocs.io/en/latest/api-reference/guild-data/#get_guilds) - List/search guilds
- [`get_guild_attendance`](https://esologs-python.readthedocs.io/en/latest/api-reference/guild-data/#get_guild_attendance) - Get guild raid attendance
- [`get_guild_members`](https://esologs-python.readthedocs.io/en/latest/api-reference/guild-data/#get_guild_members) - Get guild member list

### World Data
- [`get_world_data`](https://esologs-python.readthedocs.io/en/latest/api-reference/world-data/#get_world_data) - Get comprehensive world information
- [`get_regions`](https://esologs-python.readthedocs.io/en/latest/api-reference/world-data/#get_regions) - Get available regions
- [`get_zones`](https://esologs-python.readthedocs.io/en/latest/api-reference/world-data/#get_zones) - Get available zones
- [`get_encounters_by_zone`](https://esologs-python.readthedocs.io/en/latest/api-reference/world-data/#get_encounters_by_zone) - Get encounters in specific zone

### Report Data
- [`get_report_by_code`](https://esologs-python.readthedocs.io/en/latest/api-reference/report-data/#get_report_by_code) - Get specific report by code
- [`get_reports`](https://esologs-python.readthedocs.io/en/latest/api-reference/report-data/#get_reports) - Advanced report search with comprehensive filtering
- [`search_reports`](https://esologs-python.readthedocs.io/en/latest/api-reference/report-data/#search_reports) - Flexible report search with multiple criteria
- [`get_guild_reports`](https://esologs-python.readthedocs.io/en/latest/api-reference/report-data/#get_guild_reports) - Convenience method for guild reports
- [`get_user_reports`](https://esologs-python.readthedocs.io/en/latest/api-reference/report-data/#get_user_reports) - Convenience method for user reports
- [`get_report_events`](https://esologs-python.readthedocs.io/en/latest/api-reference/report-data/#get_report_events) - Get event-by-event combat log data with comprehensive filtering
- [`get_report_graph`](https://esologs-python.readthedocs.io/en/latest/api-reference/report-data/#get_report_graph) - Get time-series performance graphs and metrics
- [`get_report_table`](https://esologs-python.readthedocs.io/en/latest/api-reference/report-data/#get_report_table) - Get tabular analysis data with sorting and filtering
- [`get_report_rankings`](https://esologs-python.readthedocs.io/en/latest/api-reference/report-data/#get_report_rankings) - Get report rankings and leaderboard data
- [`get_report_player_details`](https://esologs-python.readthedocs.io/en/latest/api-reference/report-data/#get_report_player_details) - Get detailed player performance data from reports

### Progress Race
- [`get_progress_race`](https://esologs-python.readthedocs.io/en/latest/api-reference/progress-race-data/#get_progress_race) - Get world/realm first achievement race tracking data

### User Data (OAuth2 Required)
- [`get_user_by_id`](https://esologs-python.readthedocs.io/en/latest/api-reference/user-data/#get_user_by_id) - Get specific user information
- [`get_current_user`](https://esologs-python.readthedocs.io/en/latest/api-reference/user-data/#get_current_user) - Get authenticated user (requires /api/v2/user endpoint)
- [`get_user_data`](https://esologs-python.readthedocs.io/en/latest/api-reference/user-data/#get_user_data) - Get userData root object

### System
- [`get_rate_limit_data`](https://esologs-python.readthedocs.io/en/latest/api-reference/report-data/#get_rate_limit_data) - Check API usage and rate limits

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
│   ├── user_auth.py        # User authentication (OAuth2 flow)
│   ├── validators.py       # Parameter validation utilities
│   ├── mixins/             # Modular API functionality
│   │   ├── game_data.py    # Game data methods (abilities, items, etc.)
│   │   ├── character.py    # Character methods (info, rankings)
│   │   ├── world_data.py   # World data methods (zones, regions)
│   │   ├── guild.py        # Guild methods
│   │   ├── report.py       # Report methods (search, analysis)
│   │   ├── progress_race.py # Progress race tracking
│   │   └── user.py         # User data methods
│   └── _generated/         # Auto-generated GraphQL modules
│       ├── async_base_client.py  # Base async GraphQL client
│       ├── exceptions.py         # Custom exceptions
│       └── get_*.py             # Generated query/response models
├── tests/                  # Test suite (404 tests)
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   ├── docs/              # Documentation tests
│   └── sanity/            # Sanity tests
├── docs/                  # Documentation source
│   ├── assets/            # Images and static files
│   ├── javascripts/       # Custom JavaScript (API status)
│   └── *.md               # Documentation pages
├── examples/              # Example applications
│   ├── oauth2_sync.py     # Synchronous OAuth2 example
│   ├── oauth2_async.py    # Asynchronous OAuth2 example
│   ├── oauth2_flask_app.py # Flask web app example
│   └── oauth2_fastapi_app.py # FastAPI async app example
├── scripts/               # Development and utility scripts
│   ├── generate_client.sh # GraphQL client generation
│   ├── post_codegen.py    # Post-process generated code
│   ├── optimize_images.py # Image optimization
│   └── quick_api_check.py # API status checker
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

**Current Status: Beta Release (v0.2.0b1)**

✅ **Completed:**
- 100% API Coverage (42/42 methods)
- OAuth2 user authentication
- Comprehensive test suite (400+ tests)
- Full documentation with examples
- Client architecture refactoring

🚧 **Upcoming**
- Data transformation layer
- Performance optimization and caching
- Additional convenience methods
- Enhanced error recovery
- ... and more (see open issues)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [ESO Logs](https://www.esologs.com/) team for providing the API
- [ariadne-codegen](https://github.com/mirumee/ariadne-codegen) for GraphQL code generation
- The Elder Scrolls Online endgame community for sharing their combat logs

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
