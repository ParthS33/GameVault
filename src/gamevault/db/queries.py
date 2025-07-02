from gamevault.db.models import database, games
from sqlalchemy import or_

async def get_user_games(user_id: int) -> list[dict]:
    """
    Fetches all games owned by the user, grouped by title, with a list of launchers.
    Uses ARRAY_AGG for efficient SQL-side grouping (PostgreSQL only).
    """
    query = """
        SELECT 
            title,
            icon_url,
            ARRAY_AGG(launchers) AS launchers
        FROM user_owned_games
        WHERE user_id = :user_id
        GROUP BY title, icon_url
    """
    rows = await database.fetch_all(query, {"user_id": user_id})

    games = []
    for row in rows:
        games.append({
            "name": row["title"],
            "icon_url": row["icon_url"],
            "launchers": row["launchers"]
        })

    return games


async def get_icon_url(title: str) -> str:
    """
    Fetch the icon_url for a given game title from the games table.
    Returns an empty string if not found.
    """
    query = games.select().where(or_(
        games.c.title == title,
        games.c.title_from_launcher == title
    ))
    row = await database.fetch_one(query)
    # print(row)
    return row["cover_url"] if row else ""