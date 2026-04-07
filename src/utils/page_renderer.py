import os

from fastapi import Request
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


def render_page(request: Request, template_name: str, **context):
    base_context = {
        "request": request,
        "username": request.session.get("username"),
        "role": request.session.get("role"),
    }
    base_context.update(context)
    return templates.TemplateResponse(template_name, base_context)