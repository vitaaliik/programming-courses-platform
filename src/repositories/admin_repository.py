from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from src.models.course import Course
from src.models.test_result import TestResult
from src.models.user import User

from src.schemas.admin import AdminUserStatisticsDTO, RecentTestResultDTO

class AdminRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_total_users(self) -> int:
        return self.db.query(func.count(User.id)).scalar() or 0

    def get_total_courses(self) -> int:
        return self.db.query(func.count(Course.id)).scalar() or 0

    def get_total_results(self) -> int:
        return self.db.query(func.count(TestResult.id)).scalar() or 0

    def get_users_statistics(self) -> list[AdminUserStatisticsDTO]:
        rows = (
            self.db.query(
                User.id,
                User.username,
                User.email,
                User.role,
                User.created_at,
                func.count(TestResult.id).label("tests_passed"),
                func.coalesce(
                    func.round(func.avg((TestResult.score * 100.0) / TestResult.total), 1),
                    0,
                ).label("avg_result"),
                func.count(func.distinct(TestResult.course_id)).label("completed_courses"),
                func.max(TestResult.passed_at).label("last_activity"),
            )
            .outerjoin(TestResult, User.id == TestResult.user_id)
            .group_by(User.id)
            .order_by(desc(User.created_at))
            .all()
        )

        return [
            AdminUserStatisticsDTO(
               id=row.id,
               username=row.username,
               email=row.email,
               role=row.role,
               created_at=row.created_at,
               tests_passed=row.tests_passed,
               avg_result=row.avg_result,
               completed_courses=row.completed_courses,
               last_activity=row.last_activity,
            )
            for row in rows
        ]

    def get_recent_results(self) -> list[RecentTestResultDTO]:
        rows = (
            self.db.query(
               User.username,
               User.email,
               Course.title.label("course_title"),
               TestResult.score,
               TestResult.total,
               TestResult.passed_at,
            )
            .join(User, TestResult.user_id == User.id)
            .join(Course, TestResult.course_id == Course.id)
            .order_by(desc(TestResult.passed_at))
            .limit(12)
            .all()
        )

        return [
            RecentTestResultDTO(
               username=row.username,
               email=row.email,
               course_title=row.course_title,
               score=row.score,
               total=row.total,
               passed_at=row.passed_at,
            )
            for row in rows
        ]