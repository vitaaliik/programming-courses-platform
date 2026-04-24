from sqlalchemy.orm import Session

from src.models.password_reset import PasswordReset
from src.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(
        self,
        username: str,
        email: str,
        password_hash: str,
        role: str = "user",
    ) -> int:
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user.id

    def create_password_reset(self, email: str, code: str, expires_at: str) -> None:
        self.db.query(PasswordReset).filter(PasswordReset.email == email).delete()

        password_reset = PasswordReset(
            email=email,
            reset_code=code,
            expires_at=expires_at,
        )

        self.db.add(password_reset)
        self.db.commit()

    def get_password_reset(self, email: str, code: str) -> PasswordReset | None:
        return (
            self.db.query(PasswordReset)
            .filter(
                PasswordReset.email == email,
                PasswordReset.reset_code == code,
            )
            .order_by(PasswordReset.id.desc())
            .first()
        )

    def delete_password_resets(self, email: str) -> None:
        self.db.query(PasswordReset).filter(PasswordReset.email == email).delete()
        self.db.commit()

    def update_user_password(self, email: str, password_hash: str) -> None:
        user = self.get_user_by_email(email)

        if not user:
            return

        user.password_hash = password_hash
        self.db.commit()

    def make_user_admin_by_email(self, email: str) -> None:
        user = self.get_user_by_email(email)

        if not user:
            return

        user.role = "admin"
        self.db.commit()