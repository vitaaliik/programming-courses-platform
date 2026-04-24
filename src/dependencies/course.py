from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database_sqlalchemy import SessionLocal
from src.repositories.course_content_repository_sqlalchemy import CourseContentRepository
from src.repositories.course_repository_sqlalchemy import CourseRepository
from src.services.course_content_service_sqlalchemy import CourseContentService
from src.services.course_service_sqlalchemy import CourseService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_course_repository(db: Session = Depends(get_db)) -> CourseRepository:
    return CourseRepository(db)


def get_course_service(
    repository: CourseRepository = Depends(get_course_repository),
) -> CourseService:
    return CourseService(repository)


def get_course_content_repository(
    db: Session = Depends(get_db),
) -> CourseContentRepository:
    return CourseContentRepository(db)


def get_course_content_service(
    repository: CourseContentRepository = Depends(get_course_content_repository),
) -> CourseContentService:
    return CourseContentService(repository)