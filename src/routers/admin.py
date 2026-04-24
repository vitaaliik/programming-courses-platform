from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from src.dependencies.course import (
    get_admin_service,
    get_auth_service,
    get_course_content_service,
    get_site_service,
    get_test_service,
)
from src.services.admin_service_sqlalchemy import AdminService
from src.services.auth_service_sqlalchemy import AuthService
from src.services.course_content_service_sqlalchemy import CourseContentService
from src.services.site_service_sqlalchemy import SiteService
from src.services.test_service_sqlalchemy import TestService
from typing import Annotated

from fastapi import Depends
from src.dependencies.course import get_course_content_service, get_test_service
from src.services.course_content_service_sqlalchemy import CourseContentService

from src.services.test_service_sqlalchemy import TestService
from src.utils.page_renderer import render_page

from src.dependencies.course import get_auth_service
from src.services.auth_service_sqlalchemy import AuthService

from src.core.settings import settings

router = APIRouter()


@router.get("/admin", response_class=HTMLResponse)
async def admin_page(
    request: Request,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    course_service: Annotated[
        CourseContentService,
        Depends(get_course_content_service),
    ],
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    if request.session.get("role") != "admin":
        return RedirectResponse(url="/profile", status_code=303)

    data = admin_service.get_admin_dashboard_data()
    courses = course_service.get_courses_for_admin()

    return render_page(request, "admin.html", **data, courses=courses)


@router.get("/admin/home", response_class=HTMLResponse)
async def edit_home_page(
    request: Request,
    site_service: Annotated[SiteService, Depends(get_site_service)],
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    if request.session.get("role") != "admin":
        return RedirectResponse(url="/profile", status_code=303)

    data = site_service.get_home_editor_data()
    return render_page(request, "admin_home_editor.html", **data)


@router.post("/admin/home/update-hero")
async def update_home_hero_route(
    request: Request,
    site_service: Annotated[SiteService, Depends(get_site_service)],
    hero_title: str = Form(...),
    hero_subtitle: str = Form(...),
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    site_service.update_home_hero({
        "hero_title": hero_title,
        "hero_subtitle": hero_subtitle,
    })
    return JSONResponse({"ok": True, "message": "Hero-блок оновлено."})


@router.post("/admin/home/block/add")
async def add_home_block_route(
    request: Request,
    site_service: Annotated[SiteService, Depends(get_site_service)],
    title: str = Form(...),
    content_html: str = Form(...),
    sort_order: int = Form(...),
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    ok = site_service.add_new_home_block(title, content_html, sort_order)

    if not ok:
        return JSONResponse({"ok": False, "message": "Не вдалося додати блок."})

    return JSONResponse({"ok": True, "message": "Блок додано."})


@router.post("/admin/home/block/{block_id}/update")
async def update_home_block_route(
    request: Request,
    block_id: int,
    site_service: Annotated[SiteService, Depends(get_site_service)],
    title: str = Form(...),
    content_html: str = Form(...),
    sort_order: int = Form(...),
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    ok = site_service.save_home_block(block_id, title, content_html, sort_order)

    if not ok:
        return JSONResponse({"ok": False, "message": "Не вдалося оновити блок."})

    return JSONResponse({"ok": True, "message": "Блок оновлено."})


@router.post("/admin/home/block/{block_id}/delete")
async def delete_home_block_route(
    request: Request,
    block_id: int,
    site_service: Annotated[SiteService, Depends(get_site_service)],
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    site_service.remove_home_block(block_id)
    return JSONResponse({"ok": True, "message": "Блок видалено."})


@router.post("/admin/course/create")
async def create_course_route(
    request: Request,
    course_service: Annotated[
        CourseContentService,
        Depends(get_course_content_service),
    ],
    slug: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    result = course_service.create_new_course(slug, title, description)
    return JSONResponse(result)


@router.post("/admin/course/{slug}/delete")
async def delete_course_route(
    request: Request,
    slug: str,
    course_service: Annotated[
        CourseContentService,
        Depends(get_course_content_service),
    ],
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    result = course_service.remove_course(slug)
    return JSONResponse(result)


@router.get("/admin/course/{slug}", response_class=HTMLResponse)
async def edit_course_page(
    request: Request,
    slug: str,
    course_service: Annotated[
        CourseContentService,
        Depends(get_course_content_service),
    ],
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    if request.session.get("role") != "admin":
        return RedirectResponse(url="/profile", status_code=303)

    course = course_service.get_course_editor_data(slug)

    if not course:
        return RedirectResponse(url="/admin", status_code=303)

    return render_page(
        request,
        "admin_course_editor.html",
        course=course,
        sections=course["sections"],
    )


@router.post("/admin/course/{slug}/update-main")
async def update_course_main(
    request: Request,
    slug: str,
    course_service: Annotated[
        CourseContentService,
        Depends(get_course_content_service),
    ],
    page_title: str = Form(...),
    page_subtitle: str = Form(...),
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    ok = course_service.save_course_main_info(slug, page_title, page_subtitle)

    if not ok:
        return JSONResponse({"ok": False, "message": "Курс не знайдено."})

    return JSONResponse({"ok": True, "message": "Основну інформацію курсу оновлено."})


@router.post("/admin/course/{slug}/section/add")
async def add_course_section(
    request: Request,
    slug: str,
    course_service: Annotated[
        CourseContentService,
        Depends(get_course_content_service),
    ],
    title: str = Form(...),
    content_html: str = Form(...),
    sort_order: int = Form(...),
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    ok = course_service.add_new_course_section(slug, title, content_html, sort_order)

    if not ok:
        return JSONResponse({"ok": False, "message": "Не вдалося додати секцію."})

    return JSONResponse({"ok": True, "message": "Нову секцію додано."})


@router.post("/admin/course/section/{section_id}/update")
async def update_section(
    request: Request,
    section_id: int,
    course_service: Annotated[
        CourseContentService,
        Depends(get_course_content_service),
    ],
    title: str = Form(...),
    content_html: str = Form(...),
    sort_order: int = Form(...),
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    course_service.save_course_section(section_id, title, content_html, sort_order)
    return JSONResponse({"ok": True, "message": "Секцію оновлено."})

@router.post("/admin/course/section/{section_id}/delete")
async def delete_section(
    request: Request,
    section_id: int,
    course_service: Annotated[
        CourseContentService,
        Depends(get_course_content_service),
    ],
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    course_service.remove_course_section(section_id)
    return JSONResponse({"ok": True, "message": "Секцію видалено."})

@router.get("/admin/tests/{slug}", response_class=HTMLResponse)
async def edit_test_page(
    request: Request,
    slug: str,
    test_service: Annotated[TestService, Depends(get_test_service)],
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    if request.session.get("role") != "admin":
        return RedirectResponse(url="/profile", status_code=303)

    test_data = test_service.get_test_editor_data(slug)

    if not test_data:
        return RedirectResponse(url="/admin", status_code=303)

    return render_page(
        request,
        "admin_test_editor.html",
        course_slug=slug,
        course_title=test_data["title"],
        questions=test_data["questions"],
    )


@router.post("/admin/tests/{slug}/question/add")
async def add_test_question_route(
    request: Request,
    slug: str,
    test_service: Annotated[TestService, Depends(get_test_service)],
    question: str = Form(...),
    option_a: str = Form(...),
    option_b: str = Form(...),
    option_c: str = Form(...),
    option_d: str = Form(...),
    allow_multiple: int = Form(0),
    is_a_correct: int = Form(0),
    is_b_correct: int = Form(0),
    is_c_correct: int = Form(0),
    is_d_correct: int = Form(0),
    sort_order: int = Form(...),
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    ok = test_service.add_new_test_question(
        slug,
        question,
        option_a,
        option_b,
        option_c,
        option_d,
        allow_multiple,
        is_a_correct,
        is_b_correct,
        is_c_correct,
        is_d_correct,
        sort_order,
    )

    if not ok:
        return JSONResponse({"ok": False, "message": "Не вдалося додати питання. Перевір правильні відповіді."})

    return JSONResponse({"ok": True, "message": "Питання додано."})


@router.post("/admin/tests/question/{question_id}/update")
async def update_test_question_route(
    request: Request,
    question_id: int,
    test_service: Annotated[TestService, Depends(get_test_service)],
    question: str = Form(...),
    option_a: str = Form(...),
    option_b: str = Form(...),
    option_c: str = Form(...),
    option_d: str = Form(...),
    allow_multiple: int = Form(0),
    is_a_correct: int = Form(0),
    is_b_correct: int = Form(0),
    is_c_correct: int = Form(0),
    is_d_correct: int = Form(0),
    sort_order: int = Form(...),
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    ok = test_service.save_test_question(
        question_id,
        question,
        option_a,
        option_b,
        option_c,
        option_d,
        allow_multiple,
        is_a_correct,
        is_b_correct,
        is_c_correct,
        is_d_correct,
        sort_order,
    )

    if not ok:
        return JSONResponse({"ok": False, "message": "Не вдалося оновити питання. Перевір правильні відповіді."})

    return JSONResponse({"ok": True, "message": "Питання оновлено."})


@router.post("/admin/tests/question/{question_id}/delete")
async def delete_test_question_route(
    request: Request,
    question_id: int,
    test_service: Annotated[TestService, Depends(get_test_service)],
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    test_service.remove_test_question(question_id)
    return JSONResponse({"ok": True, "message": "Питання видалено."})


@router.get("/make-admin")
async def make_admin(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    if not settings.admin_email:
        return {"message": "ADMIN_EMAIL не заданий у .env"}

    auth_service.repository.make_user_admin_by_email(settings.admin_email)
    return {"message": "Адмін оновлений через email з .env"}