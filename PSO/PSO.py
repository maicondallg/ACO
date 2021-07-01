import pickle

import numpy as np


class PSO:
    def __init__(self, func, v_min=-2, v_max=2, num_it=300, num_particles=10):
        self.func = func
        self.num_it = num_it
        self.v_min = v_min
        self.v_max = v_max

        self.limite_inferior = -5
        self.limite_superior = 5

        self.num_particles = num_particles

        self.velocidade = None

        self.q1 = None
        self.q2 = None

        self.posicao = None
        self.melhor_posicao = None
        self.melhor_posicao_vizinho = None

        self.apt_acc = []

    def init_posicao_velocidade(self):
        """
        Inicialização das variáveis de posição, melhor posição e melhor vizinho e  velocidade
        :return: None
        """

        # Inicia posicao uniformimente variada dentro dos limites da função
        self.posicao = np.random.uniform(self.limite_inferior, self.limite_superior, (self.num_particles, 2))
        self.melhor_posicao = self.posicao.copy()
        self.melhor_posicao_vizinho = self.posicao.copy()

        # Inicia velocidade uniformimente dentro da velocidade minima e maxima
        self.velocidade = np.random.uniform(self.v_min, self.v_max, (self.num_particles, 2))

    def atualiza_velocidade(self):
        """
        Atualização da velocidade das particulas
        :return:
        """

        # Atualiza a velocidade pelo PSO Padrão
        self.velocidade = 0.72984*(self.velocidade + self.q1 * (self.melhor_posicao - self.posicao) + self.q2 * (self.melhor_posicao_vizinho - self.posicao))

        # Limitante da velocidade max e min
        self.velocidade[self.velocidade > self.v_max] = self.v_max
        self.velocidade[self.velocidade < self.v_min] = self.v_min

    def atualiza_posicao(self):
        """
        Atualiza a posição das particulas
        :return:
        """
        self.posicao = self.posicao + self.velocidade

    def define_melhor_posicao(self):
        apt = self.aptidao(self.posicao)
        apt_melhor = self.aptidao(self.melhor_posicao)

        index_melhores = np.where(apt < apt_melhor)[0]

        self.melhor_posicao[index_melhores] = self.posicao[index_melhores]

    def define_melhor_posicao_vizinho(self):
        """
        Definição da melhor posição dos vizinhos de cada particula - vizinhança local
        :return:
        """

        # Calcula a aptdao da melhor posição de cada particula e de cada melhor posicao dos vizinhos locais
        apt = self.aptidao(self.melhor_posicao)
        apt_melhor_vizinho = self.aptidao(self.melhor_posicao_vizinho)

        # Var para auxiliar a definicao do melhor vizinho
        aux_pos = []
        aux_apt = []

        # Iteração para cada particula até a penultima
        for i in range(apt.shape[0] - 1):

            # Pega os vizinhos a esquerda e a direita
            vizinhanca = [apt[i - 1], apt[i], apt[i + 1]]

            # Seleciona o com menor apt (minimização do problema)
            index_melhor = np.argmin(vizinhanca)

            # Armazena a posicao que deu este resultado e o resultado
            aux_pos.append(self.posicao[i + index_melhor - 1])
            aux_apt.append(vizinhanca[index_melhor])

        # Itera sob a ultima particula (especialmente para poder index o vizinho a direita que é a primeira particula)
        vizinhanca = [apt[0], apt[-1], apt[-2]]
        index_melhor = np.argmin(vizinhanca)
        aux_pos.append(self.posicao[-index_melhor])
        aux_apt.append(vizinhanca[index_melhor])

        # Seleciona se a melhor particula atual é melhor a melhor anterior
        index_melhores = np.where(aux_apt < apt_melhor_vizinho)[0]
        self.melhor_posicao_vizinho[index_melhores] = np.array(aux_pos)[index_melhores]

    def aptidao(self, data):
        """
        Retorna a aptidao de uma particula
        :param data: array com as cordenadas da particula
        :return:
        """
        return self.func(data[:, 0], data[:, 1])

    def gera_vetor_aleatorio(self):
        """
        Gera os vetores aleatorios dentro do intervalo 0~2.05
        :return:
        """
        self.q1 = np.random.uniform(0, 2.05, (self.num_particles, 2))
        self.q2 = np.random.uniform(0, 2.05, (self.num_particles, 2))

    def score(self):
        """
        Salva os valores minimos e médios das aptidoes ao longo das iteracoes
        :return:
        """
        apt = self.aptidao(self.posicao)
        self.apt_acc.append(np.array([np.mean(apt), np.min(apt)]))

    def run(self):
        """
        Roda as iterações do algoritmo
        :return:
        """

        # Inicia a posicao e velocidade das particulas
        self.init_posicao_velocidade()

        # Para cada iteração gera o vetor aleatorio, mede as aptidoes, define o melhor, melhor vizinho
        # atualiza a velocidade e a posicao de todas as particulas
        for _ in range(self.num_it):
            self.gera_vetor_aleatorio()
            self.score()
            self.define_melhor_posicao()
            self.define_melhor_posicao_vizinho()
            self.atualiza_velocidade()
            self.atualiza_posicao()

        # Salva a ultima iteração
        self.score()

        # Retorna as aptidoes acumuladas
        return np.array(self.apt_acc).T
