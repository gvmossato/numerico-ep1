# =================================== #
# Módulo de execução da tarefa B ou C #
# =================================== #

import numpy as np
import matplotlib.pyplot as plt

from EPLib import QR, gen_tridiagonal, ctext


# ================ #
# Executa a tarefa #
# ================ #

def run(task, epsilon, shifted, X0=None, n=None):
    # XOR: somente um desses deve ser None
    assert (X0 is None) != (n is None)

    # Define lei de formação de k consoante a tarefa
    if task.lower() == 'b':
        k = lambda i: 40 + 2*i
    elif task.lower() == 'c':
        k = lambda i: 40 + 2*(-1)**i
    else:
        raise ValueError("Erro: `task` deve ser 'B' ou 'C' e não {task} (case insensitive).")

    # Se n não foi passado, determina através do vetor X0
    if n is None:
        n = X0.shape[0]

    m = 2 # Massa
    k_vals = [k(i) for i in range(1, n+2, 1)] # Constante elástica

    # Cria diagonais da matriz tridiagonal simétrica
    main_diag = [k_vals[i] + k_vals[i+1] for i in range(len(k_vals)-1)]
    sub_diag = (-1 * np.array(k_vals[1:-1])).tolist()

    A = 1/m * gen_tridiagonal(main_diag, sub_diag, None)
    
    Q, R, _ = QR(A, epsilon=epsilon, shifted=shifted)

    # Obtém frequências através dos autovalores
    W = np.sqrt(np.diag(R)).reshape((n, 1))

    # Se X0 não foi passado, obtém seu valor através da máxima frequência
    if X0 is None:
        max_idx = np.argmax(W) # Índice da máxima frequência
        X0 = np.reshape(Q[ : , max_idx], (n, 1))

    # Gera vetor de tempo
    t_range = np.arange(0, 10.01, 0.01)  
    t_range = np.reshape(t_range, (1, t_range.shape[0]))

    # Aplica a transformação e calcula os valores
    Y0 = Q.T @ X0
    Y = Y0 * np.cos(W @ t_range)

    # Reverte a transformação 
    X = Q @ Y

    # ==== #
    # Plot #
    # ==== #

    while True:
        # Input com entrada padrão 's'
        plot_graph = input(f"\nExibir gráfico de deslocamento por tempo para as massas? ([{ctext('s', 'g')}]/{ctext('n', 'r')}): ") or 's'
        print()

        if plot_graph.lower() == 's': # Exibe gráfico

            plt.style.use('seaborn')                # Estilo: 'seaborn'
            plt.rcParams["axes.edgecolor"] = "0.65" # Contorno cinza
            plt.rcParams["axes.linewidth"] = 1.25   # com espessura 1.25

            # Gera subplots
            fig, axs = plt.subplots(n, 1, sharex=True, sharey=True)
            fig.subplots_adjust(hspace=0)

            # Gera plot invisível para agrupamento dos demais
            overall = fig.add_subplot(111, frameon=False)
            overall.grid(False)
            overall.set_xticks([])
            overall.set_yticks([])

            overall.set_title(f'Simulações para X(0)ᵀ = {X0.T}')
            overall.set_xlabel('Tempo (s)', labelpad=25)
            overall.set_ylabel('Deslocamento (m)', labelpad=35)

            # Insere dados nos plots
            for i in range(1, n+1, 1):
                axs[i-1].plot(t_range[0, : ], X[i-1, : ])
                axs[i-1].yaxis.set_label_position("right")
                axs[i-1].set_ylabel(f'Massa {i}', rotation=270, labelpad=15)  

            plt.show()
            break

        elif plot_graph.lower() == 'n': # Pula exibição do gráfico
            break

        else:
            print(ctext('Entrada inválida.', 'r'))
    
    # =================== #
    # Frequências e modos #
    # =================== #

    print(f"{ctext('> Frequências de oscilação:', 'b')}")
    print(W.T, end='\n\n')

    print(f"{ctext('> Modos de vibração:', 'b')}")
    print(Q, end='\n\n')
    
    return
