# src/routes/sync_routes.py
from starlette.routing import Route
from src.controllers.sync_controller import sync_push, sync_pull

sync_routes = [
    Route('/api/sync/push', sync_push, methods=['POST']),
    Route('/api/sync/pull', sync_pull, methods=['GET']),
]
