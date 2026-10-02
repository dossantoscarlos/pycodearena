# src/routes/user_routes.py
from starlette.routing import Route
from src.controllers.user_controller import list_users, create_user

user_routes = [
    Route('/api/users', list_users, methods=['GET']),
    Route('/api/users', create_user, methods=['POST']),
]
