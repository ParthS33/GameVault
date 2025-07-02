import asyncio
from gamevault.db.models import database, games, user_owned_games
from gamevault.api.igdb_client import query_game
from sqlalchemy import text

async def populate_missing_games():
    await database.connect()

    # Step 1: Get distinct titles with missing icon_url
    query = """
        SELECT DISTINCT title
        FROM user_owned_games
        WHERE icon_url = ''
    """
    rows = await database.fetch_all(query)
    titles = [row["title"] for row in rows]
    print(f"Found {len(titles)} games needing population\n")

    for title in titles:
        print(f"🔎 Searching IGDB for: {title}")

        try:
            # Run sync query_game() inside async context
            data = await asyncio.to_thread(query_game, title)
        except Exception as e:
            print(f"❌ Failed to query {title}: {e}\n")
            continue

        if not data:
            print(f"❌ No results for {title}\n")
            continue

        game = data[0]
        # print(game)
        # Insert into games table
        insert_query = games.insert().values(
            igdb_id=game["id"],
            title=game["name"],
            cover_url=game.get("cover", {}).get("url", ""),
            title_from_launcher=title
        )
        await database.execute(insert_query)
        print(f"✅ Inserted {title} into games table\n")

    await database.disconnect()


if __name__ == "__main__":
    asyncio.run(populate_missing_games())
