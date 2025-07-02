from fastapi import APIRouter, Form, HTTPException, status
from gamevault.db.models import database, users
from gamevault.auth.security import hash_password, verify_password
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
import os

# Load templates directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter()


# ===== FORM HANDLERS =====
@router.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    query = users.select().where(users.c.username == username)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed = hash_password(password)
    query = users.insert().values(username=username, hashed_password=hashed)
    await database.execute(query)
    return RedirectResponse(url="/login?success=1", status_code=303)


@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...), request: Request = None):
    query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    request.session["user_id"] = user["id"]
    request.session["username"] = user["username"]

    return RedirectResponse(url="/", status_code=303)


# ===== FORM VIEWS =====
print("✅ Login route registered")
@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, success: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "success": success})

@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
