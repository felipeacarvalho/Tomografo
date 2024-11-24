import os
import cv2
import numpy as np
from skimage.transform import radon
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Diretórios
dir_imgs = "imgsCrop"  # Diretório de entrada
dir_sinogramas = "sinogramas"  # Diretório para salvar sinogramas
dir_transformadas = "transformadas_radon"  # Diretório para salvar transformadas de Radon

# Criar diretórios, se necessário
os.makedirs(dir_sinogramas, exist_ok=True)
os.makedirs(dir_transformadas, exist_ok=True)

# Listar e ordenar as imagens no diretório
imagens = sorted([f for f in os.listdir(dir_imgs) if f.endswith('.jpg')])

# Número de imagens por grupo (cada sinograma será formado por 99 imagens)
grupo_tamanho = 99
transformadas_radon = []  # Lista para armazenar as transformadas de Radon

# Processar as imagens em grupos
for i in range(0, len(imagens), grupo_tamanho):
    grupo = imagens[i:i + grupo_tamanho]
    sinograma_grupo = []

    # Processar cada imagem do grupo
    for img_nome in grupo:
        img_path = os.path.join(dir_imgs, img_nome)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        # Adicionar a imagem ao sinograma (horizontalmente)
        sinograma_grupo.append(img)

    # Empilhar horizontalmente para formar o sinograma
    sinograma = np.hstack(sinograma_grupo)

    # Salvar o sinograma
    sinograma_path = os.path.join(dir_sinogramas, f"sinograma_{i//grupo_tamanho:04d}.png")
    plt.imsave(sinograma_path, sinograma, cmap='gray')

    # Calcular a Transformada de Radon
    theta = np.linspace(0., 180., sinograma.shape[1], endpoint=False)
    transformada = radon(sinograma, theta=theta, circle=True)

    # Salvar a transformada de Radon como imagem
    transformada_path = os.path.join(dir_transformadas, f"radon_{i//grupo_tamanho:04d}.png")
    plt.imsave(transformada_path, transformada, cmap='gray')

    # Adicionar a transformada à lista para visualização 3D
    transformadas_radon.append(transformada)

# Visualizar o objeto 3D com espessura de 2 mm por camada
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Parâmetros ajustáveis
light_threshold = 0.21  # O limite para partes mais claras
dark_threshold = 0.075   # O limite para as partes mais escuras
opacity_attenuation = 0.5  # Opacidade das áreas claras "atenuadas" (entre 0.0 e 1.0)
thickness = 2  # Espessura em mm de cada camada
sampling_factor = 0.001  # Fator de amostragem (0.1% dos pontos serão plotados)

# Processar cada camada de transformada de Radon
for idx, radon_img in enumerate(transformadas_radon):
    # Normalizar a intensidade para valores entre 0 e 1
    radon_img_normalized = radon_img / np.max(radon_img)

    # Criar máscara baseada nos thresholds
    mask_included = (radon_img_normalized >= dark_threshold) & (radon_img_normalized < light_threshold)

    # Máscara para as partes claras que serão atenuadas
    mask_attenuated = radon_img_normalized >= light_threshold

    # Criar imagem final para plotar (aplicando atenuação nas áreas claras)
    radon_img_filtered = np.zeros_like(radon_img_normalized)
    radon_img_filtered[mask_included] = radon_img_normalized[mask_included]
    radon_img_filtered[mask_attenuated] = radon_img_normalized[mask_attenuated] * opacity_attenuation

    # Coordenadas 3D para criar o volume
    z_bottom = idx * thickness  # Coordenada Z inferior
    z_top = z_bottom + thickness  # Coordenada Z superior
    x, y = np.meshgrid(np.arange(radon_img_filtered.shape[1]), np.arange(radon_img_filtered.shape[0]))

    # Amostrar pontos para reduzir a densidade (selecionar apenas uma fração dos pontos)
    total_points = x.shape[0] * x.shape[1]
    sampled_indices = np.random.choice(total_points, size=int(total_points * sampling_factor), replace=False)

    # Obter as coordenadas dos pontos amostrados
    x_sampled = x.flatten()[sampled_indices]
    y_sampled = y.flatten()[sampled_indices]
    z_sampled_bottom = np.full_like(x_sampled, z_bottom)
    z_sampled_top = np.full_like(x_sampled, z_top)

    # Criar o volume usando bolinhas (scatter) em vez de superfícies
    ax.scatter(x_sampled, y_sampled, z_sampled_bottom, c=plt.cm.viridis(radon_img_filtered.flatten()[sampled_indices]),
               marker='o', alpha=0.8, s=10)  # Ajuste o tamanho das bolinhas com s=10
    ax.scatter(x_sampled, y_sampled, z_sampled_top, c=plt.cm.viridis(radon_img_filtered.flatten()[sampled_indices]),
               marker='o', alpha=0.8, s=10)  # Ajuste o tamanho das bolinhas com s=10

# Configurações do gráfico 3D
ax.set_title("Reconstrução 3D com Espessura por Camada (Bolinhas e Amostragem Reduzida)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z (mm)")
plt.show()

print("Processamento concluído!")
