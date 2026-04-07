from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from src.repositories.site_repository import get_site_content
from src.utils.page_renderer import render_page

router = APIRouter()

PAGES = {
    "cpp": "cpp.html",
    "csharp": "csharp.html",
    "delphi": "delphi.html",
    "python": "python.html",
    "java": "java.html",
    "javascript": "javascript.html",
    "htmlcss": "htmlcss.html",
    "php": "php.html",
    "sql": "sql.html",
}


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    site_content = get_site_content()
    return render_page(request, "index.html", site_content=site_content)


@router.get("/courses", response_class=HTMLResponse)
async def courses_page(request: Request):
    return render_page(request, "courses.html")


@router.get("/{page}", response_class=HTMLResponse)
async def render_lang_page(page: str, request: Request):
    template = PAGES.get(page)

    if not template:
        raise HTTPException(status_code=404, detail="Сторінку не знайдено")

    return render_page(request, template)