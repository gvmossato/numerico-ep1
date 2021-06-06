import numpy as np


def QR(A0):
    n = A0.shape[0]

    I = np.eye(n)
    Q = np.copy(I)
    R = Q @ A0

    eps = 1e-6

    for m in range(n-1):
        beta_prev = 1e10
        k = 0

        while np.abs(beta_prev) >= eps:
            alpha = R[m, m]
            beta = R[m+1, m]

            mu = wilkinson_shift(alpha, alpha_prev, beta_prev) if k > 0 else 0.

            R = R - mu*I

            c, s = get_cs(alpha, beta)
            i, j = (m, m+1)

            G = givens_matrix(n, i, j, c, s)

            Q = Q @ G.T
            R = G @ R + mu*I

            k += 1

            alpha_prev = alpha
            beta_prev = beta        

    return (Q, R)

def sign(number: float) -> float:
    if number >= 0:
        return 1.
    else:
        return -1.

def wilkinson_shift(alpha, alpha_prev, beta_prev):
    d = (alpha_prev - alpha) / 2
    mu = alpha + d - sign(d) * np.abs(d - beta_prev)

    return mu

def get_cs(alpha: float, beta: float) -> tuple:
    denominator = np.sqrt(alpha**2 + beta**2)
    c = alpha / denominator
    s = - beta / denominator

    return (c, s)

def givens_matrix(n: int, i: int, j: int, c: float, s: float) -> np.ndarray:
    G = np.eye(n)

    G[i, i] = c
    G[j, j] = c

    G[i ,j] = -s
    G[j, i] = s

    return G


A = np.array(
    [[4., 3., 0.],
     [3., 4., 3.],
     [0., 3., 4.]]
)

Q, R = QR(A)
Q_np, R_np = np.linalg.qr(A)

print('Self\nQ =\n', Q, '\n', 'R =\n', R)
print('Numpy\nQ =\n', Q_np, '\n', 'R =\n', R_np)
