# gamevault/sync/steam.py
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from gamevault.db.models import user_owned_games, database, users_sessions
from gamevault.sync.sanity import sanity_check
from gamevault.db.queries import get_icon_url
import requests
import os
from sqlalchemy.dialects.postgresql import insert

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
router = APIRouter()

# Step 1: Redirect to Steam login
@router.get("/sync/steam")
async def steam_login_redirect(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login")

    row = await database.fetch_one(
        users_sessions.select().where(users_sessions.c.user_id == user_id)
    )

    if row and row["steam_id"]:
        return RedirectResponse(url="/sync/steam/fetch")

    steam_openid_url = (
        "https://steamcommunity.com/openid/login"
        "?openid.ns=http://specs.openid.net/auth/2.0"
        "&openid.mode=checkid_setup"
        "&openid.return_to=http://127.0.0.1:8006/auth/steam/callback"
        "&openid.realm=http://127.0.0.1:8006/"
        "&openid.identity=http://specs.openid.net/auth/2.0/identifier_select"
        "&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select"
    )
    return RedirectResponse(steam_openid_url)


# Step 2: Callback from Steam after login
@router.get("/auth/steam/callback")
async def steam_callback(request: Request):
    params = dict(request.query_params)
    claimed_id = params.get("openid.claimed_id")

    if not claimed_id:
        return {"error": "Missing claimed_id from Steam"}

    steam_id = claimed_id.split("/")[-1]
    print("Steam id", steam_id)

    user_id = request.session.get("user_id")
    if not user_id:
        return {"error": "Not logged in to GameVault"}


    query = insert(users_sessions).values(
        user_id=user_id,
        steam_id=steam_id
    ).on_conflict_do_update(
        index_elements=[users_sessions.c.user_id],
        set_={"steam_id": steam_id}
    )
    await database.execute(query)


    game_list = await fetch_steam_games(steam_id)

    user_id = request.session.get("user_id")
    if not user_id:
        return {"error": "Not logged in to GameVault"}

    valid_games = await sanity_check(user_id, [g["name"] for g in game_list], "Steam")

    inserted = 0
    for game in game_list:
        if game["name"] not in valid_games:
            continue
        icon_url = await get_icon_url(game["name"])
        query = user_owned_games.insert().values(
            user_id=user_id,
            title=game["name"],
            launchers="Steam",
            icon_url=icon_url
        )
        await database.execute(query)
        inserted += 1

    return RedirectResponse(url="/connect", status_code=302)

# Step 3: Fetch user's public games from Steam Web API
async def fetch_steam_games(steam_id: str):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": steam_id,
        "include_appinfo": True,
        "include_played_free_games": True
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json().get("response", {})
    return data.get("games", [])

# If user is already connected then use user's steam id
@router.get("/sync/steam/fetch")
async def fetch_steam_using_saved_id(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return {"error": "Not logged in"}

    row = await database.fetch_one(
        users_sessions.select().where(users_sessions.c.user_id == user_id)
    )
    steam_id = row["steam_id"] if row else None

    if not steam_id:
        return {"error": "Steam not connected"}

    game_list = await fetch_steam_games(steam_id)
    valid_titles = await sanity_check(user_id, [g["name"] for g in game_list], "Steam")

    inserted = 0
    for game in game_list:
        if game["name"] not in valid_titles:
            continue
        icon_url = await get_icon_url(game["name"])
        await database.execute(user_owned_games.insert().values(
            user_id=user_id,
            title=game["name"],
            launchers="Steam",
            icon_url=icon_url
        ))
        inserted += 1

    return RedirectResponse("/connect?steam=success")
