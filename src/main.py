import re
import cv2
import sys
import pytesseract as tesseract
import recognition

## main

def main() -> int:
    tesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\Tesseract.exe"

    photoPath = "C:\\Users\\User\\.visual-studio-workspace\\processamento-de-imagens\\src\\imagens\\"
    imageName = "img.jpg"
    imageRealName = re.search(r'(.+)\.[a-zA-Z]+$', imageName).group(1)

    imageFile = cv2.imread(photoPath + imageName)

    if imageFile is None:
        print('Erro ao abrir imagem ' + imageName + '!')
        return -1

    print('Imagem aberta ' + imageName + ' com sucesso!')

    imageFile = recognition.treatImage(photoPath, imageRealName, imageFile, False)

    textFileOutput = open(photoPath + '/export/' + imageRealName + '.txt', 'w', encoding='utf-8')
    textFileOutput.write(tesseract.image_to_string(imageFile, lang='eng+ces', config='--psm 1'))
    textFileOutput.close()


if __name__ == '__main__':
    sys.exit(main())