import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Class responsavel para treinar o modelo de classificacao e salvar o melhor modelo
class TreinadorModelos:
    def __init__(self, csv_path="SI/features.csv"):
        self.csv_path = csv_path
        self.df = None
        self.X = None
        self.y = None
        self.resultados = {}
        self.modelosTreinados = {}

    def carregarDados(self):
        # Carrega as features extraídas e remove a resposta
        self.df = pd.read_csv(self.csv_path)
        # self.df = self.df.drop(columns=["url"])
        self.X = self.df.drop(columns=["resposta"])
        self.y = self.df["resposta"]

    def treinarModelos(self):
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.3, random_state=42
        )

        modelos = {
            "DecisionTree": DecisionTreeClassifier(),
            "RandomForest": RandomForestClassifier(),
            "KNN": KNeighborsClassifier(n_neighbors=3)
        }
        
        # Faz o treinamento para cada modelo individualmente
        for nome, modelo in modelos.items():
            modelo.fit(X_train, y_train)
            pred = modelo.predict(X_test)
            acc = accuracy_score(y_test, pred)

            self.resultados[nome] = acc
            self.modelosTreinados[nome] = modelo

    def melhorModelo(self):
        if not self.resultados:
            return None, None
        melhor = max(self.resultados, key=self.resultados.get)
        return melhor, self.resultados[melhor]

    def iniciar(self):
        self.carregarDados()
        self.treinarModelos()

        melhor, acc = self.melhorModelo()
        print(self.resultados)
        print(f"\nMelhor modelo: {melhor} (acurácia: {acc:.4f})")

        joblib.dump(self.modelosTreinados[melhor], "SI/melhor_modelo.pkl")
        print("\nModelo salvo como SI/melhor_modelo.pkl")

if __name__ == "__main__":
    TreinadorModelos().iniciar()
