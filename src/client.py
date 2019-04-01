import requests
import webbrowser
import json
from urllib.parse import urlsplit, parse_qs
from progress.bar import Bar


class SpotifyUtil:
    def __init__(self, creds, headers):
        self.creds = creds
        self.headers = headers
        self.api_header = None

    # Initializes authentication request
    def auth_req(self):

        url = 'https://accounts.spotify.com/authorize?client_id={}&response_type=code&' \
              'redirect_uri={}&state={}&scope={}'.format(self.creds['client_id'],
                                                         self.headers['redirect_uri'], self.creds['state'], self.headers['scope'])

        print("Opening auth url...")
        webbrowser.open_new_tab(url)

    # Redirects to url with refresh token required for retreieving API access token
    def request_token(self):
        print('Paste redirect url:')
        token_url = input()
        query = urlsplit(token_url).query
        params = parse_qs(query)

        if params['state'][0] == self.creds['state']:
            refresh_token_url = 'https://accounts.spotify.com/api/token'
            refresh_token_payload = {
                'grant_type': 'authorization_code',
                'code': params['code'][0],
                'redirect_uri': self.headers['redirect_uri'],
                'client_id': self.creds['client_id'],
                'client_secret': self.creds['client_secret']
            }

            r = requests.post(refresh_token_url, data=refresh_token_payload)
            r = r.json()
            return r
        else:
            return None

    # Initialize backup and create new backup.json file
    def init_backup(self, api_header):
        self.api_header = api_header

        backup_template = {}
        backup_template['songs'] = self.get_songs('https://api.spotify.com/v1/me/tracks?limit=50')
        backup_template['playlists'] = self.get_playlist_tracks(self.get_playlist_ids())

        with open('backup.json', 'w') as new_file:
            json.dump(backup_template, new_file)

    # Retreives users 'favourite' songs list
    def get_songs(self, url, progress_name='Backing up saved songs'):
        r = requests.get(url, headers=self.api_header)
        r = r.json()

        songs_template = {}
        songs_template['songs'] = []

        bar = Bar(progress_name, max=r['total'])
        while True:
            for i in r['items']:
                song_obj = {}
                song_obj['artist'] = i['track']['artists'][0]['name']
                song_obj['name'] = i['track']['name']
                songs_template['songs'].append(song_obj)
                bar.next()

            if r['next'] == None:
                bar.finish()
                break
            else:
                r = requests.get(r['next'], headers=self.api_header)
                r = r.json()

        return songs_template['songs']

    def get_playlist_ids(self):
        me_tracks_url = 'https://api.spotify.com/v1/me/playlists?limit=50'
        r = requests.get(me_tracks_url, headers=self.api_header)
        r = r.json()

        playlist_ids = []

        while True:
            for i in r['items']:
                data = {}
                data['name'] = i['name']
                data['id'] = i['id']
                playlist_ids.append(data)

            if r['next'] == None:
                break
            else:
                r = requests.get(r['next'], headers=self.api_header)
                r = r.json()

        return playlist_ids

    def get_playlist_tracks(self, playlist_ids):
        playlists = {}
        playlists['playlists'] = {}

        for i in playlist_ids:
            url = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(i['id'])

            playlists['playlists'][i['name']] = self.get_songs(
                url, progress_name='Backing up {}'.format(i['name']))

        return playlists['playlists']
