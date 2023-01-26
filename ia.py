import configparser
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import random

class Ia:

    def __init__(self):

        # Configurações
        self.cfg = configparser.ConfigParser()
        self.cfg.read('config.ini', encoding="UTF-8")

        # Carregando os dados do CSV
        if self.cfg['MODO']['BASE_TREINAMENTO'] == "USUARIO":
            data = pd.read_csv("treinamento_usuario.csv")
        elif self.cfg['MODO']['BASE_TREINAMENTO'] == "IA":
            data = pd.read_csv("treinamento_ia.csv")

        # Dividindo os dados em conjuntos de treinamento e teste
        X = data[["bola_x", "bola_y", "centro_paddle"]]
        y = data["resultado"]

        # Treinando o modelo com o conjunto de treinamento
        self.clf = RandomForestClassifier()
        self.clf.fit(X.values, y.values)

        # Arrays de Mapeamento das posições do usuário e da IA
        self.posicoes_bola = []
        self.posicoes_paddle_esquerda = [] # usuário
        self.posicoes_paddle_direita = [] # IA

        self.escolhas_paddle_esquerda = [] # usuário
        self.escolhas_paddle_direita = [] # IA

        self.treinar = False

    def re_treinar(self):

        # Verifica se é necessário treinar
        if self.treinar:

            # Carregando os dados do CSV
            if self.cfg['MODO']['BASE_TREINAMENTO'] == "USUARIO":
                data = pd.read_csv("treinamento_usuario.csv")
            elif self.cfg['MODO']['BASE_TREINAMENTO'] == "IA":
                data = pd.read_csv("treinamento_ia.csv")

            # Dividindo os dados em conjuntos de treinamento e teste
            X = data[["bola_x", "bola_y", "centro_paddle"]]
            y = data["resultado"]
            self.clf.fit(X.values, y.values)

            self.treinar = False

    def predict(self, bola_x, bola_y, padde_y):
        """
        Realiza a predição do movimento que o paddle deve fazer
        Args:   	
            bola_x (int): posição no eixo x atual da bola
            bola_y (int): posição no eixo y atual da bola
            padde_y (int): posição no eixo y do padde
        """

        # Fazendo previsões com o conjunto de teste
        y_pred = self.clf.predict([[bola_x, bola_y, padde_y]])

        # Retorna a predição
        return (y_pred[0])

    def move(self, bola, paddle, speed):

        # Obtém a predição
        ret = self.predict(bola.x, bola.y, paddle.y - (paddle.height/2))

        # Some, Desce ou Mantém a posição
        if ret == 'S':
            paddle.move_y(-1 * speed)
        elif ret == 'D':
            paddle.move_y(speed)

        return ret

    def salva_posicoes(self, bola, paddle_esquerda, paddle_direita, escolha_paddle_esquerda, escolha_paddle_direita):
        self.posicoes_bola.append([bola.x + (bola.width/2), bola.y + (bola.height/2)])
        self.posicoes_paddle_esquerda.append(paddle_esquerda.y + (paddle_esquerda.height/2))
        self.posicoes_paddle_direita.append(paddle_direita.y + (paddle_direita.height/2))
        self.escolhas_paddle_esquerda.append(escolha_paddle_esquerda)
        self.escolhas_paddle_direita.append(escolha_paddle_direita)
    
    def grava_posicoes(self, lado_paddle):
        
        # Libera o treinamento
        self.treinar = True

        file = ""
        paddle = ""
        escolhas = ""

        if lado_paddle == "ESQUERDA":
            file = "treinamento_usuario.csv"
            paddle = self.posicoes_paddle_esquerda
            escolhas = self.escolhas_paddle_esquerda

        elif lado_paddle == "DIREITA":
            file = "treinamento_ia.csv"
            paddle = self.posicoes_paddle_direita
            escolhas = self.escolhas_paddle_direita

        with open(file, mode='a', encoding='UTF-8') as f:

            # Pega somente 1% das posições 
            posicoes = list(zip(self.posicoes_bola, paddle, escolhas))
            posicoes = random.sample(posicoes, int( 0.1 * len(posicoes) ))

            if lado_paddle == "ESQUERDA":
                for bola_p, paddle_y, escolha in posicoes:
                    bola_x, bola_y = map(int,bola_p)
                    f.write(f'\n{800 - bola_x},{bola_y},{int(paddle_y)},{escolha}')
            elif lado_paddle == "DIREITA":
                for bola_p, paddle_y, escolha in posicoes:
                    bola_x, bola_y = map(int,bola_p)
                    f.write(f'\n{bola_x},{bola_y},{int(paddle_y)},{escolha}')

        self.posicoes_bola = []
        self.posicoes_paddle_esquerda = []
        self.posicoes_paddle_direita = []

    def reseta_posicoes(self):
        self.posicoes_bola  = []
        self.posicoes_paddle_esquerda   = []
        self.posicoes_paddle_direita    = []
        self.escolhas_paddle_esquerda   = []
        self.escolhas_paddle_direita    = []

if __name__ == '__main__':
    myIa = Ia()
    myIa.predict("400","50","300")