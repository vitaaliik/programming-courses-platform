import os

from fastapi import Request
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory=TEMPLATES_DIR)


def render_page(request: Request, template_name: str, **context):
    safe_context = {
        "username": request.session.get("username"),
        "role": request.session.get("role"),
        **context,
    }

    return templates.TemplateResponse(
        request,
        template_name,
        safe_context,
    )