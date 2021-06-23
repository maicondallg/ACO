import numpy as np
from ACO.ACO import ACO
import pandas as pd

from ACO.Cidade import Cidade

if __name__ == '__main__':

    file = open("berlin52.tsp", 'r+')
    data = file.read()
    data = data.split('\n')[6:-3]
    data = np.array([i.strip().split(' ') for i in data], dtype=np.float32)

    cidade = Cidade(dados=data, alfa=1, beta=5, Q=100, p=0.7, t0=10 ** -6, b=5)
    cidade.adc_formigas(52)
    cidade.calcula_visibilidade()
    cidade.run(1000)

