#!/usr/bin/env python3
"""
ESO Logs OAuth2 Flask Web Application Example

This example demonstrates how to implement OAuth2 authentication in a Flask
web application for ESO Logs API access.

Prerequisites:
1. Set ESOLOGS_ID and ESOLOGS_SECRET environment variables
2. Add http://localhost:5000/callback to your ESO Logs app's redirect URLs
3. Install required packages: pip install esologs-python flask

Usage:
    python oauth2_flask_app.py

Then visit http://localhost:5000 in your browser.
"""

import asyncio
import os
import secrets
import sys
from functools import wraps
from typing import Any

from flask import Flask, jsonify, redirect, render_template_string, request, session

from esologs.client import Client
from esologs.user_auth import (
    exchange_authorization_code,
    generate_authorization_url,
    load_token_from_file,
    refresh_access_token,
    save_token_to_file,
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Configuration
CLIENT_ID_OPT = os.environ.get("ESOLOGS_ID")
CLIENT_SECRET_OPT = os.environ.get("ESOLOGS_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"
TOKEN_FILE = ".flask_esologs_token.json"

if not CLIENT_ID_OPT or not CLIENT_SECRET_OPT:
    print("Error: Please set ESOLOGS_ID and ESOLOGS_SECRET environment variables")
    sys.exit(1)

# Type-safe assignments after validation
CLIENT_ID: str = CLIENT_ID_OPT
CLIENT_SECRET: str = CLIENT_SECRET_OPT

# HTML Templates
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ESO Logs OAuth2 Example</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .button {
            display: inline-block;
            padding: 10px 20px;
            background: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .info { background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>ESO Logs OAuth2 Flask Example</h1>
    <div class="info">
        <p>This example demonstrates OAuth2 authentication with ESO Logs API.</p>
        <p>Click the button below to authenticate with your ESO Logs account.</p>
    </div>
    <a href="/login" class="button">Login with ESO Logs</a>
</body>
</html>
"""

PROFILE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ESO Logs Profile</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .info { background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .section { margin: 20px 0; }
        .button {
            display: inline-block;
            padding: 10px 20px;
            background: #f44336;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-right: 10px;
        }
        .button.refresh { background: #2196F3; }
        ul { list-style-type: none; padding-left: 20px; }
        li { margin: 5px 0; }
    </style>
</head>
<body>
    <h1>Welcome, {{ user.name }}!</h1>

    <div class="info">
        <strong>User ID:</strong> {{ user.id }}<br>
        {% if user.na_display_name %}
        <strong>NA Display Name:</strong> {{ user.na_display_name }}<br>
        {% endif %}
        {% if user.eu_display_name %}
        <strong>EU Display Name:</strong> {{ user.eu_display_name }}<br>
        {% endif %}
    </div>

    {% if user.guilds %}
    <div class="section">
        <h2>Guilds ({{ user.guilds|length }})</h2>
        <ul>
        {% for guild in user.guilds[:10] %}
            <li>🏰 {{ guild.name }} on {{ guild.server.name }}</li>
        {% endfor %}
        {% if user.guilds|length > 10 %}
            <li>... and {{ user.guilds|length - 10 }} more</li>
        {% endif %}
        </ul>
    </div>
    {% endif %}

    {% if user.characters %}
    <div class="section">
        <h2>Characters ({{ user.characters|length }})</h2>
        <ul>
        {% for char in user.characters[:10] %}
            <li>⚔️ {{ char.name }}</li>
        {% endfor %}
        {% if user.characters|length > 10 %}
            <li>... and {{ user.characters|length - 10 }} more</li>
        {% endif %}
        </ul>
    </div>
    {% endif %}

    <div class="section">
        <a href="/refresh" class="button refresh">Refresh Token</a>
        <a href="/logout" class="button">Logout</a>
    </div>
</body>
</html>
"""


def login_required(f: Any) -> Any:
    """Decorator to require authentication."""

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if "user_token" not in session:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")  # type: ignore[misc]
def home() -> str:
    """Home page."""
    return render_template_string(HOME_TEMPLATE)


@app.route("/login")  # type: ignore[misc]
def login() -> Any:
    """Initiate OAuth2 login flow."""
    # Generate CSRF token
    state = secrets.token_urlsafe(32)
    session["oauth_state"] = state

    # Generate authorization URL
    auth_url = generate_authorization_url(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scopes=["view-user-profile"],
        state=state,
    )

    return redirect(auth_url)


@app.route("/callback")  # type: ignore[misc]
def callback() -> Any:
    """Handle OAuth2 callback."""
    # Verify CSRF token
    state = request.args.get("state")
    if state != session.get("oauth_state"):
        return "Invalid state parameter - possible CSRF attack", 400

    # Clear the state
    session.pop("oauth_state", None)

    # Check for errors
    error = request.args.get("error")
    if error:
        error_desc = request.args.get("error_description", "Unknown error")
        return f"Authorization failed: {error} - {error_desc}", 400

    # Get authorization code
    code = request.args.get("code")
    if not code:
        return "No authorization code received", 400

    try:
        # Exchange code for token
        user_token = exchange_authorization_code(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            code=code,
            redirect_uri=REDIRECT_URI,
        )

        # Save token to file and session
        save_token_to_file(user_token, TOKEN_FILE)
        session["user_token"] = user_token.access_token
        session["refresh_token"] = user_token.refresh_token

        return redirect("/profile")

    except Exception as e:
        return f"Token exchange failed: {str(e)}", 500


@app.route("/profile")  # type: ignore[misc]
@login_required
def profile() -> str:
    """Display user profile."""
    try:
        # Load token from file to check expiration
        saved_token = load_token_from_file(TOKEN_FILE)

        if saved_token and saved_token.is_expired:
            # Try to refresh
            try:
                new_token = refresh_access_token(
                    client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    refresh_token=saved_token.refresh_token or "",
                )
                save_token_to_file(new_token, TOKEN_FILE)
                session["user_token"] = new_token.access_token
                session["refresh_token"] = new_token.refresh_token
            except Exception:
                # Refresh failed, need to re-authenticate
                session.clear()
                return redirect("/login")

        # Get user info
        user_data = asyncio.run(get_user_info(session["user_token"]))

        return render_template_string(PROFILE_TEMPLATE, user=user_data)

    except Exception as e:
        return f"Error loading profile: {str(e)}"


@app.route("/refresh")  # type: ignore[misc]
@login_required
def refresh() -> Any:
    """Manually refresh the access token."""
    try:
        refresh_token = session.get("refresh_token")
        if not refresh_token:
            return redirect("/login")

        # Refresh the token
        new_token = refresh_access_token(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            refresh_token=refresh_token,
        )

        # Update session and save
        save_token_to_file(new_token, TOKEN_FILE)
        session["user_token"] = new_token.access_token
        session["refresh_token"] = new_token.refresh_token

        return redirect("/profile")

    except Exception as e:
        # Refresh failed, clear session
        session.clear()
        return f"Token refresh failed: {str(e)}. Please login again.", 500


@app.route("/logout")  # type: ignore[misc]
def logout() -> Any:
    """Logout and clear session."""
    session.clear()
    # Optionally delete the token file
    try:
        os.unlink(TOKEN_FILE)
    except Exception:
        pass
    return redirect("/")


@app.route("/api/user")  # type: ignore[misc]
@login_required
def api_user() -> Any:
    """API endpoint returning user data as JSON."""
    try:
        user_data = asyncio.run(get_user_info(session["user_token"]))
        return jsonify(
            {
                "name": user_data["name"],
                "id": user_data["id"],
                "guilds": user_data["guilds"],
                "characters": user_data["characters"],
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


async def get_user_info(access_token: str) -> dict:
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


if __name__ == "__main__":
    print("Starting Flask app...")
    print(f"Make sure {REDIRECT_URI} is added to your ESO Logs app's redirect URLs")
    print("Visit http://localhost:5000 to start")
    app.run(host="0.0.0.0", port=5000, debug=True)
