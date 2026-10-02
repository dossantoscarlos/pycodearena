# src/data/exercises_data.py

EXERCISES = [
    # --- INICIANTE ---
    {
        "id": "ex01",
        "title": "1. Soma dos Números Pares",
        "level": "Iniciante",
        "concept": "Controle de Fluxo & Estruturas de Repetição (for/while)",
        "function_name": "soma_pares",
        "reference_code": "def soma_pares(n: int) -> int:\n    return sum(i for i in range(1, n + 1) if i % 2 == 0)\n",
        "test_cases": [[0], [1], [2], [6], [10], [12], [15], [50], [100]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Este exercício treina o uso de **laços de repetição (`for` ou `while`)** combinados com **condicionais (`if`)** para filtrar e acumular valores.

### 📋 Requisitos:
Implemente a função `soma_pares(n: int) -> int` que recebe um inteiro `n` e soma todos os números **pares** no intervalo de 1 até `n` (inclusive).

### 📥 Entrada e Saída Esperada:
- **Entrada:** `n = 10` -> **Saída:** `30` *(pois 2 + 4 + 6 + 8 + 10 = 30)*
- **Entrada:** `n = 12` -> **Saída:** `42` *(2 + 4 + 6 + 8 + 10 + 12 = 42)*
- **Entrada:** `n = 1` -> **Saída:** `0`

### 💡 Dica Algorítmica:
Um número `i` é par se `i % 2 == 0`. Acumule a soma iterando de 1 até `n`.
""",
        "template": "def soma_pares(n: int) -> int:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex02",
        "title": "2. Inversão de String",
        "level": "Iniciante",
        "concept": "Manipulação Manual de Sequências & Concatenação",
        "function_name": "inverter_string",
        "reference_code": "def inverter_string(texto: str) -> str:\n    res = ''\n    for c in texto:\n        res = c + res\n    return res\n",
        "test_cases": [["python"], ["a"], [""], ["desafio"], ["12345"], ["arara"]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Focado no conceito de **acumulação e travessia de strings caractere por caractere**, sem dependência de truques prontos da linguagem.

### 📋 Requisitos:
Crie a função `inverter_string(texto: str) -> str` que inverta a ordem dos caracteres. **Atenção:** É proibido usar slicing (`[::-1]`).

### 📥 Entrada e Saída Esperada:
- **Entrada:** `"python"` -> **Saída:** `"nohtyp"`
- **Entrada:** `"a"` -> **Saída:** `"a"`

### 💡 Dica Algorítmica:
Crie uma string vazia `resultado = ""`. Percorra cada caractere `char` da string original e adicione-o no **início** do resultado: `resultado = char + resultado`.
""",
        "template": "def inverter_string(texto: str) -> str:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex03",
        "title": "3. Fatorial Iterativo",
        "level": "Iniciante",
        "concept": "Multiplicação Acumulativa & Tratamento de Exceções",
        "function_name": "fatorial",
        "reference_code": "def fatorial(n: int) -> int:\n    if n < 0:\n        raise ValueError('Número deve ser não negativo')\n    res = 1\n    for i in range(1, n + 1):\n        res *= i\n    return res\n",
        "test_cases": [[5], [0], [1], [7], [10]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Treinar a **multiplicação acumulativa** em laços e a validação de dados de entrada com lançamento de erros (`raise ValueError`).

### 📋 Requisitos:
Calcule `n!` (fatorial de `n`). Por definição, `0! = 1`. Se `n < 0`, você deve lançar a exceção `ValueError`.

### 📥 Entrada e Saída Esperada:
- **Entrada:** `5` -> **Saída:** `120` *(5 × 4 × 3 × 2 × 1)*
- **Entrada:** `0` -> **Saída:** `1`

### 💡 Dica Algorítmica:
Inicialize `resultado = 1`. Caso `n < 0`, lance `raise ValueError("Número inválido")`. Em seguida, multiplique `resultado` de 1 até `n`.
""",
        "template": "def fatorial(n: int) -> int:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex04",
        "title": "4. Contagem de Vogais",
        "level": "Iniciante",
        "concept": "Varredura de Strings & Busca em Conjuntos/Coleções",
        "function_name": "contar_vogais",
        "reference_code": "def contar_vogais(texto: str) -> int:\n    return sum(1 for c in texto if c.lower() in 'aeiou')\n",
        "test_cases": [["Ola Mundo"], ["XYZ"], ["AEIOU"], ["Python 3.12"], ["Algoritmos"]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Focado em **normalização de texto (case insensitivity)** e **verificação de pertinência de elementos**.

### 📋 Requisitos:
Implemente `contar_vogais(texto: str) -> int` que retorne a quantidade de vogais (`a, e, i, o, u`), ignorando maiúsculas/minúsculas.

### 📥 Entrada e Saída Esperada:
- **Entrada:** `"Ola Mundo"` -> **Saída:** `4` *(O, a, u, o)*
- **Entrada:** `"XYZ"` -> **Saída:** `0`

### 💡 Dica Algorítmica:
Defina uma string `"aeiouAEIOU"`. Percorra cada caractere da frase e incremente um contador caso o caractere esteja no conjunto de vogais.
""",
        "template": "def contar_vogais(texto: str) -> int:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex05",
        "title": "5. Maior e Menor Elemento",
        "level": "Iniciante",
        "concept": "Algoritmo de Varredura Linear (Linear Scan)",
        "function_name": "maior_e_menor",
        "reference_code": "def maior_e_menor(numeros: list[int]) -> tuple[int, int]:\n    if not numeros:\n        raise ValueError('Lista vazia')\n    maior = menor = numeros[0]\n    for x in numeros:\n        if x > maior: maior = x\n        if x < menor: menor = x\n    return (maior, menor)\n",
        "test_cases": [[[5, 2, 9, 1, 7]], [[42]], [[-10, 0, 10, 5]], [[100, 200, 50]]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Compreender como **rastrear valores mínimos e máximos manualmente** mantendo estado durante a iteração sobre um array/lista.

### 📋 Requisitos:
Dada uma lista de inteiros, retorne uma tupla `(maior, menor)`. Não utilize `max()` ou `min()`. Se a lista estiver vazia, lance `ValueError`.

### 📥 Entrada e Saída Esperada:
- **Entrada:** `[5, 2, 9, 1, 7]` -> **Saída:** `(9, 1)`
- **Entrada:** `[42]` -> **Saída:** `(42, 42)`

### 💡 Dica Algorítmica:
Inicialize duas variáveis `maior` e `menor` com o primeiro elemento `numeros[0]`. Percorra a lista comparando cada elemento e atualizando as variáveis.
""",
        "template": "def maior_e_menor(numeros: list[int]) -> tuple[int, int]:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex06",
        "title": "6. Verificador de Palíndromo",
        "level": "Iniciante",
        "concept": "Técnica de Dois Ponteiros Básica & Limpeza de Dados",
        "function_name": "eh_palindromo",
        "reference_code": "def eh_palindromo(texto: str) -> bool:\n    t = ''.join(c.lower() for c in texto if c.isalnum())\n    return t == t[::-1]\n",
        "test_cases": [["Arara"], ["A man, a plan, a canal: Panama"], ["python"], ["Socorram-me subiri no onibus em Marrocos"]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Aprender a comparar uma sequência das extremidades para o centro (**dois ponteiros**) ignorando caracteres não-alfanuméricos.

### 📋 Requisitos:
Retorne `True` se a string for um palíndromo e `False` caso contrário. Desconsidere pontuações, espaços e case.

### 📥 Entrada e Saída Esperada:
- **Entrada:** `"Arara"` -> **Saída:** `True`
- **Entrada:** `"python"` -> **Saída:** `False`

### 💡 Dica Algorítmica:
Filtre a string mantendo apenas caracteres alfanuméricos (`char.isalnum()`) e converta para minúsculas. Compare o início e o fim caminhando até o centro.
""",
        "template": "def eh_palindromo(texto: str) -> bool:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex07",
        "title": "7. Tabuada Personalizada",
        "level": "Iniciante",
        "concept": "Geração e Construção de Listas",
        "function_name": "gerar_tabuada",
        "reference_code": "def gerar_tabuada(n: int) -> list[int]:\n    return [n * i for i in range(1, 11)]\n",
        "test_cases": [[5], [7], [10], [1]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Treinar a **criação e população sequencial de listas** em Python.

### 📋 Requisitos:
Implemente `gerar_tabuada(n: int) -> list[int]` que retorne uma lista com os 10 primeiros resultados da tabuada de multiplicação de `n` (de `1 * n` até `10 * n`).

### 📥 Entrada e Saída Esperada:
- **Entrada:** `5` -> **Saída:** `[5, 10, 15, 20, 25, 30, 35, 40, 45, 50]`

### 💡 Dica Algorítmica:
Utilize um laço `for i in range(1, 11)` inserindo `n * i` em uma nova lista com `.append()`.
""",
        "template": "def gerar_tabuada(n: int) -> list[int]:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex08",
        "title": "8. Avaliação de Aluno (POO)",
        "level": "Iniciante",
        "concept": "Encapsulamento & Estado em Objetos (POO Básica)",
        "function_name": "Aluno",
        "reference_code": "class Aluno:\n    def __init__(self, nome: str, notas: list[float]):\n        self.nome = nome\n        self.notas = notas\n    def calcular_media(self) -> float:\n        return sum(self.notas) / len(self.notas) if self.notas else 0.0\n    def obter_status(self) -> str:\n        return 'Aprovado' if self.calcular_media() >= 7.0 else 'Reprovado'\n",
        "test_cases": [[["Carlos", [8.0, 7.5, 9.0]]], [["Ana", [5.0, 6.0]]]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Treinar a **Orientação a Objetos simples**, focando em como métodos operam sobre atributos internos da classe.

### 📋 Requisitos:
Crie a classe `Aluno` que armazena `nome` e uma lista de `notas`.
- `calcular_media() -> float`: Retorna a média aritmética das notas.
- `obter_status() -> str`: Retorna `"Aprovado"` se média >= 7.0, senão `"Reprovado"`.

### 📥 Entrada e Saída Esperada:
- `aluno = Aluno("Carlos", [8.0, 7.5, 9.0])` -> `calcular_media()` = `8.166...`, `obter_status()` = `"Aprovado"`
""",
        "template": "class Aluno:\n    def __init__(self, nome: str, notas: list[float]):\n        self.nome = nome\n        self.notas = notas\n\n    def calcular_media(self) -> float:\n        pass\n\n    def obter_status(self) -> str:\n        pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex09",
        "title": "9. Remoção de Duplicados",
        "level": "Iniciante",
        "concept": "Tabelas Hash para Busca O(1) & Preservação de Ordem",
        "function_name": "remover_duplicados",
        "reference_code": "def remover_duplicados(lista: list) -> list:\n    vistos = set()\n    res = []\n    for item in lista:\n        if item not in vistos:\n            vistos.add(item)\n            res.append(item)\n    return res\n",
        "test_cases": [[[1, 2, 2, 3, 1, 4]], [["a", "b", "a"]], [[10, 20, 10, 30, 20]]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Focado no uso de **conjuntos (`set`) como estrutura auxiliar de busca rápida em O(1)** sem perder a ordem original de inserção da lista.

### 📋 Requisitos:
Remova elementos duplicados de uma lista, mantendo apenas a primeira ocorrência de cada item na ordem em que apareceram.

### 📥 Entrada e Saída Esperada:
- **Entrada:** `[1, 2, 2, 3, 1, 4]` -> **Saída:** `[1, 2, 3, 4]`
""",
        "template": "def remover_duplicados(lista: list) -> list:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex10",
        "title": "10. Verificador de Número Primo",
        "level": "Iniciante",
        "concept": "Otimização Matemática de Teste de Primalidade",
        "function_name": "eh_primo",
        "reference_code": "def eh_primo(n: int) -> bool:\n    if n <= 1: return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0: return False\n    return True\n",
        "test_cases": [[7], [2], [4], [1], [13], [29], [100]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Entender **otimização de laços matemáticos** (verificar divisores apenas até a raiz quadrada `√n`).

### 📋 Requisitos:
Retorne `True` se `n` for primo (divisível apenas por 1 e por ele mesmo) e `False` caso contrário. Números <= 1 não são primos.

### 📥 Entrada e Saída Esperada:
- **Entrada:** `7` -> **Saída:** `True`
- **Entrada:** `4` -> **Saída:** `False`
""",
        "template": "def eh_primo(n: int) -> bool:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },

    # --- INTERMEDIÁRIO ---
    {
        "id": "ex11",
        "title": "11. Busca Binária",
        "level": "Intermediario",
        "concept": "Divisão e Conquista em O(log n)",
        "function_name": "busca_binaria",
        "reference_code": "def busca_binaria(lista: list[int], alvo: int) -> int:\n    ini, fim = 0, len(lista) - 1\n    while ini <= fim:\n        meio = (ini + fim) // 2\n        if lista[meio] == alvo: return meio\n        elif lista[meio] < alvo: ini = meio + 1\n        else: fim = meio - 1\n    return -1\n",
        "test_cases": [[[10, 20, 30, 40, 50, 60], 40], [[10, 20, 30, 40, 50, 60], 15], [[1, 3, 5, 7, 9], 9]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Dominar o algoritmo fundamental de **Busca Binária**, reduzindo o espaço de busca pela metade a cada iteração.

### 📋 Requisitos:
Dada uma lista **ordenada** e um valor `alvo`, retorne o índice do `alvo`. Se não existir, retorne `-1`.

### 📥 Entrada e Saída Esperada:
- **Entrada:** `lista = [10, 20, 30, 40, 50, 60]`, `alvo = 40` -> **Saída:** `3`
- **Entrada:** `alvo = 15` -> **Saída:** `-1`
""",
        "template": "def busca_binaria(lista: list[int], alvo: int) -> int:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex12",
        "title": "12. Selection Sort",
        "level": "Intermediario",
        "concept": "Algoritmo de Ordenação por Seleção O(n²)",
        "function_name": "selection_sort",
        "reference_code": "def selection_sort(lista: list[int]) -> list[int]:\n    arr = lista.copy()\n    n = len(arr)\n    for i in range(n):\n        min_idx = i\n        for j in range(i + 1, n):\n            if arr[j] < arr[min_idx]: min_idx = j\n        arr[i], arr[min_idx] = arr[min_idx], arr[i]\n    return arr\n",
        "test_cases": [[[64, 25, 12, 22, 11]], [[5, 4, 3, 2, 1]], [[1, 2, 3]]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Compreender a mecânica interna de ordenação por **troca direta de posições (in-place swap)**.

### 📋 Requisitos:
Ordene uma lista de inteiros em ordem crescente usando o algoritmo Selection Sort. Retorne a lista ordenada.

### 📥 Entrada e Saída Esperada:
- **Entrada:** `[64, 25, 12, 22, 11]` -> **Saída:** `[11, 12, 22, 25, 64]`
""",
        "template": "def selection_sort(lista: list[int]) -> list[int]:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex13",
        "title": "13. Validação de Parênteses (Pilha)",
        "level": "Intermediario",
        "concept": "Estrutura de Dados Pilha (LIFO - Last In, First Out)",
        "function_name": "parenteses_validos",
        "reference_code": "def parenteses_validos(expressao: str) -> bool:\n    pilha = []\n    m = {')': '(', ']': '[', '}': '{'}\n    for c in expressao:\n        if c in m.values(): pilha.append(c)\n        elif c in m:\n            if not pilha or pilha.pop() != m[c]: return False\n    return len(pilha) == 0\n",
        "test_cases": [["{[()]}"], ["{[(])}"], ["("], ["()[]{}"]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Utilizar uma **Pilha** para resolver validação de parênteses e delimitadores alinhados.

### 📋 Requisitos:
Dada uma string com `'()'`, `'[]'`, `'{}'`, retorne `True` se estiverem corretamente pareados.

### 📥 Entrada e Saída Esperada:
- **Entrada:** `"{[()]}"` -> **Saída:** `True`
- **Entrada:** `"{[(])}"` -> **Saída:** `False`
""",
        "template": "def parenteses_validos(expressao: str) -> bool:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex14",
        "title": "14. Frequência de Palavras",
        "level": "Intermediario",
        "concept": "Processamento de Texto & Dicionários de Frequência",
        "function_name": "frequencia_palavras",
        "reference_code": "def frequencia_palavras(texto: str) -> dict[str, int]:\n    import re\n    words = re.findall(r'\\w+', texto.lower())\n    res = {}\n    for w in words:\n        res[w] = res.get(w, 0) + 1\n    return res\n",
        "test_cases": [["Python e bom, Python e facil!"], ["teste1 teste1 teste2"]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Aprender a realizar **sanitização de dados textuais** e contagem de ocorrências usando **Dicionários (Hash Maps)**.

### 📋 Requisitos:
Retorne um dicionário `{palavra: frequencia}` em minúsculas, removendo pontuações `.,!?;:`.

### 📥 Entrada e Saída Esperada:
- **Entrada:** `"Python e bom, Python e facil!"` -> **Saída:** `{"python": 2, "e": 2, "bom": 1, "facil": 1}`
""",
        "template": "def frequencia_palavras(texto: str) -> dict[str, int]:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex15",
        "title": "15. Soma das Diagonais de Matriz",
        "level": "Intermediario",
        "concept": "Manipulação de Matrizes 2D & Índices de Matriz Quadradra",
        "function_name": "soma_diagonais",
        "reference_code": "def soma_diagonais(matriz: list[list[int]]) -> tuple[int, int]:\n    n = len(matriz)\n    sp = sum(matriz[i][i] for i in range(n))\n    ss = sum(matriz[i][n - 1 - i] for i in range(n))\n    return (sp, ss)\n",
        "test_cases": [[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [[[5]]]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Navegação em **matrizes bidimensionais** acessando elementos com relacionamentos de índices de linha e coluna (`[i][i]` e `[i][n-1-i]`).

### 📋 Requisitos:
Dada uma matriz N x N, retorne uma tupla `(soma_diagonal_principal, soma_diagonal_secundaria)`.
""",
        "template": "def soma_diagonais(matriz: list[list[int]]) -> tuple[int, int]:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex16",
        "title": "16. Fila de Atendimento (FIFO)",
        "level": "Intermediario",
        "concept": "Estrutura de Dados Fila (FIFO - First In, First Out)",
        "function_name": "FilaBanco",
        "reference_code": "class FilaBanco:\n    def __init__(self):\n        self.itens = []\n    def enfileirar(self, c):\n        self.itens.append(c)\n    def desenfileirar(self):\n        if self.esta_vazia(): raise IndexError('Fila vazia')\n        return self.itens.pop(0)\n    def esta_vazia(self):\n        return len(self.itens) == 0\n    def tamanho(self):\n        return len(self.itens)\n",
        "test_cases": [[]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Implementar uma **Fila de Atendimento** respeitando a ordem de chegada (primeiro a entrar é o primeiro a sair).

### 📋 Requisitos:
Classe `FilaBanco` com `enfileirar`, `desenfileirar`, `esta_vazia` e `tamanho`.
""",
        "template": "class FilaBanco:\n    def __init__(self):\n        pass\n\n    def enfileirar(self, cliente: str) -> None:\n        pass\n\n    def desenfileirar(self) -> str:\n        pass\n\n    def esta_vazia(self) -> bool:\n        pass\n\n    def tamanho(self) -> int:\n        pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex17",
        "title": "17. Elemento Ausente",
        "level": "Intermediario",
        "concept": "Propriedade Matemática da Soma de Gauss O(n)",
        "function_name": "encontrar_ausente",
        "reference_code": "def encontrar_ausente(numeros: list[int], n: int) -> int:\n    return (n * (n + 1) // 2) - sum(numeros)\n",
        "test_cases": [[[1, 2, 4, 5, 6], 6], [[2, 3, 4], 4], [[1, 3, 4, 5], 5]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Resolver um problema de busca de elementos ausentes em tempo O(n) e espaço O(1) usando a **Fórmula da Soma da PA de Gauss**.

### 📋 Requisitos:
Dada uma lista de números de 1 a `n` com um faltando, encontre o ausente.
""",
        "template": "def encontrar_ausente(numeros: list[int], n: int) -> int:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex18",
        "title": "18. Par com Soma Alvo (Dois Ponteiros)",
        "level": "Intermediario",
        "concept": "Algoritmo de Dois Ponteiros em Array Ordenado",
        "function_name": "dois_ponteiros_soma",
        "reference_code": "def dois_ponteiros_soma(numeros: list[int], alvo: int):\n    i, j = 0, len(numeros) - 1\n    while i < j:\n        s = numeros[i] + numeros[j]\n        if s == alvo: return (numeros[i], numeros[j])\n        elif s < alvo: i += 1\n        else: j -= 1\n    return None\n",
        "test_cases": [[[1, 2, 4, 6, 10], 10], [[1, 2, 3], 100], [[2, 5, 8, 12], 20]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Utilizar **dois ponteiros nas extremidades** de uma lista ordenada para encontrar um par em tempo O(n).

### 📋 Requisitos:
Dada uma lista ordenada, encontre dois números cuja soma seja igual ao `alvo`.
""",
        "template": "def dois_ponteiros_soma(numeros: list[int], alvo: int) -> tuple[int, int] | None:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex19",
        "title": "19. Cifra de César",
        "level": "Intermediario",
        "concept": "Aritmética Modular & Manipulação de Códigos ASCII",
        "function_name": "cifra_cesar",
        "reference_code": "def cifra_cesar(texto: str, k: int) -> str:\n    res = ''\n    for c in texto:\n        if c.isalpha():\n            b = ord('A') if c.isupper() else ord('a')\n            res += chr((ord(c) - b + k) % 26 + b)\n        else: res += c\n    return res\n",
        "test_cases": [["abc", 3], ["Hello, World!", 5], ["XYZ", 1]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Trabalhar com **aritmética modular (`% 26`)** e deslocamento ASCII com `ord()` e `chr()`.

### 📋 Requisitos:
Desloque cada letra do texto por `k` posições. Mantenha maiúsculas/minúsculas e símbolos.
""",
        "template": "def cifra_cesar(texto: str, k: int) -> str:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex20",
        "title": "20. Aplatirar Lista (Flatten)",
        "level": "Intermediario",
        "concept": "Achatamento de Estruturas Aninhadas",
        "function_name": "aplatirar_lista",
        "reference_code": "def aplatirar_lista(matriz: list[list[int]]) -> list[int]:\n    return [x for sub in matriz for x in sub]\n",
        "test_cases": [[[[1, 2], [3, 4], [5]]], [[[10]], [[20, 30]]]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Aprender a **desconstruir listas aninhadas em 1 nível** convertendo para uma lista plana.
""",
        "template": "def aplatirar_lista(matriz: list[list[int]]) -> list[int]:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },

    # --- AVANÇADO ---
    {
        "id": "ex21",
        "title": "21. Fibonacci com Memorização",
        "level": "Avancado",
        "concept": "Programação Dinâmica Top-Down (Memoization)",
        "function_name": "fibonacci_memo",
        "reference_code": "def fibonacci_memo(n: int, memo=None) -> int:\n    if memo is None: memo = {}\n    if n in memo: return memo[n]\n    if n <= 0: return 0\n    if n == 1: return 1\n    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)\n    return memo[n]\n",
        "test_cases": [[10], [0], [1], [20], [30]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Otimizar uma recursão exponencial O(2ⁿ) para tempo linear O(n) utilizando **memorização/cache**.
""",
        "template": "def fibonacci_memo(n: int, memo: dict[int, int] | None = None) -> int:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex22",
        "title": "22. Busca em Profundidade (DFS)",
        "level": "Avancado",
        "concept": "Teoria dos Grafos & Travessia Recursiva DFS",
        "function_name": "existe_caminho_dfs",
        "reference_code": "def existe_caminho_dfs(grafo, inicio, destino, visitados=None):\n    if visitados is None: visitados = set()\n    if inicio == destino: return True\n    visitados.add(inicio)\n    for v in grafo.get(inicio, []):\n        if v not in visitados:\n            if existe_caminho_dfs(grafo, v, destino, visitados): return True\n    return False\n",
        "test_cases": [[{"A": ["B", "C"], "B": ["D"], "C": ["E"], "D": [], "E": []}, "A", "E"], [{"A": ["B"], "B": []}, "A", "Z"]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Navegar em grafos para determinar a acessibilidade de caminhos entre dois nós.
""",
        "template": "def existe_caminho_dfs(grafo: dict[str, list[str]], inicio: str, destino: str, visitados: set[str] | None = None) -> bool:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex23",
        "title": "23. Subsequência Crescente Máxima (LIS)",
        "level": "Avancado",
        "concept": "Programação Dinâmica Clássica (LIS)",
        "function_name": "maior_subsequencia_crescente",
        "reference_code": "def maior_subsequencia_crescente(nums: list[int]) -> int:\n    if not nums: return 0\n    dp = [1] * len(nums)\n    for i in range(1, len(nums)):\n        for j in range(i):\n            if nums[i] > nums[j]: dp[i] = max(dp[i], dp[j] + 1)\n    return max(dp)\n",
        "test_cases": [[[10, 9, 2, 5, 3, 7, 101, 18]], [[0, 1, 0, 3, 2, 3]], [[7, 7, 7]]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Encontrar o tamanho da maior subsequência em que os números estão em ordem estritamente crescente.
""",
        "template": "def maior_subsequencia_crescente(nums: list[int]) -> int:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex24",
        "title": "24. Problema do Troco Mínimo",
        "level": "Avancado",
        "concept": "Programação Dinâmica Bottom-Up",
        "function_name": "troco_minimo",
        "reference_code": "def troco_minimo(moedas: list[int], quantia: int) -> int:\n    dp = [float('inf')] * (quantia + 1)\n    dp[0] = 0\n    for i in range(1, quantia + 1):\n        for m in moedas:\n            if i - m >= 0: dp[i] = min(dp[i], dp[i - m] + 1)\n    return int(dp[quantia]) if dp[quantia] != float('inf') else -1\n",
        "test_cases": [[[1, 2, 5], 11], [[2], 3], [[1, 5, 10], 12]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Determinar o **número mínimo de moedas** necessárias para compor um valor `quantia`.
""",
        "template": "def troco_minimo(moedas: list[int], quantia: int) -> int:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex25",
        "title": "25. Árvore Binária de Busca (BST)",
        "level": "Avancado",
        "concept": "Estrutura de Dados em Árvore Hierárquica",
        "function_name": "ArvoreBusca",
        "reference_code": "class NoArvore:\n    def __init__(self, v):\n        self.valor = v\n        self.esquerda = self.direita = None\nclass ArvoreBusca:\n    def __init__(self): self.raiz = None\n    def inserir(self, v):\n        if not self.raiz: self.raiz = NoArvore(v)\n        else: self._ins(self.raiz, v)\n    def _ins(self, no, v):\n        if v < no.valor:\n            if not no.esquerda: no.esquerda = NoArvore(v)\n            else: self._ins(no.esquerda, v)\n        else:\n            if not no.direita: no.direita = NoArvore(v)\n            else: self._ins(no.direita, v)\n    def buscar(self, v):\n        curr = self.raiz\n        while curr:\n            if curr.valor == v: return True\n            elif v < curr.valor: curr = curr.esquerda\n            else: curr = curr.direita\n        return False\n",
        "test_cases": [[]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Construção e busca em uma **Árvore Binária de Busca (BST)**.
""",
        "template": "class NoArvore:\n    def __init__(self, valor: int):\n        self.valor = valor\n        self.esquerda = None\n        self.direita = None\n\nclass ArvoreBusca:\n    def __init__(self):\n        self.raiz = None\n\n    def inserir(self, valor: int) -> None:\n        pass\n\n    def buscar(self, valor: int) -> bool:\n        pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex26",
        "title": "26. Algoritmo de Kadane",
        "level": "Avancado",
        "concept": "Otimização de Subarrays com Algoritmo de Kadane O(n)",
        "function_name": "max_subarray_kadane",
        "reference_code": "def max_subarray_kadane(nums: list[int]) -> int:\n    if not nums: raise ValueError('Vazio')\n    curr = max_s = nums[0]\n    for x in nums[1:]:\n        curr = max(x, curr + x)\n        max_s = max(max_s, curr)\n    return max_s\n",
        "test_cases": [[[-2, 1, -3, 4, -1, 2, 1, -5, 4]], [[1, 2, 3, 4]], [[-1, -2, -3]]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Encontrar a **soma máxima de um subarray contínuo** em tempo linear O(n).
""",
        "template": "def max_subarray_kadane(nums: list[int]) -> int:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex27",
        "title": "27. Permutações de String",
        "level": "Avancado",
        "concept": "Técnica de Retrocesso (Backtracking)",
        "function_name": "gerar_permutacoes",
        "reference_code": "def gerar_permutacoes(s: str) -> list[str]:\n    res = []\n    def backtrack(curr, rem):\n        if not rem:\n            res.append(''.join(curr)); return\n        vistos = set()\n        for i in range(len(rem)):\n            if rem[i] not in vistos:\n                vistos.add(rem[i])\n                backtrack(curr + [rem[i]], rem[:i] + rem[i+1:])\n    backtrack([], list(s))\n    return sorted(res)\n",
        "test_cases": [["abc"], ["ab"], ["a"]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Exploração de **árvores de decisão combinatória (Backtracking)** para encontrar todas as permutações.
""",
        "template": "def gerar_permutacoes(s: str) -> list[str]:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex28",
        "title": "28. Detecção de Ciclo em Lista Encadeada",
        "level": "Avancado",
        "concept": "Algoritmo de Floyd (Pontes Lento e Rápido)",
        "function_name": "tem_ciclo",
        "reference_code": "class NoLista:\n    def __init__(self, v): self.valor = v; self.proximo = None\ndef tem_ciclo(cabeca) -> bool:\n    lento = rapido = cabeca\n    while rapido and rapido.proximo:\n        lento = lento.proximo\n        rapido = rapido.proximo.proximo\n        if lento == rapido: return True\n    return False\n",
        "test_cases": [[]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Detectar se existe um ciclo de repetição em uma lista encadeada usando ponteiro lento e rápido.
""",
        "template": "class NoLista:\n    def __init__(self, valor: int):\n        self.valor = valor\n        self.proximo = None\n\ndef tem_ciclo(cabeca: NoLista | None) -> bool:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex29",
        "title": "29. Merge Sort",
        "level": "Avancado",
        "concept": "Divisão e Conquista Recursiva O(n log n)",
        "function_name": "merge_sort",
        "reference_code": "def merge_sort(lista: list[int]) -> list[int]:\n    if len(lista) <= 1: return lista\n    m = len(lista) // 2\n    esq = merge_sort(lista[:m])\n    dir = merge_sort(lista[m:])\n    res, i, j = [], 0, 0\n    while i < len(esq) and j < len(dir):\n        if esq[i] <= dir[j]: res.append(esq[i]); i += 1\n        else: res.append(dir[j]); j += 1\n    res.extend(esq[i:]); res.extend(dir[j:])\n    return res\n",
        "test_cases": [[[38, 27, 43, 3, 9, 82, 10]], [[5, 1, 4, 2, 8]], [[10]]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Implementar o algoritmo clássico de ordenação **Merge Sort**.
""",
        "template": "def merge_sort(lista: list[int]) -> list[int]:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    },
    {
        "id": "ex30",
        "title": "30. Mochila 0/1 (Knapsack)",
        "level": "Avancado",
        "concept": "Programação Dinâmica de Otimização 2D",
        "function_name": "mochila_01",
        "reference_code": "def mochila_01(pesos: list[int], valores: list[int], capacidade: int) -> int:\n    n = len(pesos)\n    dp = [[0] * (capacidade + 1) for _ in range(n + 1)]\n    for i in range(1, n + 1):\n        for w in range(1, capacidade + 1):\n            if pesos[i-1] <= w: dp[i][w] = max(valores[i-1] + dp[i-1][w-pesos[i-1]], dp[i-1][w])\n            else: dp[i][w] = dp[i-1][w]\n    return dp[n][capacidade]\n",
        "test_cases": [[[1, 2, 3], [6, 10, 12], 5], [[2, 3, 4], [3, 4, 5], 5]],
        "description": """
### 🎯 O que este exercício foca em resolver:
Resolver o famoso **Problema da Mochila 0/1**, maximizando o valor total de itens.
""",
        "template": "def mochila_01(pesos: list[int], valores: list[int], capacidade: int) -> int:\n    # Seu código aqui\n    pass\n",
        "unittest_code": ""
    }
]
