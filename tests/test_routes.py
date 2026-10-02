# tests/test_routes.py
import pytest
import uuid

def test_login_and_dashboard_routes(client):
    # Sem autenticação: GET / deve retornar 200 (login.html)
    unauth_root = client.get("/", follow_redirects=False)
    assert unauth_root.status_code == 200

    # Sem autenticação: GET /dashboard deve redirecionar (302) para /
    unauth_dash = client.get("/dashboard", follow_redirects=False)
    assert unauth_dash.status_code == 302
    assert unauth_dash.headers["location"] == "/"

    # Registrar e logar usuário na sessão do client
    unique_user = f"dash_user_{uuid.uuid4().hex[:6]}"
    client.post("/api/auth/register", json={
        "username": unique_user,
        "name": "Dash User",
        "email": f"{unique_user}@test.com",
        "password": "pass123"
    })
    client.post("/api/auth/login", json={
        "username": unique_user,
        "password": "pass123"
    })

    # Autenticado: GET /dashboard deve retornar 200 (index.html com os exercícios)
    auth_dash = client.get("/dashboard", follow_redirects=False)
    assert auth_dash.status_code == 200

    # Autenticado: GET / deve redirecionar (302) para /dashboard
    auth_root = client.get("/", follow_redirects=False)
    assert auth_root.status_code == 302
    assert auth_root.headers["location"] == "/dashboard"

def test_auth_flow_routes(client):
    unique_user = f"route_user_{uuid.uuid4().hex[:6]}"
    email = f"{unique_user}@test.com"
    password = "password_route_123"

    # 1. Registro via POST /api/auth/register
    reg_res = client.post("/api/auth/register", json={
        "username": unique_user,
        "name": "Nome Route Test",
        "email": email,
        "password": password
    })
    assert reg_res.status_code == 201
    assert reg_res.json()["user"]["username"] == unique_user

    # 2. Logout via POST /api/auth/logout
    logout_res = client.post("/api/auth/logout")
    assert logout_res.status_code == 200

    # 3. Login via POST /api/auth/login
    login_res = client.post("/api/auth/login", json={
        "username": unique_user,
        "password": password
    })
    assert login_res.status_code == 200
    assert login_res.json()["user"]["username"] == unique_user

    # 4. Recuperação via POST /api/auth/recover
    rec_res = client.post("/api/auth/recover", json={
        "username": unique_user
    })
    assert rec_res.status_code == 200
    assert rec_res.json()["username"] == unique_user

def test_exercise_routes_authenticated(client):
    unique_user = f"ex_user_{uuid.uuid4().hex[:6]}"
    # Cadastra e loga no cliente
    client.post("/api/auth/register", json={
        "username": unique_user,
        "name": "Ex User",
        "email": f"{unique_user}@ex.com",
        "password": "password123"
    })
    client.post("/api/auth/login", json={
        "username": unique_user,
        "password": "password123"
    })

    # Listar exercícios (GET /api/exercises)
    ex_list_res = client.get("/api/exercises")
    assert ex_list_res.status_code == 200
    data = ex_list_res.json()
    assert len(data) >= 30

    # Detalhes de um exercício (GET /api/exercises/ex01)
    ex_res = client.get("/api/exercises/ex01")
    assert ex_res.status_code == 200
    assert ex_res.json()["id"] == "ex01"

    # Executar teste dinâmico (POST /api/test)
    test_res = client.post("/api/test", json={
        "exercise_id": "ex01",
        "code": "def soma_pares(n): return sum(i for i in range(1, n + 1) if i % 2 == 0)"
    })
    assert test_res.status_code == 200
    assert test_res.json()["result"]["passed"] is True

    # Enviar submissão (POST /api/submissions)
    sub_res = client.post("/api/submissions", json={
        "exercise_id": "ex01",
        "code": "def soma_pares(n): return sum(i for i in range(1, n + 1) if i % 2 == 0)"
    })
    assert sub_res.status_code == 200
    assert sub_res.json()["result"]["passed"] is True

def test_sync_routes(client):
    # GET /api/sync/pull
    pull_res = client.get("/api/sync/pull")
    assert pull_res.status_code == 200
    assert "exercises" in pull_res.json()
    assert "users" in pull_res.json()

    # POST /api/sync/push
    push_res = client.post("/api/sync/push", json={"operations": []})
    assert push_res.status_code == 200
    assert "processed" in push_res.json()

def test_ranking_and_users_routes(client):
    ranking_res = client.get("/api/ranking")
    assert ranking_res.status_code == 200
    assert isinstance(ranking_res.json(), list)

    users_res = client.get("/api/users")
    assert users_res.status_code == 403
