from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from src.services.course_content_service import get_course_page_data
from src.utils.page_renderer import render_page

router = APIRouter()


@router.get("/course/{slug}", response_class=HTMLResponse)
async def dynamic_course_page(request: Request, slug: str):
    course = get_course_page_data(slug)

    if not course:
        raise HTTPException(status_code=404, detail="Курс не знайдено")

    return render_page(
        request,
        "course_dynamic.html",
        course=course,
        sections=course["sections"],
    )