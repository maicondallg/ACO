import pickle
import numpy as np


class ACO:
    def __init__(self, dados, alfa, beta, Q, p, num_formigas_elitistas=1, num_formigas=10):
        self.cidades = dados
        self.alfa = alfa
        self.beta = beta
        self.Q = Q
        self.p = p
        self.num_formigas_elitistas = num_formigas_elitistas

        self.formigas = np.zeros((num_formigas, self.cidades.shape[0]))
        self.visibilidade = np.zeros((self.cidades.shape[0], self.cidades.shape[0]))
        self.distancia = np.zeros((self.cidades.shape[0], self.cidades.shape[0]))
        self.feromonios = None
        self.feromonios_acc = None
        self.num_cidades = 0

        self.init_cidade()
        self.calcula_dist_visib()

    def dist(self, ponto1, ponto2):
        """
        Calcula distância Euclidiana entre as cidades
        :param ponto1: Ponto da cidade 1
        :param ponto2: Ponto da cidade 2
        :return: Distancia sem unidade de medida
        """
        return np.linalg.norm(ponto1 - ponto2, ord=2)

    def init_cidade(self):
        """
        Inicia as variáveis
        :return:
        """

        self.num_cidades = self.cidades.shape[0]
        self.feromonios = np.ones((self.num_cidades, self.num_cidades)) - np.eye(self.num_cidades, self.num_cidades)
        self.feromonios_acc = np.zeros_like(self.feromonios)

    def calcula_dist_visib(self):
        """
        Calcula as distancias e visibilidade das cidades
        :return:
        """
        for i in range(self.num_cidades):
            for j in range(self.num_cidades):
                aux_dist = self.dist(self.cidades[i], self.cidades[j])

                self.distancia[i][j] = aux_dist

                if aux_dist != 0:
                    self.visibilidade[i][j] = 1/aux_dist

    def atualiza_feromonios(self, melhor_caminho):
        """
        Atualia os feromonios das rotas das cidades
        :return:
        """

        delta_feromonios = np.divide(self.Q, self.feromonios_acc, out=np.zeros_like(self.feromonios_acc),
                                                                  where=self.feromonios_acc != 0)

        L = np.zeros_like(self.feromonios_acc)

        for caminho in melhor_caminho:
            L[caminho[0]][caminho[1]] = self.feromonios_acc[caminho[0]][caminho[1]]
            L[caminho[1]][caminho[0]] = self.feromonios_acc[caminho[1]][caminho[0]]

        pickle.dump(melhor_caminho, open('melhor_caminho.p', 'wb'))
        delta_elitista = np.divide(self.Q, L, out=np.zeros_like(L), where=L != 0)

        self.feromonios = (1-self.p)*self.feromonios + delta_feromonios + self.num_formigas_elitistas*delta_elitista
        self.feromonios_acc = np.zeros_like(self.feromonios)

    def inicia_formigas(self):
        """
        Inicializa as formigas do ACO
        :return: None
        """
        # Zera as rotas das formigas
        self.formigas = np.zeros((self.formigas.shape[0], self.cidades.shape[0]))

        # Coloca cada formiga numa posição aleatória
        for formiga in self.formigas:
            formiga[np.random.randint(0, self.cidades.shape[0])] = 1

    def viaja(self, formiga):
        """
        Realiza as viagens entre as cidades
        :param formiga: formiga que irá viajar entre as cidades
        :return: distancia total percorrida pela formiga
        """

        # Define a cidade de partida
        cidade = formiga.argmax()

        # Zera a distancia que percorreu
        distancia_percorrida = 0

        caminho = []

        # Percorre todas as cidades
        for i in range(2, self.cidades.shape[0] + 1):

            # Define as cidades já visitadas
            visitadas = np.nonzero(formiga)[0]
            print(self.feromonios)
            # Calcula os feromonios e zera aquelas que a formiga já visitou
            prob = self.feromonios[cidade].copy()
            prob[visitadas] = 0

            # Calcula a probabilidade de visitar a cidade e  normaliza
            prob = (prob ** self.alfa) * (self.visibilidade[cidade] ** self.beta)
            prob = prob/prob.sum()

            # Calcula as probabilidades acumulando para definir os intervalos e definir aleatóriamente a cidade
            prob = np.cumsum(prob)
            random = np.random.random()
            prox_cidade = sum(random >= prob)
            formiga[prox_cidade] = i

            # Salva a distancia percorrida, acumula os feromonios para atualizar depois (ida e volta)
            distancia_percorrida += self.distancia[cidade][prox_cidade]
            self.feromonios_acc[cidade][prox_cidade] += self.distancia[cidade][prox_cidade]
            self.feromonios_acc[prox_cidade][cidade] += self.distancia[cidade][prox_cidade]

            caminho.append([cidade, prox_cidade])

            cidade = prox_cidade

        # Faz a volta para a primeira cidade da formiga
        prox_cidade = formiga.argmin()
        distancia_percorrida += self.distancia[cidade][prox_cidade]
        self.feromonios_acc[cidade][prox_cidade] += self.distancia[cidade][prox_cidade]
        self.feromonios_acc[prox_cidade][cidade] += self.distancia[cidade][prox_cidade]

        caminho.append((cidade, prox_cidade))

        return distancia_percorrida, caminho

    def viagens(self):
        """
        Faz todas as formigas viajarem entre as cidades e pega a melhor delas (menor distancia total)
        :return: Melhor formiga
        """

        # Define distancia infinita e nenhuma como melhor
        melhor = np.inf
        melhor_formiga = None
        melhor_caminho = None

        # Para cada formiga, realiza a viagem e substitui a melhor
        for index, formiga in enumerate(self.formigas):
            distancia, caminho = self.viaja(formiga)

            if distancia < melhor:
                melhor = distancia
                melhor_formiga = formiga.copy()
                melhor_caminho = caminho

        print(melhor)

        return melhor_formiga, melhor_caminho

    def run(self, num_iteracoes):
        formigas_plot = []

        for _ in range(num_iteracoes):
            self.inicia_formigas()
            melhor_formiga, melhor_caminho = self.viagens()
            formigas_plot.append(melhor_formiga)
            self.atualiza_feromonios(melhor_caminho)

        pickle.dump(formigas_plot, open('formiga.p','wb'))



