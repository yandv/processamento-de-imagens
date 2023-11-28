import cv2
import pytesseract
import imutils

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

photoPath = "C:\\Users\\User\\.visual-studio-workspace\\processamento-de-imagens\\src\\imagens\\"
imageName = "img.jpg"

# Carrega a imagem
image = cv2.imread(photoPath + imageName)

image = imutils.resize(image, width=400)
grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(grey, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
result = 255 - thresh 

data = pytesseract.image_to_string(result, lang='eng',config='--psm 6')
print(data)

cv2.imshow('thresh', thresh)
cv2.imshow('result', result)
cv2.waitKey()