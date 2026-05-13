from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, text

from src.core.database_sqlalchemy import Base


class TestQuestion(Base):
    __tablename__ = "test_questions"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    allow_multiple = Column(Integer, nullable=False, default=0)
    is_a_correct = Column(Integer, nullable=False, default=0)
    is_b_correct = Column(Integer, nullable=False, default=0)
    is_c_correct = Column(Integer, nullable=False, default=0)
    is_d_correct = Column(Integer, nullable=False, default=0)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))