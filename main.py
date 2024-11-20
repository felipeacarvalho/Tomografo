import PIL
import cv2
import os
import numpy as np

dir = os.path.dirname(os.path.abspath(__file__))
dirPasta = 'imgsPasta'
dirPastaCrop = 'imgsCrop'

os.makedirs(dirPastaCrop, exist_ok=True)

imgTeste = cv2.imread('imgsPasta/teste.jpg')
alt, larg = imgTeste.shape[:2]
centro = (larg // 2, alt // 2)
angulo = 88.9

matrizRotacao = cv2.getRotationMatrix2D(centro, angulo, scale=1)


for foto in os.listdir(dirPasta):
    dirFoto = os.path.join(dirPasta, foto)

    if foto.lower().endswith('.jpg'):
        img = cv2.imread(dirFoto)

        if img is not None:
            imgRot = cv2.warpAffine(img, matrizRotacao, (larg, alt))

            imgCrop = imgRot[0:400, 195:199]

            cv2.imwrite(f'{dirPastaCrop}/crop{foto}', imgCrop)

imgsCombinadas = []

imgsFinal = [img  for img in os.listdir(dirPastaCrop) if img.lower().endswith('.jpg')]

for i, imgFinal in enumerate(imgsFinal[:99]):
    dirCrop = os.path.join(dirPastaCrop, imgFinal)
    img = cv2.imread(dirCrop)

    if img is not None:
        imgsCombinadas.append(img)

if imgsCombinadas:
    sinograma = np.hstack(imgsCombinadas)

    dirImgCombinada = os.path.join(dir, 'sinograma.jpg')
    cv2.imwrite(dirImgCombinada, sinograma)
