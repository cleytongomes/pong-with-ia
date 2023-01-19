import pandas as pd
from sklearn.ensemble import RandomForestClassifier


class Ia:

    def __init__(self):

        # Carregando os dados do CSV
        data = pd.read_csv("data.csv")

        # Dividindo os dados em conjuntos de treinamento e teste
        X = data[["parametro1", "parametro2", "parametro3"]]
        y = data["resultado"]

        # Treinando o modelo com o conjunto de treinamento
        self.clf = RandomForestClassifier()
        self.clf.fit(X.values, y.values)

    def predict(self, ball_x, ball_y, bar_y):
        
        # Fazendo previsões com o conjunto de teste
        y_pred = self.clf.predict([[ball_x, ball_y, bar_y]])

        return (y_pred[0])

    def move(self, ball, paddle, speed):

        ret = self.predict(ball.x, ball.y, paddle.y - (paddle.height/2))

        if ret == 'S':
            paddle.move_y(-1 * speed)
        elif ret == 'D':
            paddle.move_y(speed)


myIa = Ia()
myIa.predict("400","50","300")