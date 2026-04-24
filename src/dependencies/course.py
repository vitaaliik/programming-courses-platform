from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database_sqlalchemy import SessionLocal
from src.repositories.course_content_repository_sqlalchemy import CourseContentRepository
from src.repositories.course_repository_sqlalchemy import CourseRepository
from src.services.course_content_service_sqlalchemy import CourseContentService
from src.services.course_service_sqlalchemy import CourseService

from src.repositories.test_repository_sqlalchemy import TestRepository
from src.services.test_service_sqlalchemy import TestService

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

def get_test_repository(db: Session = Depends(get_db)) -> TestRepository:
    return TestRepository(db)


def get_test_service(
    repository: TestRepository = Depends(get_test_repository),
) -> TestService:
    return TestService(repository)