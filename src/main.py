import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from src.core.exceptions import AppException
from src.core.settings import settings
from src.routers import admin, auth, course_content, pages, profile, tests

app = FastAPI()


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "ok": False,
            "message": exc.message,
        },
    )


app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret_key,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(admin.router)
app.include_router(tests.router)
app.include_router(course_content.router)
app.include_router(pages.router)