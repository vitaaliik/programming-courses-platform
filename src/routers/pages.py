from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.repositories.site_repository import get_home_blocks, get_site_content
from src.services.course_content_service import get_courses_for_page
from src.utils.page_renderer import render_page

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    site_content = get_site_content()
    home_blocks = get_home_blocks()

    return render_page(
        request,
        "index.html",
        site_content=site_content,
        home_blocks=home_blocks,
    )


@router.get("/courses", response_class=HTMLResponse)
async def courses_page(request: Request):
    courses = get_courses_for_page()
    return render_page(request, "courses.html", courses=courses)