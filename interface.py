# =============================================== #
# Módulo principal para a interação com o usuário #
#         e tratamento básico de entradas         #
# =============================================== #

import taskA
import taskBC
import numpy as np

from EPLib import ctext


def start():
    
    # ==================== #
    # Execução do programa #
    # ==================== #

    while True:
        print(f"Escolha uma tarefa abaixo ou digite {ctext('sair', 'r')} para finalizar a execução.\n")
        print(f"{ctext('1)', 'b')} Complexidade do algoritmo QR com e sem deslocamento espectral.")
        print(f"{ctext('2)', 'b')} Simulação de um sistema massa-mola.\n")

        task = input(f"Entre com {ctext('1', 'b')}, {ctext('2', 'b')} ou {ctext('sair', 'r')}: ")

        # ================= #
        # Executar tarefa A #
        # ================= #

        if task == '1':
            while True:
                print(f"\nEscolha uma das opções abaixo ou digite {ctext('voltar', 'r')} para retroceder.")
                print(f"\n{ctext('1)', 'm')} Executar o caso definido na tarefa A do enunciado.")
                print(f"{ctext('2)', 'm')} Customizar um caso próprio.")

                A_opt = input(f"\nEntre com {ctext('1', 'm')}, {ctext('2', 'm')} ou {ctext('voltar', 'r')}: ")
                print()

                 # Executar a tarefa A como no enunciado
                if A_opt == '1':
                    epsilon = 1e-6
                    n_vals = [2, 4, 8, 16, 32, 64]
                
                    taskA.run(epsilon, n_vals)
                    break

                # Customizar a tarefa A
                elif A_opt == '2': 
                    epsilon = float(input(f"Entre com o valor de {ctext('epsilon', 'y')}: "))
                    n_vals = input(f"Entre com os valores de {ctext('n', 'y')} separados por espaço: ")
                    n_vals = [int(n) for n in n_vals.split(' ')]

                    taskA.run(epsilon, n_vals)
                    break
                
                ### Retroceder ###
                elif A_opt.lower() == 'voltar':
                    break

                ### Erro ###
                else:
                    print(ctext('Entrada inválida.', 'r'))

        # ====================== #
        # Executar tarefa B ou C #
        # ====================== #

        elif task == '2':

            # Escolha dos parâmtros gerais (deslocamento)
            while True:
                enable_shift = input(f"\nHabilitar deslocamentos espectrais no algoritmo QR? ([{ctext('s', 'g')}]/{ctext('n', 'r')}): ") or 's'

                if enable_shift.lower() == 's':
                    shifted = True
                    break
                elif enable_shift.lower() == 'n':
                    shifted = False
                    break
                else:
                    print(ctext('Entrada inválida.', 'r'))

            # Escolha dos parâmtros gerais (precisão)
            epsilon = float(input(f"\nPrecisão para a convergência (pressione {ctext('Enter', 'g')} para utilizar {ctext('epsilon = 1e-6', 'g')}): ") or '1e-6')

            if epsilon < np.finfo(float).eps:
                print(ctext(f"AVISO: Impossível garantir precisão de {epsilon}, será utilizada a precisão de máquina: {np.finfo(float).eps}", 'r'))
                epsilon = np.finfo(float).eps                

            # Escolha de uma das tarefas
            while True:
                print(f"\nEscolha uma das simulações abaixo ou digite {ctext('voltar', 'r')} para retroceder.")
                print(f"{ctext('1)', 'm')} Executar o caso definido na tarefa B do enunciado.")
                print(f"{ctext('2)', 'm')} Executar o caso definido na tarefa C do enunciado.")
                print(f"{ctext('3)', 'm')} Customizar um caso próprio.")

                BC_opt = input(f"\nEntre com {ctext('1', 'm')}, {ctext('2', 'm')}, {ctext('3', 'm')} ou {ctext('voltar', 'r')}: ")
                print()

                # ================= #
                # Executar tarefa B #
                # ================= #

                if BC_opt == '1':
                    print("Escolha uma das opções para X0: ")
                    print(f"{ctext('1)', 'g')} X0 = [-2, -3, -1, -3, -1]")
                    print(f"{ctext('2)', 'g')} X0 = [ 1, 10, -4,  3, -2]")
                    print(f"{ctext('3)', 'g')} X0 correspondente ao modo de maior frequência")

                    B_X0_opt = input(f"\nEntre com {ctext('1', 'g')}, {ctext('2', 'g')} ou {ctext('3', 'g')}: ")
                    
                    # Executar tarefa B com primeiro X0
                    if B_X0_opt == '1':
                        X0 = np.array([-2, -3, -1, -3, -1])
                        X0 = np.reshape(X0, (X0.shape[0], 1))

                        taskBC.run('B', epsilon, shifted, X0, None)
                        break

                    # Executar tarefa B com segundo X0
                    elif B_X0_opt == '2': 
                        X0 = np.array([1, 10, -4, 3, -2])
                        X0 = np.reshape(X0, (X0.shape[0], 1))

                        taskBC.run('B', epsilon, shifted, X0, None)
                        break
                    
                    # Executar tarefa B com terceiro X0
                    elif B_X0_opt == '3': 
                        n = 5

                        taskBC.run('B', epsilon, shifted, None, n)
                        break

                    # Usuário não escolheu um X0 na tarefa B
                    else:
                        print(ctext('Entrada inválida.', 'r'))

                # ================= #
                # Executar tarefa C #
                # ================= #
                
                elif BC_opt == '2':
                    print("Escolha uma das opções para X0: ")
                    print(f"{ctext('1)', 'g')} X0 = [-2, -3, -1, -3, -1, -2, -3, -1, -3, -1]")
                    print(f"{ctext('2)', 'g')} X0 = [ 1, 10, -4,  3, -2,  1, 10, -4,  3, -2]")
                    print(f"{ctext('3)', 'g')} X0 correspondente ao modo de maior frequência")

                    C_X0_opt = input(f"\nEntre com {ctext('1', 'g')}, {ctext('2', 'g')} ou {ctext('3', 'g')}: ")

                    # Executar tarefa C com primeiro X0
                    if C_X0_opt == '1':
                        X0 = np.array([-2, -3, -1, -3, -1, -2, -3, -1, -3, -1])
                        X0 = np.reshape(X0, (X0.shape[0], 1))

                        taskBC.run('C', epsilon, shifted, X0, None)
                        break

                    # Executar tarefa C com segundo X0
                    elif C_X0_opt == '2': # Executar tarefa C com segundo X0
                        X0 = np.array([ 1, 10, -4,  3, -2,  1, 10, -4,  3, -2])
                        X0 = np.reshape(X0, (X0.shape[0], 1))

                        taskBC.run('C', epsilon, shifted, X0, None)
                        break

                    # Executar tarefa C com terceiro X0
                    elif C_X0_opt == '3': 
                        n = 10

                        taskBC.run('C', epsilon, shifted, None, n)
                        break
                    
                    # Usuário não escolheu um X0 na tarefa C
                    else:
                        print(ctext('Entrada inválida.', 'r'))

                # ======================== #
                # Customizar tarefa B ou C #
                # ======================== #

                elif BC_opt == '3':
                    k_type = input(f"A constante elástica das molas deve ser definida como na tarefa {ctext('B', 'y')} ou como na tarefa {ctext('C', 'y')}? ")
                    X0 = input(f"Entre com os {ctext('valores do vetor X0', 'y')} separados por espaço: ")
                    X0 = np.array([float(x) for x in X0.split(' ')])
                    X0 = np.reshape(X0, (X0.shape[0], 1))

                    taskBC.run(k_type, epsilon, shifted, X0, None)
                    break

                ### Retroceder ###
                elif BC_opt.lower() == 'voltar':
                        break

                ### Erro ###
                else:
                    print(ctext('Entrada inválida.', 'r'))
        
        ### Sair ###
        elif task.lower() == 'sair': # Finalizar o programa
            break
        
        ### Erro ###
        else:
            print(ctext('Entrada inválida.', 'r'))
    
    return
