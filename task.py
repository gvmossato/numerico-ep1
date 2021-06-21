import numpy as np
import matplotlib.pyplot as plt

from qr import QR, givens_rotations


def gen_tridiagonal(n, beta, alpha, gamma):
    b = (n-1) * [beta]
    a = (n) * [alpha]
    g = (n-1) * [gamma]

    M = np.diag(b, k=-1)
    M += np.diag(a, k=0)
    M += np.diag(g, k=1)

    return M

k_shifted = []
k_non_shifted = []

epsilon = 1e-6
n_vals = [4, 16, 32, 64]

for shifted in [True, False]:
    for n in n_vals:
        A = gen_tridiagonal(n, beta=3, alpha=4, gamma=3)
        Q, R, k = QR(A, epsilon, shifted=shifted)

        if shifted:
            k_shifted.append(k)
        else:
            k_non_shifted.append(k)

        print(f"Shifted? {shifted}; n = {n} => k = {k}")


plt.plot(n_vals, k_shifted)
plt.plot(n_vals, k_non_shifted)

plt.show()
