import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Carregando os dados do CSV
data = pd.read_csv("data.csv")

# Dividindo os dados em conjuntos de treinamento e teste
X = data[["parametro1", "parametro2", "parametro3"]]
y = data["resultado"]


# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# # Treinando o modelo com o conjunto de treinamento
clf = RandomForestClassifier()
clf.fit(X, y)

# # Fazendo previsões com o conjunto de teste
y_pred = clf.predict([["400","50","300"]])

print(y_pred)

# # Calculando a precisão do modelo
# accuracy = accuracy_score(y_test, y_pred)
# print("Precisão: ", accuracy)