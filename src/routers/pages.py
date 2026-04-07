from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.repositories.site_repository import get_site_content
from src.utils.page_renderer import render_page

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    site_content = get_site_content()
    return render_page(request, "index.html", site_content=site_content)


@router.get("/courses", response_class=HTMLResponse)
async def courses_page(request: Request):
    return render_page(request, "courses.html")