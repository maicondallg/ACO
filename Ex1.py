import pickle
import random
import numpy as np
from PSO.PSO import PSO
from AlgsGeneticos.Algoritmos.alg_genetico2 import algort_genetico_2d
from AlgsGeneticos.Utils.funcs import func3
from Utils.PlotEx1 import plot_graficos_comparacao

if __name__ == '__main__':

    # Definição de semente para reprodução de exp
    np.random.seed(11)
    random.seed(11)


    # Definição de variáveis para execução do exercicio
    function = lambda x, y: (1 - x) ** 2 + 100 * (y - x ** 2) ** 2
    fc = func3
    fc((0, 0))

    historico_pso = []
    historico_gen = []

    for i in range(10):
        cls = PSO(function, num_particles=16, num_it=400)
        historico_pso.append(cls.run())

        _, _, _, valores_best, valores_media = algort_genetico_2d(fc, num_ind=16, pc=1, pm=1, num_geracoes=400,
                                                                tipo_apt='qualidade', obj='min', tipo_selecao='torneio')
        historico_gen.append([valores_media, valores_best])

    plot_graficos_comparacao(historico_pso, historico_gen)
