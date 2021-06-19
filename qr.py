import numpy as np


def sign(x: float) -> float:
    if x >= 0.0:
        return 1.0
    else:
        return -1.0

def wilkinson_shift(alpha: float, alpha_prev: float, beta_prev: float) -> float:
    d = (alpha_prev - alpha) / 2.0
    mu = alpha + d - sign(d) * np.sqrt(d**2 + beta_prev**2)

    return mu

def cos_and_sin(alpha: float, beta: float) -> "tuple[float, float]":
    if np.abs(alpha) > np.abs(beta):
        tau = - beta / alpha
        c = 1 / np.sqrt(1 + tau**2)
        s = c * tau
    else:
        tau = - alpha / beta
        s = 1 / np.sqrt(1 + tau**2)
        c = s * tau

    return (c, s)

def givens_matrix(n: int, i: int, j: int, c: float, s: float) -> np.ndarray:
    G = np.eye(n)

    G[i, i] = c
    G[j, j] = c

    G[i ,j] = -s
    G[j, i] = s

    return G

def QR(A0: np.ndarray, epsilon: float=1e-6, shifted: bool=True) -> "tuple[np.ndarray, np.ndarray]":
    n = A0.shape[0]

    I = np.eye(n)
    Q = np.copy(I)
    R = Q @ A0

    for m in range(n-1):
        beta_prev = np.inf # Initialize beta as something big
        iter_count = 1 # Counts iterations per eigenvalue found

        while np.abs(beta_prev) >= epsilon:
            alpha = R[m, m]
            beta = R[m+1, m]

            i, j = (m, m+1)
            c, s = cos_and_sin(alpha, beta)
            G = givens_matrix(n, i, j, c, s)
            mu = wilkinson_shift(alpha, alpha_prev, beta_prev) if (shifted and iter_count > 1) else 0.0

            R = R - mu*I
            Q = Q @ G.T
            R = G @ R + mu*I

            alpha_prev = alpha
            beta_prev = beta

            iter_count += 1
        
        R[m+1, m] = 0 # If while loop stops, beta converged (is zero)

        print(f"Element in positon {(m, m)} converged to eigenvalue after {iter_count} iterations.")

    # Last eigenvalue converges with last but one eigenvalue
    print(f"Element in positon {(m+1, m+1)} converged to eigenvalue after {iter_count} iterations.")

    #fix_sign = [ sign(x) for x in R[0,:] ]
    #Q *= fix_sign
    #R *= fix_sign

    return (Q, R)


#A = np.array(
#    [[4., 3., 0.],
#     [3., 4., 3.],
#     [0., 3., 4.]]
#)

#Q, R = QR(A)
#Q_np, R_np = np.linalg.qr(A)

#print('Self\nQ =\n', Q, '\n', 'R =\n', R)
#print('Numpy\nQ =\n', Q_np, '\n', 'R =\n', R_np)
