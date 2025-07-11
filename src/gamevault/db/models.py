from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, MetaData, Date, ARRAY, TIMESTAMP
from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
database = Database(DATABASE_URL)
metadata = MetaData()

users_sessions = Table(
    "users_sessions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), unique=True),
    Column("epic_id", String, nullable=True),   # stores Epic user ID (or None)
    Column("steam_id", String, nullable=True),  # stores SteamID64
    Column("xbox_id", String, nullable=True)    # stores Xbox user ID
)

user_owned_games = Table(
    "user_owned_games",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id")),
    Column("title", String),
    Column("icon_url", String),
    Column("launchers", String)
)

from sqlalchemy import Table, Column, Integer, String, MetaData

# Add this to existing metadata
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False)
)

from sqlalchemy import Table, Column, Integer, String, Text, TIMESTAMP, UniqueConstraint
from gamevault.db.setup import metadata

non_games = Table(
    "non_games",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", Text, nullable=False),
    Column("source", Text),
    Column("reason", Text),
    Column("added_at", TIMESTAMP),
    UniqueConstraint("title", "source", name="uq_non_games_title_source")
)

games = Table(
    "games",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("igdb_id", Integer),
    Column("title", Text, nullable=False),
    Column("cover_url", Text),
    Column("title_from_launcher", Text)
)
