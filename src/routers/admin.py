from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from src.services.admin_service import (
    get_admin_dashboard_data,
    make_user_admin_by_email,
    update_home_page_content,
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
    return render_page(request, "admin.html", **data)


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


@router.get("/make-admin")
async def make_admin():
    make_user_admin_by_email("vitaliklutchak12@gmail.com")
    return {"message": "Ти тепер адмін 😎"}