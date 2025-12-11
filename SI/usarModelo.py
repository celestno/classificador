import joblib
import pandas as pd

# Isso aqui le o melhor modelo
modelo = joblib.load("SI/melhor_modelo.pkl")

# Isso aqui le o arquivo features que foi gerado apos extrair a imagem
exemplo = pd.read_csv("SI/features.csv")
pred = modelo.predict(exemplo)

# isso converte para que nos meros mortais possamos entender melhor o resultado da maquina
mapa = {
    0: "Não brasileiro",
    1: "Brasileiro"
}

resultado_texto = [mapa[v] for v in pred]

print("Resultado:")
for r in resultado_texto:
    print("-", r)
