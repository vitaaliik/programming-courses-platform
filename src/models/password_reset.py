from sqlalchemy import Column, DateTime, Integer, String, text

from src.core.database_sqlalchemy import Base


class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    reset_code = Column(String, nullable=False)
    expires_at = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))