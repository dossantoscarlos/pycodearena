import os
import logging
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from src.database import init_db
from src.routes import all_routes

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


@asynccontextmanager
async def lifespan(app: Starlette):
    print("Inicializando banco de dados SQLite...")
    init_db()
    print("Servidor PyCode Arena pronto com Avaliador Comparativo Dinâmico!")
    yield
    print("Desligando servidor...")


secret_key = os.getenv("SECRET_KEY", "PyCodeArena_Secret_Key_Default_9931")
middleware = [
    Middleware(SessionMiddleware, secret_key=secret_key, session_cookie="pycode_session", max_age=86400)
]

app = Starlette(debug=True, routes=all_routes, middleware=middleware, lifespan=lifespan)