import os
import cv2
import numpy as np
from skimage.transform import radon
from skimage import exposure
from scipy.ndimage import median_filter, gaussian_filter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dirImgs = "imgsCrop"
dirSinogramas = "sinogramas"
dirRadon = "transformadasRadon"

os.makedirs(dirSinogramas, exist_ok=True)
os.makedirs(dirRadon, exist_ok=True)

imgs = sorted([f for f in os.listdir(dirImgs) if f.endswith('.jpg')])

tamGrupo = 99
transformadasRadon = []

for i in range(0, len(imgs), tamGrupo):
    grupo = imgs[i:i + tamGrupo]
    sinogramas = []

    for img in grupo:
        pathImg = os.path.join(dirImgs, img)
        img = cv2.imread(pathImg, cv2.IMREAD_GRAYSCALE)
        sinogramas.append(img)

    sinograma = np.hstack(sinogramas)
    pathSinograma = os.path.join(dirSinogramas, f"sinograma_{i//tamGrupo:04d}.png")
    plt.imsave(pathSinograma, sinograma, cmap='gray')

    theta = np.linspace(0., 180., sinograma.shape[1], endpoint=False)
    transformada = radon(sinograma, theta=theta, circle=False)
    transformadaFiltrada = median_filter(transformada, size=3)
    transformadaFiltrada = gaussian_filter(transformadaFiltrada, sigma=1)

    transformadaNormalizada = (transformadaFiltrada - np.min(transformadaFiltrada)) / (np.max(transformadaFiltrada) - np.min(transformadaFiltrada))
    transformadaContrate = exposure.equalize_adapthist(transformadaNormalizada, clip_limit=0.03)

    pathTransformada = os.path.join(dirRadon, f"radon_{i//tamGrupo:04d}.png")
    plt.imsave(pathTransformada, transformadaContrate, cmap='gray')

    transformadasRadon.append(transformadaContrate)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

margemLuz = 0.9
margemSombra = 0.75
espessura = 2
qtdAmostras = 0.002

for i, radonImg in enumerate(transformadasRadon):
    radonImgNormalizada = (radonImg - np.min(radonImg)) / (np.max(radonImg) - np.min(radonImg))
    contraste = (radonImgNormalizada >= margemSombra) & (radonImgNormalizada < margemLuz)
    radonImgFiltrada = radonImgNormalizada[contraste]

    x, y = np.meshgrid(np.arange(radonImgNormalizada.shape[1]), np.arange(radonImgNormalizada.shape[0]))
    xFiltrado = x[contraste]
    yFiltrado = y[contraste]
    zFiltrado = np.full_like(xFiltrado, i * espessura)

    pontos = len(xFiltrado)
    pontosAmostras = np.random.choice(pontos, size=int(pontos * qtdAmostras), replace=False)

    xAmostras = xFiltrado[pontosAmostras]
    yAmostras = yFiltrado[pontosAmostras]
    zAmostras = zFiltrado[pontosAmostras]

    ax.scatter(xAmostras, yAmostras, zAmostras, 
               c=plt.cm.viridis(radonImgFiltrada[pontosAmostras]),
               marker='o', alpha=0.3, s=20)

ax.set_title("Reconstrução 3D com Redução de Ruído e Sem Borda")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z (mm)")
plt.show()

print("Processamento concluído!")

