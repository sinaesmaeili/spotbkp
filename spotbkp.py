import json
from src.util import SpotifyUtil

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'redirect_uri': 'https://example.com/callback',
    'scope': 'user-library-read%20playlist-read-private'
}

with open('credentials.json') as creds:
    data = json.load(creds)
    su = SpotifyUtil(data, headers)
    su.auth_req()
    su.request_token()