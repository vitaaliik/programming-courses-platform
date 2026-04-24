from sqlalchemy import Column, DateTime, Integer, Text, text

from src.core.database_sqlalchemy import Base


class HomeBlock(Base):
    __tablename__ = "home_blocks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    content_html = Column(Text, nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))