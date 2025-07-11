from gamevault.db.models import database
from sqlalchemy import text


async def sanity_check(user_id: int, titles: list[str], launchers: str) -> list[str]:
    """
    Scalable and clean version:
    - Uses temp table for filtering
    - Safely escapes titles
    - Excludes non-games and owned games
    """
    if not titles:
        return []

    async with database.transaction():

        # Step 0: Drop table if already present
        await database.execute("""
            DROP TABLE IF EXISTS temp_titles
        """)
        # Step 1: Create temp table
        await database.execute(text("""
            CREATE TEMP TABLE temp_titles(title TEXT)
        """))

        # Step 2: Bulk insert titles with clean escaping
        insert_query = "INSERT INTO temp_titles(title) VALUES (:title)"
        await database.execute_many(insert_query, [{"title": t} for t in titles])

        # Step 2.5: Insert Packs into non_games
        await database.execute("""
                    INSERT INTO non_games(title, source, reason)
                    SELECT title, :launchers, 'Pack'
                    FROM temp_titles
                    WHERE title ILIKE '%Combo Pack' OR title ILIKE '%Starter Pack'
                    ON CONFLICT (title, source) DO NOTHING
                """, {"launchers": launchers})

        # Step 3: Select only valid games
        query = """
            SELECT temp_titles.title
            FROM temp_titles
            LEFT JOIN non_games ON temp_titles.title = non_games.title
            LEFT JOIN user_owned_games ON temp_titles.title = user_owned_games.title
                                        AND user_owned_games.user_id = :user_id
                                        AND user_owned_games.launchers = :launchers
            WHERE non_games.title IS NULL
              AND user_owned_games.title IS NULL
        """

        rows = await database.fetch_all(query, {"user_id": user_id, "launchers": launchers})

    return [row["title"] for row in rows]
