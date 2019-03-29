import requests
import webbrowser
from urllib.parse import urlsplit, parse_qs

class SpotifyUtil:
    def __init__(self, creds, headers):
        self.creds = creds
        self.headers = headers

    def auth_req(self):

        url = 'https://accounts.spotify.com/authorize?client_id={}&response_type=code&' \
              'redirect_uri={}&state={}&scope={}'.format(self.creds['client_id'],
               self.headers['redirect_uri'], self.creds['state'], self.headers['scope'])

        print("Opening auth url...")
        webbrowser.open_new_tab(url)

    def request_token(self):
        print('Paste redirect url:')
        token_url = input()
        query = urlsplit(token_url).query
        params = parse_qs(query)

        refresh_token_url = 'https://accounts.spotify.com/api/token'
        refresh_token_payload = {
            'grant_type': 'authorization_code', 
            'code': params['code'][0],
            'redirect_uri': self.headers['redirect_uri'],
            'client_id': self.creds['client_id'],
            'client_secret': self.creds['client_secret']
        }

        r = requests.post(refresh_token_url, data=refresh_token_payload)