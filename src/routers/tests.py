from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse

from src.dependencies.course import get_test_service
from src.services.test_service_sqlalchemy import TestService
from src.utils.page_renderer import render_page

router = APIRouter()


@router.get("/test/{course_name}", response_class=HTMLResponse)
async def show_test(
    request: Request,
    course_name: str,
    test_service: Annotated[TestService, Depends(get_test_service)],
):
    course = test_service.get_test_by_course_name(course_name)

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
async def submit_test(
    request: Request,
    course_name: str,
    test_service: Annotated[TestService, Depends(get_test_service)],
):
    course = test_service.get_test_by_course_name(course_name)

    if not course:
        raise HTTPException(status_code=404, detail="Тест для цього курсу не знайдено")

    form = await request.form()
    score, total, detailed_results = test_service.calculate_test_result(
        form,
        course["questions"],
    )

    user_id = request.session.get("user_id")
    test_service.save_result_if_logged_in(user_id, course_name, score, total)

    return render_page(
        request,
        "result.html",
        course_name=course_name,
        course_title=course["title"],
        score=score,
        total=total,
        details=detailed_results,
    )