from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse

from src.dependencies.course import get_course_content_service
from src.services.course_content_service_sqlalchemy import CourseContentService
from src.utils.page_renderer import render_page

router = APIRouter()


@router.get("/course/{slug}", response_class=HTMLResponse)
async def course_page(
    request: Request,
    slug: str,
    course_service: Annotated[
        CourseContentService,
        Depends(get_course_content_service),
    ],
):
    course = course_service.get_course_page_data(slug)

    if not course:
        raise HTTPException(status_code=404, detail="Курс не знайдено")

    return render_page(
        request,
        "course_dynamic.html",
        course=course,
        sections=course["sections"],
    )