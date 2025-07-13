<div class="hero-section">
  <h1>ESO Logs Python</h1>
  <p>A comprehensive Python client library for the ESO Logs API v2</p>
  <p>Access Elder Scrolls Online combat logging data with both synchronous and asynchronous interfaces, built-in data transformation, and analysis capabilities.</p>
  <a href="installation/" class="md-button md-button--primary">Get Started</a>
  <a href="api-reference/game-data/" class="md-button">API Reference</a>
</div>

## Quickstart

=== "Installation"

    ```bash
    # Clone the repository
    git clone https://github.com/knowlen/esologs-python.git
    cd esologs-python
    
    # Install the package
    pip install -e .
    ```

=== "Authentication"

    ```bash
    # Set your API credentials
    export ESOLOGS_ID="your_client_id"
    export ESOLOGS_SECRET="your_client_secret"
    ```

=== "Basic Usage"

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
            
            # Get character information
            character = await client.get_character_by_id(id=12345)
            print(f"Character: {character.character_data.character.name}")
            
            # Search for reports
            reports = await client.search_reports(
                guild_id=123,
                zone_id=456,
                limit=10
            )
    
    asyncio.run(main())
    ```


## Project Status

<div class="feature-grid">
  <div class="feature-card">
    <h3>Current Version</h3>
    <p><strong>v0.2.0-alpha</strong><br>
    <span class="status-badge status-badge--completed">75% API Coverage</span></p>
    <p>Active development with comprehensive testing and documentation.</p>
  </div>
  <div class="feature-card">
    <h3>Coming Soon (25%)</h3>
    <ul>
      <li><span class="status-badge status-badge--planned">User Accounts</span> Account management & settings</li>
      <li><span class="status-badge status-badge--planned">Progress Tracking</span> Race & achievement tracking</li>
      <li><span class="status-badge status-badge--planned">Enhanced Guilds</span> Advanced guild management</li>
      <li><span class="status-badge status-badge--planned">Caching</span> Performance optimization</li>
    </ul>
  </div>
</div>

## API Coverage
## Architecture
- **Type Safety**: Full type hints with Pydantic models
- **Async First**: Native async/await support with HTTP and WebSocket
- **GraphQL Integration**: Code generation with `ariadne-codegen`
- **Security**: OAuth2 authentication with parameter validation
- **Testing**: 278 tests with comprehensive coverage
- **Code Quality**: Pre-commit hooks, linting, and formatting

---

!!! note "Development Status"
    This library is in active development. While the core functionality is stable and tested, 
    the API may change before the 1.0 release. See our [changelog](changelog.md) for the latest updates.
