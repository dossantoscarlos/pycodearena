# src/database/repository.py
import sqlite3
import os
import json
import uuid
import logging
from datetime import datetime

logger = logging.getLogger("database")

from src.data import EXERCISES
from src.utils import encrypt_email, decrypt_email, hash_password, verify_password

# Raiz do projeto (database.db na pasta starlete)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(ROOT_DIR, "database.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Inicializa o banco de dados SQLite, cria as tabelas necessárias e atualiza/popula
    os 30 exercícios com os códigos de referência nativos para avaliação comparativa.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de Exercícios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        level TEXT NOT NULL,
        concept TEXT,
        function_name TEXT,
        reference_code TEXT,
        test_cases_json TEXT,
        description TEXT NOT NULL,
        template TEXT NOT NULL,
        unittest_code TEXT
    )
    """)

    # Adiciona as novas colunas caso não existam
    cursor.execute("PRAGMA table_info(exercises)")
    columns = [col["name"] for col in cursor.fetchall()]
    if "function_name" not in columns:
        cursor.execute("ALTER TABLE exercises ADD COLUMN function_name TEXT")
    if "reference_code" not in columns:
        cursor.execute("ALTER TABLE exercises ADD COLUMN reference_code TEXT")
    if "test_cases_json" not in columns:
        cursor.execute("ALTER TABLE exercises ADD COLUMN test_cases_json TEXT")

    # Tabela de Usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email_encrypted TEXT,
        password_hash TEXT,
        password_salt TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # Adiciona colunas caso não existam
    cursor.execute("PRAGMA table_info(users)")
    user_cols = [col["name"] for col in cursor.fetchall()]
    if "email_encrypted" not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN email_encrypted TEXT")
    if "password_hash" not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
    if "password_salt" not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN password_salt TEXT")

    # Tabela de Submissões e Progresso
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        exercise_id TEXT NOT NULL,
        user_code TEXT,
        passed INTEGER NOT NULL,
        status TEXT NOT NULL,
        message TEXT,
        output TEXT,
        execution_time_ms REAL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (exercise_id) REFERENCES exercises (id)
    )
    """)

    # Tabela de Operações Processadas para Idempotência
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processed_operations (
        operation_id TEXT PRIMARY KEY,
        entity TEXT NOT NULL,
        action TEXT NOT NULL,
        processed_at TEXT NOT NULL
    )
    """)

    conn.commit()

    # Upsert dos 30 exercícios no SQLite com reference_code e test_cases
    for ex in EXERCISES:
        concept_val = ex.get("concept", "Algoritmos e Lógica")
        func_name = ex.get("function_name", "")
        ref_code = ex.get("reference_code", "")
        test_cases_json = json.dumps(ex.get("test_cases", []))

        cursor.execute("""
        INSERT INTO exercises (id, title, level, concept, function_name, reference_code, test_cases_json, description, template, unittest_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title,
            level=excluded.level,
            concept=excluded.concept,
            function_name=excluded.function_name,
            reference_code=excluded.reference_code,
            test_cases_json=excluded.test_cases_json,
            description=excluded.description,
            template=excluded.template
        """, (ex["id"], ex["title"], ex["level"], concept_val, func_name, ref_code, test_cases_json, ex["description"], ex["template"], ex.get("unittest_code", "")))
    conn.commit()

    # Cria usuário padrão caso não exista nenhum
    cursor.execute("SELECT COUNT(*) as count FROM users")
    user_count = cursor.fetchone()["count"]
    if user_count == 0:
        cursor.execute("""
        INSERT INTO users (id, username, name, created_at)
        VALUES (?, ?, ?, ?)
        """, ("user_default", "dev_padrao", "Desenvolvedor Python", datetime.now().isoformat()))
        conn.commit()

    conn.close()


def get_all_exercises(user_id: str = "user_default"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, level, concept, description, template FROM exercises ORDER BY id")
    rows = cursor.fetchall()

    cursor.execute("""
    SELECT DISTINCT exercise_id FROM submissions 
    WHERE user_id = ? AND passed = 1
    """, (user_id,))
    passed_ids = {r["exercise_id"] for r in cursor.fetchall()}

    conn.close()

    result = []
    for r in rows:
        result.append({
            "id": r["id"],
            "title": r["title"],
            "level": r["level"],
            "concept": r["concept"] or "Algoritmos",
            "description": r["description"],
            "template": r["template"],
            "passed": r["id"] in passed_ids
        })
    return result


def get_exercise_by_id(ex_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exercises WHERE id = ?", (ex_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        res = dict(row)
        if res.get("test_cases_json"):
            try:
                res["test_cases"] = json.loads(res["test_cases_json"])
            except Exception:
                res["test_cases"] = []
        else:
            res["test_cases"] = []
        return res
    return None


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total FROM exercises")
    total_exercises = cursor.fetchone()["total"]

    result = []
    for u in users:
        cursor.execute("""
        SELECT COUNT(DISTINCT exercise_id) as passed_count 
        FROM submissions WHERE user_id = ? AND passed = 1
        """, (u["id"],))
        passed_count = cursor.fetchone()["passed_count"]

        result.append({
            "id": u["id"],
            "username": u["username"],
            "name": u["name"],
            "passed_count": passed_count,
            "total_exercises": total_exercises
        })

    conn.close()
    return result


def get_leaderboard():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total FROM exercises")
    total_exercises = cursor.fetchone()["total"]

    result = []
    for u in users:
        cursor.execute("""
        SELECT COUNT(DISTINCT exercise_id) as passed_count 
        FROM submissions WHERE user_id = ? AND passed = 1
        """, (u["id"],))
        passed_count = cursor.fetchone()["passed_count"]

        cursor.execute("""
        SELECT e.level, COUNT(DISTINCT s.exercise_id) as count
        FROM submissions s
        JOIN exercises e ON s.exercise_id = e.id
        WHERE s.user_id = ? AND s.passed = 1
        GROUP BY e.level
        """, (u["id"],))
        levels_rows = cursor.fetchall()
        level_counts = {r["level"].lower(): r["count"] for r in levels_rows}

        result.append({
            "id": u["id"],
            "username": u["username"],
            "name": u["name"],
            "passed_count": passed_count,
            "total_exercises": total_exercises,
            "iniciante_count": level_counts.get("iniciante", 0),
            "intermediario_count": level_counts.get("intermediario", 0),
            "avancado_count": level_counts.get("avancado", 0)
        })

    result.sort(key=lambda x: (x["passed_count"], x["iniciante_count"] + x["intermediario_count"]*2 + x["avancado_count"]*3), reverse=True)

    for index, u in enumerate(result, start=1):
        u["rank"] = index

    conn.close()
    return result


def create_or_get_user(username: str, name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username,))
    existing = cursor.fetchone()

    if existing:
        user_id = existing["id"]
        res_name = existing["name"]
        res_username = existing["username"]
        conn.close()
        passed_cnt = get_user_passed_count(user_id)
        return {
            "id": user_id,
            "username": res_username,
            "name": res_name,
            "passed_count": passed_cnt
        }, False

    user_id = f"user_{uuid.uuid4().hex[:8]}"
    created_at = datetime.now().isoformat()
    final_name = name or username

    cursor.execute("""
    INSERT INTO users (id, username, name, created_at)
    VALUES (?, ?, ?, ?)
    """, (user_id, username, final_name, created_at))
    conn.commit()
    conn.close()

    return {
        "id": user_id,
        "username": username,
        "name": final_name,
        "passed_count": 0
    }, True


def get_user_passed_count(user_id: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(DISTINCT exercise_id) as count 
    FROM submissions WHERE user_id = ? AND passed = 1
    """, (user_id,))
    cnt = cursor.fetchone()["count"]
    conn.close()
    return cnt


def save_submission(user_id: str, exercise_id: str, user_code: str, passed: bool, status: str, message: str, output: str, execution_time_ms: float):
    conn = get_connection()
    cursor = conn.cursor()

    sub_id = f"sub_{uuid.uuid4().hex[:8]}"
    now_str = datetime.now().strftime("%H:%M:%S")

    cursor.execute("""
    INSERT INTO submissions (id, user_id, exercise_id, user_code, passed, status, message, output, execution_time_ms, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (sub_id, user_id, exercise_id, user_code, 1 if passed else 0, status, message, output, execution_time_ms, now_str))

    conn.commit()
    conn.close()


def get_saved_user_code(user_id: str, exercise_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT user_code FROM submissions 
    WHERE user_id = ? AND exercise_id = ? 
    ORDER BY timestamp DESC LIMIT 1
    """, (user_id, exercise_id))
    row = cursor.fetchone()
    conn.close()
    if row and row["user_code"]:
        return row["user_code"]
    return None


def get_user_history(user_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT s.id, s.user_id, s.exercise_id, s.user_code, s.passed, s.status, 
           s.message, s.output, s.execution_time_ms, s.timestamp,
           e.title as exercise_title, e.level as exercise_level, e.concept as exercise_concept
    FROM submissions s
    JOIN exercises e ON s.exercise_id = e.id
    WHERE s.user_id = ?
    ORDER BY s.rowid DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def process_sync_operations(operations: list):
    """
    Processa um lote de operações enviadas pela fila de sincronização PWA local com idempotência.
    """
    conn = get_connection()
    cursor = conn.cursor()

    processed_list = []
    conflicts_list = []

    for op in operations:
        op_id = op.get("operation_id")
        entity = op.get("entity")
        action = op.get("action")
        payload = op.get("payload", {})

        if not op_id:
            continue

        # Verifica se já foi processado (Garantia de Idempotência)
        cursor.execute("SELECT 1 FROM processed_operations WHERE operation_id = ?", (op_id,))
        if cursor.fetchone():
            processed_list.append({
                "operation_id": op_id,
                "status": "already_processed"
            })
            continue

        try:
            if action == "create_user":
                user_id = payload.get("id") or f"user_{uuid.uuid4().hex[:8]}"
                username = payload.get("username", "user_offline")
                name = payload.get("name", username)
                created_at = payload.get("created_at") or datetime.now().isoformat()

                cursor.execute("""
                INSERT INTO users (id, username, name, created_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(username) DO UPDATE SET name=excluded.name
                """, (user_id, username, name, created_at))

            elif action == "submit_code":
                sub_id = payload.get("id") or f"sub_{uuid.uuid4().hex[:8]}"
                user_id = payload.get("user_id", "user_default")
                ex_id = payload.get("exercise_id")
                user_code = payload.get("user_code", "")
                passed = 1 if payload.get("passed") else 0
                status = payload.get("status", "OK")
                msg = payload.get("message", "")
                output = payload.get("output", "")
                exec_time = payload.get("execution_time_ms", 0.0)
                ts = payload.get("timestamp") or datetime.now().strftime("%H:%M:%S")

                if ex_id:
                    cursor.execute("""
                    INSERT INTO submissions (id, user_id, exercise_id, user_code, passed, status, message, output, execution_time_ms, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        user_code=excluded.user_code,
                        passed=excluded.passed,
                        status=excluded.status,
                        message=excluded.message,
                        output=excluded.output,
                        execution_time_ms=excluded.execution_time_ms,
                        timestamp=excluded.timestamp
                    """, (sub_id, user_id, ex_id, user_code, passed, status, msg, output, exec_time, ts))

            elif action == "save_code":
                user_id = payload.get("user_id")
                ex_id = payload.get("exercise_id")
                code = payload.get("code", "")
                if user_id and ex_id:
                    sub_id = f"draft_{user_id}_{ex_id}"
                    ts = datetime.now().strftime("%H:%M:%S")
                    cursor.execute("""
                    INSERT INTO submissions (id, user_id, exercise_id, user_code, passed, status, message, output, execution_time_ms, timestamp)
                    VALUES (?, ?, ?, ?, 0, 'DRAFT', 'Rascunho salvo', '', 0.0, ?)
                    ON CONFLICT(id) DO UPDATE SET user_code=excluded.user_code, timestamp=excluded.timestamp
                    """, (sub_id, user_id, ex_id, code, ts))

            # Marca a operação como processada no banco central
            now_iso = datetime.now().isoformat()
            cursor.execute("""
            INSERT INTO processed_operations (operation_id, entity, action, processed_at)
            VALUES (?, ?, ?, ?)
            """, (op_id, entity or "unknown", action or "unknown", now_iso))

            processed_list.append({
                "operation_id": op_id,
                "status": "applied"
            })

        except Exception as e:
            print(f"Erro ao processar operação {op_id}: {e}")
            conflicts_list.append({
                "operation_id": op_id,
                "error": str(e)
            })

    conn.commit()
    conn.close()

    return {
        "processed": processed_list,
        "conflicts": conflicts_list
    }


def get_sync_pull_data():
    """
    Retorna a lista completa de exercícios e usuários para sincronização do PWA.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, level, concept, description, template FROM exercises ORDER BY id")
    exercises = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, username, name, created_at FROM users")
    users = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return {
        "exercises": exercises,
        "users": users
    }


def register_user_db(username: str, name: str, email: str, password: str):
    """
    Cadastra um novo usuário no SQLite garantindo username ÚNICO e salvando e-mail criptografado.
    """
    username = username.strip().lower()
    name = name.strip() or username
    email = email.strip()

    if not username or len(username) < 3:
        return None, "O username deve ter pelo menos 3 caracteres."
    if not password or len(password) < 4:
        return None, "A senha deve ter pelo menos 4 caracteres."

    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se username já existe (Case Insensitive)
    cursor.execute("SELECT id FROM users WHERE LOWER(username) = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return None, f"O username '{username}' já está em uso por outro usuário."

    user_id = f"user_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now().isoformat()

    # Criptografa o e-mail usando a salt do .env
    encrypted_email = encrypt_email(email)

    # Gera hash seguro da senha
    pwd_hash, pwd_salt = hash_password(password)

    try:
        cursor.execute("""
        INSERT INTO users (id, username, name, email_encrypted, password_hash, password_salt, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, username, name, encrypted_email, pwd_hash, pwd_salt, now_iso))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return None, "Este username já está cadastrado."
    except Exception as e:
        conn.close()
        return None, f"Erro ao cadastrar usuário: {e}"

    cursor.execute("SELECT id, username, name, created_at FROM users WHERE id = ?", (user_id,))
    user_row = dict(cursor.fetchone())
    conn.close()

    user_row["passed_count"] = 0
    return user_row, None


def authenticate_user_db(username: str, password: str):
    """
    Autentica um usuário por username e senha.
    """
    username = username.strip().lower()
    if not username or not password:
        logger.warning("[AUTH DB] Tentativa de login com campos obrigatórios vazios.")
        return None, "Username e senha são obrigatórios."

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE LOWER(username) = ?", (username,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        logger.warning(f"[AUTH DB] Usuário '{username}' NÃO foi encontrado no banco de dados.")
        return None, "Nome de usuário não encontrado."

    user_dict = dict(row)
    stored_hash = user_dict.get("password_hash")
    stored_salt = user_dict.get("password_salt")

    # Caso seja um usuário legado sem senha, aceita ou exige definição
    if stored_hash and stored_salt:
        if not verify_password(password, stored_hash, stored_salt):
            conn.close()
            logger.warning(f"[AUTH DB] ERRO DE SENHA: A senha fornecida para o usuário '{username}' está incorreta.")
            return None, "Senha incorreta."

    # Contagem de exercícios concluídos
    cursor.execute("SELECT COUNT(DISTINCT exercise_id) as cnt FROM submissions WHERE user_id = ? AND passed = 1", (user_dict["id"],))
    cnt_row = cursor.fetchone()
    conn.close()

    logger.info(f"[AUTH DB] Usuário '{username}' autenticado com sucesso no banco de dados.")
    # Retorna o usuário autenticado sem expor a hash da senha
    return {
        "id": user_dict["id"],
        "username": user_dict["username"],
        "name": user_dict["name"],
        "created_at": user_dict["created_at"],
        "passed_count": cnt_row["cnt"] if cnt_row else 0
    }, None


def recover_password_db(username: str):
    """
    Recupera o cadastro do usuário pelo username e descriptografa o e-mail de recuperação.
    """
    username = username.strip().lower()
    if not username:
        return None, "Informe o username para recuperação."

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, name, email_encrypted FROM users WHERE LOWER(username) = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None, f"Nenhum cadastro encontrado para o username '{username}'."

    enc_email = row["email_encrypted"]
    decrypted = decrypt_email(enc_email) if enc_email else "Não informado"

    # Ofusca parte do e-mail para privacidade na tela
    masked_email = decrypted
    if "@" in decrypted:
        parts = decrypted.split("@")
        name_part = parts[0]
        if len(name_part) > 2:
            masked = name_part[0] + "***" + name_part[-1]
        else:
            masked = name_part[0] + "***"
        masked_email = f"{masked}@{parts[1]}"

    return {
        "username": row["username"],
        "name": row["name"],
        "masked_email": masked_email,
        "email_decrypted": decrypted
    }, None
