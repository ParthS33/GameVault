from fastapi import APIRouter, Request
from gamevault.db.models import user_owned_games, database
from gamevault.sync.sanity import sanity_check
from gamevault.db.queries import get_icon_url
router = APIRouter()

@router.post("/epic/extension-sync")
async def epic_extension_sync(request: Request):
    """
    Endpoint for extension to sync Epic purchases.
    - Filters duplicates and non-games using sanity_check
    - Inserts only valid games
    """
    data = await request.json()
    games = data.get("games", [])

    user_id = request.session.get("user_id")
    if not user_id:
        return {"error": "Not logged in"}

    if not games:
        return {"status": "success", "inserted": 0, "message": "No games provided"}

    valid_games = await sanity_check(user_id, games, "Epic")

    inserted_count = 0
    for title in valid_games:
        icon_url = await get_icon_url(title)
        # print(title, icon_url)
        query = user_owned_games.insert().values(
            user_id=user_id,
            title=title,
            launchers="Epic",
            icon_url=icon_url
        )
        await database.execute(query)
        inserted_count += 1

    return {
        "status": "success",
        "inserted": inserted_count,
        "skipped": len(games) - inserted_count
    }
