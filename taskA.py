import numpy as np
import matplotlib.pyplot as plt

from EPLib import QR, gen_tridiagonal, gen_eign, print_table, ctext


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
            A = gen_tridiagonal(alpha=2, beta=-1, n=n)
            Q, R, k = QR(A, epsilon, shifted)

            Lambda = np.diag(R)

            results.append((Q, Lambda))
            valid.append(gen_eign(n))

            infos['Teste'].append(str(count))
            infos['Desloc.'].append(shifted)
            infos['k'].append(k)
            infos['n'].append(n)

            count += 1
            progress = np.round(count/(2*amount) * 100, 2)

            print(f"Progresso: {progress}%     ", end='\r')
        
    print()
    print(f"\n{ctext('Concluído!', 'g')} Comparação dos resultados:\n")
    print_table(infos)

    # ==== #
    # Plot #
    # ==== #

    while True:
        # Hacky: input com entrada padrão 's'
        plot_graph = input(f"\nExibir gráfico de iterações por dimensão da matriz? ([{ctext('s', 'g')}]/{ctext('n', 'r')}): ") or 's'

        if plot_graph.lower() == 's':
            plt.style.use('seaborn')
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
            print(ctext('Entrada inválida.', 'r'))
    
    # ========================= #
    # Autovalores e Autovetores #
    # ========================= #

    while True:
        print(f"\nDeseja verificar {ctext('autovalores', 'm')} e {ctext('autovetores', 'm')} para algum teste?")
        num = input(f"Entre com o {ctext('número de um teste', 'y')} ou digite {ctext('n', 'r')} para finalizar: ")

        if num.lower() == 'n':
            break

        elif num in infos['Teste']:
            num = int(num)

            print('\033[35m') # magenta 
            print('\n' + 50*'=')
            print(f"> Teste #{infos['Teste'][num]}")
            print(50*'=')
            print('\033[0m')

            print(ctext('> OBTIDOS', 'b'))
            print('Autovalores:\n', results[num][1], end='\n\n')
            print('Autovetores:\n', results[num][0])

            print(ctext('\n> ESPERADOS', 'b'))
            print('Autovalores:\n', valid[num][1], end='\n\n')
            print('Autovetores:\n', valid[num][0])
        
        else:
            print(ctext('Entrada inválida.', 'r'))

    return
