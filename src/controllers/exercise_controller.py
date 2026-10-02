# src/controllers/exercise_controller.py
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.database import (
    get_all_exercises,
    get_exercise_by_id,
    get_saved_user_code,
    save_submission
)
from src.evaluator import run_code_evaluation

async def list_exercises(request: Request) -> JSONResponse:
    user_id = request.session.get("user_id") or request.query_params.get("user_id")
    if not user_id:
        return JSONResponse({"error": "Não autorizado. Faça login primeiro no servidor."}, status_code=401)
    exercises = get_all_exercises(user_id)
    return JSONResponse(exercises)

async def get_exercise(request: Request) -> JSONResponse:
    ex_id = request.path_params["ex_id"]
    ex = get_exercise_by_id(ex_id)
    if not ex:
        return JSONResponse({"error": "Exercício não encontrado no banco de dados SQLite"}, status_code=404)
    return JSONResponse(ex)

async def get_user_code(request: Request) -> JSONResponse:
    user_id = request.session.get("user_id") or request.path_params.get("user_id")
    if not user_id:
        return JSONResponse({"error": "Não autorizado. Faça login primeiro no servidor."}, status_code=401)
    ex_id = request.path_params["ex_id"]
    
    saved_code = get_saved_user_code(user_id, ex_id)
    if saved_code:
        return JSONResponse({"code": saved_code, "has_saved": True})
    
    ex = get_exercise_by_id(ex_id)
    template = ex["template"] if ex else ""
    return JSONResponse({"code": template, "has_saved": False})

async def run_test(request: Request) -> JSONResponse:
    user_id = request.session.get("user_id")
    if not user_id:
        return JSONResponse({"error": "Não autorizado. Faça login primeiro no servidor."}, status_code=401)

    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Payload JSON inválido"}, status_code=400)

    ex_id = body.get("exercise_id")
    user_code = body.get("code", "")

    ex = get_exercise_by_id(ex_id)
    if not ex:
        return JSONResponse({"error": "Exercício não encontrado no banco de dados SQLite"}, status_code=404)

    eval_result = run_code_evaluation(
        user_code=user_code,
        reference_code=ex.get("reference_code", ""),
        function_name=ex.get("function_name", ""),
        test_cases=ex.get("test_cases", [])
    )
    return JSONResponse({"result": eval_result})

async def submit_code(request: Request) -> JSONResponse:
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Payload JSON inválido"}, status_code=400)

    user_id = request.session.get("user_id") or body.get("user_id")
    if not user_id:
        return JSONResponse({"error": "Não autorizado. Faça login primeiro no servidor."}, status_code=401)

    ex_id = body.get("exercise_id")
    user_code = body.get("code", "")

    ex = get_exercise_by_id(ex_id)
    if not ex:
        return JSONResponse({"error": "Exercício não encontrado no banco de dados SQLite"}, status_code=404)

    eval_result = run_code_evaluation(
        user_code=user_code,
        reference_code=ex.get("reference_code", ""),
        function_name=ex.get("function_name", ""),
        test_cases=ex.get("test_cases", [])
    )

    save_submission(
        user_id=user_id,
        exercise_id=ex_id,
        user_code=user_code,
        passed=eval_result["passed"],
        status=eval_result["status"],
        message=eval_result["message"],
        output=eval_result["output"],
        execution_time_ms=eval_result["execution_time_ms"]
    )

    return JSONResponse({
        "result": eval_result,
        "user_id": user_id
    })
