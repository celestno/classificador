import cv2
import pytesseract

# Caso esteja no Windows, descomente:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def passport_to_text(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    gray = cv2.resize(gray, None, fx=2, fy=2)

    text = pytesseract.image_to_string(gray, lang="eng")

    clean_text = " ".join(text.split())

    return clean_text


# -----------------------
# Uso
# -----------------------
texto = passport_to_text("passport.jpeg")

print("\n=== TEXTO CORRIDO ===\n")
print(texto)
