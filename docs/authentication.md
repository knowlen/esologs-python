# Authentication

ESO Logs Python uses OAuth2 authentication to securely access the ESO Logs API v2.

## Prerequisites

Before you can authenticate, you need:

1. **ESO Logs Account**: Create a free account at [esologs.com](https://www.esologs.com/)
2. **API Client**: Register an application to get your credentials
3. **Environment Setup**: Configure your credentials securely

## Creating an API Client

### Step 1: Register Your Application

1. Visit [ESO Logs API Clients](https://www.esologs.com/api/clients/)
2. Click **"Create New Client"**
3. Fill out the application form:

   | Field | Value | Notes |
   |-------|-------|-------|
   | **Name** | Your Application Name | e.g., "My ESO Analysis Tool" |
   | **Description** | Brief description | What your app does |
   | **Type** | **Public Client** | For most use cases |
   | **Redirect URI** | Not required | Leave blank for server-side apps |

4. Click **"Create Client"**

### Step 2: Get Your Credentials

After creating your client, you'll receive:

- **Client ID**: Public identifier (like a username)
- **Client Secret**: Private key (keep this secure!)

!!! warning "Keep Your Secret Safe"
    **Never** commit your Client Secret to version control or share it publicly. 
    Treat it like a password - store it securely using environment variables.

## Setting Up Credentials

### Method 1: Environment Variables (Recommended)

Set your credentials as environment variables:

=== "Linux/macOS"

    ```bash
    # Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
    export ESOLOGS_ID="your_client_id_here"
    export ESOLOGS_SECRET="your_client_secret_here"
    
    # Apply changes
    source ~/.bashrc  # or restart your terminal
    ```

=== "Windows (PowerShell)"

    ```powershell
    # Set for current session
    $env:ESOLOGS_ID="your_client_id_here"
    $env:ESOLOGS_SECRET="your_client_secret_here"
    
    # Set permanently (requires restart)
    [Environment]::SetEnvironmentVariable("ESOLOGS_ID", "your_client_id_here", "User")
    [Environment]::SetEnvironmentVariable("ESOLOGS_SECRET", "your_client_secret_here", "User")
    ```

=== "Windows (Command Prompt)"

    ```cmd
    # Set for current session
    set ESOLOGS_ID=your_client_id_here
    set ESOLOGS_SECRET=your_client_secret_here
    
    # Set permanently
    setx ESOLOGS_ID "your_client_id_here"
    setx ESOLOGS_SECRET "your_client_secret_here"
    ```

### Method 2: .env File

Create a `.env` file in your project root:

```bash
# .env
ESOLOGS_ID=your_client_id_here
ESOLOGS_SECRET=your_client_secret_here
```

!!! danger "Security Warning"
    Add `.env` to your `.gitignore` file to prevent committing credentials:
    
    ```gitignore
    # .gitignore
    .env
    *.env
    .env.local
    ```

### Method 3: Direct Parameter Passing

For testing or specific use cases, you can pass credentials directly:

```python
from access_token import get_access_token

# Direct parameter passing (not recommended for production)
token = get_access_token(
    client_id="your_client_id",
    client_secret="your_client_secret"
)
```

## Using Authentication

### Basic Authentication

```python
from access_token import get_access_token

# Get access token using environment variables
token = get_access_token()

print(f"Access token: {token[:20]}...")  # Show first 20 chars
```

### With the Client

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def main():
    # Get authentication token
    token = get_access_token()
    
    # Create authenticated client
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:
        
        # Test authentication with rate limit check
        rate_limit = await client.get_rate_limit_data()
        print(f"Rate limit: {rate_limit.rate_limit_data.limit_per_hour}")
        print(f"Points used: {rate_limit.rate_limit_data.points_spent_this_hour}")

asyncio.run(main())
```

### Error Handling

```python
from access_token import get_access_token
from esologs.exceptions import AuthenticationError

try:
    token = get_access_token()
    print("✅ Authentication successful")
except AuthenticationError as e:
    print(f"❌ Authentication failed: {e}")
    print("Check your ESOLOGS_ID and ESOLOGS_SECRET environment variables")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

## Authentication Flow

ESO Logs Python uses the OAuth2 Client Credentials flow:

```mermaid
graph LR
    A[Your App] --> B[get_access_token()]
    B --> C[ESO Logs OAuth2]
    C --> D[Access Token]
    D --> E[API Requests]
    E --> F[ESO Logs API v2]
```

1. **Client Registration**: Your app is registered with ESO Logs
2. **Token Request**: App requests access token using credentials
3. **Token Response**: ESO Logs returns a bearer token
4. **API Access**: Token is used for authenticated API requests
5. **Token Refresh**: Tokens are automatically refreshed as needed

## Token Management

### Automatic Token Refresh

ESO Logs Python automatically handles token refresh:

- Tokens are cached and reused until expiration
- New tokens are requested automatically when needed
- No manual token management required

### Token Validation

Verify your token is working:

```python
import asyncio
from esologs.client import Client
from access_token import get_access_token

async def validate_token():
    """Validate authentication token by making a simple API call."""
    try:
        token = get_access_token()
        
        async with Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": f"Bearer {token}"}
        ) as client:
            
            # Simple validation call
            rate_limit = await client.get_rate_limit_data()
            
            print("✅ Token valid")
            print(f"Rate limit: {rate_limit.rate_limit_data.limit_per_hour}/hour")
            print(f"Used: {rate_limit.rate_limit_data.points_spent_this_hour}")
            return True
            
    except Exception as e:
        print(f"❌ Token validation failed: {e}")
        return False

# Run validation
asyncio.run(validate_token())
```

## Security Best Practices

### Environment Variables

✅ **Do**:
- Use environment variables for production
- Add to your shell profile for persistence
- Use different credentials for development/production

❌ **Don't**:
- Hard-code credentials in source code
- Commit credentials to version control
- Share credentials in chat/email

### File-based Configuration

If using `.env` files:

```python
# config.py
import os
from pathlib import Path

# Load from .env file
def load_env():
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

load_env()
```

### Production Deployment

For production environments:

- Use secure environment variable management
- Consider services like AWS Secrets Manager, Azure Key Vault
- Implement credential rotation
- Monitor API usage and rate limits

## Troubleshooting

### Common Authentication Errors

#### Invalid Client Credentials

```
AuthenticationError: Invalid client credentials
```

**Solutions**:
1. Verify your Client ID and Secret are correct
2. Check for extra spaces or hidden characters
3. Ensure environment variables are set properly
4. Try regenerating your Client Secret

#### Rate Limit Exceeded

```
RateLimitError: API rate limit exceeded
```

**Solutions**:
1. Check your current usage with `get_rate_limit_data()`
2. Implement request throttling in your application
3. Consider upgrading your ESO Logs plan
4. Cache responses to reduce API calls

#### Network Connection Issues

```
ConnectionError: Unable to connect to ESO Logs API
```

**Solutions**:
1. Check your internet connection
2. Verify ESO Logs API status
3. Check firewall/proxy settings
4. Try again after a brief delay

### Debugging Authentication

Enable debug logging to troubleshoot issues:

```python
import logging
from access_token import get_access_token

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Get token with debug info
token = get_access_token()
```

## Next Steps

With authentication configured:

1. **[Start with Quick Start](quickstart.md)** - Make your first API calls
2. **[Explore Examples](examples/basic-usage.md)** - Learn common patterns
3. **[Read API Reference](api-reference/game-data.md)** - Understand available methods

!!! tip "Rate Limits"
    ESO Logs API has rate limits based on points per hour. Use `get_rate_limit_data()` 
    to monitor your usage and avoid hitting limits.

!!! info "Multiple Applications"
    You can create multiple API clients for different applications or environments. 
    Each client gets its own rate limit allocation.