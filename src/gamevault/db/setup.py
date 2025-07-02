from sqlalchemy import create_engine
from gamevault.db.models import metadata, DATABASE_URL

engine = create_engine(DATABASE_URL.replace("+asyncpg", ""))
metadata.create_all(engine)

print("✅ Tables created successfully.")
