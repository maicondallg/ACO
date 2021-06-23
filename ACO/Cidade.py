import numpy as np

from ACO.Formiga import Formiga


class Cidade:
    def __init__(self, dados, alfa, beta, Q, p, t0, b):
        self.cidades = dados
        self.alfa = alfa
        self.beta = beta
        self.Q = Q
        self.p = p
        self.t0 = t0
        self.b = b

        self.formigas = np.array([])
        self.visibilidade = {}
        self.feromonios = {}
        self.distancia = {}

    def adc_formigas(self, num_formigas):
        self.formigas = np.append(self.formigas, np.array([Formiga(self.cidades) for _ in range(num_formigas)]))

    def dist(self, ponto1, ponto2):
        return np.linalg.norm(ponto1 - ponto2, ord=2)

    def calcula_probabilidades(self):
        for formiga in self.formigas:
            p = {}
            cidade_atual = formiga.ja_visitada[-1]

            for cidade_a_visitar in formiga.a_visitar:
                rota = tuple(sorted((cidade_atual, cidade_a_visitar)))
                p[cidade_a_visitar] = (self.feromonios[rota] ** self.alfa) * (self.visibilidade[rota]) ** self.beta

            total_p = sum(p.values())
            for cidade_a_visitar in p.keys():
                p[cidade_a_visitar] = p[cidade_a_visitar] / total_p

            probs = np.cumsum(list(p.values()))
            random = np.random.random()
            formiga.set_prox_viagem(sum(random >= probs))

    def calcula_visibilidade(self):
        for i in range(self.cidades.shape[0]):
            for j in range(i + 1, self.cidades.shape[0]):
                self.feromonios[(i, j)] = self.t0
                aux_dist = self.dist(self.cidades[i], self.cidades[j])
                self.distancia[(i, j)] = aux_dist
                self.visibilidade[(i, j)] = 1 / (aux_dist)

    def total_feromonios(self):
        return sum([self.Q / (formiga.distancia_total) for formiga in self.formigas])

    def atualiza_feromonios(self):
        delta_feromonios = self.total_feromonios()
        for i in range(self.cidades.shape[0]):
            for j in range(i + 1, self.cidades.shape[0]):
                self.feromonios[(i, j)] = (1 - self.p) * self.feromonios[(i, j)] + delta_feromonios

    def reseta_formgias(self):
        for formiga in self.formigas:
            formiga.reseta_caminhos()

    def run(self, num_iteracoes):
        for iteracoes in range(num_iteracoes):
            for _ in range(self.cidades.shape[0] - 1):
                self.calcula_probabilidades()
                for formiga in self.formigas:
                    formiga.viaja(self.distancia)

            for formiga in self.formigas:
                formiga.retorna(self.distancia)

            self.atualiza_feromonios()

            print(min([formiga.distancia_total for formiga in self.formigas]))

            self.reseta_formgias()

            aux = []
            for i in range(self.cidades.shape[0]):
                for j in range(i + 1, self.cidades.shape[0]):
            aux.append([self.cidades[i], self.cidades[j], np.random.random ()])
