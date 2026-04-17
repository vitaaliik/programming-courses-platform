from src.core.database_sqlalchemy import Base, engine
from src.models import Course, User  # noqa: F401


def init_sqlalchemy_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_sqlalchemy_tables()
    print("SQLAlchemy tables checked/created successfully.")