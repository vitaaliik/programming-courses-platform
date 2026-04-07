import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from src.core.config import settings
from src.routers import admin, auth, course_content, pages, profile, tests

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(admin.router)
app.include_router(tests.router)
app.include_router(course_content.router)
app.include_router(pages.router)