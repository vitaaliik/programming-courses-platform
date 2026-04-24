from typing import Annotated

from fastapi import APIRouter, Depends

from src.dependencies.course import get_course_service
from src.schemas.course import CourseRead
from src.services.course_service_sqlalchemy import CourseService

router = APIRouter(prefix="/debug/sqlalchemy", tags=["sqlalchemy-demo"])


@router.get("/courses", response_model=list[CourseRead])
async def debug_sqlalchemy_courses(
    course_service: Annotated[CourseService, Depends(get_course_service)],
):
    return course_service.get_all_courses()