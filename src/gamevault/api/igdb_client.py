import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

_token_cache = {
    "access_token": None,
    "expires_at": 0
}

def get_igdb_token():
    if _token_cache["access_token"] and time.time() < _token_cache["expires_at"]:
        return _token_cache["access_token"]

    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    res = requests.post(url, params=params)
    res.raise_for_status()
    data = res.json()

    _token_cache["access_token"] = data["access_token"]
    _token_cache["expires_at"] = time.time() + data["expires_in"] - 60
    return data["access_token"]

def query_game(game_name: str):
    token = get_igdb_token()
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    url = "https://api.igdb.com/v4/games"
    query = f'''
    search "{game_name}";
    fields name, slug, summary, cover.url, first_release_date, genres.name, platforms.name;
    limit 1;
    '''
    res = requests.post(url, headers=headers, data=query)
    res.raise_for_status()
    return res.json()
