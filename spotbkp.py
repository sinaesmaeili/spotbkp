import json
from src.client import SpotifyUtil

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'redirect_uri': 'https://example.com/callback',
    'scope': 'user-library-read%20playlist-read-private'
}

with open('credentials.json') as creds:
    # Parsing credentials.json file
    data = json.load(creds)
    su = SpotifyUtil(data, headers)
    # Requesting user authentication
    su.auth_req()
    # Create a token from authentication
    tokens = su.request_token()

    if tokens != None:
        api_header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(tokens['access_token']) 
        }

        # Begin backup process
        su.init_backup(api_header)