from sqlalchemy.orm import Session

from src.models.course import Course


def get_all_courses_sa(db: Session):
    return db.query(Course).order_by(Course.title.asc()).all()


def get_course_by_slug_sa(db: Session, slug: str):
    return db.query(Course).filter(Course.slug == slug).first()