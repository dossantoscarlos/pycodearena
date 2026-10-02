# src/routes/auth_routes.py
from starlette.routing import Route
from src.controllers.auth_controller import (
    auth_register,
    auth_login,
    auth_logout,
    auth_recover
)

auth_routes = [
    Route('/api/auth/register', auth_register, methods=['POST']),
    Route('/api/auth/login', auth_login, methods=['POST']),
    Route('/api/auth/logout', auth_logout, methods=['POST']),
    Route('/api/auth/recover', auth_recover, methods=['POST']),
]
