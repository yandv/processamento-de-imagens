import cv2
import pytesseract as tesseract
import PIL as Image
import re

def pre_processamento(imagem) -> cv2.typing.MatLike:
    preProcessedImage = cv2.resize(imagem, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Converte a imagem para escala de cinza
    preProcessedImage = cv2.cvtColor(preProcessedImage, cv2.COLOR_BGR2GRAY)

    preProcessedImage = cv2.GaussianBlur(preProcessedImage, (3, 3), 0)

    # Aplica um threshold para binarizar a imagem
    #preProcessedImage = cv2.threshold(preProcessedImage, 0, 255, cv2.THRESH_BINARY)[1]
    preProcessedImage = cv2.adaptiveThreshold(preProcessedImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 41, 10)

    # Aumenta o contraste da imagem para melhorar a segmentação dos caracteres da imagem binarizada (opcional)
    preProcessedImage = cv2.addWeighted(preProcessedImage, 1.5, preProcessedImage, -0.5, 0)

    # Dilatação da imagem 
    preProcessedImage = cv2.dilate(preProcessedImage, None, iterations=1)

    # Errosão da imagem
    preProcessedImage = cv2.erode(preProcessedImage, None, iterations=1)

    return preProcessedImage

def localizar_texto(preProcessedImage):
    # Aplica a função findContours para encontrar os contornos da imagem
    contornos, _ = cv2.findContours(preProcessedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(imagem, contornos, -1, (0, 255, 0), 2) SE QUISER DA UMA OLHADA NOS CONTORNOS

    # Retorna apenas os contornos maiores
    contornos = [c for c in contornos if cv2.contourArea(c) > 100]
    
    return contornos

def segmentar_caracteres(contorno, preProcessedImage):
    # Calcula o retângulo que engloba o contorno
    (x, y, w, h) = cv2.boundingRect(contorno)

    # Segmenta o caractere da imagem
    caractere = preProcessedImage[y:y + h, x:x + w]

    return caractere

def reconhecer_caractere(caractere):
    # Converte a imagem do caractere para um texto legível por humanos
    text = tesseract.image_to_string(caractere, lang="por")

    return text

def pos_processamento(textos):
    # Remove espaços em branco extras dos textos
    textos = [text.strip() for text in textos]

    # Retorna os textos
    
    textos = [text for text in textos if text]

    # Remove os textos vazios

    textos = [text for text in textos if len(text) > 1]

    # regex

    textos = [re.sub(r'[^\w\s]|_+$', '', text) for text in textos]

    # juntar palavras

    textos = [''.join(text.split()) for text in textos]

    # splitar palavras

    textos = [re.sub(r"([A-Z])", r" \1", text).split() for text in textos]

    return textos

def main():
    tesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/Tesseract.exe"
    # Carregue a imagem
    photoPath = r"C:\\Users\\User\\.visual-studio-workspace\\processamento-de-imagens\\src\\imagens\\"
    imageName = r"tweet-enner-valencia.jpg"
    realNameImage = imageName.split('.')[0]
    # Carrega a imagem
    imagem = cv2.imread(photoPath + imageName)
    # Pré-processamento da imagem
    preProcessedImage = pre_processamento(imagem)

    cv2.imwrite(photoPath + 'export/' + realNameImage + '-pre-processada.jpg', preProcessedImage)
    # Localização do texto
    contornos = localizar_texto(preProcessedImage)
    # Segmentação dos caracteres
    caracteres = [segmentar_caracteres(contorno, preProcessedImage) for contorno in contornos]
    # Reconhecimento dos caracteres
    textos = [reconhecer_caractere(caractere) for caractere in caracteres]
    # Pós-processamento
    textos = pos_processamento(textos)
    # Imprime os textos reconhecidos
    for i, texto in enumerate(textos):
        print(f"Texto {i + 1}: {texto}")

if __name__ == "__main__":
    main()