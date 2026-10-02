# src/controllers/ranking_controller.py
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.database import get_leaderboard

async def list_ranking(request: Request) -> JSONResponse:
    leaderboard = get_leaderboard()
    return JSONResponse(leaderboard)
