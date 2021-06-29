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

    if task == '1':

        while True:
            print(f"\n{ctext('1)', 'm')} Executar o caso definido no enunciado.")
            print(f"{ctext('2)', 'm')} Customizar um caso próprio.")

            A_opt1 = input(f"\nEntre com {ctext('1', 'm')} ou {ctext('2', 'm')}: ")
            print()

            if A_opt1 == '1':
                epsilon = 1e-6
                n_vals = [2, 4, 8, 16, 32, 64]
             
                taskA.run(epsilon, n_vals)
                break

            elif A_opt1 == '2':
                epsilon = float(input(f"Entre com o valor de {ctext('epsilon', 'y')}: "))
                n_vals = input(f"Entre com os valores de {ctext('n', 'y')} separados por espaço: ")
                n_vals = [int(n) for n in n_vals.split(' ')]

                taskA.run(epsilon, n_vals)
                break
                
            else:
                print(ctext('Entrada inválida.', 'r'))

    elif task == '2':
        pass
    else:
        print(ctext('Entrada inválida.', 'r'))