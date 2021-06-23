import numpy as np


class Formiga:
    def __init__(self, cidades):
        self.ja_visitada = np.random.randint(cidades.shape[0], size=1)
        self.cidades = np.array(range(cidades.shape[0]))
        self.a_visitar = np.array(range(cidades.shape[0]))
        self.a_visitar = np.delete(self.a_visitar, self.ja_visitada[-1])
        self.distancia_total = 0

    def seleciona_cidade(self):
        return self.prox_viagem

    def set_prox_viagem(self, index):
        self.prox_viagem = index

    def retorna(self, distancia):
        index = self.ja_visitada[0]
        rota = tuple(sorted((self.ja_visitada[-1], self.cidades[index])))

        self.distancia_total += distancia[rota]
        self.a_visitar = np.delete(self.cidades, self.ja_visitada[0])
        self.ja_visitada = np.array([index])

    def reseta_caminhos(self):
        self.distancia_total = 0

    def viaja(self, distancia):
        index = self.seleciona_cidade()
        rota = tuple(sorted((self.ja_visitada[-1], self.a_visitar[index])))

        self.distancia_total += distancia[rota]
        self.ja_visitada = np.append(self.ja_visitada, self.a_visitar[index])
        self.a_visitar = np.delete(self.a_visitar, index)