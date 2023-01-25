import configparser
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

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

    def predict(self, bola_x, bola_y, bar_y):
        
        # Fazendo previsões com o conjunto de teste
        y_pred = self.clf.predict([[bola_x, bola_y, bar_y]])

        return (y_pred[0])

    def move(self, bola, paddle, speed):

        # Obtém a predição
        ret = self.predict(bola.x, bola.y, paddle.y - (paddle.height/2))

        # Some, Desce ou Mantém a posição
        if ret == 'S':
            paddle.move_y(-1 * speed)
        elif ret == 'D':
            paddle.move_y(speed)

    def salva_posicoes(self, bola, paddle_esquerda, paddle_direita):
        self.posicoes_bola.append([bola.x + (bola.width/2), bola.y + (bola.height/2)])
        self.posicoes_paddle_esquerda.append(paddle_esquerda.y + (paddle_esquerda.height/2))
        self.posicoes_paddle_direita.append(paddle_direita.y + (paddle_direita.height/2))
    
    def grava_posicoes(self, lado_paddle):
        
        file = ""
        paddle = ""

        if lado_paddle == "ESQUERDA":
            file = "treinamento_usuario.csv"
            paddle = self.posicoes_paddle_esquerda
        elif lado_paddle == "DIREITA":
            file = "treinamento_ia.csv"
            paddle = self.posicoes_paddle_direita

        with open(file, mode='a', encoding='UTF-8') as f:
            print(list(zip(self.posicoes_bola, paddle)))
            for bola_p, paddle_y in list(zip(self.posicoes_bola, paddle)):
                bola_x, bola_y = bola_p
                
                f.write(f'{bola_x},{bola_y},{paddle_y}\n')

            
        
        self.posicoes_bola = []
        self.posicoes_paddle_esquerda = []
        self.posicoes_paddle_direita = []


if __name__ == '__main__':
    myIa = Ia()
    myIa.predict("400","50","300")