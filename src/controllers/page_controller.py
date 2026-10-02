# src/controllers/page_controller.py
import logging
from starlette.requests import Request
from starlette.responses import FileResponse, RedirectResponse, Response
from starlette.templating import Jinja2Templates

from src.database import get_user_passed_count

templates = Jinja2Templates(directory='templates')

def get_session_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    passed_count = get_user_passed_count(user_id)
    return {
        "id": user_id,
        "username": request.session.get("username"),
        "name": request.session.get("name"),
        "passed_count": passed_count,
        "total_exercises": 30
    }

async def index_page(request: Request):
    session_user = get_session_user(request)
    if session_user:
        return RedirectResponse('/dashboard', status_code=302)
    return templates.TemplateResponse(request, 'login.html', {
        "is_authenticated": False,
        "session_user": None
    })


async def login_page(request: Request):
    """
    Rota '/': Aponta para a tela de Login (login.html).
    Se o usuário já estiver autenticado na sessão, redireciona para o '/dashboard'.
    """
    session_user = get_session_user(request)
    if session_user:
        return RedirectResponse('/dashboard', status_code=302)
    
    return templates.TemplateResponse(request, 'login.html', {
        "is_authenticated": False,
        "session_user": None
    })

async def dashboard_page(request: Request):
    """
    Rota '/dashboard': Aponta para a tela de Dashboard (index.html).
    Se o usuário NÃO estiver logado, redireciona para a tela de login ('/').
    """
    session_user = get_session_user(request)
    if not session_user:
        return RedirectResponse('/', status_code=302)

    return templates.TemplateResponse(request, 'index.html', {
        "is_authenticated": True,
        "session_user": session_user
    })

async def history_page(request: Request):
    session_user = get_session_user(request)
    if not session_user:
        return RedirectResponse('/', status_code=302)
    return templates.TemplateResponse(request, 'history.html', {
        "is_authenticated": True,
        "session_user": session_user
    })

async def ranking_page(request: Request):
    session_user = get_session_user(request)
    if not session_user:
        return RedirectResponse('/', status_code=302)
    return templates.TemplateResponse(request, 'ranking.html', {
        "is_authenticated": True,
        "session_user": session_user
    })
