import numpy as np
from ACO.ACO import ACO
import pandas as pd

from ACO.ACO import ACO

if __name__ == '__main__':

    file = open("berlin52.tsp", 'r+')
    data = file.read()
    data = data.split('\n')[6:-3]
    data = np.array([i.strip().split(' ') for i in data], dtype=np.float32)

    cidade = ACO(dados=data, alfa=1, beta=5, Q=100, p=0.7, num_formigas_elitistas=5, num_formigas=10)

    cidade.run(5)

