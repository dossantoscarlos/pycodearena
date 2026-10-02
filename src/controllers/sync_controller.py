# src/controllers/sync_controller.py
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.database import process_sync_operations, get_sync_pull_data

async def sync_push(request: Request) -> JSONResponse:
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Payload JSON inválido"}, status_code=400)

    operations = body.get("operations", [])
    result = process_sync_operations(operations)
    return JSONResponse(result)

async def sync_pull(request: Request) -> JSONResponse:
    data = get_sync_pull_data()
    return JSONResponse(data)
