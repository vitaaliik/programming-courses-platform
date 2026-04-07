import random
from datetime import datetime, timedelta

from fastapi.responses import JSONResponse

from src.core.security import hash_password, verify_password
from src.repositories.user_repository import (
    create_password_reset,
    create_user,
    delete_password_resets,
    get_password_reset,
    get_user_by_email,
    update_user_password,
)
from src.utils.email_sender import send_reset_email


def generate_reset_code() -> str:
    return str(random.randint(100000, 999999))


def register_user(request, username: str, email: str, password: str, confirm_password: str):
    username = username.strip()
    email = email.strip().lower()

    if not username or not email or not password or not confirm_password:
        return JSONResponse({"ok": False, "message": "Усі поля обов'язкові для заповнення."})

    if password != confirm_password:
        return JSONResponse({"ok": False, "message": "Паролі не співпадають."})

    if len(password) < 6:
        return JSONResponse({"ok": False, "message": "Пароль не може бути меншим за 6 символів."})

    if len(password) > 72:
        return JSONResponse({"ok": False, "message": "Пароль занадто довгий (максимум 72 символи)."})

    existing_user = get_user_by_email(email)
    if existing_user:
        return JSONResponse({"ok": False, "message": "Така пошта вже зареєстрована."})

    password_hash = hash_password(password)
    user_id = create_user(username, email, password_hash, "user")

    request.session["user_id"] = user_id
    request.session["username"] = username
    request.session["role"] = "user"

    return JSONResponse({"ok": True, "redirect": "/profile"})


def login_user(request, email: str, password: str):
    email = email.strip().lower()

    if not email or not password:
        return JSONResponse({"ok": False, "message": "Введіть пошту і пароль."})

    user = get_user_by_email(email)

    if not user:
        return JSONResponse({"ok": False, "message": "Користувача з такою поштою не знайдено."})

    if not verify_password(password, user["password_hash"]):
        return JSONResponse({"ok": False, "message": "Неправильний пароль."})

    request.session["user_id"] = user["id"]
    request.session["username"] = user["username"]
    request.session["role"] = user["role"]

    if user["role"] == "admin":
        return JSONResponse({"ok": True, "redirect": "/admin"})

    return JSONResponse({"ok": True, "redirect": "/profile"})


def forgot_password(email: str):
    email = email.strip().lower()

    if not email:
        return JSONResponse({"ok": False, "message": "Введіть пошту."})

    user = get_user_by_email(email)

    if not user:
        return JSONResponse({"ok": False, "message": "Користувача з такою поштою не знайдено."})

    code = generate_reset_code()
    expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()

    create_password_reset(email, code, expires_at)

    try:
        send_reset_email(email, code)
    except Exception as e:
        return JSONResponse({"ok": False, "message": f"Не вдалося надіслати лист: {str(e)}"})

    return JSONResponse({"ok": True, "redirect": f"/verify-code?email={email}"})


def verify_reset_code(email: str, code: str):
    email = email.strip().lower()
    code = code.strip()

    if not email or not code:
        return JSONResponse({"ok": False, "message": "Заповніть усі поля."})

    reset_row = get_password_reset(email, code)

    if not reset_row:
        return JSONResponse({"ok": False, "message": "Неправильний код."})

    expires_at = datetime.fromisoformat(reset_row["expires_at"])
    if datetime.now() > expires_at:
        return JSONResponse({"ok": False, "message": "Час дії коду минув."})

    return JSONResponse({"ok": True, "redirect": f"/reset-password?email={email}&code={code}"})


def reset_password(email: str, code: str, new_password: str, confirm_password: str):
    email = email.strip().lower()
    code = code.strip()

    if not email or not code or not new_password or not confirm_password:
        return JSONResponse({"ok": False, "message": "Усі поля обов'язкові."})

    if new_password != confirm_password:
        return JSONResponse({"ok": False, "message": "Паролі не співпадають."})

    if len(new_password) < 6:
        return JSONResponse({"ok": False, "message": "Пароль не може бути меншим за 6 символів."})

    if len(new_password) > 72:
        return JSONResponse({"ok": False, "message": "Пароль занадто довгий (максимум 72 символи)."})

    reset_row = get_password_reset(email, code)

    if not reset_row:
        return JSONResponse({"ok": False, "message": "Неправильний код."})

    expires_at = datetime.fromisoformat(reset_row["expires_at"])
    if datetime.now() > expires_at:
        return JSONResponse({"ok": False, "message": "Час дії коду минув."})

    password_hash = hash_password(new_password)

    update_user_password(email, password_hash)
    delete_password_resets(email)

    return JSONResponse({"ok": True, "redirect": "/login"})