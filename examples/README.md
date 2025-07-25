# Examples Directory

This directory contains example applications demonstrating how to use the ESO Logs Python client with OAuth2 authentication.

## Prerequisites

Before running any examples, you need:

1. **ESO Logs OAuth2 Application**
   - Create an app at https://www.esologs.com/oauth/clients
   - Add `http://localhost:8765/callback` (for sync/async examples) or the appropriate port for web apps to your redirect URLs

2. **Environment Variables**
   ```bash
   export ESOLOGS_ID="your-client-id"
   export ESOLOGS_SECRET="your-client-secret"
   ```

3. **Python Dependencies**
   ```bash
   pip install esologs-python
   ```

## Available Examples

### oauth2_sync.py

Demonstrates synchronous OAuth2 authentication flow using the `OAuth2Flow` class.

**Features:**
- Browser-based authorization
- Automatic token management
- Token persistence to file
- Token refresh handling
- API calls using authenticated client

**Usage:**
```bash
python examples/oauth2_sync.py
```

**What happens:**
1. Opens your browser for ESO Logs authorization
2. Starts local server on port 8765 to receive callback
3. Exchanges authorization code for access token
4. Saves token to `.esologs_token.json`
5. Makes authenticated API calls to get user data
6. Demonstrates token refresh if needed

---

### oauth2_async.py

Asynchronous version using `AsyncOAuth2Flow` for better performance in async applications.

**Features:**
- Async/await pattern throughout
- Async file I/O for token storage
- Efficient for concurrent operations
- Same functionality as sync version

**Additional Requirements:**
```bash
pip install aiofiles
```

**Usage:**
```bash
python examples/oauth2_async.py
```

**Key Differences from Sync:**
- Uses `AsyncOAuth2Flow` instead of `OAuth2Flow`
- All I/O operations are async (`await`)
- Better for integration with async frameworks

---

### oauth2_flask_app.py

Complete Flask web application with OAuth2 integration.

**Features:**
- Full web UI with login/logout
- Session management
- Token storage and refresh
- Protected routes
- User profile display
- JSON API endpoints

**Additional Requirements:**
```bash
pip install flask
```

**Usage:**
```bash
python examples/oauth2_flask_app.py
```
Then visit http://localhost:5000

**Routes:**
- `/` - Home page
- `/login` - Start OAuth2 flow
- `/callback` - OAuth2 callback handler
- `/profile` - User profile (requires auth)
- `/api/user` - JSON API endpoint
- `/refresh` - Refresh token endpoint
- `/logout` - Clear session

**Important:** Update redirect URL in ESO Logs app to `http://localhost:5000/callback`

---

### oauth2_fastapi_app.py

Modern async web application using FastAPI.

**Features:**
- Fully async implementation
- Auto-generated API documentation
- Type hints and validation
- Cookie-based sessions
- Dependency injection for auth
- OpenAPI/Swagger UI

**Additional Requirements:**
```bash
pip install fastapi uvicorn python-multipart
```

**Usage:**
```bash
python examples/oauth2_fastapi_app.py
```
Then visit http://localhost:8000

**API Documentation:**
- http://localhost:8000/docs - Swagger UI
- http://localhost:8000/redoc - ReDoc

**Important:** Update redirect URL in ESO Logs app to `http://localhost:8000/callback`

## Security Notes

1. **Never commit tokens**: The `.esologs_token.json` files contain sensitive access tokens. These are gitignored but be careful not to commit them.

2. **Environment Variables**: Store client credentials in environment variables, never hardcode them.

3. **Production Considerations**:
   - Use proper session management (Redis, database)
   - Implement CSRF protection
   - Use HTTPS in production
   - Store tokens securely (encrypted database)
   - Validate redirect URIs

## Common Patterns

### Loading Saved Tokens

```python
# Sync
from esologs.user_auth import load_token_from_file
token = load_token_from_file(".esologs_token.json")

# Async
from esologs.user_auth import load_token_from_file_async
token = await load_token_from_file_async(".esologs_token.json")
```

### Refreshing Expired Tokens

```python
# Sync
if token.is_expired:
    token = refresh_access_token(
        client_id, client_secret, token.refresh_token
    )

# Async
if token.is_expired:
    token = await refresh_access_token_async(
        client_id, client_secret, token.refresh_token
    )
```

### Using Tokens with Client

```python
# Option 1: Pass token object
async with Client(
    url="https://www.esologs.com/api/v2/user",
    user_token=token
) as client:
    user = await client.get_current_user()

# Option 2: Pass token string
async with Client(
    url="https://www.esologs.com/api/v2/user",
    user_token=token.access_token
) as client:
    user = await client.get_current_user()
```

## Troubleshooting

### "Invalid redirect URI"
- Ensure your redirect URI in the code matches exactly what's configured in your ESO Logs app
- Include the protocol (`http://` or `https://`)
- Include the port if not 80/443

### "Token expired"
- Tokens expire after the time specified in `expires_in`
- Use the refresh token to get a new access token
- Check `token.is_expired` before making API calls

### "Port already in use"
- Another process is using the callback port
- Change the port in both your code and ESO Logs app settings
- Or kill the process: `lsof -ti:8765 | xargs kill -9`

### API Returns 401
- Token may be expired - refresh it
- Ensure you're using the `/user` endpoint for user authentication
- Check that scopes include what you're trying to access

## Additional Resources

- [ESO Logs API Documentation](https://www.esologs.com/v2-api-docs/eso/)
- [OAuth2 Application Management](https://www.esologs.com/oauth/clients)
- [Project Documentation](https://esologs-python.readthedocs.io/)
