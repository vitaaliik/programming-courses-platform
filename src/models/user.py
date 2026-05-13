from sqlalchemy import Column, DateTime, Integer, String, text

from src.core.database_sqlalchemy import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))