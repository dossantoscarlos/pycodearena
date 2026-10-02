# src/routes/history_routes.py
from starlette.routing import Route
from src.controllers.history_controller import get_history

history_routes = [
    Route('/api/history/{user_id}', get_history, methods=['GET']),
]
