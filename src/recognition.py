import cv2
import numpy as np

def treatImage(photoPath: str, imageRealName: str, image: cv2.typing.MatLike, showImagesInWindow: bool) -> cv2.typing.MatLike:
    print('Começando tratamento de imagem')

    originalImage = image

    image = runProcess(photoPath, imageRealName, 'gray-scale', image, showImagesInWindow, transformGrayScale)
    image = runProcess(photoPath, imageRealName, 'median-blur', image, showImagesInWindow, transformMedianBlur)
    # image = runProcess(photoPath, imageRealName, 'thresholding', image, showImagesInWindow, thresholding)
    # image = runProcess(photoPath, imageRealName, 'dilate', image, showImagesInWindow, thresholding)
    # image = runProcess(photoPath, imageRealName, 'erode', image, showImagesInWindow, erode)

    print('Tratamento de imagem finalizadso')
    return image;

def runProcess(photoPath: str, imageRealName: str, filterName: str, image: cv2.typing.MatLike, showImagesInWindow: bool, f) -> cv2.typing.MatLike:
    image = f(image)
    createSave(photoPath, imageRealName, filterName, image)

    if (showImagesInWindow):
        cv2.imshow(filterName, image) 
        cv2.waitKey(0) 
    
    return image

def transformGrayScale(image) -> cv2.typing.MatLike:
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def transformMedianBlur(image) -> cv2.typing.MatLike:
    return cv2.medianBlur(image, 3)

def transformGaussian(image) -> cv2.typing.MatLike:
    return cv2.GaussianBlur(image, (5,5), 0)

def thresholding(image) -> cv2.typing.MatLike:
    return cv2.threshold(image, 90, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def dilate(image) -> cv2.typing.MatLike:
    return cv2.dilate(image, np.ones((2, 2), np.uint8), iterations=1)

def erode(image) -> cv2.typing.MatLike:
    return cv2.erode(image, np.ones((2, 2), np.uint8), iterations=1)

def canny(image) -> cv2.typing.MatLike:
    return cv2.Canny(image, 0, 0)

def createSave(photoPath, imageRealName, imageId, imageFile):
    cv2.imwrite(photoPath + '/export/' + imageRealName + '-' + imageId + '.jpg', imageFile)