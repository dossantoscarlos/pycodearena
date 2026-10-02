# src/routes/page_routes.py
from starlette.routing import Route
from src.controllers.page_controller import (
    index_page,
    login_page,
    dashboard_page,
    history_page,
    ranking_page
)

page_routes = [
    Route('/', index_page),
    Route('/login', login_page),
    Route('/dashboard', dashboard_page),
    Route('/historico', history_page),
    Route('/ranking', ranking_page),
]
