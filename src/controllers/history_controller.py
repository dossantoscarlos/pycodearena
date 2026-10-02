# src/controllers/history_controller.py
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.database import get_user_history

async def get_history(request: Request) -> JSONResponse:
    user_id = request.session.get("user_id") or request.path_params.get("user_id")
    if not user_id:
        return JSONResponse({"error": "Não autorizado. Faça login primeiro no servidor."}, status_code=401)
    history = get_user_history(user_id)
    return JSONResponse(history)
