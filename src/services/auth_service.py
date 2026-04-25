import random
from datetime import datetime, timedelta

from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from src.core.security import hash_password, verify_password
from src.repositories.user_repository import UserRepository
from src.utils.email_sender import send_reset_email


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def generate_reset_code(self) -> str:
        return str(random.randint(100000, 999999))

    def register_user(self, request, username: str, email: str, password: str, confirm_password: str):
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

        try:
            existing_user = self.repository.get_user_by_email(email)
            if existing_user:
                return JSONResponse({"ok": False, "message": "Така пошта вже зареєстрована."})

            password_hash = hash_password(password)
            user_id = self.repository.create_user(username, email, password_hash, "user")

            self.repository.db.commit()

            request.session["user_id"] = user_id
            request.session["username"] = username
            request.session["role"] = "user"

            return JSONResponse({"ok": True, "redirect": "/profile"})
        except SQLAlchemyError:
            self.repository.db.rollback()
            return JSONResponse({"ok": False, "message": "Помилка бази даних. Реєстрацію не виконано."})

    def login_user(self, request, email: str, password: str):
        email = email.strip().lower()

        if not email or not password:
            return JSONResponse({"ok": False, "message": "Введіть пошту і пароль."})

        user = self.repository.get_user_by_email(email)

        if not user:
            return JSONResponse({"ok": False, "message": "Користувача з такою поштою не знайдено."})

        if not verify_password(password, user.password_hash):
            return JSONResponse({"ok": False, "message": "Неправильний пароль."})

        request.session["user_id"] = user.id
        request.session["username"] = user.username
        request.session["role"] = user.role

        if user.role == "admin":
            return JSONResponse({"ok": True, "redirect": "/admin"})

        return JSONResponse({"ok": True, "redirect": "/profile"})

    def forgot_password(self, email: str):
        email = email.strip().lower()

        if not email:
            return JSONResponse({"ok": False, "message": "Введіть пошту."})

        user = self.repository.get_user_by_email(email)

        if not user:
            return JSONResponse({"ok": False, "message": "Користувача з такою поштою не знайдено."})

        code = self.generate_reset_code()
        expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()

        try:
            self.repository.create_password_reset(email, code, expires_at)
            self.repository.db.commit()
        except SQLAlchemyError:
            self.repository.db.rollback()
            return JSONResponse({"ok": False, "message": "Помилка бази даних. Код не створено."})

        try:
            send_reset_email(email, code)
        except Exception as e:
            return JSONResponse({"ok": False, "message": f"Не вдалося надіслати лист: {str(e)}"})

        return JSONResponse({"ok": True, "redirect": f"/verify-code?email={email}"})

    def verify_reset_code(self, email: str, code: str):
        email = email.strip().lower()
        code = code.strip()

        if not email or not code:
            return JSONResponse({"ok": False, "message": "Заповніть усі поля."})

        reset_row = self.repository.get_password_reset(email, code)

        if not reset_row:
            return JSONResponse({"ok": False, "message": "Неправильний код."})

        expires_at = datetime.fromisoformat(reset_row.expires_at)

        if datetime.now() > expires_at:
            return JSONResponse({"ok": False, "message": "Час дії коду минув."})

        return JSONResponse({"ok": True, "redirect": f"/reset-password?email={email}&code={code}"})

    def reset_password(self, email: str, code: str, new_password: str, confirm_password: str):
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

        reset_row = self.repository.get_password_reset(email, code)

        if not reset_row:
            return JSONResponse({"ok": False, "message": "Неправильний код."})

        expires_at = datetime.fromisoformat(reset_row.expires_at)

        if datetime.now() > expires_at:
            return JSONResponse({"ok": False, "message": "Час дії коду минув."})

        try:
            password_hash = hash_password(new_password)
            self.repository.update_user_password(email, password_hash)
            self.repository.delete_password_resets(email)
            self.repository.db.commit()

            return JSONResponse({"ok": True, "redirect": "/login"})
        except SQLAlchemyError:
            self.repository.db.rollback()
            return JSONResponse({"ok": False, "message": "Помилка бази даних. Пароль не змінено."})

    def make_user_admin_by_email(self, email: str):
        try:
            self.repository.make_user_admin_by_email(email)
            self.repository.db.commit()
            return True
        except SQLAlchemyError:
            self.repository.db.rollback()
            return False