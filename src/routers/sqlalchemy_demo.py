from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database_sqlalchemy import get_db_session
from src.services.course_service_sqlalchemy import get_all_courses_via_sqlalchemy

router = APIRouter()


@router.get("/debug/sqlalchemy/courses")
async def debug_sqlalchemy_courses(db: Session = Depends(get_db_session)):
    courses = get_all_courses_via_sqlalchemy(db)

    return [
        {
            "id": course.id,
            "slug": course.slug,
            "title": course.title,
        }
        for course in courses
    ]