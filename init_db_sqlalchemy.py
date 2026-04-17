from src.core.database_sqlalchemy import engine, Base
from src.models.user import User

Base.metadata.create_all(bind=engine)