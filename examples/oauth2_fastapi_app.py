#!/usr/bin/env python3
"""
ESO Logs OAuth2 FastAPI Async Web Application Example

This example demonstrates how to implement OAuth2 authentication in a FastAPI
web application using async/await for optimal performance.

Prerequisites:
1. Set ESOLOGS_ID and ESOLOGS_SECRET environment variables
2. Add http://localhost:8000/callback to your ESO Logs app's redirect URLs
3. Install required packages: pip install esologs-python fastapi uvicorn python-multipart

Usage:
    python oauth2_fastapi_app.py

Then visit http://localhost:8000 in your browser.
API docs available at http://localhost:8000/docs
"""

import os
import secrets
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel

from esologs.client import Client
from esologs.user_auth import (
    exchange_authorization_code_async,
    generate_authorization_url,
    refresh_access_token_async,
    save_token_to_file_async,
)

# Configuration
CLIENT_ID_OPT = os.environ.get("ESOLOGS_ID")
CLIENT_SECRET_OPT = os.environ.get("ESOLOGS_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"
TOKEN_FILE = ".fastapi_esologs_token.json"

if not CLIENT_ID_OPT or not CLIENT_SECRET_OPT:
    print("Error: Please set ESOLOGS_ID and ESOLOGS_SECRET environment variables")
    sys.exit(1)

# Type-safe assignments after validation
CLIENT_ID: str = CLIENT_ID_OPT
CLIENT_SECRET: str = CLIENT_SECRET_OPT

# Initialize FastAPI app
app = FastAPI(
    title="ESO Logs OAuth2 Example",
    description="FastAPI application demonstrating ESO Logs OAuth2 authentication",
    version="1.0.0",
)

# In-memory session store (use Redis in production)
sessions: Dict[str, Dict[str, Any]] = {}


# Pydantic models
class UserInfo(BaseModel):
    id: int
    name: str
    na_display_name: Optional[str] = None
    eu_display_name: Optional[str] = None
    guilds: list = []
    characters: list = []


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    message: str = "Token refreshed successfully"


# HTML Templates
HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ESO Logs OAuth2 FastAPI Example</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 40px;
            background: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #333; margin-bottom: 10px; }
        .subtitle { color: #666; margin-bottom: 30px; }
        .button {
            display: inline-block;
            padding: 12px 30px;
            background: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 600;
            transition: background 0.3s;
        }
        .button:hover { background: #45a049; }
        .info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 30px 0;
            border-left: 4px solid #4CAF50;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .feature {
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
            text-align: center;
        }
        .api-link {
            margin-top: 30px;
            padding-top: 30px;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ESO Logs OAuth2 FastAPI Example</h1>
        <p class="subtitle">Async authentication with ESO Logs API</p>

        <div class="info">
            <p><strong>Welcome!</strong> This example demonstrates OAuth2 authentication with ESO Logs API using FastAPI's async capabilities.</p>
            <p>Click the button below to authenticate with your ESO Logs account.</p>
        </div>

        <div class="features">
            <div class="feature">
                <h3>🚀 Async</h3>
                <p>Built with async/await for optimal performance</p>
            </div>
            <div class="feature">
                <h3>🔐 Secure</h3>
                <p>OAuth2 with CSRF protection</p>
            </div>
            <div class="feature">
                <h3>📄 API Docs</h3>
                <p>Auto-generated OpenAPI documentation</p>
            </div>
        </div>

        <div style="text-align: center;">
            <a href="/login" class="button">Login with ESO Logs</a>
        </div>

        <div class="api-link">
            <p>🔗 Check out the <a href="/docs">interactive API documentation</a></p>
        </div>
    </div>
</body>
</html>
"""

PROFILE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ESO Logs Profile</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 40px;
            background: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1, h2 { color: #333; }
        .info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .section { margin: 30px 0; }
        .button {
            display: inline-block;
            padding: 10px 20px;
            background: #f44336;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-right: 10px;
            font-weight: 600;
            transition: background 0.3s;
        }
        .button:hover { background: #da190b; }
        .button.refresh { background: #2196F3; }
        .button.refresh:hover { background: #0b7dda; }
        .button.api { background: #FF9800; }
        .button.api:hover { background: #e68900; }
        ul { list-style-type: none; padding-left: 0; }
        li {
            margin: 8px 0;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #4CAF50;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome, {{ name }}!</h1>

        <div class="info">
            <strong>User ID:</strong> {{ id }}<br>
            {% if na_display_name %}
            <strong>NA Display Name:</strong> {{ na_display_name }}<br>
            {% endif %}
            {% if eu_display_name %}
            <strong>EU Display Name:</strong> {{ eu_display_name }}<br>
            {% endif %}
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-number">{{ guilds|length }}</div>
                <div>Guilds</div>
            </div>
            <div class="stat">
                <div class="stat-number">{{ characters|length }}</div>
                <div>Characters</div>
            </div>
        </div>

        {% if guilds %}
        <div class="section">
            <h2>🏰 Guilds</h2>
            <ul>
            {% for guild in guilds[:10] %}
                <li>{{ guild.name }} on {{ guild.server.name }}</li>
            {% endfor %}
            {% if guilds|length > 10 %}
                <li style="text-align: center;">... and {{ guilds|length - 10 }} more</li>
            {% endif %}
            </ul>
        </div>
        {% endif %}

        {% if characters %}
        <div class="section">
            <h2>⚔️ Characters</h2>
            <ul>
            {% for char in characters[:10] %}
                <li>{{ char.name }}</li>
            {% endfor %}
            {% if characters|length > 10 %}
                <li style="text-align: center;">... and {{ characters|length - 10 }} more</li>
            {% endif %}
            </ul>
        </div>
        {% endif %}

        <div class="section">
            <a href="/api/user" class="button api">View JSON</a>
            <a href="/refresh" class="button refresh">Refresh Token</a>
            <a href="/logout" class="button">Logout</a>
        </div>
    </div>
</body>
</html>
"""


async def get_current_user_token(request: Request) -> Optional[str]:
    """Get current user token from session."""
    state = request.cookies.get("session_state")
    if state and state in sessions:
        return sessions[state].get("access_token")
    return None


async def require_auth(token: Optional[str] = Depends(get_current_user_token)) -> str:
    """Dependency to require authentication."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    return token


@app.get("/", response_class=HTMLResponse)  # type: ignore[misc]
async def home() -> str:
    """Home page."""
    return HOME_HTML


@app.get("/login")  # type: ignore[misc]
async def login() -> str:
    """Initiate OAuth2 login flow."""
    # Generate CSRF token
    state = secrets.token_urlsafe(32)

    # Store state
    sessions[state] = {"created_at": datetime.utcnow(), "status": "pending"}

    # Generate authorization URL
    auth_url = generate_authorization_url(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scopes=["view-user-profile"],
        state=state,
    )

    # Redirect to ESO Logs
    response = RedirectResponse(url=auth_url)
    response.set_cookie(key="oauth_state", value=state, httponly=True, max_age=600)
    return response


@app.get("/callback")  # type: ignore[misc]
async def callback(
    request: Request,
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
) -> RedirectResponse:
    """Handle OAuth2 callback."""
    # Check for errors
    if error:
        error_desc = request.query_params.get("error_description", "Unknown error")
        raise HTTPException(
            status_code=400, detail=f"Authorization failed: {error} - {error_desc}"
        )

    # Verify state
    stored_state = request.cookies.get("oauth_state")
    if not state or state != stored_state or state not in sessions:
        raise HTTPException(
            status_code=400, detail="Invalid state parameter - possible CSRF attack"
        )

    if not code:
        raise HTTPException(status_code=400, detail="No authorization code received")

    try:
        # Exchange code for token asynchronously
        user_token = await exchange_authorization_code_async(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            code=code,
            redirect_uri=REDIRECT_URI,
        )

        # Save token to file
        await save_token_to_file_async(user_token, TOKEN_FILE)

        # Create session
        session_state = secrets.token_urlsafe(32)
        sessions[session_state] = {
            "access_token": user_token.access_token,
            "refresh_token": user_token.refresh_token,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow()
            + timedelta(seconds=user_token.expires_in or 3600),
        }

        # Redirect to profile
        response = RedirectResponse(url="/profile", status_code=302)
        response.set_cookie(
            key="session_state", value=session_state, httponly=True, max_age=86400
        )
        response.delete_cookie(key="oauth_state")
        return response

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Token exchange failed: {str(e)}"
        ) from e


@app.get("/profile", response_class=HTMLResponse)  # type: ignore[misc]
async def profile(request: Request, token: str = Depends(require_auth)) -> str:
    """Display user profile."""
    try:
        # Get user info
        user_data = await get_user_info(token)

        # Simple template rendering (use Jinja2 in production)
        html = PROFILE_HTML
        for key, value in user_data.items():
            html = html.replace(f"{{{{ {key} }}}}", str(value))

        # Handle conditionals
        import re

        # Process if statements
        def process_if(match: re.Match[str]) -> str:
            condition = match.group(1)
            content = match.group(2)
            if condition in user_data and user_data[condition]:
                return content
            return ""

        html = re.sub(
            r"{%\s*if\s+(\w+)\s*%}(.*?){%\s*endif\s*%}",
            process_if,
            html,
            flags=re.DOTALL,
        )

        # Process for loops
        def process_for(match: re.Match[str]) -> str:
            var = match.group(1)
            collection = match.group(2)
            limit = match.group(3)
            template = match.group(4)

            if collection in user_data:
                items = user_data[collection]
                if limit:
                    items = items[: int(limit)]

                result = ""
                for item in items:
                    item_html = template
                    item_html = item_html.replace(
                        f"{{{{ {var}.name }}}}", getattr(item, "name", str(item))
                    )
                    if hasattr(item, "server"):
                        item_html = item_html.replace(
                            f"{{{{ {var}.server.name }}}}", item.server.name
                        )
                    result += item_html
                return result
            return ""

        html = re.sub(
            r"{%\s*for\s+(\w+)\s+in\s+(\w+)(?:\[:(\d+)\])?\s*%}(.*?){%\s*endfor\s*%}",
            process_for,
            html,
            flags=re.DOTALL,
        )

        # Handle length filters
        html = re.sub(
            r"{{\s*(\w+)\|length\s*}}",
            lambda m: str(len(user_data.get(m.group(1), []))),
            html,
        )

        return HTMLResponse(content=html)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading profile: {str(e)}"
        ) from e


@app.get("/api/user", response_model=UserInfo)  # type: ignore[misc]
async def api_user(token: str = Depends(require_auth)) -> Dict[str, Any]:
    """Get current user information as JSON."""
    return await get_user_info(token)


@app.post("/refresh", response_model=TokenResponse)  # type: ignore[misc]
async def refresh_token(request: Request) -> Dict[str, Any]:
    """Refresh the access token."""
    state = request.cookies.get("session_state")
    if not state or state not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = sessions[state]
    refresh_token = session.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token available")

    try:
        # Refresh token asynchronously
        new_token = await refresh_access_token_async(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            refresh_token=refresh_token,
        )

        # Update session
        session["access_token"] = new_token.access_token
        session["refresh_token"] = new_token.refresh_token
        session["expires_at"] = datetime.utcnow() + timedelta(
            seconds=new_token.expires_in or 3600
        )

        # Save to file
        await save_token_to_file_async(new_token, TOKEN_FILE)

        return TokenResponse(
            access_token=new_token.access_token,
            token_type=new_token.token_type,
            expires_in=new_token.expires_in or 3600,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Token refresh failed: {str(e)}"
        ) from e


@app.get("/logout")  # type: ignore[misc]
async def logout(request: Request) -> RedirectResponse:
    """Logout and clear session."""
    state = request.cookies.get("session_state")
    if state and state in sessions:
        del sessions[state]

    response = RedirectResponse(url="/")
    response.delete_cookie(key="session_state")
    return response


async def get_user_info(access_token: str) -> Dict[str, Any]:
    """Get user information from ESO Logs API."""
    async with Client(
        url="https://www.esologs.com/api/v2/user", user_token=access_token
    ) as client:
        current_user = await client.get_current_user()  # type: ignore[attr-defined]
        user = current_user.user_data.current_user

        return {
            "name": user.name,
            "id": user.id,
            "na_display_name": user.na_display_name,
            "eu_display_name": user.eu_display_name,
            "guilds": user.guilds or [],
            "characters": user.characters or [],
        }


@app.on_event("startup")  # type: ignore[misc]
async def startup_event() -> None:
    """Clean up old sessions on startup."""
    # In production, use a proper session store with TTL
    print("FastAPI OAuth2 Example started")
    print("Visit http://localhost:8000 to begin")
    print("API documentation available at http://localhost:8000/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
