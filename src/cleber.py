import pytesseract as tesseract
from PIL import Image
import cv2

tesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\Tesseract.exe"

# Carregue a imagem
photoPath = "C:\\Users\\User\\.visual-studio-workspace\\processamento-de-imagens\\src\\imagens\\"
imageName = "img.jpg"
image = cv2.imread(photoPath + imageName)

# Redução de ruído usando filtragem da média
image_noise_reduced = cv2.GaussianBlur(image, (5, 5), 0)  # Pode usar também cv2.medianBlur ou cv2.blur

# Binarização da imagem usando o algoritmo de Otsu
gray_image = cv2.cvtColor(image_noise_reduced, cv2.COLOR_BGR2GRAY)
_, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Ajuste de contraste
alpha = 3252  # Ajuste o valor de alpha para alterar o contraste
beta = 0    # Ajuste o valor de beta para alterar o brilho

adjusted_image = cv2.convertScaleAbs(binary_image, alpha=alpha, beta=beta)

# Exibir a imagem original, imagem com redução de ruído e imagem binarizada
cv2.imshow('Imagem Original', image)
cv2.imshow('Imagem com Redução de Ruído', image_noise_reduced)
cv2.imshow('Imagem Binarizada', binary_image)
cv2.imshow('Imagem Ajustada', adjusted_image)

contours, _ = cv2.findContours(adjusted_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Inicialize uma lista para armazenar o texto de cada região
text_list = []

# Loop através dos contornos
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    roi = binary_image[y:y + h, x:x + w]  # Extrair a região de interesse (ROI)
    
    # Executar o OCR com Tesseract na ROI
    text_list.append(tesseract.image_to_string(Image.fromarray(roi), lang='eng+ces'))

# Aguarde uma tecla ser pressionada e feche as janelas
cv2.waitKey(0)
cv2.destroyAllWindows()

for i, text in enumerate(text_list):
    print(f"ROI {i + 1}: {text}")