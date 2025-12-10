import cv2
import csv
import json
import os
import random
import numpy as np
import albumentations as A
from PIL import Image, ImageFont, ImageDraw

# --- CONFIGURAÇÕES ---
ARQUIVO_CSV = "dados_passaporte.csv"
ARQUIVO_JSON = "posicoes.json"
TEMPLATE = "Tamplate_Passaporte.jpg"
PASTA_FONTES = "fontes"
PASTA_SAIDA = "dataset_sintetico"

LIMITE_TESTE = 400

# CORES DAS FONTES
COR_TEXTO_OPENCV = (35, 35, 35)
COR_MRZ_OPENCV = (20, 20, 20)
COR_ASSINATURA_PIL = (0, 0, 160)

# AUGMENTAÇÕES
transform = A.Compose([
    A.RandomRotate90(p=0.01),
    A.Rotate(limit=2, p=0.5),
    A.RandomBrightnessContrast(p=0.2),
    A.GaussNoise(p=0.15),
    A.Blur(blur_limit=3, p=0.1),
])

def carregar_fontes():
    if not os.path.exists(PASTA_FONTES):
        print("ERRO: Pasta de fontes não encontrada.")
        return []

    fontes_cursivas = [
        os.path.join(PASTA_FONTES, f)
        for f in os.listdir(PASTA_FONTES)
        if f.lower().endswith(".ttf")
        and "arial" not in f.lower()
        and "consola" not in f.lower()
    ]

    return fontes_cursivas


# REDUZ FONTE ATÉ CABER NA ÁREA DE ASSINATURA
def desenhar_assinatura(draw, texto, x, y, lista_fontes):
    tamanho_fonte = 110
    limite_largura = 1000

    caminho = random.choice(lista_fontes) if lista_fontes else "arial.ttf"

    while True:
        try:
            fonte = ImageFont.truetype(caminho, tamanho_fonte)
        except:
            fonte = ImageFont.load_default()
            break

        bbox = draw.textbbox((0, 0), texto, font=fonte)
        largura = bbox[2] - bbox[0]

        if largura < limite_largura or tamanho_fonte < 50:
            break

        tamanho_fonte -= 5

    draw.text((x, y), texto, font=fonte, fill=COR_ASSINATURA_PIL)


def main():
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)

    try:
        with open(ARQUIVO_JSON, 'r') as f:
            posicoes = json.load(f)
    except:
        return print("ERRO: JSON não encontrado.")

    img_base_cv2 = cv2.imread(TEMPLATE)
    fontes_cursivas = carregar_fontes()

    if img_base_cv2 is None:
        return print("ERRO: Template não encontrado.")

    print(f"--- Gerando {LIMITE_TESTE} passaportes (Somente Dados, Sem Foto) ---")

    with open(ARQUIVO_CSV, newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)

        for i, linha in enumerate(leitor):
            if i >= LIMITE_TESTE:
                break

            img = img_base_cv2.copy()

            # -------------------------
            # DESENHAR CAMPOS DE TEXTO
            # -------------------------
            for campo, valor in linha.items():
                if campo in posicoes and campo != "nome_assinatura":
                    coords = tuple(posicoes[campo])

                    if "mrz" in campo:
                        cv2.putText(img, valor, coords,
                                    cv2.FONT_HERSHEY_PLAIN, 2.4,
                                    COR_MRZ_OPENCV, 2, cv2.LINE_AA)
                    else:
                        escala = 0.9 if len(valor) < 25 else 0.7
                        cv2.putText(img, valor, coords,
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    escala, COR_TEXTO_OPENCV,
                                    2, cv2.LINE_AA)

            # -------------------------
            # ASSINATURA
            # -------------------------
            img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(img_pil)

            if "nome_assinatura" in posicoes:
                x, y = posicoes["nome_assinatura"]
                desenhar_assinatura(draw, linha["nome_assinatura"],
                                    x, y, fontes_cursivas)

            img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

            # -------------------------
            # AUMENTAÇÃO
            # -------------------------
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            augmented = transform(image=img_rgb)["image"]
            img_final = cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR)

            # SALVAR
            cv2.imwrite(f"{PASTA_SAIDA}/passaporte_br_{i}.jpg", img_final)
            print(f"Gerado: {i + 1}...")

    print("Concluído!")


if __name__ == "__main__":
    main()
