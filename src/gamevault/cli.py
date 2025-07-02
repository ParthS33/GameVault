# src/gamevault/cli.py

import json
import time
from pprint import pprint
from gamevault.api.igdb_client import query_game
from pathlib import Path

def print_game_info(game_data):
    if not game_data:
        print("No game found.")
        return

    game = game_data[0]
    print(f"\n🎮 Title: {game.get('name')}")
    print(f"🆔 Slug: {game.get('slug')}")
    print(f"📅 Release Date: {game.get('first_release_date')}")
    print(f"📝 Summary: {game.get('summary', '')[:300]}...")
    genres = [g['name'] for g in game.get('genres', [])]
    print(f"🎭 Genres: {', '.join(genres)}")
    platforms = [p['name'] for p in game.get('platforms', [])]
    print(f"🕹️ Platforms: {', '.join(platforms)}")
    cover = game.get('cover', {}).get('url')
    print(f"🖼️ Cover URL: https:{cover}" if cover else "🖼️ No cover")

def load_game_titles(filename):
    project_root = Path(__file__).resolve().parents[2]
    filepath = project_root / filename
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def run_single():
    game_name = input("Enter game name to search IGDB: ")
    result = query_game(game_name)
    pprint(result)

def run_bulk():
    titles = load_game_titles("epic_owned_games.json")
    for title in titles:
        print(f"\n🔎 Searching IGDB for: {title}")
        try:
            data = query_game(title)
            print_game_info(data)
            time.sleep(0.5)  # Avoid hammering IGDB too fast
        except Exception as e:
            print(f"❌ Failed to fetch '{title}': {e}")

def main():
    run_bulk()

if __name__ == "__main__":
    main()
