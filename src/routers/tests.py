from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from src.services.test_service import (
    calculate_test_result,
    get_test_by_course_name,
    save_result_if_logged_in,
)
from src.utils.page_renderer import render_page
from src.utils.page_renderer import templates

router = APIRouter()


@router.get("/test/{course_name}", response_class=HTMLResponse)
async def show_test(request: Request, course_name: str):
    course = get_test_by_course_name(course_name)

    if not course:
        raise HTTPException(status_code=404, detail="Тест для цього курсу не знайдено")

    return render_page(
        request,
        "test.html",
        course_name=course_name,
        course_title=course["title"],
        questions=course["questions"],
    )


@router.post("/test/{course_name}", response_class=HTMLResponse)
async def submit_test(request: Request, course_name: str):
    course = get_test_by_course_name(course_name)

    if not course:
        raise HTTPException(status_code=404, detail="Тест для цього курсу не знайдено")

    form = await request.form()
    score, total, detailed_results = calculate_test_result(form, course["questions"])

    user_id = request.session.get("user_id")
    save_result_if_logged_in(user_id, course_name, score, total)

    return templates.TemplateResponse(
    request,
    "result.html",
    {
        "username": request.session.get("username"),
        "role": request.session.get("role"),
        "course_name": course_name,
        "course_title": course["title"],
        "score": score,
        "total": total,
        "details": detailed_results,
    },
    )