from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from src.services.admin_service import (
    get_admin_dashboard_data,
    make_user_admin_by_email,
    update_home_page_content,
)
from src.services.course_content_service import (
    add_new_course_section,
    get_course_editor_data,
    get_courses_for_admin,
    remove_course_section,
    save_course_main_info,
    save_course_section,
)
from src.utils.page_renderer import render_page

router = APIRouter()


@router.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    if request.session.get("role") != "admin":
        return RedirectResponse(url="/profile", status_code=303)

    data = get_admin_dashboard_data()
    courses = get_courses_for_admin()

    return render_page(request, "admin.html", **data, courses=courses)


@router.post("/admin/update-home")
async def update_home_content(
    request: Request,
    hero_title: str = Form(...),
    hero_subtitle: str = Form(...),
    about_title: str = Form(...),
    about_text_1: str = Form(...),
    about_text_2: str = Form(...),
    audience_title: str = Form(...),
    audience_item_1: str = Form(...),
    audience_item_2: str = Form(...),
    audience_item_3: str = Form(...),
    audience_item_4: str = Form(...),
    features_title: str = Form(...),
    features_item_1: str = Form(...),
    features_item_2: str = Form(...),
    features_item_3: str = Form(...),
    features_item_4: str = Form(...),
    features_item_5: str = Form(...),
    college_title: str = Form(...),
    college_text_1: str = Form(...),
    college_text_2: str = Form(...),
    creator_title: str = Form(...),
    creator_text: str = Form(...),
    skills_title: str = Form(...),
    skills_text_1: str = Form(...),
    skills_text_2: str = Form(...),
    importance_title: str = Form(...),
    importance_text_1: str = Form(...),
    importance_text_2: str = Form(...),
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    data = {
        "hero_title": hero_title,
        "hero_subtitle": hero_subtitle,
        "about_title": about_title,
        "about_text_1": about_text_1,
        "about_text_2": about_text_2,
        "audience_title": audience_title,
        "audience_item_1": audience_item_1,
        "audience_item_2": audience_item_2,
        "audience_item_3": audience_item_3,
        "audience_item_4": audience_item_4,
        "features_title": features_title,
        "features_item_1": features_item_1,
        "features_item_2": features_item_2,
        "features_item_3": features_item_3,
        "features_item_4": features_item_4,
        "features_item_5": features_item_5,
        "college_title": college_title,
        "college_text_1": college_text_1,
        "college_text_2": college_text_2,
        "creator_title": creator_title,
        "creator_text": creator_text,
        "skills_title": skills_title,
        "skills_text_1": skills_text_1,
        "skills_text_2": skills_text_2,
        "importance_title": importance_title,
        "importance_text_1": importance_text_1,
        "importance_text_2": importance_text_2,
    }

    update_home_page_content(data)
    return JSONResponse({"ok": True, "message": "Головну сторінку успішно оновлено."})


@router.get("/admin/course/{slug}", response_class=HTMLResponse)
async def edit_course_page(request: Request, slug: str):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    if request.session.get("role") != "admin":
        return RedirectResponse(url="/profile", status_code=303)

    course = get_course_editor_data(slug)
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
    page_title: str = Form(...),
    page_subtitle: str = Form(...),
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    ok = save_course_main_info(slug, page_title, page_subtitle)
    if not ok:
        return JSONResponse({"ok": False, "message": "Курс не знайдено."})

    return JSONResponse({"ok": True, "message": "Основну інформацію курсу оновлено."})


@router.post("/admin/course/{slug}/section/add")
async def add_course_section(
    request: Request,
    slug: str,
    title: str = Form(...),
    content_html: str = Form(...),
    sort_order: int = Form(...),
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    ok = add_new_course_section(slug, title, content_html, sort_order)
    if not ok:
        return JSONResponse({"ok": False, "message": "Не вдалося додати секцію."})

    return JSONResponse({"ok": True, "message": "Нову секцію додано."})


@router.post("/admin/course/section/{section_id}/update")
async def update_section(
    request: Request,
    section_id: int,
    title: str = Form(...),
    content_html: str = Form(...),
    sort_order: int = Form(...),
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    save_course_section(section_id, title, content_html, sort_order)
    return JSONResponse({"ok": True, "message": "Секцію оновлено."})


@router.post("/admin/course/section/{section_id}/delete")
async def delete_section(request: Request, section_id: int):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    remove_course_section(section_id)
    return JSONResponse({"ok": True, "message": "Секцію видалено."})


@router.get("/make-admin")
async def make_admin():
    make_user_admin_by_email("vitaliklutchak12@gmail.com")
    return {"message": "Ти тепер адмін 😎"}