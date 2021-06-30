import numpy as np

import taskA
import taskBC

from EPLib import ctext


print(
"""\033[32m
===================================================
                Exercício-Programa #1
===================================================

Algoritmo QR: autovalores e autovetores de matrizes
tridiagonais simétricas.

MAP3121 – Métodos Numéricos e Aplicações

===================================================
\033[0m"""
)

while True:
    print("Qual tarefa deseja executar?\n")
    print(f"{ctext('1)', 'b')} Convergência do algoritmo QR com e sem deslocamento espectral.")
    print(f"{ctext('2)', 'b')} Simulação de um sistema massa-mola.\n")

    task = input(f"Entre com {ctext('1', 'b')} ou {ctext('2', 'b')}: ")

    if task == '1': # Executar tarefa A
        while True:
            print(f"\n{ctext('1)', 'm')} Executar o caso definido na tarefa A do enunciado.")
            print(f"{ctext('2)', 'm')} Customizar um caso próprio.")

            A_opt = input(f"\nEntre com {ctext('1', 'm')} ou {ctext('2', 'm')}: ")
            print()

            if A_opt == '1': # Executar a tarefa A como no enunciado
                epsilon = 1e-6
                n_vals = [2, 4, 8, 16, 32, 64]
             
                taskA.run(epsilon, n_vals)
                break

            elif A_opt == '2': # Customizar a tarefa A
                epsilon = float(input(f"Entre com o valor de {ctext('epsilon', 'y')}: "))
                n_vals = input(f"Entre com os valores de {ctext('n', 'y')} separados por espaço: ")
                n_vals = [int(n) for n in n_vals.split(' ')]

                taskA.run(epsilon, n_vals)
                break
                
            else:
                print(ctext('Entrada inválida.', 'r'))

    elif task == '2': # Executar tarefa B ou C
        while True:
            print('Qual simulação deseja executar?\n')
            print(f"{ctext('1)', 'm')} Executar o caso definido na tarefa B do enunciado.")
            print(f"{ctext('2)', 'm')} Executar o caso definido na tarefa C do enunciado.")
            print(f"{ctext('3)', 'm')} Customizar um caso próprio.")

            BC_opt = input(f"\nEntre com {ctext('1', 'm')}, {ctext('2', 'm')} ou {ctext('3', 'm')}: ")
            print()

            if BC_opt == '1': # Exercutar tarefa B
                print("Escolha uma das opções para X0: ")
                print(f"{ctext('1)', 'g')} X0 = [-2, -3, -1, -3, -1]")
                print(f"{ctext('2)', 'g')} X0 = [ 1, 10, -4,  3, -2]")
                print(f"{ctext('3)', 'g')} X0 correspondente ao modo de maior frequência")

                B_X0_opt = input(f"\nEntre com {ctext('1', 'g')}, {ctext('2', 'g')} ou {ctext('3', 'g')}: ")

                if B_X0_opt == '1': # Exercutar tarefa B com primeiro X0
                    X0 = np.array([-2, -3, -1, -3, -1])
                    X0 = np.reshape(X0, (X0.shape[0], 1))

                    taskBC.run('B', X0, None)
                    break

                elif B_X0_opt == '2': # Exercutar tarefa B com segundo X0
                    X0 = np.array([1, 10, -4, 3, -2])
                    X0 = np.reshape(X0, (X0.shape[0], 1))

                    taskBC.run('B', X0, None)
                    break

                elif B_X0_opt == '3': # Exercutar tarefa B com terceiro X0
                    n = 5

                    taskBC.run('B', None, n)
                    break

                else:
                    print(ctext('Entrada inválida.', 'r'))


            elif BC_opt == '2': # Exercutar tarefa C
                print("Escolha uma das opções para X0: ")
                print(f"{ctext('1)', 'g')} X0 = [-2, -3, -1, -3, -1, -2, -3, -1, -3, -1]")
                print(f"{ctext('2)', 'g')} X0 = [ 1, 10, -4,  3, -2,  1, 10, -4,  3, -2]")
                print(f"{ctext('3)', 'g')} X0 correspondente ao modo de maior frequência")

                C_X0_opt = input(f"\nEntre com {ctext('1', 'g')}, {ctext('2', 'g')} ou {ctext('3', 'g')}: ")

                if C_X0_opt == '1': # Exercutar tarefa C com primeiro X0
                    X0 = np.array([-2, -3, -1, -3, -1, -2, -3, -1, -3, -1])
                    X0 = np.reshape(X0, (X0.shape[0], 1))

                    taskBC.run('C', X0, None)
                    break

                elif C_X0_opt == '2': # Exercutar tarefa C com segundo X0
                    X0 = np.array([ 1, 10, -4,  3, -2,  1, 10, -4,  3, -2])
                    X0 = np.reshape(X0, (X0.shape[0], 1))

                    taskBC.run('C', X0, None)
                    break

                elif C_X0_opt == '3': # Exercutar tarefa C com terceiro X0
                    n = 10

                    taskBC.run('C', None, n)
                    break

                else:
                    print(ctext('Entrada inválida.', 'r'))

            elif BC_opt == '3': # Customizar a tarefa B ou C
                k_type = input(f"A constante elástica das molas deve ser definida como na tarefa B ou como na tarefa C? ")
                X0 = input(f"Entre com os valores do vetor X0 separados por espaço: ")
                X0 = np.array([float(x) for x in X0.split(' ')])
                X0 = np.reshape(X0, (X0.shape[0], 1))

                taskBC.run(k_type, X0, None)
                break

            else:
                print(ctext('Entrada inválida.', 'r'))
    else:
        print(ctext('Entrada inválida.', 'r'))
