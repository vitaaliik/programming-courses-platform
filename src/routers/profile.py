from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from src.dependencies.course import get_profile_service
from src.services.profile_service import ProfileService
from src.utils.page_renderer import render_page

router = APIRouter()


@router.get("/profile", response_class=HTMLResponse)
async def profile_page(
    request: Request,
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    profile_data = profile_service.get_profile_data(user_id)

    if not profile_data:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)

    return render_page(request, "profile.html", **profile_data)


@router.post("/profile/update-username")
async def update_username(
    request: Request,
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
    new_username: str = Form(...),
):
    user_id = request.session.get("user_id")

    if not user_id:
        return JSONResponse({"ok": False, "message": "Спочатку увійдіть у систему."})

    new_username = new_username.strip()

    if not new_username:
        return JSONResponse({"ok": False, "message": "Нікнейм не може бути порожнім."})

    if len(new_username) < 2:
        return JSONResponse({"ok": False, "message": "Нікнейм має містити щонайменше 2 символи."})

    if len(new_username) > 30:
        return JSONResponse({"ok": False, "message": "Нікнейм занадто довгий (максимум 30 символів)."})

    profile_service.update_username(user_id, new_username)

    request.session["username"] = new_username

    return JSONResponse({"ok": True, "message": "Нікнейм успішно оновлено."})