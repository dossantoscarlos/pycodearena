# src/controllers/auth_controller.py
import logging
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.database import (
    register_user_db,
    authenticate_user_db,
    recover_password_db
)

logger = logging.getLogger("auth")

async def auth_register(request: Request) -> JSONResponse:
    try:
        body = await request.json()
    except Exception:
        logger.warning("[AUTH REGISTER] Request de cadastro com payload JSON inválido.")
        return JSONResponse({"error": "Payload JSON inválido"}, status_code=400)

    username = body.get("username", "")
    name = body.get("name", "")
    email = body.get("email", "")
    password = body.get("password", "")

    logger.info(f"[AUTH REGISTER] Request de cadastro recebida para username: '{username}'")

    user, err = register_user_db(username, name, email, password)
    if err:
        logger.warning(f"[AUTH REGISTER FAILED] Falha no cadastro de '{username}': {err}")
        return JSONResponse({"error": err}, status_code=400)

    logger.info(f"[AUTH REGISTER SUCCESS] Usuário '{username}' cadastrado com sucesso.")
    return JSONResponse({"message": "Usuário cadastrado com sucesso!", "user": user}, status_code=201)

async def auth_login(request: Request) -> JSONResponse:
    try:
        body = await request.json()
    except Exception:
        logger.warning("[AUTH LOGIN] Request de login recebida com payload JSON inválido.")
        return JSONResponse({"error": "Payload JSON inválido"}, status_code=400)

    username = body.get("username", "")
    password = body.get("password", "")

    logger.info(f"[AUTH LOGIN] Request de login recebida para o usuário: '{username}'")

    user, err = authenticate_user_db(username, password)
    if err:
        logger.warning(f"[AUTH LOGIN FAILED] Login FALHOU para usuário '{username}': {err}")
        return JSONResponse({"error": err}, status_code=401)

    request.session["user_id"] = user["id"]
    request.session["username"] = user["username"]
    request.session["name"] = user["name"]

    logger.info(f"[AUTH LOGIN SUCCESS] Login efetuado com SUCESSO para usuário '{username}' (ID: {user['id']})")
    return JSONResponse({"message": "Login efetuado com sucesso!", "user": user})

async def auth_logout(request: Request) -> JSONResponse:
    request.session.clear()
    return JSONResponse({"message": "Sessão destruída no servidor."})

async def auth_recover(request: Request) -> JSONResponse:
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Payload JSON inválido"}, status_code=400)

    username = body.get("username", "")
    info, err = recover_password_db(username)
    if err:
        return JSONResponse({"error": err}, status_code=404)
    return JSONResponse(info)
