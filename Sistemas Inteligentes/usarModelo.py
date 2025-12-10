import joblib
import pandas as pd

modelo = joblib.load("melhor_modelo.pkl")

exemplo = pd.read_csv("features.csv")
pred = modelo.predict(exemplo)

# Mapeamento da classe
mapa = {
    0: "Não brasileiro",
    1: "Brasileiro"
}

resultado_texto = [mapa[v] for v in pred]

print("Resultado:")
for r in resultado_texto:
    print("-", r)
