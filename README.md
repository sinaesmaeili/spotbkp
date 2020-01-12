# spotbkp

spotbkp is a Python script which saves all your songs and playlists from Spotify into a JSON file

## Setup

To run locally, first register a Spotify app to get a client_id, client_secret
https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app

Make new `credentials.json` file in this format and use the client_id and client_secret from your recently made spotify app:
```
{
    "client_id": YOUR SPOTIFY APP CLIENT ID,
    "client_secret": YOUR SPOTIFY APP CLIENT SECRET ID,
    "state": RANDOM PASSWORD STATE TO PREVENT CSRF ATTACK
}
```
Save the file in the root directory of spotbkp

## Usage

Run the following command to start the app:

```
python spotbkp.py
```