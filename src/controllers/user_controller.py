# src/controllers/user_controller.py
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.database import get_all_users, create_or_get_user

async def list_users(request: Request) -> JSONResponse:
    return JSONResponse({"error": "Acesso não permitido à listagem de usuários"}, status_code=403)

async def create_user(request: Request) -> JSONResponse:
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Payload JSON inválido"}, status_code=400)

    username = body.get("username", "").strip()
    name = body.get("name", "").strip() or username

    if not username:
        return JSONResponse({"error": "O campo username é obrigatório"}, status_code=400)

    user_info, created = create_or_get_user(username, name)
    status_code = 201 if created else 200
    msg = "Usuário criado com sucesso no SQLite" if created else "Usuário selecionado com sucesso"

    return JSONResponse({
        "message": msg,
        "user": user_info
    }, status_code=status_code)
