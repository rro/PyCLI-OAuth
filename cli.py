# cli.py
import os
import sys
import webbrowser
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session

load_dotenv()
CLIENT_ID = os.getenv("OAUTH_CLIENT_ID")
CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: Set OAUTH_CLIENT_ID and OAUTH_CLIENT_SECRET in .env file.")
    sys.exit(1)

REDIRECT_URI = "http://localhost:8000/callback"
AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
TOKEN_URL = 'https://github.com/login/oauth/access_token'

def main():
    github = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope="read:user,user:email")

    authorization_url, _ = github.authorization_url(AUTHORIZATION_BASE_URL)

    print("\nOpen this URL in your browser to authorize:")
    print(authorization_url)
    try:
        webbrowser.open(authorization_url)
    except Exception:
        pass

    print("\nAfter authorizing, look at the server terminal for the printed authorization code.")
    auth_code = input("Paste the authorization code here: ").strip()

    if not auth_code:
        print("Authorization code is required.")
        sys.exit(1)

    token = github.fetch_token(
        TOKEN_URL,
        client_secret=CLIENT_SECRET,
        code=auth_code,
    )

    print("\nLogin successful! Access token obtained.\n")

    response = github.get('https://api.github.com/user')
    if response.status_code == 200:
        user_info = response.json()
        print("Logged in user info:")
        print(f"  Username: {user_info.get('login')}")
        print(f"  Name: {user_info.get('name')}")
        print(f"  GitHub URL: {user_info.get('html_url')}")
        print(f"  Public repos: {user_info.get('public_repos')}")
    else:
        print("Failed to fetch user info from GitHub.")
        print("Response:", response.text)

if __name__ == '__main__':
    main()
