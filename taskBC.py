import numpy as np
import matplotlib.pyplot as plt

from EPLib import QR, gen_tridiagonal


def run(task, X0=None, n=None):
    assert (X0 is None) != (n is None) # xor
   
    if task.lower() == 'b':
        k = lambda i: 40 + 2*i
    elif task.lower() == 'c':
        k = lambda i: 40 + 2*(-1)**i
    else:
        raise ValueError("Erro: `task` deve ser 'B' ou 'C' (case insensitive)")

    if n is None:
        n = X0.shape[0]

    m = 2
    k_vals = [k(i) for i in range(1, n+2, 1)]

    main_diag = [k_vals[i] + k_vals[i+1] for i in range(len(k_vals)-1)]
    sub_diag = (-1 * np.array(k_vals[1:-1])).tolist()

    A = 1/m * gen_tridiagonal(sub_diag, main_diag, sub_diag)
    
    Q, R, _ = QR(A, epsilon=1e-26, shifted=False)

    W = np.sqrt(np.diag(R)).reshape((n, 1))

    if X0 is None:
        max_idx = np.argmax(W)
        X0 = np.reshape(Q[ : , max_idx], (n, 1))

    t_range = np.arange(0, 60+0.01, 0.01)    
    t_range = np.reshape(t_range, (1, t_range.shape[0]))

    Y0 = Q.T @ X0
    Y = Y0 * np.cos(W @ t_range)

    X = Q @ Y

    # ==== #
    # Plot #
    # ==== #

    plt.style.use('seaborn')
    plt.rcParams["axes.edgecolor"] = "0.65"
    plt.rcParams["axes.linewidth"] = 1.25

    fig, axs = plt.subplots(n, 1, sharex=True, sharey=True)
    fig.subplots_adjust(hspace=0)

    overall = fig.add_subplot(111, frameon=False)
    overall.grid(False)
    overall.set_xticks([])
    overall.set_yticks([])

    overall.set_title(f'Simulações para X(0)ᵀ = {X0.T}')
    overall.set_xlabel('Tempo (s)', labelpad=25)
    overall.set_ylabel('Deslocamento', labelpad=35)

    for i in range(1, n+1, 1):
        axs[i-1].plot(t_range[0, : ], X[i-1, : ])
        axs[i-1].yaxis.set_label_position("right")
        axs[i-1].set_ylabel(f'Massa {i}', rotation=270, labelpad=15)  

    plt.show()

    return
