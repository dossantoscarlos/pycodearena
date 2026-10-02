# tests/test_database.py
import pytest
import uuid
from src.database import (
    get_all_exercises,
    get_exercise_by_id,
    register_user_db,
    authenticate_user_db,
    recover_password_db,
    save_submission,
    get_saved_user_code,
    get_user_history,
    get_leaderboard,
    process_sync_operations
)

def test_exercises_seed():
    exercises = get_all_exercises()
    assert len(exercises) >= 30
    ex01 = get_exercise_by_id("ex01")
    assert ex01 is not None
    assert ex01["title"] == "1. Soma dos Números Pares"
    assert "test_cases" in ex01

def test_register_and_authenticate_user_db():
    unique_user = f"user_test_{uuid.uuid4().hex[:6]}"
    email = f"{unique_user}@test.com"
    password = "secret_password_123"

    # Registro de usuário
    user, err = register_user_db(unique_user, "Nome Teste", email, password)
    assert err is None
    assert user["username"] == unique_user

    # Registro duplicado (deve retornar erro)
    dup_user, dup_err = register_user_db(unique_user, "Outro Nome", email, password)
    assert dup_user is None
    assert dup_err is not None

    # Autenticação correta
    auth_user, auth_err = authenticate_user_db(unique_user, password)
    assert auth_err is None
    assert auth_user["id"] == user["id"]

    # Autenticação com senha errada
    wrong_user, wrong_err = authenticate_user_db(unique_user, "senha_errada")
    assert wrong_user is None
    assert wrong_err == "Senha incorreta."

def test_recover_password_db():
    unique_user = f"recover_test_{uuid.uuid4().hex[:6]}"
    email = "recuperar@exemplo.com"
    password = "password123"

    register_user_db(unique_user, "Usuario Recuperacao", email, password)

    info, err = recover_password_db(unique_user)
    assert err is None
    assert info["username"] == unique_user
    assert info["email_decrypted"] == email
    assert "r***r@exemplo.com" in info["masked_email"]

def test_submission_and_history_db():
    unique_user = f"sub_user_{uuid.uuid4().hex[:6]}"
    user, _ = register_user_db(unique_user, "Submissao Teste", f"{unique_user}@test.com", "pass123")

    user_id = user["id"]
    ex_id = "ex01"
    code = "def soma_pares(n): return 0"

    save_submission(
        user_id=user_id,
        exercise_id=ex_id,
        user_code=code,
        passed=True,
        status="ACEITO",
        message="Sucesso",
        output="OK",
        execution_time_ms=10.5
    )

    saved_code = get_saved_user_code(user_id, ex_id)
    assert saved_code == code

    history = get_user_history(user_id)
    assert len(history) == 1
    assert history[0]["exercise_id"] == ex_id
    assert history[0]["passed"] == 1

def test_leaderboard_db():
    leaderboard = get_leaderboard()
    assert isinstance(leaderboard, list)
    assert len(leaderboard) > 0
    assert "rank" in leaderboard[0]

def test_sync_operations_idempotency_db():
    op_id = f"op_{uuid.uuid4().hex}"
    ops = [
        {
            "operation_id": op_id,
            "entity": "user",
            "action": "create_user",
            "payload": {
                "id": f"sync_user_{uuid.uuid4().hex[:6]}",
                "username": f"sync_user_{uuid.uuid4().hex[:6]}",
                "name": "Sync User"
            }
        }
    ]

    res1 = process_sync_operations(ops)
    assert len(res1["processed"]) == 1
    assert res1["processed"][0]["status"] == "applied"

    # Segunda chamada com mesmo op_id deve ser idenfificada como already_processed (Idempotência)
    res2 = process_sync_operations(ops)
    assert len(res2["processed"]) == 1
    assert res2["processed"][0]["status"] == "already_processed"
