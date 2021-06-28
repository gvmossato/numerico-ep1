import numpy as np
import matplotlib.pyplot as plt

from EPLib import QR, gen_tridiagonal, gen_eign, print_table


# ================ #
# Executa a tarefa #
# ================ #

def run(epsilon, n_vals):
    amount = len(n_vals)
    count = 0

    results = []

    infos = {
        '#' : [],
        'Desloc.' : [],
        'n' : [],
        'k' : []
    }

    for shifted in [True, False]:
        for n in n_vals:
            A = gen_tridiagonal(beta=-1, alpha=2, gamma=-1, n=n)
            Q, R, k = QR(A, epsilon=epsilon, shifted=shifted)

            Lambda = np.diag(R)

            results.append((Q, Lambda))

            infos['#'].append(count)
            infos['Desloc.'].append(shifted)
            infos['k'].append(k)
            infos['n'].append(n)

            count += 1
            progress = np.round(count/(2*amount) * 100, 2)
            print(f"Progresso: {progress}%    ", end='\r')            
        
    print('Concluído! Comparação dos resultados:\n')
    print_table(infos)

    # ==== #
    # Plot #
    # ==== #

    while True:
        # Hacky: input com entrada padrão 's'
        plot_graph = input('\nExibir gráfico de iterações por dimensão da matriz? ([s]/n): ') or 's'

        if plot_graph.lower() == 's':
            plt.plot(n_vals, infos['k'][ :amount], marker='o') # Com deslocamento
            plt.plot(n_vals, infos['k'][amount: ], marker='o') # Sem deslocamento

            plt.title('Influência do deslocamento na complexidade do algoritmo')
            plt.xlabel('Dimensão da matriz (n)')
            plt.ylabel('Iterações até a convergência (k)')
            plt.legend(['Com deslocamento', 'Sem deslocamento'])
            plt.show()

            break

        elif plot_graph.lower() == 'n':
            break

        else:
            print('Entrada inválida.')
    
#    # ======== #
#    # Matrizes
#    # ======== #
#
#    print('Matrizes finais encontradas:\n')
#
#    for i in range(len(infos['n'])):
#        print(20*'=')
#        print('Caso #{}: Deslocamento? {}; n={}; k={}')
#        print('Autovalores=\n', )
#        print('Autovetores=\n', )
#
#        print('\nValores esperados:')
#        print('Autovalores=\n', )
#        print('Autovetores=\n', )
#
#    return
#
#run(epsilon=1e-6, n_vals=[2, 4, 8, 16])