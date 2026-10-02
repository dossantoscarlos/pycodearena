# src/database/__init__.py
from src.database.repository import (
    get_connection,
    init_db,
    get_all_exercises,
    get_exercise_by_id,
    get_all_users,
    get_leaderboard,
    create_or_get_user,
    get_user_passed_count,
    save_submission,
    get_saved_user_code,
    get_user_history,
    process_sync_operations,
    get_sync_pull_data,
    register_user_db,
    authenticate_user_db,
    recover_password_db
)

__all__ = [
    "get_connection",
    "init_db",
    "get_all_exercises",
    "get_exercise_by_id",
    "get_all_users",
    "get_leaderboard",
    "create_or_get_user",
    "get_user_passed_count",
    "save_submission",
    "get_saved_user_code",
    "get_user_history",
    "process_sync_operations",
    "get_sync_pull_data",
    "register_user_db",
    "authenticate_user_db",
    "recover_password_db"
]
