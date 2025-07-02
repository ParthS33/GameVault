from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from gamevault.db.models import database
from contextlib import asynccontextmanager
from gamevault.auth.routes import router as auth_router
from starlette.middleware.sessions import SessionMiddleware
from gamevault.sync.epic import router as epic_router
from gamevault.db.queries import get_user_games

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()
app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="your-super-secret-key")
app.include_router(auth_router)
app.include_router(epic_router)
print("✅ Auth routes loaded")
print("✅ Epic routes loaded")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only, restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up paths for templates and static files
BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")



# Homepage route (Game library)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = request.session.get("username")
    user_id = request.session.get("user_id")
    print("User deetss",user, user_id)

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    games = await get_user_games(user_id)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "games": games,
        "user": user,
        "user_id": user_id
    })

# Connect page route
@app.get("/connect", response_class=HTMLResponse)
async def connect(request: Request):
    return templates.TemplateResponse("connect.html", {
        "request": request
    })

# Sync launcher handler (stub for now)
# @app.post("/sync/{platform}")
# async def sync_platform(platform: str):
#     # In the future, call sync_epic(), sync_steam(), etc.
#     print(platform)
#     return {"status": f"Initiated sync for {platform}"}

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)