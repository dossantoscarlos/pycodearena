# tests/conftest.py
import os
import pytest
from starlette.testclient import TestClient

from src.main import app
from src.database import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Garante que o banco SQLite esteja inicializado para a sessão de testes."""
    init_db()

@pytest.fixture
def client():
    """Retorna o TestClient do Starlette para requisições HTTP em testes."""
    with TestClient(app) as test_client:
        yield test_client
