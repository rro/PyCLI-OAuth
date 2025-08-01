from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
import os

load_dotenv()

client_id = os.getenv("OAUTH_CLIENT_ID")
client_secret = os.getenv("OAUTH_CLIENT_SECRET")

# OAuth endpoints for GitHub
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

# Start an OAuth2 session
github = OAuth2Session(client_id)

# Step 1: User Authorization. Redirect the user to GitHub for authorization
authorization_url, state = github.authorization_url(authorization_base_url)
print('Please go to this URL and authorize access:')
print(authorization_url)

# Step 2: Get the full callback URL after authorization
redirect_response = input('Paste the full redirect URL here: ')

# Step 3: Fetch the access token
token = github.fetch_token(
    token_url,
    client_secret=client_secret,
    authorization_response=redirect_response
)

# Step 4: Access a protected resource (get authenticated user profile)
response = github.get('https://api.github.com/user')
print('Authenticated user profile:')
print(response.json())
