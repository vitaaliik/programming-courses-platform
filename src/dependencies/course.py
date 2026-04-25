from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database_sqlalchemy import SessionLocal
from src.repositories.course_content_repository import CourseContentRepository
from src.repositories.course_repository import CourseRepository
from src.services.course_content_service import CourseContentService
from src.services.course_service import CourseService

from src.repositories.test_repository import TestRepository
from src.services.test_service import TestService

from src.repositories.user_repository import UserRepository
from src.services.auth_service import AuthService

from src.repositories.admin_repository import AdminRepository
from src.repositories.site_repository import SiteRepository
from src.services.admin_service import AdminService
from src.services.site_service import SiteService

from src.repositories.profile_repository import ProfileRepository
from src.services.profile_service import ProfileService

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

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_auth_service(
    repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(repository)

def get_site_repository(db: Session = Depends(get_db)) -> SiteRepository:
    return SiteRepository(db)


def get_site_service(
    repository: SiteRepository = Depends(get_site_repository),
) -> SiteService:
    return SiteService(repository)


def get_admin_repository(db: Session = Depends(get_db)) -> AdminRepository:
    return AdminRepository(db)


def get_admin_service(
    repository: AdminRepository = Depends(get_admin_repository),
) -> AdminService:
    return AdminService(repository)

def get_profile_repository(db: Session = Depends(get_db)) -> ProfileRepository:
    return ProfileRepository(db)


def get_profile_service(
    repository: ProfileRepository = Depends(get_profile_repository),
) -> ProfileService:
    return ProfileService(repository)