"""Módulo de suporte para realização das tarefas."""

import numpy as np


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


def QR(A0: np.ndarray, epsilon: float=1e-6, shifted: bool=True) -> "tuple[np.ndarray, np.ndarray]":
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
        tuple: tupla com a matriz V (primeira posição) e a matriz Lambda (segunda posição).
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
