import numpy as np


def traca_caminhos(formiga, data):
    caminhos = np.zeros((formiga.shape[0] * 2, 2))
    i = 0
    for index, index2 in zip(np.argsort(formiga), np.argsort(formiga)[1:]):
        caminhos[i] = data[index]
        caminhos[i + 1] = data[index2]
        i += 2

    index = index2
    index2 = np.argsort(formiga)[0]
    caminhos[i] = data[index]
    caminhos[i + 1] = data[index2]

    return caminhos