# Troubleshooting

This guide helps you resolve common issues when using ESO Logs Python.

## API Connection Issues

### 502 Bad Gateway or 503 Service Unavailable

If you receive these errors, the ESO Logs API may be experiencing an outage:

```python
# Error example:
# GraphQLClientHttpError: 502 Bad Gateway
```

**What to do:**
1. Check if the API is down by running:
   ```bash
   python scripts/quick_api_check.py
   ```

2. Check ESO Logs social media for updates:
   - Twitter: [@LogsEso](https://twitter.com/LogsEso)
   - Discord: [ESO Logs Discord](https://discord.gg/rZQQ6bqtQb)

3. Wait and retry - outages are typically resolved quickly

### 401 Unauthorized

This error means your credentials are invalid or expired:

```python
# Error example:
# GraphQLClientHttpError: 401 Unauthorized
```

**Solutions:**
1. Check your environment variables:
   ```bash
   echo $ESOLOGS_ID
   echo $ESOLOGS_SECRET
   ```

2. Verify credentials are correct in your [ESO Logs API Clients](https://www.esologs.com/api/clients/) page

3. Generate a new token:
   ```python
   from esologs.auth import get_access_token
   token = get_access_token()  # This will use your env variables
   ```

### Network Timeouts

If requests are timing out:

```python
# Error example:
# TimeoutError: Request timed out
```

**Solutions:**
1. Check your internet connection
2. Try increasing timeout in client initialization:
   ```python
   client = Client(
       url="https://www.esologs.com/api/v2/client",
       headers={"Authorization": f"Bearer {token}"},
       timeout=30  # Increase from default
   )
   ```

## OAuth2 Issues

### "Invalid redirect URI"

The redirect URI in your code must exactly match one configured in your ESO Logs app.

**Solution:**
1. Go to [ESO Logs OAuth Clients](https://www.esologs.com/oauth/clients)
2. Add your redirect URI (e.g., `http://localhost:8765/callback`)
3. Ensure it matches exactly in your code (including port and protocol)

### Token Expired

OAuth2 tokens expire after the time specified in `expires_in`.

**Solution:**
```python
from esologs.user_auth import refresh_access_token

if token.is_expired:
    new_token = refresh_access_token(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=token.refresh_token
    )
```

## Common GraphQL Errors

### "Field not found"

This usually means you're trying to access a field that doesn't exist or requires specific permissions.

**Solution:**
1. Check the [ESO Logs API documentation](https://www.esologs.com/v2-api-docs/eso/)
2. Ensure you have the required scopes for user data endpoints
3. Verify the field exists for your query type

### Rate Limiting

If you're hitting rate limits:

```python
# Check your current usage
rate_limit = await client.get_rate_limit_data()
print(f"Points used: {rate_limit.rate_limit_data.points_spent_this_hour}")
```

**Solutions:**
1. Add delays between requests
2. Cache results when possible
3. Use pagination efficiently

## Installation Issues

### "No module named 'esologs'"

**Solution:**
```bash
# Make sure you've installed the package
pip install esologs-python

# Or for development
pip install -e ".[dev]"
```

### Dependency Conflicts

If you have dependency version conflicts:

**Solution:**
```bash
# Create a fresh virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install esologs-python
```

## Getting Help

If you're still experiencing issues:

1. **Check existing issues**: [GitHub Issues](https://github.com/knowlen/esologs-python/issues)
2. **Ask for help**: Create a new issue with:
   - Your Python version (`python --version`)
   - ESO Logs Python version (`pip show esologs-python`)
   - Full error message and traceback
   - Minimal code example that reproduces the issue
3. **Community support**: Join the [ESO Logs Discord](https://discord.gg/rZQQ6bqtQb)
