# tests/test_evaluator.py
import pytest
from src.evaluator import run_code_evaluation

def test_evaluation_success():
    user_code = """
def soma_pares(n: int) -> int:
    return sum(i for i in range(1, n + 1) if i % 2 == 0)
"""
    ref_code = """
def soma_pares(n: int) -> int:
    return sum(i for i in range(1, n + 1) if i % 2 == 0)
"""
    result = run_code_evaluation(
        user_code=user_code,
        reference_code=ref_code,
        function_name="soma_pares",
        test_cases=[[6], [10]]
    )

    assert result["passed"] is True
    assert result["status"] == "ACEITO"
    assert "execution_time_ms" in result

def test_evaluation_divergence():
    user_code = """
def soma_pares(n: int) -> int:
    return n * 2 # Código incorreto
"""
    ref_code = """
def soma_pares(n: int) -> int:
    return sum(i for i in range(1, n + 1) if i % 2 == 0)
"""
    result = run_code_evaluation(
        user_code=user_code,
        reference_code=ref_code,
        function_name="soma_pares",
        test_cases=[[6], [10]]
    )

    assert result["passed"] is False
    assert result["status"] == "DIVERGENCIA"

def test_evaluation_syntax_error():
    user_code = "def soma_pares(n: return n +"
    ref_code = "def soma_pares(n): return n"

    result = run_code_evaluation(
        user_code=user_code,
        reference_code=ref_code,
        function_name="soma_pares",
        test_cases=[[5]]
    )

    assert result["passed"] is False
    assert result["status"] == "ERRO_SINTAXE"

def test_evaluation_missing_function():
    user_code = "def funcao_com_nome_errado(): pass"
    ref_code = "def soma_pares(n): return n"

    result = run_code_evaluation(
        user_code=user_code,
        reference_code=ref_code,
        function_name="soma_pares",
        test_cases=[[5]]
    )

    assert result["passed"] is False
    assert result["status"] == "FUNCAO_NAO_ENCONTRADA"

def test_evaluation_runtime_exception():
    user_code = """
def soma_pares(n: int) -> int:
    return 1 / 0 # ZeroDivisionError
"""
    ref_code = "def soma_pares(n): return n"

    result = run_code_evaluation(
        user_code=user_code,
        reference_code=ref_code,
        function_name="soma_pares",
        test_cases=[[5]]
    )

    assert result["passed"] is False
    assert result["status"] == "ERRO_EXECUCAO"
