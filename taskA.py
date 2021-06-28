import numpy as np
import matplotlib.pyplot as plt

from EPLib import QR, gen_tridiagonal, gen_eign, print_table, normalize


# ================ #
# Executa a tarefa #
# ================ #

def run(epsilon, n_vals):
    amount = len(n_vals)
    count = 0

    results = []
    valid = []
    
    infos = {
        'Teste' : [],
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
            valid.append(gen_eign(n))

            infos['Teste'].append(str(count))
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
            print('\33[91mEntrada inválida.\33[0m')
    
    # ========================= #
    # Autovalores e Autovetores #
    # ========================= #

    while True:
        print('\nDeseja verificar autovalores e autovetores para algum teste?')
        num = input("Entre com o número de um teste ou digite 'n' para finalizar: ")

        if num.lower() == 'n':
            break

        elif num in infos['Teste']:
            num = int(num)

            print('\33[92m')
            print('\n' + 50*'=')
            print(f"> Teste #{infos['Teste'][num]}")
            print(50*'=')
            print('\33[0m')

            print('\33[34m> OBTIDOS\33[0m')
            print('Autovalores:\n', results[num][1], end='\n\n')
            print('Autovetores:\n', results[num][0])

            print('\33[34m\n> ESPERADOS\33[0m')
            print('Autovalores:\n', valid[num][1], end='\n\n')
            print('Autovetores:\n', valid[num][0])
        
        else:
            print('\33[91mEntrada inválida.\33[0m')

    return
