import numpy as np


def sign(x: float) -> float:
    if x >= 0.0:
        return 1.0
    else:
        return -1.0

def wilkinson_shift(alpha: float, beta: float, alpha_last: float) -> float:
    d = (alpha - alpha_last) / 2.0
    mu = alpha_last + d - sign(d) * np.sqrt(d**2 + beta**2)

    return mu

def cos_and_sin(alpha: float, beta: float) -> "tuple[float, float]":
    if np.abs(alpha) > np.abs(beta):
        tau = - beta / alpha
        c = 1.0 / np.sqrt(1.0 + tau**2)
        s = c * tau
    else:
        tau = - alpha / beta
        s = 1.0 / np.sqrt(1.0 + tau**2)
        c = s * tau

    return (c, s)

def givens_matrix(n: int, i: int, j: int, c: float, s: float) -> np.ndarray:
    G = np.eye(n)

    G[i, i] = c
    G[j, j] = c

    G[i ,j] = -s
    G[j, i] = s

    return G

def givens_rotations(A):
    n = A.shape[0]    
    R = np.copy(A)    
    Q = np.eye(n)

    for m in range(n-1):
        alpha = R[m, m]
        beta = R[m+1, m]

        i, j = (m, m+1)
        c, s = cos_and_sin(alpha, beta)
        G = givens_matrix(n, i, j, c, s)

        Q = Q @ G.T
        R = G @ R

    return (Q, R)

def QR(A0: np.ndarray, epsilon: float=1e-16, shifted: bool=True) -> "tuple[np.ndarray, np.ndarray]":
    n = A0.shape[0]

    I = np.eye(n)
    A = np.copy(A0)
    V = np.eye(n)

    k = 0

    for m in range(n-1, 0, -1):       
        beta = A[m, m-1]

        while np.abs(beta) >= epsilon:

            mu = wilkinson_shift(alpha, beta, alpha_last) if (shifted and k > 0) else 0.0

            A = A - mu*I
            Q, R = givens_rotations(A)

            A = R @ Q + mu*I
            V = V @ Q

            beta = A[m, m-1]

            alpha = A[m-1, m-1]
            alpha_last = A[m, m]

            k += 1

    return (V, A, k)
