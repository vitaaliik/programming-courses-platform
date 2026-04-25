from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.course import Course
from src.models.test_result import TestResult
from src.models.user import User


class ProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def update_username(self, user_id: int, new_username: str) -> None:
        user = self.get_user(user_id)
        if not user:
            return

        user.username = new_username
        self.db.commit()

    def get_user_results(self, user_id: int):
        rows = (
            self.db.query(
                TestResult.score,
                TestResult.total,
                TestResult.passed_at,
                Course.title,
                Course.slug,
            )
            .join(Course, TestResult.course_id == Course.id)
            .filter(TestResult.user_id == user_id)
            .order_by(TestResult.passed_at.desc())
            .all()
        )

        return [
            {
                "score": r.score,
                "total": r.total,
                "passed_at": r.passed_at,
                "title": r.title,
                "slug": r.slug,
            }
            for r in rows
        ]

    def get_total_courses(self) -> int:
        return self.db.query(func.count(Course.id)).scalar() or 0