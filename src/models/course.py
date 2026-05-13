from sqlalchemy import Column, DateTime, Integer, String, Text, text

from src.core.database_sqlalchemy import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, nullable=False, unique=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    content_file = Column(String)
    page_title = Column(Text)
    page_subtitle = Column(Text)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))