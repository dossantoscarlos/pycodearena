# src/routes/__init__.py
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from src.routes.page_routes import page_routes
from src.routes.auth_routes import auth_routes
from src.routes.exercise_routes import exercise_routes
from src.routes.history_routes import history_routes
from src.routes.ranking_routes import ranking_routes
from src.routes.user_routes import user_routes
from src.routes.sync_routes import sync_routes

all_routes = (
    page_routes +
    auth_routes +
    exercise_routes +
    history_routes +
    ranking_routes +
    user_routes +
    sync_routes +
    [Mount('/static', StaticFiles(directory="static"), name="static")]
)
