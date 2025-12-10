import os
import cv2
import numpy as np
import pytesseract
import csv
from passporteye import read_mrz

class ExtratorPassaportes:
    def __init__(self):
        self.imagens = []

        self.listarImagens('./images')
        self.inicializarCSV()

    def inicializarCSV(self):
        self.csv_path = "features.csv"
        self.headers = [
            "republica", "federativa", "brasil", "filiacao", "filiation",
            "titular", "identidade", "emissor", "paisBrasil", "resposta"
        ]


        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()

    def iniciar(self):
        for url in self.imagens:
            try:
                features = self.extrairFeatures(url)
                self.salvarCSV(features)
            except Exception as err:
                print(err)
                pass

    def extrairFeatures(self, url):
        features = {}
        print(f"Lendo Imagem: {url}")

        img = cv2.imread(url)

        
        if img is None:
            print("Nao foi possivel ler")
            return;

        texto = self.imagemParaTexto(img)

        # features["url"] = url
        features['republica'] = 1 if 'republica' in texto else 0
        features['federativa'] = 1 if 'federativa' in texto else 0
        features['brasil'] = 1 if 'brasil' in texto else 0
        features['filiacao'] = 1 if 'filiacao' in texto else 0
        features['filiation'] = 1 if 'filiation' in texto else 0
        features['titular'] = 1 if 'titular' in texto else 0
        features['identidade'] = 1 if 'identidade' in texto else 0
        features['emissor'] = 1 if 'emissor' in texto else 0
        features['resposta'] = 1 if 'brasileiro' in url else 0
        features['paisBrasil'] = 0

        try:
            mrz = read_mrz(url)
            data = mrz.to_dict()
            features["paisBrasil"] = 1 if data.get("country", "") == "BRA" else 0
        except:
            pass

        return features

    def salvarCSV(self, features: dict):
        with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(features)

    def listarImagens(self, pasta):
        for nome in os.listdir(pasta):
            caminho = os.path.join(pasta, nome)

            if os.path.isfile(caminho):
                self.imagens.append(caminho)

            elif os.path.isdir(caminho):
                self.listarImagens(caminho)

    def imagemParaTexto(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        gray = cv2.resize(gray, None, fx=2, fy=2)

        text = pytesseract.image_to_string(gray, lang="eng")

        clean_text = " ".join(text.split())

        return clean_text.lower()

    def extrairMRZ(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 3))
        dil = cv2.dilate(thresh, kernel, iterations=3)

        cnts, _ = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        mrz_contorno = None
        max_area = 0

        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)

            if w > img.shape[1] * 0.5 and h < img.shape[0] * 0.3:
                area = w * h
                if area > max_area:
                    max_area = area
                    mrz_contorno = (x, y, w, h)

        if mrz_contorno is None:
            print("Nenhuma MRZ encontrada.")
            return None

        x, y, w, h = mrz_contorno

        mrz = img[y:y + h, x:x + w]

        return mrz


if __name__ == "__main__":
    passaportes = ExtratorPassaportes()
    passaportes.iniciar()
