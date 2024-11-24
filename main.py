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

def apply_circular_mask(image):
    """Aplica uma máscara circular a uma imagem."""
    h, w = image.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    center = (w // 2, h // 2)
    radius = min(center)
    cv2.circle(mask, center, radius, 255, -1)
    return cv2.bitwise_and(image, image, mask=mask)

def enhance_contrast(image):
    """Aumenta o contraste da imagem."""
    return cv2.equalizeHist(image)

# Verificação para 'teste.jpg'
caminho_teste = os.path.join(dirPasta, 'teste.jpg')
imgTeste = cv2.imread(caminho_teste, cv2.IMREAD_GRAYSCALE)

if imgTeste is None:
    print("Aviso: 'teste.jpg' não foi encontrado ou está corrompido. Gerando uma imagem de teste.")
    os.makedirs(dirPasta, exist_ok=True)
    imgTeste = np.zeros((, 3), dtype=np.uint8)  # Imagem preta padrão (400x4 pixels)
    cv2.imwrite(caminho_teste, imgTeste)
    print(f"Imagem de teste gerada e salva em: {caminho_teste}")
else:
    print(f"Imagem carregada com sucesso! Dimensões: {imgTeste.shape}")

# Processamento das imagens
if input('Deseja tratar as imagens novamente? (s/n)') in ['s', 'sim', 'y', 'yes']:
    os.makedirs(dirPastaCrop, exist_ok=True)
    os.makedirs(dirSinogramas, exist_ok=True)
    os.makedirs(dirPastaRadon, exist_ok=True)

    alt, larg = imgTeste.shape[:2]
    centro = (larg // 2, alt // 2)
    angulo = 88.9

    matrizRotacao = cv2.getRotationMatrix2D(centro, angulo, scale=1)

    for foto in os.listdir(dirPasta):
        dirFoto = os.path.join(dirPasta, foto)

        if foto.lower().endswith('.jpg'):
            img = cv2.imread(dirFoto, cv2.IMREAD_GRAYSCALE)

            if img is not None:
                imgRot = cv2.warpAffine(img, matrizRotacao, (larg, alt))
                imgCrop = imgRot[0:400, 195:199]
                imgContrastada = enhance_contrast(imgCrop)
                imgCircular = apply_circular_mask(imgContrastada)
                cv2.imwrite(f'{dirPastaCrop}/crop{foto}', imgCircular)

    imgsFinal = [img for img in os.listdir(dirPastaCrop) if img.lower().endswith('.jpg')]

    if imgsFinal:
        imgsFinal = imgsFinal[:-1]

    for i in range(0, len(imgsFinal), numGrupo):
        imgsCombinadas = []

        grupoTratado = imgsFinal[i:i+numGrupo]

        for imgTratada in grupoTratado:
            dirCrop = os.path.join(dirPastaCrop, imgTratada)
            img = cv2.imread(dirCrop, cv2.IMREAD_GRAYSCALE)

            if img is not None:
                imgsCombinadas.append(img)

        if imgsCombinadas:
            sinograma = np.hstack(imgsCombinadas)
            sinogramaCircular = apply_circular_mask(sinograma)
            sinogramaContrastado = enhance_contrast(sinogramaCircular)

            contGrupo += 1
            dirImgCombinada = os.path.join(dir, f'{dirSinogramas}/sinograma{contGrupo}.jpg')
            cv2.imwrite(dirImgCombinada, sinogramaContrastado)

        theta = np.linspace(0., 180., max(sinogramaContrastado.shape), endpoint=False)
        imgRadon = skimage.transform.radon(sinogramaContrastado, theta=theta, circle=False)
        imgRadonContrastada = enhance_contrast((255 * imgRadon / np.max(imgRadon)).astype(np.uint8))
        imgRadonCircular = apply_circular_mask(imgRadonContrastada)

        dirRadon = os.path.join(dir, f'{dirPastaRadon}/radon{contGrupo}.jpg')
        cv2.imwrite(dirRadon, imgRadonCircular)

imgsRadon = []
for arq in os.listdir(dirPastaRadon):
    if arq.lower().endswith('.jpg'):
        dirImg = os.path.join(dirPastaRadon, arq)
        img = cv2.imread(dirImg, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            imgsRadon.append(img)

imgsRadon = imgsRadon[:-1]

vol = np.stack(imgsRadon, axis=0)

# Adicionando espessura ao volume
espessura = 10
volEspessura = []
for layer in vol:
    for _ in range(espessura):
        volEspessura.append(layer)
volEspessura = np.stack(volEspessura, axis=0)

# Ajustando opacidade para visualização 3D
opacity_transfer_function = [0, 0, 0.2, 0.6, 1]

volumePv = pv.wrap(volEspessura)
plotter = pv.Plotter()
plotter.add_volume(volumePv, opacity=opacity_transfer_function, cmap='gray')
plotter.show()
