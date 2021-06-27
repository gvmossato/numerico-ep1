import numpy as np


def sign(x: float) -> float:
    "Sign function: returns 1.0 if x is greater than or equal to zero and -1.0 otherwise."
    if x >= 0.0:
        return 1.0
    else:
        return -1.0


def wilkinson_shift(alpha: float, beta: float, alpha_last: float) -> float:
    "Returns "
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


def givens_rotations(A: np.ndarray) -> "tuple[np.ndarray, np.ndarray]":
    "Through Given's Rotation Method, do one step of QR decopomsition"
    n = A.shape[0]
    Q = np.eye(n) # Initialize ortoghonal matrix
    R = np.copy(A) # Non-inplace operations

    for m in range(0, n-1, 1):
        alpha = R[m, m]
        beta = R[m+1, m]

        i, j = (m, m+1)
        c, s = cos_and_sin(alpha, beta)
        G = givens_matrix(n, i, j, c, s)

        # Find Q and R
        Q = Q @ G.T
        R = G @ R
    
    R = np.triu(R)

    return (Q, R)


def QR(A0: np.ndarray, epsilon: float=1e-6, shifted: bool=True) -> "tuple[np.ndarray, np.ndarray]":
    n = A0.shape[0]
    k = 0

    A = np.copy(A0) # Non-inplace operations
    V = np.eye(n)   # Initialize eigenvectors matrix
    I = np.eye(n)

    for m in range(n-1, 0, -1):
        beta = A[m, m-1] # Element to be minimized

        while np.abs(beta) >= epsilon: # Loop until covergence of beta to approx. zero
            mu = wilkinson_shift(alpha, beta, alpha_last) if (shifted and k > 0) else 0.0
            Q, R = givens_rotations(A - mu*I) # Do QR decomposition
            
            # Calculates new matrix
            A = R @ Q + mu*I
            V = V @ Q
            
            # Update variables
            beta = A[m, m-1]
            alpha = A[m-1, m-1]
            alpha_last = A[m, m]

            k += 1 # New iteration

        A[m, m-1] = 0 # If while breaks, beta converged (considered equal to zero)

    return (V, A, k)
