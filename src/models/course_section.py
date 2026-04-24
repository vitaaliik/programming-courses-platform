from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, text

from src.core.database_sqlalchemy import Base


class CourseSection(Base):
    __tablename__ = "course_sections"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title = Column(Text, nullable=False)
    content_html = Column(Text, nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))