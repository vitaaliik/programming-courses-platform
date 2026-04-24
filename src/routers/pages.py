from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from src.dependencies.course import get_course_content_service, get_site_service
from src.services.course_content_service_sqlalchemy import CourseContentService
from src.services.site_service_sqlalchemy import SiteService
from src.utils.page_renderer import render_page

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    site_service: Annotated[SiteService, Depends(get_site_service)],
):
    site_content = site_service.get_site_content()
    home_blocks = site_service.get_home_blocks()

    return render_page(
        request,
        "index.html",
        site_content=site_content,
        home_blocks=home_blocks,
    )


@router.get("/courses", response_class=HTMLResponse)
async def courses_page(
    request: Request,
    course_service: Annotated[
        CourseContentService,
        Depends(get_course_content_service),
    ],
):
    courses = course_service.get_courses_for_page()
    return render_page(request, "courses.html", courses=courses)