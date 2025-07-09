# Python ESO Logs

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/knowlen/python-esologs)

A comprehensive Python client library for the [ESO Logs API v2](https://www.esologs.com/v2-api-docs/eso/). This library provides both synchronous and asynchronous interfaces to access Elder Scrolls Online combat logging data, with built-in support for data transformation and analysis.

## 🎯 Project Status

**Current Version:** 0.2.0-alpha  
**API Coverage:** ~20% (expanding to 95%+ coverage)  
**Development Stage:** Active development with major refactoring in progress

### What's Working
- ✅ OAuth2 authentication with ESO Logs API
- ✅ Basic game data queries (abilities, classes, items, NPCs, maps)
- ✅ Character and guild information retrieval
- ✅ Basic report data access
- ✅ Rate limiting information
- ✅ Async/await support with HTTP and WebSocket connections

### Coming Soon
- 🚧 Character rankings and performance metrics
- 🚧 Detailed report analysis (events, graphs, tables)
- 🚧 Progress race tracking
- 🚧 User account integration
- 🚧 Pandas DataFrame integration for data analysis
- 🚧 Comprehensive test coverage

## 🚀 Installation

**Note**: This package is currently in development and not yet published to PyPI.

### Current Installation Method

```bash
# Clone the repository
git clone https://github.com/knowlen/python-esologs.git
cd python-esologs

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

## 🔑 API Setup

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

## 📖 Quick Start

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
        print(f"Character: {character.character_data.character.name}")
        
        # Get recent reports for character
        reports = await client.get_character_reports(character_id=12345, limit=10)
        for report in reports.character_data.character.recent_reports.data:
            print(f"Report: {report.code} - {report.zone.name}")
        
        # Get game data
        abilities = await client.get_abilities(limit=50, page=1)
        for ability in abilities.game_data.abilities.data:
            print(f"Ability: {ability.name}")

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

## 📊 Available API Methods

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
- `get_np_cs(limit, page)` - List NPCs with pagination

### Character Data
- `get_character_by_id(id)` - Get character profile
- `get_character_reports(character_id, limit)` - Get character's reports
- `get_character_encounter_ranking(character_id, encounter_id)` - Get character rankings

### Guild Data
- `get_guild_by_id(guild_id)` - Get guild information

### World Data
- `get_world_data()` - Get comprehensive world information
- `get_regions()` - Get available regions
- `get_zones()` - Get available zones
- `get_encounters_by_zone(zone_id)` - Get encounters in specific zone

### Report Data
- `get_report_by_code(code)` - Get specific report by code

### System
- `get_rate_limit_data()` - Check API usage and rate limits

## 🛠️ Development

### Setup Development Environment

```bash
# Clone and install
git clone https://github.com/knowlen/python-esologs.git
cd python-esologs

# Current method
pip install -r requirements.txt

# Future method (when pyproject.toml is fully implemented)
pip install -e ".[dev]"

# Install pre-commit hooks (when available)
pre-commit install

# Run tests (when test suite is available)
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
python-esologs/
├── esologs/                 # Main package
│   ├── client.py           # Main client implementation
│   ├── async_base_client.py # Base async GraphQL client
│   ├── exceptions.py       # Custom exceptions
│   └── get_*.py           # Generated GraphQL query modules
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── access_token.py        # OAuth2 authentication
├── schema.graphql         # GraphQL schema
├── queries.graphql        # GraphQL queries
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

## 🔗 API Reference

### GraphQL Schema
The complete GraphQL schema is available at: https://www.esologs.com/v2-api-docs/eso/

### Rate Limiting
- The ESO Logs API uses rate limiting based on points per hour
- Use `get_rate_limit_data()` to check your current usage
- The client includes automatic retry logic for rate limit errors

### Data Models
All API responses are validated using Pydantic models for type safety and data validation.

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install dependencies (`pip install -r requirements.txt`)
4. Make your changes
5. Run tests (`pytest`)
6. Run code quality checks (`pre-commit run --all-files`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Development Roadmap

- **Phase 1** ✅: Security fixes and foundation improvements
- **Phase 2** 🚧: Core architecture and missing API functionality
- **Phase 3** 🚧: Data transformation and pandas integration
- **Phase 4** 🚧: Comprehensive testing and documentation
- **Phase 5** 🚧: Performance optimization and caching

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ESO Logs](https://www.esologs.com/) for providing the API
- [ariadne-codegen](https://github.com/mirumee/ariadne-codegen) for GraphQL code generation
- The Elder Scrolls Online community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/knowlen/python-esologs/issues)
- **Documentation**: [GitHub Repository](https://github.com/knowlen/python-esologs)
- **ESO Logs API**: [Official Documentation](https://www.esologs.com/v2-api-docs/eso/)

---

**Note**: This library is not officially affiliated with ESO Logs or ZeniMax Online Studios.
