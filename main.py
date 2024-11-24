import cv2
import os
import numpy as np
import skimage
import matplotlib.pyplot as plt
import pyvista as pv
    
dir = os.path.dirname(os.path.abspath(__file__))
dirPasta = 'imgsPasta'
dirPastaCrop = 'imgsCrop'
dirSinogramas = 'sinogramas'
dirPastaRadon = 'radonPasta'
dirPastaRadon2 = 'radonPasta2'

numGrupo = 99
contGrupo = 0

os.makedirs(dirPastaCrop, exist_ok=True)
os.makedirs(dirSinogramas, exist_ok=True)
os.makedirs(dirPastaRadon, exist_ok=True)

if input("Deseja tratar as imagens novamente? (s/n)") == ('s' or 'ss' or 'sim' or 'y' or 'yes'):

    print('Processando...')

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
            sinogramaCinza = cv2.cvtColor(sinograma, cv2.COLOR_BGR2GRAY)
            sinogramaNormalizado = cv2.normalize(sinogramaCinza, None, 0, 255, cv2.NORM_MINMAX)

            contGrupo += 1
            dirImgCombinada = os.path.join(dir, f'{dirSinogramas}/sinograma{contGrupo}.jpg')
            cv2.imwrite(dirImgCombinada, (sinogramaNormalizado * 255).astype(np.uint8))

            theta = np.linspace(0., 180., max(sinogramaNormalizado.shape), endpoint=False)
            imgRadon = skimage.transform.radon(sinogramaNormalizado, theta=theta, circle=False)

            radonNorm = cv2.normalize(imgRadon, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            dirRadon = os.path.join(dir, f'{dirPastaRadon}/radon{contGrupo}.jpg')
            cv2.imwrite(dirRadon, radonNorm)

imgsRadon = []
for arq in os.listdir(dirPastaRadon):
    if arq.lower().endswith('.jpg'):
        dirImg = os.path.join(dirPastaRadon, arq)
        img = cv2.imread(dirImg, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            imgsRadon.append(img)

vol = np.stack(imgsRadon, axis=0)

camReconstruidas = []
for imgRadon in imgsRadon:
    theta = np.linspace(0., 180., imgRadon.shape[1], endpoint=False)
    camReconstruida = skimage.transform.iradon(imgRadon, theta=theta, circle=False)
    camReconstruidas.append(camReconstruida)
    dirRadon2 = os.path.join(dir, f'{dirPastaRadon2}/radon{contGrupo}.jpg')
    cv2.imwrite(dirRadon2, camReconstruida)

volume = np.stack(camReconstruidas, axis=0)
volumePv = pv.wrap(volume)
plotter = pv.Plotter()
plotter.add_volume(volumePv, opacity="sigmoid_3")
plotter.show()