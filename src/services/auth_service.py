import random
from datetime import datetime, timedelta

from sqlalchemy.exc import SQLAlchemyError

from src.core.exceptions import DatabaseException, NotFoundException, ValidationException
from src.core.security import hash_password, verify_password
from src.repositories.user_repository import UserRepository
from src.utils.email_sender import send_reset_email


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def generate_reset_code(self) -> str:
        return str(random.randint(100000, 999999))

    def register_user(
        self,
        request,
        username: str,
        email: str,
        password: str,
        confirm_password: str,
    ) -> dict:
        username = username.strip()
        email = email.strip().lower()

        if not username or not email or not password or not confirm_password:
            raise ValidationException("All fields are required")

        if password != confirm_password:
            raise ValidationException("Passwords do not match")

        if len(password) < 6:
            raise ValidationException("Password must be at least 6 characters")

        if len(password) > 72:
            raise ValidationException("Password is too long. Maximum length is 72 characters")

        try:
            existing_user = self.repository.get_user_by_email(email)

            if existing_user:
                raise ValidationException("This email address is already registered")

            password_hash = hash_password(password)
            user_id = self.repository.create_user(username, email, password_hash, "user")

            self.repository.db.commit()

            request.session["user_id"] = user_id
            request.session["username"] = username
            request.session["role"] = "user"

            return {"ok": True, "redirect": "/profile"}

        except ValidationException:
            self.repository.db.rollback()
            raise

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Failed to register user") from exc

    def login_user(self, request, email: str, password: str) -> dict:
        email = email.strip().lower()

        if not email or not password:
            raise ValidationException("Email and password are required")

        user = self.repository.get_user_by_email(email)

        if not user:
            raise NotFoundException("User with this email address was not found")

        if not verify_password(password, user.password_hash):
            raise ValidationException("Incorrect password")

        request.session["user_id"] = user.id
        request.session["username"] = user.username
        request.session["role"] = user.role

        if user.role == "admin":
            return {"ok": True, "redirect": "/admin"}

        return {"ok": True, "redirect": "/profile"}

    def forgot_password(self, email: str) -> dict:
        email = email.strip().lower()

        if not email:
            raise ValidationException("Email is required")

        user = self.repository.get_user_by_email(email)

        if not user:
            raise NotFoundException("User with this email address was not found")

        code = self.generate_reset_code()
        expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()

        try:
            self.repository.create_password_reset(email, code, expires_at)
            self.repository.db.commit()

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Failed to create password reset code") from exc

        try:
            send_reset_email(email, code)
        except Exception as exc:
            raise DatabaseException("Failed to send password reset email") from exc

        return {"ok": True, "redirect": f"/verify-code?email={email}"}

    def verify_reset_code(self, email: str, code: str) -> dict:
        email = email.strip().lower()
        code = code.strip()

        if not email or not code:
            raise ValidationException("Email and reset code are required")

        reset_row = self.repository.get_password_reset(email, code)

        if not reset_row:
            raise ValidationException("Incorrect reset code")

        expires_at = datetime.fromisoformat(reset_row.expires_at)

        if datetime.now() > expires_at:
            raise ValidationException("Reset code has expired")

        return {"ok": True, "redirect": f"/reset-password?email={email}&code={code}"}

    def reset_password(
        self,
        email: str,
        code: str,
        new_password: str,
        confirm_password: str,
    ) -> dict:
        email = email.strip().lower()
        code = code.strip()

        if not email or not code or not new_password or not confirm_password:
            raise ValidationException("All fields are required")

        if new_password != confirm_password:
            raise ValidationException("Passwords do not match")

        if len(new_password) < 6:
            raise ValidationException("Password must be at least 6 characters")

        if len(new_password) > 72:
            raise ValidationException("Password is too long. Maximum length is 72 characters")

        reset_row = self.repository.get_password_reset(email, code)

        if not reset_row:
            raise ValidationException("Incorrect reset code")

        expires_at = datetime.fromisoformat(reset_row.expires_at)

        if datetime.now() > expires_at:
            raise ValidationException("Reset code has expired")

        try:
            password_hash = hash_password(new_password)

            self.repository.update_user_password(email, password_hash)
            self.repository.delete_password_resets(email)
            self.repository.db.commit()

            return {"ok": True, "redirect": "/login"}

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Failed to reset password") from exc

    def make_user_admin_by_email(self, email: str) -> bool:
        try:
            self.repository.make_user_admin_by_email(email)
            self.repository.db.commit()
            return True

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Failed to update user role") from exc