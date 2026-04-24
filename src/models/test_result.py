from sqlalchemy import Column, DateTime, ForeignKey, Integer, text

from src.core.database_sqlalchemy import Base


class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    passed_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))