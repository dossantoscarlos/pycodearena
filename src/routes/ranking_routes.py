# src/routes/ranking_routes.py
from starlette.routing import Route
from src.controllers.ranking_controller import list_ranking

ranking_routes = [
    Route('/api/ranking', list_ranking, methods=['GET']),
]
