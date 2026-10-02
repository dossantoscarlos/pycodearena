# src/evaluator/engine.py
import sys
import os
import subprocess
import tempfile
import json
import time
from typing import Any

def run_code_evaluation(user_code: str, reference_code: str, function_name: str, test_cases: list) -> dict[str, Any]:
    """
    Executa o Motor de Avaliação Comparativa Dinâmica.
    Executa a Solução Nativa Oficial (Gabarito) e a Solução do Usuário
    em namespaces isolados sobre o mesmo conjunto de entradas de teste.
    """
    start_time = time.time()
    
    test_cases_json = json.dumps(test_cases or [])

    script_content = f"""# -*- coding: utf-8 -*-
import sys
import json
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ref_code = {repr(reference_code)}
user_code = {repr(user_code)}
func_name = {repr(function_name)}
test_inputs = {test_cases_json}

def run_comparative_eval():
    # 1. Executa Solução Nativa em Namespace Isolado
    ref_scope = {{}}
    try:
        exec(ref_code, ref_scope)
    except Exception as e:
        return {{
            "passed": False,
            "status": "ERRO_REF",
            "message": "Erro no código de referência.",
            "output": f"❌ Erro no código gabarito: {{type(e).__name__}}: {{str(e)}}"
        }}

    ref_obj = ref_scope.get(func_name)

    # 2. Executa Solução do Usuário em Namespace Isolado
    user_scope = {{}}
    try:
        exec(user_code, user_scope)
    except Exception as e:
        return {{
            "passed": False,
            "status": "ERRO_SINTAXE",
            "message": "Erro de Sintaxe no código enviado.",
            "output": f"❌ Erro de Sintaxe ao compilar o código Python:\\n   -> {{type(e).__name__}}: {{str(e)}}"
        }}

    user_obj = user_scope.get(func_name)

    if user_obj is None:
        return {{
            "passed": False,
            "status": "FUNCAO_NAO_ENCONTRADA",
            "message": f"Função ou Classe '{{func_name}}' não foi encontrada.",
            "output": f"❌ A função ou classe '{{func_name}}' não foi declarada no seu código.\\n   Verifique se a assinatura da função coincide com a solicitada."
        }}

    inputs = test_inputs or [[]]

    # 3. Executa ambas no mesmo conjunto de dados
    for idx, raw_args in enumerate(inputs, 1):
        if isinstance(raw_args, list):
            args = tuple(raw_args)
        elif isinstance(raw_args, dict):
            args = (raw_args,)
        else:
            args = (raw_args,)

        formatted_args = ", ".join(map(repr, args))

        # Executa Solução Nativa Oficial
        try:
            if callable(ref_obj):
                ref_res = ref_obj(*args)
            else:
                ref_res = "NATIVE_OK"
        except Exception as err_ref:
            ref_res = f"EXCEPTION:{{type(err_ref).__name__}}"

        # Executa Solução do Usuário
        try:
            if callable(user_obj):
                user_res = user_obj(*args)
            else:
                user_res = "USER_OK"
        except Exception as err_user:
            err_type = type(err_user).__name__
            err_msg = (
                f"❌ Erro de Execução no Teste #{{idx}}\\n"
                f"   Entrada: {{func_name}}({{formatted_args}})\\n"
                f"   -> Sua solução lançou exceção: {{err_type}}: {{str(err_user)}}"
            )
            return {{
                "passed": False,
                "status": "ERRO_EXECUCAO",
                "message": f"Erro de Execução no teste #{{idx}}.",
                "output": err_msg
            }}

        # Compara resultados (Ambas devem retornar exatamente o mesmo valor)
        if user_res != ref_res:
            diff_msg = (
                f"❌ Divergência de Resultado no Teste #{{idx}}\\n"
                f"   Entrada: {{func_name}}({{formatted_args}})\\n"
                f"   -> Esperado (Solução Nativa): {{repr(ref_res)}}\\n"
                f"   -> Recebido (Sua Solução):   {{repr(user_res)}}"
            )
            return {{
                "passed": False,
                "status": "DIVERGENCIA",
                "message": f"Resultado divergente no teste #{{idx}}.",
                "output": diff_msg
            }}

    return {{
        "passed": True,
        "status": "ACEITO",
        "message": "Solução executada com êxito! Todos os testes comparativos passaram. 🎉",
        "output": f"✅ Todos os {{len(inputs)}} testes comparativos passaram com sucesso!\\nO resultado da sua solução bateu 100% com a Solução Nativa Oficial. 🎉"
    }}

print(json.dumps(run_comparative_eval(), ensure_ascii=False))
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp_file:
        tmp_file.write(script_content)
        tmp_file_path = tmp_file.name

    try:
        process = subprocess.run(
            [sys.executable, tmp_file_path],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=5.0
        )
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        
        stdout = (process.stdout or "").strip()
        stderr = (process.stderr or "").strip()

        if process.returncode != 0:
            return {
                "passed": False,
                "status": "ERRO_SINTAXE",
                "message": "Erro de Sintaxe no código enviado.",
                "output": stderr or stdout or "Erro desconhecido ao interpretar o código enviado.",
                "execution_time_ms": elapsed_ms
            }

        try:
            res_dict = json.loads(stdout)
            res_dict["execution_time_ms"] = elapsed_ms
            return res_dict
        except Exception:
            return {
                "passed": False,
                "status": "ERRO_PARSE",
                "message": "Erro ao interpretar resultado do teste.",
                "output": stdout or stderr,
                "execution_time_ms": elapsed_ms
            }

    except subprocess.TimeoutExpired:
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "passed": False,
            "status": "TIMEOUT",
            "message": "Tempo limite de execução excedido (5 segundos). Verifique se há laço infinito.",
            "output": "❌ TimeoutExpired: O tempo limite de 5 segundos foi excedido. Verifique se existe um loop 'while True' sem parada.",
            "execution_time_ms": elapsed_ms
        }
    finally:
        if os.path.exists(tmp_file_path):
            try:
                os.remove(tmp_file_path)
            except Exception:
                pass
