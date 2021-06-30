# ============================================= #
# Módulo de suporte para realização das tarefas #
# ============================================= #

import numpy as np


# ============================================= #
# Algoritmo QR                                  #
# ============================================= #

def sign(x: float) -> float:
    """
    Função sinal: retorna 1.0 se x é maior ou igual a zero, -1.0 caso contrário.
    
    Args:
        x (float): valor a ser comparado com zero.
    
    Returns:
        float: 1.0 ou -1.0, a depender do valor de x.
    """

    if x >= 0.0:
        return 1.0
    else:
        return -1.0


def wilkinson_shift(alpha: float, beta: float, alpha_last: float) -> float:
    """
    Calcula o valor do deslocamento espectral de acordo com a heurística de Wilkinson.

    Args:
        alpha (float): (n-1)-ésimo elemento da diagonal principal.
        beta (float): n-ésimo elemento da diagonal abaixo da principal.
        alpha_last (float): n-ésimo elemento da diagonal principal.
    
    Returns:
        float: valor do deslocamento espectral.
    """

    d = (alpha - alpha_last) / 2.0
    mu = alpha_last + d - sign(d) * np.sqrt(d**2 + beta**2)

    return mu


def cos_and_sin(alpha: float, beta: float) -> "tuple[float, float]":
    """
    Calcula os valores de cosseno e seno que compõem uma dada matriz de rotação de Givens.
    Utilizou-se o "método numericamente mais estável" tal como descrito no enunciado.

    Args:
        alpha (float): (n-1)-ésimo elemento da diagonal principal.
        beta (float): n-ésimo elemento da diagonal abaixo da principal.
    
    Returns:
        tuple: valor do cosseno (primeira posição) e do seno (segunda posição) em uma tupla.
    """

    if np.abs(alpha) > np.abs(beta):
        tau = - beta / alpha
        c = 1.0 / np.sqrt(1.0 + tau**2)
        s = c * tau
    else:
        tau = - alpha / beta
        s = 1.0 / np.sqrt(1.0 + tau**2)
        c = s * tau

    return (c, s)


def givens_matrix(n: int, i: int, c: float, s: float) -> np.ndarray:
    """
    Gera a matriz de rotação de Givens para duas linhas consecutivas doutra matriz.

    Args:
        n (int): dimensão da matriz a sofrer rotação (igual a dimensão da matriz de Givens).
        i (int): índice da linha a sofrer rotação com i+1.
        c (float): valor do cosseno calculado sobre alpha e beta.
        s (float): valor do seno calculado sobre alpha e beta.
    
    Returns:
        np.ndarray: matriz de rotação de Givens de ordem n.
    """

    G = np.eye(n)

    G[i, i] = c
    G[i+1, i+1] = c

    G[i, i+1] = -s
    G[i+1, i] = s

    return G


def givens_rotation(A: np.ndarray) -> "tuple[np.ndarray, np.ndarray]":
    """
    Realiza um passo da decomposição QR em matrizes tridiagonais simétricas por meio da rotação de Givens.

    Args:
        A (np.ndarray): matriz tridiagonal simétrica a ser decomposta em Q (ortonormal) e R (triangular superior).

    Returns:
        tuple: uma tupla com as matrizes Q (primeira posição) e R (segunda posição).
    """

    n = A.shape[0]
    Q = np.eye(n) # Inicializa a matriz ortogonal
    R = np.copy(A) # Operações não in-place

    # Itera ao longo da diagonal principal (crescente)
    for m in range(0, n-1, 1):
        # Gera a matriz de rotação
        c, s = cos_and_sin(R[m, m], R[m+1, m])
        G = givens_matrix(n, m, c, s)

        # Calcula Q e R
        Q = Q @ G.T
        R = G @ R

    return (Q, R)


def QR(A0: np.ndarray, epsilon: float=1e-6, shifted: bool=True) -> "tuple[np.ndarray, np.ndarray, int]":
    """
    Por meio de decomposições QR com deslocamento espectral, calcula as matrizes Lambda e V tais que
    V @ Lambda @ V.T == A0, sendo:
    
    - A0: tridiagonal simétrica;
    - V: ortonormal, cujas colunas são autovetores de A0;
    - Lambda: tridiagonal simétrica, cuja diagonal principal são autovalores de A0. 

    Args:
        A0 (np.ndarray): matriz tridiagonal simétrica a ser decomposta.
        epsilon (float): precisão mínima para determinação da convergência.
        shifted (bool): aplica (True) ou não (False) os deslocamentos espectrais.

    Returns:
        tuple: tupla com a matriz V (primeira posição), a matriz Lambda (segunda posição) e o número
        total de iterações até a convergência (terceira posição).
    """

    n = A0.shape[0]
    k = 0 # Número de iterações até a convergência de todos os elementos

    A = np.copy(A0) # Operações não in-place
    V = np.eye(n)   # Inicializa matriz de autovetores
    I = np.eye(n)

    # Itera ao longo da diagonal principal (decrescente)
    for m in range(n-1, 0, -1):
        # Loop até a convergência de beta
        while np.abs(A[m, m-1]) >= epsilon: 
            mu = wilkinson_shift(A[m-1, m-1], A[m, m-1], A[m, m]) if (shifted and k > 0) else 0.0
            Q, R = givens_rotation(A - mu*I)
            
            # Atualiza as matrizes
            A = R @ Q + mu*I
            V = V @ Q

            k += 1 # Nova iteração

        A[m, m-1] = 0 # Quebra do laço while: beta convergiu (é nulo)
    
    Lambda = A
    
    return (V, Lambda, k)


# ============================================= #
# Tarefas                                       #
# ============================================= #

def normalize(matrix: np.ndarray) -> np.ndarray:
    """
    Normaliza as colunas de uma matriz in-place por meio da  
    norma Euclidiana para um vetor do R^n.

    Args:
        matrix (np.ndarray): matriz a ter suas colunas normalizadas.

    Returns:
        np.ndarray: matriz com as colunas normalizadas.
    """

    norm = np.sqrt(np.sum(matrix**2, axis=0))
    matrix = matrix / norm

    return matrix


def gen_eign(n: int) -> "tuple[list, np.ndarray]":
    """
    Gera autovalores e autovetores (analitacamente conhecidos) para uma 
    matriz tridiagonal simétrica cujos elementos da diagonal principal são 
    todos iguais a 2 e das diagonais abaixo e acima dessa são iguais a -1.

    Args:
        n (int): dimensão da matriz tridiagonal simétrica.

    Returns:
        tuple: lista de autovalores da matriz (primeira posição) e uma matriz
        cujas colunas são os respectivos autovetores associados (segunda posição).
    """

    # Vetor base (constante) para calcular autovetores 
    base_vec = np.arange(1, n+1, 1) * np.pi/(n+1)
    base_vec = np.reshape(base_vec, (n, 1))
    
    eigs_vals = [] # Armazena autovalores
    eign_vecs = [] # Armazena autovetores

    # Gera autovalores e autovetores
    for j in range(1, n+1):
        val = 2 * (1 - np.cos( j*np.pi / (n+1) ))
        vec = np.sin(base_vec * j)

        eigs_vals.append(val)
        eign_vecs.append(vec)

    # Concatena uma lista de vetores coluna em uma matriz, normalizando-a
    eign_vecs = normalize(np.hstack(eign_vecs))

    return (eign_vecs, eigs_vals)


def gen_tridiagonal(alpha, beta, n=None) -> np.ndarray:
    """
    Gera uma matriz diagonal simétrica.
    
    Se alpha e beta forem listas, as insere como diagonal principal (alpha)
    e diagonais acima e abaixo dessa (beta) numa matriz de zeros.

    Se alpha e beta forem números, cria uma matriz de zeros com dimensão n 
    em que os elementos da diagonal princpal são iguais a alpha e os da
    diagonais axima e abaixo dessa são iguais a beta. 

    Args:
        alpha (int/float/list): elemento(s) da diagonal principal.
        beta (int/float/list): elemento(s) das diagonais abaixo e acima da principal.
        n (int/None): se int, n é a dimensão da matriz; se None, a dimensão deve
                          estar implícita em alpha e beta.

    Returns:
        np.ndarray: matriz diagonal simétrica.
    """

    assert type(alpha) == type(beta)

    if isinstance(alpha, (float, int)):
        assert n is not None
        
        # Cria vetores baseado nos valores passados
        alpha_vec = n * [alpha]
        beta_vec = (n-1) * [beta]
        
        # Insere vetores em uma matriz de zeros
        M = np.diag(beta_vec, k=-1)
        M += np.diag(alpha_vec, k=0)        
        M += np.diag(beta_vec, k=1)

    elif isinstance(alpha, list):
        assert len(alpha) == len(beta)+1
        assert n is None

        # Insere vetores em uma matriz de zeros
        M = np.diag(beta, k=-1)
        M += np.diag(alpha, k=0)
        M += np.diag(beta, k=1)

    return M


# ============================================= #
# Miscelânia                                    #
# ============================================= #

def print_table(data: dict) -> None:
    """
    Imprime linha a linha um dicionário de listas formatado
    como uma tabela.

    Args:
        data (dict): dicionário de listas a ser impresso.
    """

    header_fields = list(data.keys())
    table_vals = list(data.values())

    # Células com até 10 caracteres alinhados à esquerda
    row_shape = "| {:<10}"*len(header_fields) + " |" 

    header = row_shape.format(*header_fields)
    columns = np.array(table_vals).T

    print(header)            # Cabeçalho
    print('=' * len(header)) # Separador
    for row_vals in columns: # Linhas
        print(row_shape.format(*row_vals))
    
    return


def ctext(text: str, tag: str) -> str:
    """
    Aplica cor a uma string a ser impressa no terminal, através de tags pré-definidas.
    As cores podem sofrer alterações conforme as configurações do terminal do usuário.

    Args:
        text (str): texto a ser colorido.
        tag (str): identificador que mapeia a cor desejada a um código ASCII; tags válidas:
                   'r' --> Vermelho; 'g' --> Verde; 'y' --> Amarelo; 'b' --> Azul;
                   'm' --> Magenta; 'c' --> Ciano.
    
    Returns:
        str: string idêntica a text, exceto pelas tags de cor.
    """

    color_dict = {
        'r' : '\033[31m', # Red
        'g' : '\033[32m', # Green
        'y' : '\033[33m', # Yellow
        'b' : '\033[34m', # Blue
        'm' : '\033[35m', # Magenta
        'c' : '\033[36m'  # Cyan
    }

    # Aplica a tag de cor e reseta para a cor padrão do terminal do usuário.
    text = color_dict[tag] + text + '\033[0m'

    return text
