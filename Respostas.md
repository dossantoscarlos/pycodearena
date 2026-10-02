# Gabarito de Respostas - Algoritmos em Python

Este arquivo contém o gabarito oficial com a solução em Python para todos os 30 exercícios de algoritmos, divididos nas seções **Iniciante**, **Intermediario** e **Avancado**, acompanhados das suítes de testes unitários (`unittest`).

---

## Iniciante

### Exercício 1: Soma dos Números Pares
```python
def soma_pares(n: int) -> int:
    soma = 0
    for i in range(1, n + 1):
        if i % 2 == 0:
            soma += i
    return soma
```

---

### Exercício 2: Inversão de String
```python
def inverter_string(texto: str) -> str:
    resultado = ""
    for char in texto:
        resultado = char + resultado
    return resultado
```

---

### Exercício 3: Fatorial Iterativo
```python
def fatorial(n: int) -> int:
    if n < 0:
        raise ValueError("Número deve ser não negativo")
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado
```

---

### Exercício 4: Contagem de Vogais
```python
def contar_vogais(texto: str) -> int:
    vogais = "aeiouAEIOU"
    contador = 0
    for char in texto:
        if char in vogais:
            contador += 1
    return contador
```

---

### Exercício 5: Maior e Menor Elemento
```python
def maior_e_menor(numeros: list[int]) -> tuple[int, int]:
    if not numeros:
        raise ValueError("A lista não pode estar vazia")
    maior = numeros[0]
    menor = numeros[0]
    for num in numeros:
        if num > maior:
            maior = num
        if num < menor:
            menor = num
    return (maior, menor)
```

---

### Exercício 6: Verificador de Palíndromo
```python
def eh_palindromo(texto: str) -> bool:
    texto_limpo = "".join(char.lower() for char in texto if char.isalnum())
    inicio = 0
    fim = len(texto_limpo) - 1
    while inicio < fim:
        if texto_limpo[inicio] != texto_limpo[fim]:
            return False
        inicio += 1
        fim -= 1
    return True
```

---

### Exercício 7: Tabuada Personalizada
```python
def gerar_tabuada(n: int) -> list[int]:
    tabuada = []
    for i in range(1, 11):
        tabuada.append(n * i)
    return tabuada
```

---

### Exercício 8: Avaliação de Aluno (OOP Algorítmica)
```python
class Aluno:
    def __init__(self, nome: str, notas: list[float]):
        self.nome = nome
        self.notas = notas

    def calcular_media(self) -> float:
        if not self.notas:
            return 0.0
        soma = 0.0
        for nota in self.notas:
            soma += nota
        return soma / len(self.notas)

    def obter_status(self) -> str:
        media = self.calcular_media()
        if media >= 7.0:
            return "Aprovado"
        return "Reprovado"
```

---

### Exercício 9: Remoção de Duplicados Preservando Ordem
```python
def remover_duplicados(lista: list) -> list:
    resultado = []
    vistos = set()
    for item in lista:
        if item not in vistos:
            vistos.add(item)
            resultado.append(item)
    return resultado
```

---

### Exercício 10: Verificador de Número Primo
```python
def eh_primo(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
```

---

### Suíte de Testes Unitários - Iniciante

```python
import unittest

class TesteIniciante(unittest.TestCase):

    def test_ex01_soma_pares(self):
        self.assertEqual(soma_pares(10), 30)
        self.assertEqual(soma_pares(1), 0)
        self.assertEqual(soma_pares(0), 0)

    def test_ex02_inverter_string(self):
        self.assertEqual(inverter_string("python"), "nohtyp")
        self.assertEqual(inverter_string("a"), "a")
        self.assertEqual(inverter_string(""), "")

    def test_ex03_fatorial(self):
        self.assertEqual(fatorial(5), 120)
        self.assertEqual(fatorial(0), 1)
        with self.assertRaises(ValueError):
            fatorial(-1)

    def test_ex04_contar_vogais(self):
        self.assertEqual(contar_vogais("Ola Mundo"), 4)
        self.assertEqual(contar_vogais("XYZ"), 0)

    def test_ex05_maior_e_menor(self):
        self.assertEqual(maior_e_menor([5, 2, 9, 1, 7]), (9, 1))
        self.assertEqual(maior_e_menor([42]), (42, 42))

    def test_ex06_eh_palindromo(self):
        self.assertTrue(eh_palindromo("Arara"))
        self.assertTrue(eh_palindromo("A man, a plan, a canal: Panama"))
        self.assertFalse(eh_palindromo("python"))

    def test_ex07_gerar_tabuada(self):
        self.assertEqual(gerar_tabuada(5), [5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

    def test_ex08_aluno(self):
        aluno1 = Aluno("Carlos", [8.0, 7.5, 9.0])
        self.assertAlmostEqual(aluno1.calcular_media(), 8.1666666, places=4)
        self.assertEqual(aluno1.obter_status(), "Aprovado")

        aluno2 = Aluno("Ana", [5.0, 6.0])
        self.assertEqual(aluno2.obter_status(), "Reprovado")

    def test_ex09_remover_duplicados(self):
        self.assertEqual(remover_duplicados([1, 2, 2, 3, 1, 4]), [1, 2, 3, 4])
        self.assertEqual(remover_duplicados(["a", "b", "a"]), ["a", "b"])

    def test_ex10_eh_primo(self):
        self.assertTrue(eh_primo(7))
        self.assertTrue(eh_primo(2))
        self.assertFalse(eh_primo(4))
        self.assertFalse(eh_primo(1))

if __name__ == "__main__":
    unittest.main()
```

---

## Intermediario

### Exercício 11: Busca Binária
```python
def busca_binaria(lista: list[int], alvo: int) -> int:
    inicio = 0
    fim = len(lista) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if lista[meio] == alvo:
            return meio
        elif lista[meio] < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1
```

---

### Exercício 12: Ordenação por Seleção (Selection Sort)
```python
def selection_sort(lista: list[int]) -> list[int]:
    arr = lista.copy()
    n = len(arr)
    for i in range(n):
        indice_minimo = i
        for j in range(i + 1, n):
            if arr[j] < arr[indice_minimo]:
                indice_minimo = j
        arr[i], arr[indice_minimo] = arr[indice_minimo], arr[i]
    return arr
```

---

### Exercício 13: Validação de Parênteses (Pilha)
```python
def parenteses_validos(expressao: str) -> bool:
    pilha = []
    mapeamento = {')': '(', ']': '[', '}': '{'}
    for char in expressao:
        if char in mapeamento.values():
            pilha.append(char)
        elif char in mapeamento.keys():
            if not pilha or pilha.pop() != mapeamento[char]:
                return False
    return len(pilha) == 0
```

---

### Exercício 14: Frequência de Palavras
```python
def frequencia_palavras(texto: str) -> dict[str, int]:
    pontuacoes = ".,!?;:"
    texto_limpo = ""
    for char in texto.lower():
        if char not in pontuacoes:
            texto_limpo += char
        else:
            texto_limpo += " "
    
    palavras = texto_limpo.split()
    frequencias = {}
    for palavra in palavras:
        frequencias[palavra] = frequencias.get(palavra, 0) + 1
    return frequencias
```

---

### Exercício 15: Soma das Diagonais de uma Matriz
```python
def soma_diagonais(matriz: list[list[int]]) -> tuple[int, int]:
    n = len(matriz)
    soma_p = 0
    soma_s = 0
    for i in range(n):
        soma_p += matriz[i][i]
        soma_s += matriz[i][n - 1 - i]
    return (soma_p, soma_s)
```

---

### Exercício 16: Fila de Atendimento (Estrutura de Fila)
```python
class FilaBanco:
    def __init__(self):
        self.itens = []

    def enfileirar(self, cliente: str) -> None:
        self.itens.append(cliente)

    def desenfileirar(self) -> str:
        if self.esta_vazia():
            raise IndexError("A fila está vazia")
        return self.itens.pop(0)

    def esta_vazia(self) -> bool:
        return len(self.itens) == 0

    def tamanho(self) -> int:
        return len(self.itens)
```

---

### Exercício 17: Elemento Ausente na Sequência
```python
def encontrar_ausente(numeros: list[int], n: int) -> int:
    soma_esperada = n * (n + 1) // 2
    soma_real = sum(numeros)
    return soma_esperada - soma_real
```

---

### Exercício 18: Par com Soma Alvo (Dois Ponteiros)
```python
def dois_ponteiros_soma(numeros: list[int], alvo: int) -> tuple[int, int] | None:
    esquerda = 0
    direita = len(numeros) - 1
    while esquerda < direita:
        soma_atual = numeros[esquerda] + numeros[direita]
        if soma_atual == alvo:
            return (numeros[esquerda], numeros[direita])
        elif soma_atual < alvo:
            esquerda += 1
        else:
            direita -= 1
    return None
```

---

### Exercício 19: Cifra de César
```python
def cifra_cesar(texto: str, k: int) -> str:
    resultado = ""
    for char in texto:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            novo_char = chr((ord(char) - base + k) % 26 + base)
            resultado += novo_char
        else:
            resultado += char
    return resultado
```

---

### Exercício 20: Aplatirar Lista (Flatten Level 1)
```python
def aplatirar_lista(matriz: list[list[int]]) -> list[int]:
    plana = []
    for sublista in matriz:
        for elemento in sublista:
            plana.append(elemento)
    return plana
```

---

### Suíte de Testes Unitários - Intermediario

```python
import unittest

class TesteIntermediario(unittest.TestCase):

    def test_ex11_busca_binaria(self):
        arr = [10, 20, 30, 40, 50, 60]
        self.assertEqual(busca_binaria(arr, 40), 3)
        self.assertEqual(busca_binaria(arr, 15), -1)

    def test_ex12_selection_sort(self):
        self.assertEqual(selection_sort([64, 25, 12, 22, 11]), [11, 12, 22, 25, 64])

    def test_ex13_parenteses_validos(self):
        self.assertTrue(parenteses_validos("{[()]}"))
        self.assertFalse(parenteses_validos("{[(])}"))
        self.assertFalse(parenteses_validos("("))

    def test_ex14_frequencia_palavras(self):
        res = frequencia_palavras("Python e bom, Python e facil!")
        self.assertEqual(res["python"], 2)
        self.assertEqual(res["e"], 2)

    def test_ex15_soma_diagonais(self):
        matriz = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.assertEqual(soma_diagonais(matriz), (15, 15))

    def test_ex16_fila_banco(self):
        fila = FilaBanco()
        fila.enfileirar("Maria")
        fila.enfileirar("João")
        self.assertEqual(fila.tamanho(), 2)
        self.assertEqual(fila.desenfileirar(), "Maria")
        self.assertEqual(fila.tamanho(), 1)

    def test_ex17_encontrar_ausente(self):
        self.assertEqual(encontrar_ausente([1, 2, 4, 5, 6], 6), 3)

    def test_ex18_dois_ponteiros_soma(self):
        self.assertEqual(dois_ponteiros_soma([1, 2, 4, 6, 10], 10), (4, 6))
        self.assertIsNone(dois_ponteiros_soma([1, 2, 3], 100))

    def test_ex19_cifra_cesar(self):
        self.assertEqual(cifra_cesar("abc", 3), "def")
        self.assertEqual(cifra_cesar("Hello, World!", 5), "Mjqqt, Btwqi!")

    def test_ex20_aplatirar_lista(self):
        self.assertEqual(aplatirar_lista([[1, 2], [3, 4], [5]]), [1, 2, 3, 4, 5])

if __name__ == "__main__":
    unittest.main()
```

---

## Avancado

### Exercício 21: Fibonacci com Memorização (Programação Dinâmica)
```python
def fibonacci_memo(n: int, memo: dict[int, int] | None = None) -> int:
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 0:
        return 0
    if n == 1:
        return 1
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]
```

---

### Exercício 22: Busca em Profundidade (DFS) em Grafo
```python
def existe_caminho_dfs(grafo: dict[str, list[str]], inicio: str, destino: str, visitados: set[str] | None = None) -> bool:
    if visitados is None:
        visitados = set()
    if inicio == destino:
        return True
    visitados.add(inicio)
    for vizinho in grafo.get(inicio, []):
        if vizinho not in visitados:
            if existe_caminho_dfs(grafo, vizinho, destino, visitados):
                return True
    return False
```

---

### Exercício 23: Subsequência Crescente Máxima (LIS)
```python
def maior_subsequencia_crescente(nums: list[int]) -> int:
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
    return max(dp)
```

---

### Exercício 24: Problema do Troco Mínimo
```python
def troco_minimo(moedas: list[int], quantia: int) -> int:
    dp = [float('inf')] * (quantia + 1)
    dp[0] = 0
    for i in range(1, quantia + 1):
        for moeda in moedas:
            if i - moeda >= 0:
                dp[i] = min(dp[i], dp[i - moeda] + 1)
    return int(dp[quantia]) if dp[quantia] != float('inf') else -1
```

---

### Exercício 25: Árvore Binária de Busca (BST)
```python
class NoArvore:
    def __init__(self, valor: int):
        self.valor = valor
        self.esquerda = None
        self.direita = None

class ArvoreBusca:
    def __init__(self):
        self.raiz = None

    def inserir(self, valor: int) -> None:
        if not self.raiz:
            self.raiz = NoArvore(valor)
        else:
            self._inserir_recursivo(self.raiz, valor)

    def _inserir_recursivo(self, atual: NoArvore, valor: int) -> None:
        if valor < atual.valor:
            if atual.esquerda is None:
                atual.esquerda = NoArvore(valor)
            else:
                self._inserir_recursivo(atual.esquerda, valor)
        else:
            if atual.direita is None:
                atual.direita = NoArvore(valor)
            else:
                self._inserir_recursivo(atual.direita, valor)

    def buscar(self, valor: int) -> bool:
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, atual: NoArvore | None, valor: int) -> bool:
        if atual is None:
            return False
        if atual.valor == valor:
            return True
        if valor < atual.valor:
            return self._buscar_recursivo(atual.esquerda, valor)
        return self._buscar_recursivo(atual.direita, valor)
```

---

### Exercício 26: Maior Soma de Subarray (Algoritmo de Kadane)
```python
def max_subarray_kadane(nums: list[int]) -> int:
    if not nums:
        raise ValueError("A lista não pode estar vazia")
    soma_atual = nums[0]
    soma_maxima = nums[0]
    for num in nums[1:]:
        soma_atual = max(num, soma_atual + num)
        soma_maxima = max(soma_maxima, soma_atual)
    return soma_maxima
```

---

### Exercício 27: Permutações de String (Backtracking)
```python
def gerar_permutacoes(s: str) -> list[str]:
    resultado = []
    
    def backtrack(caminho_atual, resto):
        if not resto:
            resultado.append("".join(caminho_atual))
            return
        vistos = set()
        for i in range(len(resto)):
            if resto[i] not in vistos:
                vistos.add(resto[i])
                backtrack(caminho_atual + [resto[i]], resto[:i] + resto[i+1:])
                
    backtrack([], list(s))
    return resultado
```

---

### Exercício 28: Detecção de Ciclo em Lista Encadeada
```python
class NoLista:
    def __init__(self, valor: int):
        self.valor = valor
        self.proximo = None

def tem_ciclo(cabeca: NoLista | None) -> bool:
    lento = cabeca
    rapido = cabeca
    while rapido is not None and rapido.proximo is not None:
        lento = lento.proximo
        rapido = rapido.proximo.proximo
        if lento == rapido:
            return True
    return False
```

---

### Exercício 29: Merge Sort (Ordenação por Intercalação)
```python
def merge_sort(lista: list[int]) -> list[int]:
    if len(lista) <= 1:
        return lista
    
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio])
    direita = merge_sort(lista[meio:])
    
    return _intercalar(esquerda, direita)

def _intercalar(esq: list[int], dir: list[int]) -> list[int]:
    resultado = []
    i = j = 0
    while i < len(esq) and j < len(dir):
        if esq[i] <= dir[j]:
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir[j])
            j += 1
    resultado.extend(esq[i:])
    resultado.extend(dir[j:])
    return resultado
```

---

### Exercício 30: Problema da Mochila 0/1 (Knapsack Problem)
```python
def mochila_01(pesos: list[int], valores: list[int], capacidade: int) -> int:
    n = len(pesos)
    dp = [[0] * (capacidade + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacidade + 1):
            if pesos[i - 1] <= w:
                dp[i][w] = max(
                    valores[i - 1] + dp[i - 1][w - pesos[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]
                
    return dp[n][capacidade]
```

---

### Suíte de Testes Unitários - Avancado

```python
import unittest

class TesteAvancado(unittest.TestCase):

    def test_ex21_fibonacci_memo(self):
        self.assertEqual(fibonacci_memo(10), 55)
        self.assertEqual(fibonacci_memo(0), 0)

    def test_ex22_existe_caminho_dfs(self):
        grafo = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["E"],
            "D": [],
            "E": []
        }
        self.assertTrue(existe_caminho_dfs(grafo, "A", "E"))
        self.assertFalse(existe_caminho_dfs(grafo, "D", "A"))

    def test_ex23_maior_subsequencia_crescente(self):
        nums = [10, 9, 2, 5, 3, 7, 101, 18]
        self.assertEqual(maior_subsequencia_crescente(nums), 4)

    def test_ex24_troco_minimo(self):
        self.assertEqual(troco_minimo([1, 2, 5], 11), 3)
        self.assertEqual(troco_minimo([2], 3), -1)

    def test_ex25_arvore_busca(self):
        bst = ArvoreBusca()
        bst.inserir(10)
        bst.inserir(5)
        bst.inserir(15)
        self.assertTrue(bst.buscar(5))
        self.assertFalse(bst.buscar(20))

    def test_ex26_max_subarray_kadane(self):
        nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
        self.assertEqual(max_subarray_kadane(nums), 6)

    def test_ex27_gerar_permutacoes(self):
        perms = gerar_permutacoes("abc")
        self.assertEqual(len(perms), 6)
        self.assertIn("abc", perms)
        self.assertIn("cba", perms)

    def test_ex28_tem_ciclo(self):
        n1 = NoLista(1)
        n2 = NoLista(2)
        n3 = NoLista(3)
        n1.proximo = n2
        n2.proximo = n3
        self.assertFalse(tem_ciclo(n1))
        
        n3.proximo = n1
        self.assertTrue(tem_ciclo(n1))

    def test_ex29_merge_sort(self):
        self.assertEqual(merge_sort([38, 27, 43, 3, 9, 82, 10]), [3, 9, 10, 27, 38, 43, 82])

    def test_ex30_mochila_01(self):
        pesos = [1, 2, 3]
        valores = [6, 10, 12]
        capacidade = 5
        self.assertEqual(mochila_01(pesos, valores, capacidade), 22)

if __name__ == "__main__":
    unittest.main()
```
