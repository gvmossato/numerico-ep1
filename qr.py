import numpy as np


def sign(number: float) -> float:
    if number >= 0:
        return 1.
    else:
        return -1.

def wilkinson_shift(alpha, alpha_prev, beta_prev):
    d = (alpha_prev - alpha) / 2
    mu = alpha + d - sign(d) * np.sqrt(d**2 - beta_prev**2)

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

n = A.shape[0]

R = np.copy(A)
Q = np.eye(n)

max_iter = 1

for i in range(max_iter):
    for k in range(n-1):

        alpha = R[k, k]
        beta = R[k+1, k]

        c, s = get_cs(alpha, beta)

        i, j = (k, k+1)   

        Q = givens_matrix(n, i, j, c, s) @ Q
        R = Q @ A

    A = R @ Q.T
    V = Q.T

print('R =\n', R, end='\n\n')
print('A =\n', A, end='\n\n')
print('V =\n', V, end='\n\n')
