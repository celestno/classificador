import csv
import random

headers = [
    "republica","federativa","brasil","filiacao","filiation",
    "titular","identidade","emissor","paisBrasil"
]

total = 5231
total_positivos = int(total * 0.1111)   # ~111
total_negativos = total - total_positivos  # ~889

linhas = []

# -------------------------------
# Gerar dados NEGATIVOS (resposta=0)
# -------------------------------
for _ in range(total_negativos):
    linha = [
        0, 0, 0, 0, 0,
        random.choice([0,0,0,1]),   # titular às vezes 1
        0,
        0,
        0,  # paisBrasil
    ]
    linhas.append(linha)

# -------------------------------
# Gerar dados POSITIVOS (resposta=1)
# -------------------------------
for _ in range(total_positivos):
    linha = [
        1, 1, random.choice([1,1,0]),  # brasil quase sempre
        0, 0,
        1,                              # titular
        random.choice([0,1]),           # identidade às vezes
        0,
        random.choice([0,1]),  # paisBrasil sempre
    ]
    linhas.append(linha)

# Embaralhar as linhas
random.shuffle(linhas)

# -------------------------------
# Salvar CSV
# -------------------------------
with open("features.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(linhas)

print("Arquivo 'dados.csv' gerado com sucesso!")
