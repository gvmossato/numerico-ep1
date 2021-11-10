# 💻 Exercício-Programa #1

Repositório utilizado para o primeiro exercício-programa da disciplina **MAP3121 - Métodos Numéricos e Aplicações**, contendo a implementação do Algoritmo QR com deslocamentos espectrais (aplicados por meio da heurística de Wilkinson) para obtenção de autovalores e autovetores de matrizes tridiagonais simétricas. 

# 📦 Dependências

* [NumPy](https://numpy.org/)
* [Matplotlib](https://matplotlib.org/)

# 📝 Tarefas

✔️ Obtenção dos autovalores e autovetores de uma matriz tridiagonal simétrica `n x n` cuja diagonal principal é toda composta por `2` e as diagonais imediatamente acima e abaixo dessa por `-1`.

✔️ Obtenção da solução gráfica (deslocamento por tempo) de um sistema massa-mola ideal composto por `5` massas inicialmente em repouso, para diversos deslocamentos iniciais.

✔️ Problema análogo ao anterior, em que o maior diferencial passam a ser as `10` massas que compõem o sistema.

# ⚙️ Instalação

Na alternativa descrita abaixo utiliza-se o [Anaconda](https://www.anaconda.com/), existem outras possibilidades. 

```
conda create --name <env-name> python=3.7
conda activate <env-name>
conda install numpy matplotlib
```

# 🚀 Uso

```
python run.py
```

# ✨ Exemplo

![example](https://i.ibb.co/yRkzXdh/numerico-ep1.gif)
