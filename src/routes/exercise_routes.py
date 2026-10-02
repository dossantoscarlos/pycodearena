# src/routes/exercise_routes.py
from starlette.routing import Route
from src.controllers.exercise_controller import (
    list_exercises,
    get_exercise,
    get_user_code,
    run_test,
    submit_code
)

exercise_routes = [
    Route('/api/exercises', list_exercises, methods=['GET']),
    Route('/api/exercises/{ex_id}', get_exercise, methods=['GET']),
    Route('/api/user-code/{user_id}/{ex_id}', get_user_code, methods=['GET']),
    Route('/api/test', run_test, methods=['POST']),
    Route('/api/submissions', submit_code, methods=['POST']),
]
