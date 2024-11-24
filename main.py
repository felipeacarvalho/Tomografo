import os
import cv2
import numpy as np
from skimage.transform import radon, iradon
import matplotlib.pyplot as plt

# Diretórios
dir_imgs = "imgsCrop"  # Diretório de entrada
dir_sinogramas = "sinogramas"  # Diretório para salvar sinogramas
dir_reconstrucoes = "reconstrucoes_3d"  # Diretório para salvar reconstruções 3D

# Criar diretórios, se necessário
os.makedirs(dir_sinogramas, exist_ok=True)
os.makedirs(dir_reconstrucoes, exist_ok=True)

# Listar e ordenar as imagens no diretório
imagens = sorted([f for f in os.listdir(dir_imgs) if f.endswith('.jpg')])

# Número de imagens por grupo
grupo_tamanho = 99

# Processar as imagens em grupos
for i in range(0, len(imagens), grupo_tamanho):
    grupo = imagens[i:i+grupo_tamanho]
    sinograma_grupo = None

    # Processar cada imagem do grupo
    for img_nome in grupo:
        img_path = os.path.join(dir_imgs, img_nome)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        # Rotacionar a imagem em 88.9 graus
        altura, largura = img.shape
        centro = (largura // 2, altura // 2)
        matriz_rotacao = cv2.getRotationMatrix2D(centro, 88.9, 1.0)
        img_rotacionada = cv2.warpAffine(img, matriz_rotacao, (largura, altura))

        # Empilhar horizontalmente para formar o sinograma
        if sinograma_grupo is None:
            sinograma_grupo = img_rotacionada
        else:
            sinograma_grupo = np.hstack((sinograma_grupo, img_rotacionada))

    # Salvar o sinograma
    sinograma_path = os.path.join(dir_sinogramas, f"sinograma_{i//grupo_tamanho:04d}.png")
    plt.imsave(sinograma_path, sinograma_grupo, cmap='gray')

    # Calcular a Transformada Inversa de Radon
    theta = np.linspace(0., 180., sinograma_grupo.shape[1], endpoint=False)
    reconstruido = iradon(sinograma_grupo, theta=theta, circle=True)

    # Salvar a reconstrução 3D
    reconstruido_path = os.path.join(dir_reconstrucoes, f"reconstrucao_{i//grupo_tamanho:04d}.npy")
    np.save(reconstruido_path, reconstruido)

    # Visualizar a reconstrução 3D (opcional)
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    x, y = np.meshgrid(np.arange(reconstruido.shape[1]), np.arange(reconstruido.shape[0]))
    ax.plot_surface(x, y, reconstruido, cmap='viridis')
    ax.set_title(f"Reconstrução 3D - Grupo {i//grupo_tamanho}")
    plt.savefig(os.path.join(dir_reconstrucoes, f"reconstrucao_{i//grupo_tamanho:04d}.png"))
    plt.close()

print("Processamento concluído!")
