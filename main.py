import PIL
import cv2
import os
import numpy as np

dir = os.path.dirname(os.path.abspath(__file__))
dirPasta = 'imgsPasta'
dirPastaCrop = 'imgsCrop'
dirSinogramas = 'sinogramas'

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

numGrupo = 99
contGrupo = 0

imgsFinal = [img  for img in os.listdir(dirPastaCrop) if img.lower().endswith('.jpg')]

if imgsFinal:
    imgsFinal = imgsFinal[:-1]

for i in range(0, len(imgsFinal), numGrupo):
    imgsCombinadas = []

    grupoTratado = imgsFinal[i:i+numGrupo]

    for imgTratada in grupoTratado:
        dirCrop = os.path.join(dirPastaCrop, imgTratada)
        img = cv2.imread(dirCrop)

        if img is not None:
            imgsCombinadas.append(img)

    if imgsCombinadas:
        sinograma = np.hstack(imgsCombinadas)

        contGrupo += 1
        dirImgCombinada = os.path.join(dir, f'{dirSinogramas}/sinograma{contGrupo}.jpg')
        cv2.imwrite(dirImgCombinada, sinograma)
