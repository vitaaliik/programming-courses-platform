from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.services.auth_service import (
    forgot_password,
    login_user,
    register_user,
    reset_password,
    verify_reset_code,
)
from src.utils.page_renderer import render_page

router = APIRouter()


@router.get("/auth", response_class=HTMLResponse)
async def auth_page(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse(url="/profile", status_code=303)
    return render_page(request, "auth.html")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse(url="/profile", status_code=303)
    return render_page(request, "login.html")


@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    return register_user(request, username, email, password, confirm_password)


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    return login_user(request, email, password)


@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return render_page(request, "forgot_password.html")


@router.post("/forgot-password")
async def forgot_password_post(email: str = Form(...)):
    return forgot_password(email)


@router.get("/verify-code", response_class=HTMLResponse)
async def verify_code_page(request: Request, email: str = ""):
    return render_page(request, "verify_code.html", reset_email=email)


@router.post("/verify-code")
async def verify_code_post(
    email: str = Form(...),
    code: str = Form(...),
):
    return verify_reset_code(email, code)


@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request, email: str = "", code: str = ""):
    return render_page(request, "reset_password.html", reset_email=email, reset_code=code)


@router.post("/reset-password")
async def reset_password_post(
    email: str = Form(...),
    code: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
):
    return reset_password(email, code, new_password, confirm_password)


@router.get("/logout")
async def logout_user(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)