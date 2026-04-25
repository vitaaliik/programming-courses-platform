from sqlalchemy.orm import Session

from src.models.course import Course


class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Course]:
        return self.db.query(Course).order_by(Course.title.asc()).all()

    def get_by_slug(self, slug: str) -> Course | None:
        return self.db.query(Course).filter(Course.slug == slug).first()