# Exercícios de Algoritmos em Python

Este arquivo contém 30 exercícios de algoritmos divididos em três níveis: **Iniciante**, **Intermediario** e **Avancado**. Cada seção contém 10 desafios com suas respectivas assinaturas de funções/classes prontas para você implementar sua solução e rodar os testes unitários disponibilizados ao final de cada bloco.

---

## Iniciante

### Exercício 1: Soma dos Números Pares

**Descrição:** Escreva uma função que receba um número inteiro positivo `n` e retorne a soma de todos os números pares no intervalo de 1 até `n` (inclusive).

```python
def soma_pares(n: int) -> int:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 2: Inversão de String

**Descrição:** Crie uma função que inverta uma string sem utilizar o recurso de *slicing* (`[::-1]`).

```python
def inverter_string(texto: str) -> str:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 3: Fatorial Iterativo

**Descrição:** Implemente uma função para calcular o fatorial de um número inteiro não negativo `n` utilizando um laço de repetição. Se `n < 0`, deve lançar `ValueError`.

```python
def fatorial(n: int) -> int:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 4: Contagem de Vogais

**Descrição:** Escreva uma função que receba uma string e retorne a quantidade total de vogais (a, e, i, o, u), ignorando maiúsculas e minúsculas.

```python
def contar_vogais(texto: str) -> int:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 5: Maior e Menor Elemento

**Descrição:** Desenvolva uma função que receba uma lista de números inteiros e retorne uma tupla contendo o maior e o menor elemento da lista `(maior, menor)`, sem usar as funções embutidas `max()` e `min()`. Se a lista estiver vazia, lance `ValueError`.

```python
def maior_e_menor(numeros: list[int]) -> tuple[int, int]:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 6: Verificador de Palíndromo

**Descrição:** Crie uma função que verifique se uma frase ou palavra é um palíndromo (lê-se igual de frente para trás), ignorando espaços e diferenças entre maiúsculas e minúsculas.

```python
def eh_palindromo(texto: str) -> bool:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 7: Tabuada Personalizada

**Descrição:** Escreva uma função que gere uma lista com os 10 primeiros resultados da tabuada de multiplicação de um número `n` (de `n * 1` até `n * 10`).

```python
def gerar_tabuada(n: int) -> list[int]:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 8: Avaliação de Aluno (OOP Algorítmica)

**Descrição:** Crie uma classe `Aluno` que receba o nome e uma lista de notas. Adicione os métodos `calcular_media()` e `obter_status()` ("Aprovado" se média >= 7.0, caso contrário "Reprovado").

```python
class Aluno:
    def __init__(self, nome: str, notas: list[float]):
        self.nome = nome
        self.notas = notas

    def calcular_media(self) -> float:
        # TODO: Implemente o cálculo da média
        pass

    def obter_status(self) -> str:
        # TODO: Implemente a verificação de status
        pass
```

---

### Exercício 9: Remoção de Duplicados Preservando Ordem

**Descrição:** Implemente uma função que receba uma lista e remova os elementos duplicados, mantendo a primeira ocorrência de cada elemento na ordem original.

```python
def remover_duplicados(lista: list) -> list:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 10: Verificador de Número Primo

**Descrição:** Escreva uma função que determine se um determinado número inteiro `n` é um número primo (retorne `True` ou `False`).

```python
def eh_primo(n: int) -> bool:
    # TODO: Implemente a lógica do algoritmo
    pass
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

**Descrição:** Implemente o algoritmo de busca binária para encontrar a posição de um elemento em uma lista ordenada. Retorne o índice do elemento ou `-1` se ele não for encontrado.

```python
def busca_binaria(lista: list[int], alvo: int) -> int:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 12: Ordenação por Seleção (Selection Sort)

**Descrição:** Implemente o algoritmo de ordenação Selection Sort para ordenar uma lista de inteiros em ordem crescente.

```python
def selection_sort(lista: list[int]) -> list[int]:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 13: Validação de Parênteses (Pilha)

**Descrição:** Utilizando a estrutura de dados pilha (stack), implemente uma função para verificar se os caracteres de abertura e fechamento `'()'`, `'[]'`, `'{}'` estão corretamente balanceados.

```python
def parenteses_validos(expressao: str) -> bool:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 14: Frequência de Palavras

**Descrição:** Escreva uma função que receba um texto e retorne um dicionário indicando a contagem de frequência de cada palavra (convertida para minúsculas e removendo pontuações como `.,!?;:`).

```python
def frequencia_palavras(texto: str) -> dict[str, int]:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 15: Soma das Diagonais de uma Matriz

**Descrição:** Dada uma matriz quadrada \(N \times N\), calcule a soma dos elementos da diagonal principal e da diagonal secundária. Retorne uma tupla `(soma_principal, soma_secundaria)`.

```python
def soma_diagonais(matriz: list[list[int]]) -> tuple[int, int]:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 16: Fila de Atendimento (Estrutura de Fila)

**Descrição:** Crie uma classe `FilaBanco` que simule uma estrutura de dados Fila (FIFO). Implemente os métodos `enfileirar(cliente)`, `desenfileirar()`, `esta_vazia()` e `tamanho()`. Se desempilhar/desenfileirar de fila vazia, lance `IndexError`.

```python
class FilaBanco:
    def __init__(self):
        # TODO: Inicialize a estrutura interna da fila
        pass

    def enfileirar(self, cliente: str) -> None:
        # TODO: Adicione o cliente à fila
        pass

    def desenfileirar(self) -> str:
        # TODO: Remova e retorne o primeiro cliente da fila
        pass

    def esta_vazia(self) -> bool:
        # TODO: Retorne se a fila está vazia
        pass

    def tamanho(self) -> int:
        # TODO: Retorne o tamanho da fila
        pass
```

---

### Exercício 17: Elemento Ausente na Sequência

**Descrição:** Dada uma lista de inteiros contendo números de `1` a `n` em qualquer ordem, onde exatamente um número está faltando, encontre o número ausente.

```python
def encontrar_ausente(numeros: list[int], n: int) -> int:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 18: Par com Soma Alvo (Dois Ponteiros)

**Descrição:** Dada uma lista de números inteiros **ordenada**, determine se existem dois números cuja soma seja igual a um valor `alvo`. Retorne uma tupla com os dois números ou `None`.

```python
def dois_ponteiros_soma(numeros: list[int], alvo: int) -> tuple[int, int] | None:
    # TODO: Implemente a lógica do algoritmo utilizando dois ponteiros
    pass
```

---

### Exercício 19: Cifra de César

**Descrição:** Desenvolva uma função que aplique a Cifra de César em um texto, deslocando cada letra alfabética por uma quantidade fixa `k` de posições.

```python
def cifra_cesar(texto: str, k: int) -> str:
    # TODO: Implemente a lógica do algoritmo
    pass
```

---

### Exercício 20: Aplatirar Lista (Flatten Level 1)

**Descrição:** Implemente uma função que receba uma lista contendo sublistas de inteiros e converta-a em uma única lista unidimensional.

```python
def aplatirar_lista(matriz: list[list[int]]) -> list[int]:
    # TODO: Implemente a lógica do algoritmo
    pass
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

**Descrição:** Implemente o cálculo do `n`-ésimo termo da sequência de Fibonacci utilizando recursão com memorização (Top-Down DP).

```python
def fibonacci_memo(n: int, memo: dict[int, int] | None = None) -> int:
    # TODO: Implemente a lógica da solução dinâmica
    pass
```

---

### Exercício 22: Busca em Profundidade (DFS) em Grafo

**Descrição:** Dado um grafo representado como lista de adjacências (dicionário), implemente uma função baseada em Busca em Profundidade (DFS) para verificar se existe um caminho entre um nó `inicio` e um nó `destino`.

```python
def existe_caminho_dfs(grafo: dict[str, list[str]], inicio: str, destino: str, visitados: set[str] | None = None) -> bool:
    # TODO: Implemente o algoritmo DFS recursivo
    pass
```

---

### Exercício 23: Subsequência Crescente Máxima (LIS)

**Descrição:** Implemente uma função que calcule o comprimento da maior subsequência estritamente crescente em uma lista de números inteiros.

```python
def maior_subsequencia_crescente(nums: list[int]) -> int:
    # TODO: Implemente a programação dinâmica para LIS
    pass
```

---

### Exercício 24: Problema do Troco Mínimo

**Descrição:** Dada uma lista de valores de moedas disponíveis e um valor total `quantia`, encontre o menor número de moedas necessárias para formar essa quantia. Se não for possível, retorne `-1`.

```python
def troco_minimo(moedas: list[int], quantia: int) -> int:
    # TODO: Implemente a solução dinâmica para o problema do troco
    pass
```

---

### Exercício 25: Árvore Binária de Busca (BST)

**Descrição:** Implemente a classe de Nó de Árvore (`NoArvore`) e a classe `ArvoreBusca` com os métodos `inserir(valor)` e `buscar(valor)`.

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
        # TODO: Implemente a inserção recursiva/iterativa na BST
        pass

    def buscar(self, valor: int) -> bool:
        # TODO: Implemente a busca na BST
        pass
```

---

### Exercício 26: Maior Soma de Subarray (Algoritmo de Kadane)

**Descrição:** Dada uma lista de inteiros que pode conter números negativos, encontre a soma máxima de um subarray contínuo utilizando o algoritmo de Kadane.

```python
def max_subarray_kadane(nums: list[int]) -> int:
    # TODO: Implemente o algoritmo de Kadane
    pass
```

---

### Exercício 27: Permutações de String (Backtracking)

**Descrição:** Crie uma função que gere todas as permutações únicas dos caracteres de uma string utilizando a técnica de retrocesso (backtracking).

```python
def gerar_permutacoes(s: str) -> list[str]:
    # TODO: Implemente o algoritmo de backtracking
    pass
```

---

### Exercício 28: Detecção de Ciclo em Lista Encadeada

**Descrição:** Dada a estrutura de uma Lista Encadeada, implemente o algoritmo de Floyd (ponteiro lento e ponteiro rápido) para determinar se a lista encadeada contém um ciclo.

```python
class NoLista:
    def __init__(self, valor: int):
        self.valor = valor
        self.proximo = None

def tem_ciclo(cabeca: NoLista | None) -> bool:
    # TODO: Implemente o algoritmo dos dois ponteiros (lento e rápido)
    pass
```

---

### Exercício 29: Merge Sort (Ordenação por Intercalação)

**Descrição:** Implemente o algoritmo de ordenação recursivo Merge Sort.

```python
def merge_sort(lista: list[int]) -> list[int]:
    # TODO: Implemente o algoritmo de divisão e conquista (Merge Sort)
    pass
```

---

### Exercício 30: Problema da Mochila 0/1 (Knapsack Problem)

**Descrição:** Dados os pesos e valores de `N` itens e uma capacidade de mochila `W`, determine o valor total máximo que pode ser transportado sem exceder a capacidade `W`.

```python
def mochila_01(pesos: list[int], valores: list[int], capacidade: int) -> int:
    # TODO: Implemente a programação dinâmica 0/1 Knapsack
    pass
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
