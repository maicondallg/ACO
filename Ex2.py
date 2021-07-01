import numpy as np
import pickle

from ACO.ACO import ACO

if __name__ == '__main__':
    np.random.seed(14)

    file = open("berlin52.tsp", 'r+')
    data = file.read()
    data = data.split('\n')[6:-3]
    data = np.array([i.strip().split(' ') for i in data], dtype=np.float32)

    cidade = ACO(dados=data, alfa=1, beta=5, Q=100, p=0.1, num_formigas_elitistas=10, num_formigas=25)
    history = cidade.run(500)
    pickle.dump(history, open('historico.p','wb'))

